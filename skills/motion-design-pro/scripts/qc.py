"""Contrôle qualité motion : mesure une vidéo et la compare aux références.

Usage : python -I qc.py <video.mp4> [--json]
Besoin : ffmpeg et ffprobe dans le PATH. Pas de dépendance Python.
"""
import sys, subprocess, json, math, array, re, statistics as st

# Seuils calibrés sur les 13 vidéos de référence (voir references/metrics.md).
# "bloquant" : aucune référence ne le dépasse, la vidéo test "diaporama" oui.
# "cible" : valeur visée ; la dépasser donne un conseil, pas un refus.
SEUILS = {
    "images_fixes": {"bloquant": 0.60, "cible": 0.40},        # réf. 0.06-0.60, médiane 0.31 ; test 0.86
    "plus_long_fixe_s": {"bloquant": 2.5, "cible": 1.5},      # réf. 0.38-2.5 ; test 4.37
    "animations_par_s": {"bloquant": 0.50, "cible": 0.65},    # réf. 0.57-1.46 ; test 0.23
    "part_ease_in": {"bloquant": 0.50, "cible": 0.35},        # réf. 0.05-0.40 ; test 0.62
    "lufs": {"bloquant": (-16.0, -12.0), "cible": (-15.0, -13.0)},  # réf. -14.1 à -14.3 (12/13)
    "true_peak": {"cible": -1.0},
    "premier_mouvement_s": {"cible": 0.5},
}


def run(cmd):
    return subprocess.run(cmd, capture_output=True)


def probe(f):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
               "-of", "json", f]).stdout
    j = json.loads(out)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = any(s["codec_type"] == "audio" for s in j["streams"])
    n, d = v["r_frame_rate"].split("/")
    return float(j["format"]["duration"]), int(v["width"]), int(v["height"]), float(n) / float(d), a


def mouvement(f, fps):
    # Analyse toujours à 30 i/s au plus : à 60 i/s, l'écart entre deux images est deux fois plus petit
    # et les seuils (calibrés sur des références à 30 i/s) compteraient trop d'images comme fixes.
    fps = min(fps, 30.0)
    W, H = 96, 54
    raw = run(["ffmpeg", "-v", "error", "-i", f, "-vf", f"fps={fps},scale={W}:{H}:flags=area,format=gray",
               "-f", "rawvideo", "-"]).stdout
    fs = W * H
    n = len(raw) // fs
    d = [0.0]
    for k in range(1, n):
        a = raw[(k - 1) * fs:k * fs]
        b = raw[k * fs:(k + 1) * fs]
        d.append(sum(abs(a[i] - b[i]) for i in range(fs)) / fs)
    fixe = [x < 0.3 for x in d]
    # plus longue tenue immobile, hors 4 dernières secondes (la fin est tenue volontairement)
    limite = max(1, n - int(4 * fps))
    best = run_len = 0
    best_at = 0
    for i in range(limite):
        run_len = run_len + 1 if fixe[i] else 0
        if run_len > best:
            best, best_at = run_len, i - run_len + 1
    premier = next((i / fps for i in range(1, n) if d[i] > 0.6), None)
    thr = max(0.6, st.median(d) * 1.5)
    ev = []
    i = 1
    while i < n:
        if d[i] > thr:
            j = i
            while j < n and d[j] > thr:
                j += 1
            if j - i >= 5:
                seg = d[i:j]
                ev.append((seg.index(max(seg)) / (j - i - 1), (j - i) / fps))
            i = j
        else:
            i += 1
    pk = [e[0] for e in ev] or [0.5]
    return {
        "images_fixes": round(sum(fixe) / n, 2),
        "plus_long_fixe_s": round(best / fps, 2),
        "plus_long_fixe_debut_s": round(best_at / fps, 2),
        "premier_mouvement_s": round(premier, 2) if premier is not None else None,
        "animations": len(ev),
        "part_ease_out": round(sum(p < 0.35 for p in pk) / len(pk), 2),
        "part_ease_in_out": round(sum(0.35 <= p <= 0.65 for p in pk) / len(pk), 2),
        "part_ease_in": round(sum(p > 0.65 for p in pk) / len(pk), 2),
        "duree_animation_mediane_ms": round(st.median([e[1] for e in ev]) * 1000) if ev else 0,
    }


def coupes(f):
    err = run(["ffmpeg", "-i", f, "-vf", "select='gt(scene,0.3)',showinfo", "-an", "-f", "null", "-"]).stderr.decode("utf8", "ignore")
    return [round(float(x), 2) for x in re.findall(r"pts_time:([0-9.]+)", err)]


def volume(f):
    err = run(["ffmpeg", "-nostats", "-hide_banner", "-i", f, "-af", "ebur128=framelog=quiet:peak=true", "-f", "null", "-"]).stderr.decode("utf8", "ignore")
    s = err[err.rfind("Summary"):]
    i = re.search(r"I:\s+(-?[0-9.]+) LUFS", s)
    p = re.search(r"Peak:\s+(-?[0-9.]+) dBFS", s)
    return float(i.group(1)) if i else None, float(p.group(1)) if p else None


def impacts(f):
    sr, hop = 8000, 80
    raw = run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]).stdout
    a = array.array("h")
    a.frombytes(raw)
    n = len(a) // hop
    le = [20 * math.log10(math.sqrt(sum(v * v for v in a[i * hop:(i + 1) * hop]) / hop) + 1) for i in range(n)]
    fl = [0] + [max(0, le[i] - le[i - 1]) for i in range(1, n)]
    ons = []
    for i in range(3, n - 3):
        w = fl[max(0, i - 50):i + 50]
        if fl[i] > sum(w) / len(w) * 2.5 + 1.5 and fl[i] == max(fl[i - 3:i + 4]) and (not ons or i - ons[-1] > 8):
            ons.append(i)
    return [o / 100 for o in ons]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    f = sys.argv[1]
    dur, w, h, fps, has_audio = probe(f)
    r = {"fichier": f, "duree_s": round(dur, 1), "format": f"{w}x{h}", "fps": round(fps, 2)}
    r.update(mouvement(f, fps))
    r["animations_par_s"] = round(r["animations"] / dur, 2)
    r["coupes"] = coupes(f)
    if has_audio:
        r["lufs"], r["true_peak"] = volume(f)
        ons = impacts(f)
        r["impacts_par_s"] = round(len(ons) / dur, 2)
        sync = [c for c in r["coupes"] if any(abs(c - o) <= 0.1 for o in ons)]
        r["coupes_avec_son"] = f"{len(sync)}/{len(r['coupes'])}"
    else:
        r["lufs"] = r["true_peak"] = None

    S = SEUILS

    def niveau(ok_bloquant, ok_cible):
        return "OK" if ok_cible else ("CONSEIL" if ok_bloquant else "BLOQUANT")

    checks = []
    v = r["images_fixes"]
    checks.append(("Images fixes", niveau(v <= S["images_fixes"]["bloquant"], v <= S["images_fixes"]["cible"]),
                   f"{v:.0%} (cible ≤ {S['images_fixes']['cible']:.0%}, refus > {S['images_fixes']['bloquant']:.0%})"))
    v = r["plus_long_fixe_s"]
    checks.append(("Plus longue tenue immobile", niveau(v <= S["plus_long_fixe_s"]["bloquant"], v <= S["plus_long_fixe_s"]["cible"]),
                   f"{v} s à {r['plus_long_fixe_debut_s']} s (cible ≤ {S['plus_long_fixe_s']['cible']} s, refus > {S['plus_long_fixe_s']['bloquant']} s)"))
    v = r["animations_par_s"]
    checks.append(("Densité d'animation", niveau(v >= S["animations_par_s"]["bloquant"], v >= S["animations_par_s"]["cible"]),
                   f"{v}/s (cible ≥ {S['animations_par_s']['cible']}, refus < {S['animations_par_s']['bloquant']})"))
    v = r["part_ease_in"]
    checks.append(("Fondus / sorties dominants", niveau(v <= S["part_ease_in"]["bloquant"], v <= S["part_ease_in"]["cible"]),
                   f"{v:.0%} des animations finissent vite (cible ≤ {S['part_ease_in']['cible']:.0%}, refus > {S['part_ease_in']['bloquant']:.0%})"))
    v = r["premier_mouvement_s"]
    checks.append(("Premier mouvement visible", niveau(True, v is not None and v <= S["premier_mouvement_s"]["cible"]),
                   f"{v} s (cible ≤ {S['premier_mouvement_s']['cible']} s ; mesure grossière, vérifier à l'œil)"))
    if has_audio:
        v = r["lufs"]
        b, c = S["lufs"]["bloquant"], S["lufs"]["cible"]
        checks.append(("Volume intégré", niveau(v is not None and b[0] <= v <= b[1], v is not None and c[0] <= v <= c[1]),
                       f"{v} LUFS (cible -14, refus hors {b[0]} à {b[1]})"))
        v = r["true_peak"]
        checks.append(("Crête", niveau(True, v is not None and v <= S["true_peak"]["cible"]), f"{v} dBFS (cible ≤ {S['true_peak']['cible']})"))
    else:
        checks.append(("Piste audio", "BLOQUANT", "absente"))
    r["controles"] = [{"controle": c, "niveau": n, "valeur": v} for c, n, v in checks]
    niveaux = [n for _, n, _ in checks]
    r["verdict"] = "A REPRENDRE" if "BLOQUANT" in niveaux else ("OK AVEC CONSEILS" if "CONSEIL" in niveaux else "OK")

    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    print(f"{r['fichier']}  ({r['duree_s']} s, {r['format']}, {r['fps']} i/s)")
    for c, n, v in checks:
        print(f"  {n:<8} {c} : {v}")
    print(f"  info : {r['animations']} animations ; ease-out {r['part_ease_out']:.0%} / in-out {r['part_ease_in_out']:.0%} / in {r['part_ease_in']:.0%} ; "
          f"durée médiane {r['duree_animation_mediane_ms']} ms ; {len(r['coupes'])} coupes" +
          (f" ; {r['impacts_par_s']} impacts/s ; coupes avec son {r['coupes_avec_son']}" if has_audio else ""))
    print(f"  VERDICT : {r['verdict']}")


if __name__ == "__main__":
    main()
