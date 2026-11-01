"""Générer la voix off avec ElevenLabs, bloc par bloc, avec l'instant de chaque mot.

Usage :
  python -I voix_elevenlabs.py voix                                   # liste les voix du compte
  python -I voix_elevenlabs.py genere <voice_id> <script.txt> <dossier> [--prises 3] [--modele eleven_multilingual_v2]
        [--stabilite 0.48] [--similarite 0.75] [--style 0] [--vitesse 1.03]

script.txt : un bloc par paragraphe (séparés par une ligne vide), un bloc = une scène.
Sortie dans <dossier> : bloc01_prise1.mp3 …, bloc01_prise1.mots.json (mot, début, fin en secondes),
et reglages.json (voix, modèle, réglages, seed de chaque prise) pour reproduire la prise choisie.

Clé : variable d'environnement ELEVENLABS_API_KEY. Chaque prise consomme ~1 crédit par caractère.
Plan gratuit = usage non commercial : ne servir qu'aux tests et échantillons (voir references/voix-off.md).
"""
import sys, os, json, base64, random, urllib.request

API = "https://api.elevenlabs.io/v1"


def cle():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k:
        sys.exit("ELEVENLABS_API_KEY absente (Profil ElevenLabs > API Keys), à définir en variable d'environnement.")
    return k


def appel(chemin, corps=None):
    req = urllib.request.Request(API + chemin, method="POST" if corps else "GET",
                                 headers={"xi-api-key": cle(), "Content-Type": "application/json", "User-Agent": "motion-design-pro"},
                                 data=json.dumps(corps).encode() if corps else None)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def opt(a, nom, defaut, typ=float):
    return typ(a[a.index(nom) + 1]) if nom in a else defaut


def mots(al):
    res, mot, debut = [], "", None
    for c, s, e in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if mot:
                res.append({"mot": mot, "debut": round(debut, 3), "fin": round(fin, 3)})
            mot, debut = "", None
        else:
            if debut is None:
                debut = s
            mot += c
            fin = e
    if mot:
        res.append({"mot": mot, "debut": round(debut, 3), "fin": round(fin, 3)})
    return res


def genere(voice_id, script, dossier, a):
    os.makedirs(dossier, exist_ok=True)
    blocs = [b.strip() for b in open(script, encoding="utf-8").read().split("\n\n") if b.strip()]
    reglages = {
        "stability": opt(a, "--stabilite", 0.48),
        "similarity_boost": opt(a, "--similarite", 0.75),
        "style": opt(a, "--style", 0.0),
        "use_speaker_boost": True,
        "speed": opt(a, "--vitesse", 1.03),
    }
    modele = opt(a, "--modele", "eleven_multilingual_v2", str)
    prises = opt(a, "--prises", 3, int)
    if modele.startswith("eleven_v3"):
        reglages.pop("similarity_boost")
        reglages.pop("use_speaker_boost")
    total = sum(len(b) for b in blocs) * prises
    print(f"{len(blocs)} blocs × {prises} prises ≈ {total} crédits")
    journal = {"voice_id": voice_id, "modele": modele, "reglages": reglages, "prises": []}
    for i, texte in enumerate(blocs, 1):
        for p in range(1, prises + 1):
            seed = random.randint(1, 4294967295)
            r = appel(f"/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128",
                      {"text": texte, "model_id": modele, "voice_settings": reglages, "seed": seed})
            base = os.path.join(dossier, f"bloc{i:02d}_prise{p}")
            with open(base + ".mp3", "wb") as f:
                f.write(base64.b64decode(r["audio_base64"]))
            al = r.get("normalized_alignment") or r.get("alignment")
            if al:
                with open(base + ".mots.json", "w", encoding="utf-8") as f:
                    json.dump(mots(al), f, ensure_ascii=False, indent=1)
            journal["prises"].append({"fichier": os.path.basename(base) + ".mp3", "bloc": i, "texte": texte, "seed": seed})
            print(base + ".mp3")
    with open(os.path.join(dossier, "reglages.json"), "w", encoding="utf-8") as f:
        json.dump(journal, f, ensure_ascii=False, indent=1)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a and a[0] == "voix":
        for v in appel("/voices")["voices"]:
            lab = v.get("labels") or {}
            print(f"{v['voice_id']}  {v['name']}  {lab.get('language', '')} {lab.get('accent', '')} {lab.get('use_case', '')}")
    elif len(a) >= 4 and a[0] == "genere":
        genere(a[1], a[2], a[3], a)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
