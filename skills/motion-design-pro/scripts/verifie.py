"""Vérification finale d'une vidéo avant rendu ou livraison : tout ce qui peut se mesurer.

Usage :
  python -I verifie.py <video.mp4> [--script script.txt] [--duree 30] [--format 9:16|16:9|1:1|4:5]
                       [--whisper-model chemin/ggml-base.bin] [--rapport rapport.md] [--json]

Contrôles : technique (format, cadence, durée, codec), image (mouvement, écrans noirs, images figées),
son (volume, crête, silences, fin muette, fond musical, synchro), texte (tics IA du script),
voix contre script (si un modèle Whisper est fourni ou dans WHISPER_MODEL).
Écrit un rapport Markdown avec la liste des vérifications manuelles restantes.
Verdict : BLOQUANT = ne pas rendre ni livrer ; CONSEIL = corriger ou justifier ; OK.
Besoin : ffmpeg et ffprobe dans le PATH. Voir references/verification-finale.md.
"""
import sys, os, re, json, subprocess, unicodedata, importlib.util, tempfile

ICI = os.path.dirname(os.path.abspath(__file__))


def charge(nom):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


qc = charge("qc")
anti = charge("anti_ia")


def err(cmd):
    return subprocess.run(cmd, capture_output=True).stderr.decode("utf8", "ignore")


def opt(a, nom, defaut=None):
    return a[a.index(nom) + 1] if nom in a else defaut


class Rapport:
    def __init__(self):
        self.lignes = []

    def add(self, groupe, nom, niveau, valeur, conseil=""):
        self.lignes.append({"groupe": groupe, "controle": nom, "niveau": niveau, "valeur": valeur, "a_faire": conseil})

    def verdict(self):
        n = [l["niveau"] for l in self.lignes]
        return "A REPRENDRE" if "BLOQUANT" in n else ("OK AVEC CONSEILS" if "CONSEIL" in n else "OK")


def info_video(f):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                   "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt",
                                   "-of", "json", f], capture_output=True).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    n, d = v["r_frame_rate"].split("/")
    return float(j["format"]["duration"]), v, a, float(n) / float(d)


def zones(texte, debut, fin):
    s = [float(x) for x in re.findall(debut + r"[:=]\s*([0-9.]+)", texte)]
    e = [float(x) for x in re.findall(fin + r"[:=]\s*([0-9.]+)", texte)]
    return list(zip(s, e + [None] * (len(s) - len(e))))


def normalise(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", t)


def transcrit(f, modele):
    dossier, nom = os.path.split(os.path.abspath(modele))
    sortie = os.path.join(tempfile.gettempdir(), "verifie_transcription.srt")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.abspath(f), "-vn", "-af",
                    f"whisper=model={nom}:language=auto:queue=10:destination=verifie_transcription.srt:format=srt",
                    "-f", "null", "-"], cwd=dossier, capture_output=True)
    src = os.path.join(dossier, "verifie_transcription.srt")
    if not os.path.exists(src):
        return None
    txt = open(src, encoding="utf-8", errors="ignore").read()
    os.replace(src, sortie)
    return " ".join(l for l in txt.splitlines() if l.strip() and not l.strip().isdigit() and "-->" not in l)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if not a or a[0].startswith("--"):
        print(__doc__)
        return
    f = a[0]
    script = opt(a, "--script")
    duree_cible = float(opt(a, "--duree")) if "--duree" in a else None
    fmt = opt(a, "--format")
    modele = opt(a, "--whisper-model", os.environ.get("WHISPER_MODEL"))
    R = Rapport()

    duree, v, aud, fps = info_video(f)
    w, h = int(v["width"]), int(v["height"])

    # 1. Technique
    if fmt:
        fw, fh = (int(x) for x in fmt.split(":"))
        ok = abs(w / h - fw / fh) < 0.01
        R.add("Technique", "Format", "OK" if ok else "BLOQUANT", f"{w}x{h} (attendu {fmt})", "" if ok else "Refaire la composition au bon format")
    petit = min(w, h) < 1080
    R.add("Technique", "Résolution", "CONSEIL" if petit else "OK", f"{w}x{h}", "Rendre en 1080 minimum sur le petit côté" if petit else "")
    R.add("Technique", "Cadence", "OK" if round(fps) in (24, 25, 30, 50, 60) else "CONSEIL", f"{fps:.2f} i/s")
    compat = v.get("codec_name") == "h264" and v.get("pix_fmt") == "yuv420p"
    R.add("Technique", "Codec (compatibilité réseaux et téléphones)", "OK" if compat else "CONSEIL",
          f"{v.get('codec_name')} / {v.get('pix_fmt')}", "" if compat else "Exporter en H.264, yuv420p")
    if duree_cible:
        ecart = duree - duree_cible
        niv = "OK" if abs(ecart) <= 0.5 else ("CONSEIL" if abs(ecart) <= 2 else "BLOQUANT")
        R.add("Technique", "Durée", niv, f"{duree:.2f} s (cible {duree_cible} s)")
    else:
        R.add("Technique", "Durée", "OK", f"{duree:.2f} s")

    # 2. Image
    m = qc.mouvement(f, fps)
    S = qc.SEUILS
    def lvl(ok_b, ok_c):
        return "OK" if ok_c else ("CONSEIL" if ok_b else "BLOQUANT")
    R.add("Image", "Images fixes", lvl(m["images_fixes"] <= S["images_fixes"]["bloquant"], m["images_fixes"] <= S["images_fixes"]["cible"]),
          f"{m['images_fixes']:.0%} (cible ≤ 40 %)", "Ajouter caméra qui dérive, interface qui agit (production-html.md)")
    R.add("Image", "Plus longue tenue immobile", lvl(m["plus_long_fixe_s"] <= 2.5, m["plus_long_fixe_s"] <= 1.5),
          f"{m['plus_long_fixe_s']} s à {m['plus_long_fixe_debut_s']} s", "Animer ce passage")
    dens = m["animations"] / duree
    R.add("Image", "Densité d'animation", lvl(dens >= 0.5, dens >= 0.65), f"{dens:.2f}/s (cible ≥ 0,65)")
    R.add("Image", "Fondus / sorties dominants", lvl(m["part_ease_in"] <= 0.5, m["part_ease_in"] <= 0.35),
          f"{m['part_ease_in']:.0%} (cible ≤ 35 %)", "Remplacer les fondus par des transitions causées par un objet")
    noir = zones(err(["ffmpeg", "-hide_banner", "-i", f, "-vf", "blackdetect=d=0.25:pix_th=0.08", "-an", "-f", "null", "-"]),
                 "black_start", "black_end")
    noir = [z for z in noir if z[0] > 0.15]
    R.add("Image", "Écrans noirs", "BLOQUANT" if noir else "OK",
          ", ".join(f"{s:.2f}-{e:.2f} s" for s, e in noir) or "aucun", "Trou dans la timeline : une scène manque ou démarre trop tard" if noir else "")
    gele = zones(err(["ffmpeg", "-hide_banner", "-i", f, "-vf", "freezedetect=n=0.002:d=2", "-an", "-f", "null", "-"]),
                 "freeze_start", "freeze_end")
    gele = [(s, e) for s, e in gele if s < duree - 4.5]
    R.add("Image", "Images figées (hors fin)", "BLOQUANT" if gele else "OK",
          ", ".join(f"{s:.2f}-{(e or duree):.2f} s" for s, e in gele) or "aucune", "Scène qui ne s'anime pas : vérifier son script et sa timeline" if gele else "")

    # 3. Son
    if not aud:
        R.add("Son", "Piste audio", "BLOQUANT", "absente", "Ajouter voix, musique et effets")
    else:
        lufs, crete = qc.volume(f)
        R.add("Son", "Volume intégré", lvl(lufs is not None and -16 <= lufs <= -12, lufs is not None and -15 <= lufs <= -13),
              f"{lufs} LUFS (cible -14)", "npx hyperframes normalize-audio ou loudnorm FFmpeg")
        R.add("Son", "Crête", "OK" if crete is not None and crete <= -1 else "CONSEIL", f"{crete} dBFS (cible ≤ -1)")
        sil = zones(err(["ffmpeg", "-hide_banner", "-i", f, "-vn", "-af", "silencedetect=noise=-50dB:d=0.8", "-f", "null", "-"]),
                    "silence_start", "silence_end")
        sil = [(s, e if e is not None else duree) for s, e in sil if s > 0.3]
        R.add("Son", "Silences complets", "BLOQUANT" if sil else "OK",
              ", ".join(f"{s:.2f}-{e:.2f} s" for s, e in sil) or "aucun", "La musique doit couvrir toute la vidéo, fin comprise" if sil else "")
        fin = err(["ffmpeg", "-hide_banner", "-sseof", "-3", "-i", f, "-vn", "-af", "volumedetect", "-f", "null", "-"])
        mv = re.search(r"mean_volume:\s*(-?[0-9.]+)", fin)
        mv = float(mv.group(1)) if mv else -99
        R.add("Son", "Fin de vidéo audible", "BLOQUANT" if mv < -40 else "OK", f"{mv} dB sur les 3 dernières secondes",
              "Musique et impact sur le logo jusqu'à la dernière image" if mv < -40 else "")
        grave = err(["ffmpeg", "-hide_banner", "-i", f, "-vn", "-af",
                     "aresample=8000,lowpass=f=150,asetnsamples=4000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
                     "-f", "null", "-"])
        vals = re.findall(r"RMS_level=(-?[0-9.]+|-inf)", grave)
        if vals:
            absent = sum(1 for x in vals if x == "-inf" or float(x) < -50) / len(vals)
            R.add("Son", "Fond musical continu", "OK" if absent <= 0.25 else "CONSEIL",
                  f"graves absents sur {absent:.0%} de la durée (références : 4-6 %)",
                  "Pas de musique ou musique coupée : en ajouter une (audio.md)" if absent > 0.25 else "")
        ons = qc.impacts(f)
        coupes = qc.coupes(f)
        if coupes:
            sync = sum(1 for c in coupes if any(abs(c - o) <= 0.1 for o in ons))
            R.add("Son", "Coupes franches avec un son", "OK" if sync == len(coupes) else "CONSEIL", f"{sync}/{len(coupes)}",
                  "Placer un whoosh ou un impact sur chaque coupe")

    # 4. Texte et voix
    if script:
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            n = anti.analyse(script)
        R.add("Texte", "Tics d'écriture IA dans le script", "OK" if n == 0 else "CONSEIL", f"{n} alerte(s)",
              "python -I scripts/anti_ia.py " + os.path.basename(script) if n else "")
        if aud and modele and os.path.exists(modele):
            tr = transcrit(f, modele)
            if tr:
                mots_tr = set(normalise(tr))
                phrases = [p for p in re.split(r"(?<=[.!?])\s+|\n+", open(script, encoding="utf-8").read()) if len(normalise(p)) >= 3]
                douteuses = []
                for p in phrases:
                    mots = normalise(p)
                    if sum(1 for x in mots if x in mots_tr) / len(mots) < 0.6:
                        douteuses.append(p.strip()[:70])
                R.add("Voix", "Voix conforme au script", "OK" if not douteuses else "CONSEIL",
                      f"{len(phrases) - len(douteuses)}/{len(phrases)} phrases retrouvées",
                      ("Réécouter : " + " | ".join(douteuses)) if douteuses else "")
        elif aud:
            R.add("Voix", "Voix conforme au script", "CONSEIL", "non vérifiée (pas de modèle Whisper)",
                  "Fournir --whisper-model ou WHISPER_MODEL, ou réécouter en entier")

    manuel = [
        "Coordonnées, prix, nom de marque et appel à l'action identiques à ceux fournis par le client (lettre par lettre)",
        "Orthographe de chaque texte à l'écran ; noms propres ; citations et versets exacts validés par le client",
        "Hook compréhensible son coupé en moins de 2,5 s",
        "Écoute de contrôle de la voix (voix-off.md §8) au casque, en entier",
        "Licences : voix (plan commercial), musique, effets (SOURCES_SFX.md), polices, photos, droits des personnes filmées",
        "Aucune vraie donnée personnelle visible (noms, numéros, messages)",
        "Polices : aucune police de secours (Times, Arial) sur aucune image",
        "Zones de sécurité : texte important hors des 8 % du haut et 10 % du bas en 9:16",
        "Anti « look IA » visuel (anti-ia.md §3) sur la planche d'images",
        "Lecture sur un vrai téléphone, luminosité moyenne, à bout de bras",
    ]

    res = {"fichier": f, "verdict": R.verdict(), "controles": R.lignes, "verifications_manuelles": manuel}
    if "--json" in a:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print(f"{f}  ({duree:.1f} s, {w}x{h}, {fps:.0f} i/s)")
        for l in R.lignes:
            print(f"  {l['niveau']:<8} [{l['groupe']}] {l['controle']} : {l['valeur']}" + (f"  -> {l['a_faire']}" if l["a_faire"] and l["niveau"] != "OK" else ""))
        print(f"  VERDICT AUTOMATIQUE : {R.verdict()}  (+ {len(manuel)} vérifications manuelles, voir le rapport)")
    sortie = opt(a, "--rapport")
    if sortie:
        with open(sortie, "w", encoding="utf-8") as fo:
            fo.write(f"# Rapport de vérification\n\nFichier : `{f}`  \nDurée : {duree:.2f} s · {w}x{h} · {fps:.0f} i/s  \n**Verdict automatique : {R.verdict()}**\n\n")
            fo.write("| Groupe | Contrôle | Niveau | Mesure | À faire |\n|---|---|---|---|---|\n")
            for l in R.lignes:
                fo.write(f"| {l['groupe']} | {l['controle']} | {l['niveau']} | {l['valeur']} | {l['a_faire']} |\n")
            fo.write("\n## Vérifications manuelles (à cocher avant le rendu final)\n\n")
            fo.write("\n".join(f"- [ ] {x}" for x in manuel) + "\n")
        print(f"  Rapport : {sortie}")


if __name__ == "__main__":
    main()
