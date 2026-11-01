"""Trouver un effet sonore : pack local du skill, dossier personnel (ex. Sonniss), puis Freesound (CC0 uniquement).

Usage :
  python -I sfx.py liste                         # tout le pack local, par catégorie
  python -I sfx.py cherche whoosh                # cherche dans le pack local et SFX_DIR
  python -I sfx.py freesound "cash register" [--max 5] [--duree 3]
                                                 # recherche Freesound, licence CC0 seulement
  python -I sfx.py telecharge <id> <dossier_projet>
                                                 # télécharge l'aperçu HQ d'un son Freesound CC0
                                                 # et l'ajoute au registre SOURCES_SFX.md du projet

Variables d'environnement :
  FREESOUND_API_KEY  clé gratuite (https://freesound.org/apiv2/apply)
  SFX_DIR            dossier personnel de sons (ex. bundle Sonniss), fouillé par « cherche »
"""
import sys, os, json, urllib.request, urllib.parse, datetime

ICI = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.normpath(os.path.join(ICI, "..", "assets", "sfx"))
EXT = (".wav", ".mp3", ".ogg", ".flac", ".aif", ".aiff")
API = "https://freesound.org/apiv2"


def fichiers(racine):
    for d, _, fs in os.walk(racine):
        for f in fs:
            if f.lower().endswith(EXT):
                yield os.path.join(d, f)


def liste():
    for cat in sorted(os.listdir(PACK)):
        p = os.path.join(PACK, cat)
        if os.path.isdir(p):
            print(f"{cat}/ : " + ", ".join(sorted(os.listdir(p))))


def cherche(mot):
    mot = mot.lower()
    racines = [PACK] + ([os.environ["SFX_DIR"]] if os.environ.get("SFX_DIR") else [])
    n = 0
    for r in racines:
        for f in fichiers(r):
            if mot in os.path.relpath(f, r).lower():
                print(f)
                n += 1
                if n >= 50:
                    print("… (50 premiers résultats)")
                    return
    if not n:
        print("Aucun son local. Essayer : sfx.py freesound \"" + mot + "\"")


def cle():
    k = os.environ.get("FREESOUND_API_KEY")
    if not k:
        sys.exit("FREESOUND_API_KEY absente. Créer une clé gratuite sur https://freesound.org/apiv2/apply puis la définir comme variable d'environnement.")
    return k


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "motion-design-pro"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def freesound(requete, maxi=8, duree=4.0):
    q = urllib.parse.urlencode({
        "query": requete,
        "filter": f'license:"Creative Commons 0" duration:[0 TO {duree}]',
        "fields": "id,name,duration,license,username,url,avg_rating,num_downloads",
        "sort": "rating_desc",
        "page_size": maxi,
        "token": cle(),
    })
    res = json.loads(get(f"{API}/search/text/?{q}"))
    if not res.get("results"):
        print("Aucun résultat CC0. Essayer un autre mot (en anglais : whoosh, swoosh, impact, riser, pop, click, ding, cash).")
    for s in res.get("results", []):
        print(f"{s['id']:>8}  {s['duration']:5.2f} s  note {s.get('avg_rating', 0):.1f}  {s.get('num_downloads', 0):>6} téléch.  {s['name']}  ({s['username']})  {s['url']}")


def telecharge(son_id, projet):
    k = cle()
    s = json.loads(get(f"{API}/sounds/{son_id}/?fields=id,name,license,username,url,previews&token={k}"))
    if "publicdomain/zero" not in s["license"]:
        sys.exit(f"Refusé : licence {s['license']} (seul CC0 est accepté sans vérification).")
    dossier = os.path.join(projet, "assets", "sfx")
    os.makedirs(dossier, exist_ok=True)
    nom = "".join(c if c.isalnum() or c in "-_" else "_" for c in os.path.splitext(s["name"])[0])[:40]
    chemin = os.path.join(dossier, f"fs{s['id']}_{nom}.mp3")
    with open(chemin, "wb") as f:
        f.write(get(s["previews"]["preview-hq-mp3"]))
    registre = os.path.join(projet, "SOURCES_SFX.md")
    neuf = not os.path.exists(registre)
    with open(registre, "a", encoding="utf-8") as f:
        if neuf:
            f.write("# Sources des effets sonores\n\n| Fichier | Source | Auteur | Licence | Date |\n|---|---|---|---|---|\n")
        f.write(f"| {os.path.basename(chemin)} | {s['url']} | {s['username']} | CC0 | {datetime.date.today()} |\n")
    print(chemin)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if not a or a[0] == "liste":
        liste()
    elif a[0] == "cherche":
        cherche(a[1])
    elif a[0] == "freesound":
        maxi = int(a[a.index("--max") + 1]) if "--max" in a else 8
        duree = float(a[a.index("--duree") + 1]) if "--duree" in a else 4.0
        freesound(a[1], maxi, duree)
    elif a[0] == "telecharge":
        telecharge(a[1], a[2])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
