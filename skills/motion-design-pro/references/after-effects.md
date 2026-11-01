# Spécification d'animation After Effects / Motion

Valeurs issues de mesures image par image sur 292 animations (13 vidéos) et du suivi de formes isolées. La traduction en influences After Effects est [DÉDUIT] : les réglages exacts des animateurs sont [INCONNU].

## Répartition mesurée

| Pic de vitesse | Courbe | Part | Usage |
|---|---|---|---|
| 1er tiers | ease-out | 41 % | Entrées de texte et d'interface |
| Milieu | ease-in-out | 42 % | Déplacements, morphings, caméra |
| Dernier tiers | ease-in | 17 % | Sorties, balayages de transition |

Durée médiane d'une animation : 183 à 450 ms (200 à 430 ms en général), soit 6 à 14 images à 30 i/s.

## Presets à appliquer

| Preset | Usage | Influence sortante (clé 1) | Influence entrante (clé 2) | Équivalent cubic-bezier | Durée @30 i/s |
|---|---|---|---|---|---|
| **ENTRÉE** | Mot, carte, bouton, élément UI qui arrive | 0-15 % | 80-90 % | `0.16, 1, 0.3, 1` (expo out) | 8-12 im. |
| **DÉPLACEMENT** | Morph, déplacement, mouvement de caméra | 60-80 % | 60-80 % | `0.83, 0, 0.17, 1` (expo in-out) | 10-18 im. |
| **SORTIE / BALAYAGE** | Élément qui part, disque ou bande de transition | 80-90 % | 0 % (linéaire jusqu'à la coupe) | `0.7, 0, 0.84, 0` (expo in) | 4-6 im. |
| **POP** | Point, icône, bouton qui apparaît | Clés d'échelle : 0 → 115-145 % → 90 % → 100 % | - | ressort (amplitude ~0,4, fréquence 3-4, amortissement fort) | 4-8 im. |
| **DÉPASSEMENT** | Fin d'un déplacement latéral | Clé à 115-120 % de la distance, puis retour | - | back out ≈ 1,7 | ~6 im. de retour |
| **PULSE** | Battement sur un temps fort | Échelle 100 → 110 → 100 % | - | ease in-out | 2-4 im. |

### Mesures de référence
- Pop d'un point (V11) : 0 → 26 → 16 → 18 px : +44 % puis −11 %, stable en 4 images (~130 ms), puis pulse 18 → 20 → 18 sur le temps fort.
- Balayage circulaire (V10, V11) : diamètre 24 → 54 → 100 → 186 → plein écran ; double à chaque image, plein écran en 4 images.
- Déplacement latéral (V6) : dépassement ~18 %, retour en ~200 ms.
- Rebond de balle (V6) : chute accélérée (0,5 → 1,8 → 8 → 12 px/image), remontée décélérée : gravité = ease-in puis ease-out à chaque rebond, avec squash & stretch.

## Règles par type d'élément

**Texte**
- Apparition mot par mot, décalage 3-5 images entre mots (ou calé sur la voix).
- Chaque mot : opacité 0 → 100 %, flou 8-12 px → 0, position Y +10-20 px → 0, preset ENTRÉE.
- Surlignage : masque ou trim d'un rectangle de gauche à droite, 6-8 images, preset ENTRÉE, démarre 2-3 images après le mot.
- Mot clé en transition : échelle 100 → 2000 %+ en preset SORTIE, l'intérieur d'une lettre devient la scène suivante.
- Lettres en chute : rotation aléatoire ±30°, décalage 1-2 images par lettre, flou de mouvement activé.

**Interface**
- Construction pièce par pièce : décalage 2-4 images entre éléments, preset ENTRÉE ou POP pour les boutons.
- Curseur ou main : déplacement preset DÉPLACEMENT, clic = POP inversé du bouton (100 → 92 → 100 %).
- Chiffres : compteur (expression ou Slider Control) en preset ENTRÉE sur 15-30 images, finir sur la valeur exacte.
- Barre de progression : remplissage ease-out, avec petits arrêts (5 % … 100 %).
- Téléphone ou carte en 3D : rotation Y 15-25° qui revient à 0, preset DÉPLACEMENT ; léger flottement continu (±2-4 px, 2-3 s) pendant les tenues.

**Transitions**
- Disque/cercle : preset SORTIE, 4-6 images, calé sur un temps fort, whoosh ou impact.
- Bandes diagonales : 2-4 bandes décalées de 1-2 images, preset SORTIE.
- Vague liquide : chemin animé ou Wave Warp, 10-15 images.
- Inversion clair/sombre : disque qui s'ouvre depuis le centre ou depuis l'élément qui morphe.

**Illustration**
- Trim Paths 0 → 100 %, preset ENTRÉE, 12-20 images ; remplissage (verre, jauge) en ease-out.

## Rigueur d'atelier (repris de « launch-motion »)
- Curseur en arc (pas en ligne droite), ease in-out, léger dépassement à l'arrivée ; clic = bouton 100 → 96 → 100 % en ~8 images à 60 i/s.
- Parenting : regrouper les éléments liés sous un Null et animer le Null ; décaler les enfants de 2-4 images ; chevaucher les mouvements (le suivant démarre dans les 20-50 % finaux du précédent).
- Interface importée en vectoriel (Illustrator/SVG, calques de forme) pour rester nette quand la caméra zoome.
- Composer depuis le centre, élément clé dans le carré central, pour décliner 9:16 et 1:1 en recadrant.
- Textes, chiffres et couleurs pilotés par un calque de contrôle (Essential Graphics ou Null avec curseurs) : une correction client = une valeur.
- Avant le rendu : image fixe de chaque frontière de scène pour vérifier chevauchements et sorties de cadre.

## Réglages de projet
- 1920×1080 (16:9) et 1080×1920 (9:16), 30 i/s par défaut ; 60 i/s si beaucoup de défilements d'interface.
- Flou de mouvement activé sur les calques rapides (angle d'obturateur 180° par défaut [DÉDUIT]).
- Construire en compositions imbriquées par scène, marqueurs de calque sur chaque mot de la voix et chaque temps fort.
- Outils utiles (optionnels) : Flow / Motion Tools pour les presets de courbes, expressions d'overshoot pour POP. [INCONNU] : outils réellement utilisés dans les références.
