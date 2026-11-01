"""Repère les tics d'écriture « IA » dans un script, une voix off ou une légende.

Usage : python -I anti_ia.py <fichier.txt|.md> [autres fichiers…]
Liste des règles : references/anti-ia.md. Sortie : une ligne par alerte (fichier:ligne, règle, extrait).
"""
import sys, re

MOTS = ["véritable", "incontournable", "révolution", "plongez", "plonger dans", "découvrez", "sublimer",
        "libérer le potentiel", "au cœur de", "sans compromis", "fluide", "booster", "un jeu d'enfant",
        "en toute sérénité", "l'avenir de", "dans un monde où", "imaginez", "que vous soyez",
        "élevez", "transformez", "game changer", "next level"]
OUVERTURES = ["bien sûr", "excellente question", "voici", "absolument", "certainement"]

REGLES = [
    ("Tiret cadratin", re.compile("—")),
    ("Tiret demi-cadratin en incise", re.compile(" – ")),
    ("« Ce n'est pas X, c'est Y »", re.compile(r"\b(ce n['’]est pas|c['’]est pas)\b[^.!?\n]{1,60}\bc['’]est\b", re.I)),
    ("« Pas seulement / non seulement »", re.compile(r"\b(pas seulement|non seulement|pas juste|plus qu['’]un(e)?)\b", re.I)),
    ("Question rhétorique + réponse", re.compile(r"\b(le résultat|le secret|la solution|la différence|pourquoi)\s*\?", re.I)),
    ("Émoji", re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅❌]")),
    ("Mise en forme résiduelle", re.compile(r"(\*\*[^*]+\*\*|^\s*#{1,6}\s|[─-╿])", re.M)),
    ("Mot gonflé", re.compile(r"\b(" + "|".join(re.escape(m) for m in MOTS) + r")", re.I)),
    ("Ouverture de chatbot", re.compile(r"^\s*(" + "|".join(OUVERTURES) + r")\b", re.I | re.M)),
]
TRIADE = re.compile(r"\b[\wÀ-ÿ'’-]+(?: [\wÀ-ÿ'’-]+)?, [\wÀ-ÿ'’-]+(?: [\wÀ-ÿ'’-]+)?,? et [\wÀ-ÿ'’-]+", re.I)


def analyse(chemin):
    n = 0
    triades = []
    lignes = open(chemin, encoding="utf-8").read().splitlines()
    for i, l in enumerate(lignes, 1):
        for nom, rx in REGLES:
            for m in rx.finditer(l):
                print(f"{chemin}:{i}  {nom}  «{l[max(0, m.start() - 25):m.end() + 25].strip()}»")
                n += 1
        for m in TRIADE.finditer(l):
            triades.append((i, m.group(0)))
    if len(triades) > 1:
        for i, t in triades:
            print(f"{chemin}:{i}  Triade ({len(triades)} dans le texte, 1 max)  «{t}»")
            n += 1
    return n


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__)
        return
    total = sum(analyse(f) for f in sys.argv[1:])
    print(f"\n{total} alerte(s)." + (" Texte propre." if total == 0 else " Corriger ou justifier chaque alerte (references/anti-ia.md)."))


if __name__ == "__main__":
    main()
