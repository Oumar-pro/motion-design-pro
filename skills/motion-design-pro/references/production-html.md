# Production en HTML (HyperFrames / GSAP)

À lire **avant d'écrire la moindre scène** quand la vidéo est rendue en HTML. Lire aussi le skill `hyperframes` (contrat, `references/motion.md`) : ses règles techniques priment, ce fichier dit **quoi** construire pour obtenir le style des références.

## Pourquoi le premier essai ressemblait à un PowerPoint (contre-exemple mesuré)

Vidéo test « Nassib » (34,5 s, 9:16) : 86 % d'images fixes (réf. 6-60 %), 8 animations (réf. 20-46), surtout des fondus, une scène = un écran qui apparaît puis attend, éléments petits au centre d'un grand vide, voix de synthèse sur appareil, volume -17,5 LUFS (réf. -14). Tout ce qui suit sert à ne jamais refaire ça.

## Règles anti-diaporama (obligatoires)

1. **Pas de « scène = écran fixe ».** Chaque scène contient au moins 3 temps de mouvement : entrée, action (l'interface agit, un chiffre défile, un élément se coche, la caméra se déplace), sortie qui devient la transition.
2. **Rien d'immobile plus de 1,5 s** (hors fin tenue). Ce qui bouge pendant une tenue : l'interface qui fonctionne, la caméra (dérive lente du plateau, 2-4 % d'échelle ou 20-40 px sur la durée de la scène), un fond (halo qui glisse, particules, motif qui défile). **Les titres posés, eux, restent parfaitement immobiles** : le mouvement passe à l'élément suivant.
3. **Aucun fondu enchaîné entre scènes.** Chaque changement de scène passe par un objet à l'écran (voir « Transitions »). 3 à 5 types de transitions par film, au plus un tiers de coupes franches.
4. **Chevauchement** : l'élément suivant démarre quand le précédent est à 30-50 % de son animation. Jamais séquentiel strict.
5. **Varier les entrées** : pas le même « fondu + montée » sur chaque mot ou chaque scène.

## Une seule scène continue (caméra)

Construire chaque scène sur un **plateau** (`.stage`) plus grand que le cadre, dans un **rig de caméra** (`.cam`). La caméra se déplace (`x`, `y`, `scale`) pendant toute la scène ; les éléments sont posés sur le plateau. C'est ce qui donne l'effet « plan-séquence » des références.

```html
<div id="root">
  <div class="cam" id="cam1">
    <div class="stage" id="stage1"> … éléments … </div>
  </div>
</div>
```
```js
const tl = gsap.timeline({ paused: true });
// dérive continue de la caméra sur toute la scène
tl.fromTo("#cam1", { scale: 1.0, x: 0 }, { scale: 1.04, x: -30, duration: SCENE_DUR, ease: "none" }, 0);
// punch-in sur un élément important (0,5 s, aller-retour)
tl.to("#cam1", { scale: 1.25, x: -180, y: 120, duration: 0.5, ease: "power2.inOut" }, 3.2);
```

## Recettes des techniques des références

Les durées sont en secondes. `expo.out` = preset ENTRÉE, `power2.inOut`/`expo.inOut` = DÉPLACEMENT, `power3.in`/`expo.in` = SORTIE, `back.out(1.7)` = DÉPASSEMENT, `elastic.out(1, 0.5)` = POP (après-effects.md).

**Texte mot par mot calé sur la voix** (V1, V2, V7, V9)
```js
// mots = [{id:"#w1", t:0.12}, …] : t = instant où le mot est prononcé (transcription horodatée)
mots.forEach(m => tl.fromTo(m.id, { opacity: 0, filter: "blur(10px)", y: 18 },
  { opacity: 1, filter: "blur(0px)", y: 0, duration: 0.3, ease: "expo.out" }, m.t - 0.05));
```

**Surlignage qui se dessine** (V2, V7, V9, V13) : un `<span class="hl">` derrière le mot, `scaleX` de 0 à 1 depuis la gauche.
```js
tl.fromTo("#hl1", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.25, ease: "expo.out" }, tMot + 0.08);
```

**Mot qui grossit jusqu'à devenir la scène suivante** (V2 « bachelier », V7 « un plan. »)
```js
tl.to("#motCle", { scale: 1, duration: 0.01 }, t)            // état posé
  .to("#motCle", { scale: 28, x: dx, y: dy, duration: 0.45, ease: "power3.in" }, t + 0.6) // on plonge dans une lettre
  .set("#scene2", { opacity: 1 }, t + 1.0);                    // la couleur de la lettre = fond de la scène suivante
```

**Disque / iris qui ouvre la scène suivante** (V1, V2, V7, V10) : `clip-path: circle()` sur la scène entrante, centré sur l'objet qui déclenche.
```js
tl.fromTo("#scene3", { clipPath: "circle(0% at 50% 45%)" }, { clipPath: "circle(150% at 50% 45%)", duration: 0.35, ease: "expo.in" }, t);
```

**Point qui pulse puis explose** (V11) : POP 0 → 1,44 → 0,89 → 1 en 4 images, ondes concentriques, puis disque plein écran en 4 images.
```js
tl.fromTo("#dot", { scale: 0 }, { scale: 1, duration: 0.25, ease: "elastic.out(1, 0.45)" }, 0.13)
  .fromTo(".ring", { scale: 1, opacity: 0.6 }, { scale: 4, opacity: 0, duration: 0.8, stagger: 0.25, ease: "expo.out" }, 0.3)
  .to("#dot", { scale: 40, duration: 0.14, ease: "expo.in" }, 1.13);
```

**Morphing forme → interface** (V1 point → pastilles, V10 icône → pilule → menu) : un même conteneur change `width`, `height`, `borderRadius` via `scaleX/scaleY` sur un wrapper et un `clip-path: inset(... round R)`, avec un flou horizontal 12 → 0 px ; le contenu de l'état suivant apparaît pendant les 30 derniers %.

**Bandes diagonales** (V8, V11) : 3 rectangles tournés de -30°, plus larges que le cadre, qui traversent en `power3.in` 0,3 s, décalés de 0,04 s ; la dernière bande a la couleur de la scène suivante.

**Vague liquide** (V12) : un `<path>` SVG en forme de vague dont on anime `y` de 100 % à -10 % (0,5 s `power2.inOut`) et le `d` entre deux formes (ou deux vagues décalées en `x`).

**Inversion clair/sombre** : le fond change en 0,4 s `power2.inOut` pendant que l'objet principal reste en place (colour flood), ou par un disque qui part de l'objet.

**Interface qui se construit et agit** (V2, V7, V12)
- Les éléments arrivent décalés de 0,06-0,12 s (`expo.out`), les boutons en `back.out(1.7)`.
- Une main ou un curseur se déplace en `power2.inOut` 0,5 s, le bouton cliqué fait 1 → 0,92 → 1 en 0,2 s, et la réaction (écran suivant, coche, notification) part **sur le rebond du clic**.
- Les champs se remplissent lettre par lettre (0,03-0,05 s par lettre).
- Le téléphone n'est jamais posé à plat et immobile : rotation Y 12-20° qui revient, ou caméra qui s'en approche.

**Chiffres qui défilent** (V4, V6, V7) : un objet `{v:0}` tweené en `expo.out` sur 0,8-1,2 s, `onUpdate` écrit la valeur arrondie et formatée (espaces des milliers, devise).

**Mots géants en filigrane / contour** (V5, V7, V8, V11) : texte à 30-45 % de la hauteur, `-webkit-text-stroke` ou opacité 6-10 %, qui glisse lentement en sens inverse de la caméra (parallaxe).

**Dessin au trait** (V9, V13) : SVG avec `stroke-dasharray` = longueur du chemin, `stroke-dashoffset` de la longueur à 0 en 0,4-0,7 s `expo.out`.

**Bandeaux défilants** (V11) : deux bandes de texte répété, `x` linéaire sur toute la durée (vitesse constante = le seul usage du linéaire).

Avant d'écrire une de ces recettes à la main, chercher l'équivalent dans le registre : `npx hyperframes catalog --tag transition --json` (skill `hyperframes-registry`).

## Rigueur d'atelier (repris du skill « launch-motion », compatible avec nos mesures)

**Curseur et main**
- Jamais en ligne droite : trajet en arc (courbe de Bézier quadratique, point de contrôle décalé de ~15 % de la distance, perpendiculaire au trajet), `power2.inOut`, léger dépassement de 3-6 px à l'arrivée puis retour.
```js
// arc du point A au point B : on anime un paramètre p de 0 à 1 et on calcule x, y
const A = {x: 300, y: 900}, B = {x: 1250, y: 520};
const C = {x: (A.x + B.x) / 2 + 0.15 * (B.y - A.y), y: (A.y + B.y) / 2 - 0.15 * (B.x - A.x)};
const st = {p: 0};
tl.to(st, {p: 1, duration: 0.6, ease: "power2.inOut", onUpdate: () => {
  const p = st.p, q = 1 - p;
  gsap.set("#cursor", {x: q*q*A.x + 2*q*p*C.x + p*p*B.x, y: q*q*A.y + 2*q*p*C.y + p*p*B.y});
}}, t);
```
- **Appui du clic** : le bouton fait 1 → 0,96 → 1 en ~8 images à 60 i/s (0,13 s) ; le curseur se rétracte légèrement (0,9) en même temps ; la réaction de l'interface part sur le rebond.

**Grouper comme dans After Effects (parenting)**
- Les éléments liés (une carte et son contenu, un téléphone et son écran) sont dans un même conteneur parent qu'on anime d'un bloc ; on n'anime pas chaque pièce séparément.
- **Décalage** : chaque élément d'un groupe démarre 2-4 images après le précédent. Les éléments répétés (cartes, lignes, coches) n'apparaissent jamais tous en même temps.
- **Chevauchement** : le mouvement suivant démarre pendant les 20-50 % finaux du précédent.
- Sorties plus courtes que les entrées (~60 % de leur durée), en ease-in.

**Caméra**
- Un rig de caméra par scène ; panoramiques et zooms toujours en ease in-out ; un panoramique sur toute la largeur ne dure pas moins de ~0,8 s.

**Interface et images nettes**
- Interface en **SVG** exporté de Figma plutôt qu'en capture dès que la caméra zoome dessus (net à 250 %). Captures PNG acceptées si la caméra reste à ≤ 120 %.
- Figma fait souvent 1440 px de large : appliquer **un seul facteur d'échelle** par écran et le centrer.
- Fonds derrière l'interface avec une légère parallaxe.

**Polices**
- Charger les polices avant la première image (`@font-face` vers `assets/fonts/`, attendre `document.fonts.ready`). Une police de secours (Times New Roman) qui apparaît = bug bloquant.

**Positionner depuis le centre (déclinaisons sans tout refaire)**
- Tout est placé par rapport au centre du cadre, pas aux bords.
- L'élément clé de chaque plan reste dans le **carré central** (1080×1080 dans un 1920×1080) : le 1:1 et le 9:16 se déclinent alors en recadrant.
- Titres à au moins 5 % de chaque bord.

**Organisation du projet**
- Un composant / une sous-composition par scène ; un fichier de thème partagé (couleurs, polices, constantes d'easing) ; composants partagés Caméra, Curseur, Compteur.
- Textes, chiffres, couleurs et coordonnées dans **un seul fichier de configuration** : une correction client = une ligne.
- Avant le brouillon complet : une **image fixe de l'instant clé de chaque scène** et une image à **chaque frontière de scène** (textes qui se chevauchent, éléments hors cadre).
- Compteurs : ~1 s en ease-out, jamais de saut à la valeur finale en une image.
- Correction demandée : changer le minimum, garder le reste, refaire le rendu.

**Ce qu'on ne reprend pas de launch-motion** (contredit par nos mesures) : la micro-dérive permanente sur tous les éléments (nos titres posés restent immobiles ; seule la caméra et l'interface bougent), les entrées de 0,5 s avec rebond sur tout (nos références : 0,2-0,43 s, rebond seulement sur les éléments qui « pop »), l'absence de voix off.

## Format vertical 9:16 (1080×1920)

Modèle : V12 Wave.
- Titre principal : **6 à 9 % de la hauteur** (115-170 px), 1 à 3 lignes ; texte secondaire au moins 3 % (58 px). Rien sous 40 px.
- Téléphone / produit : **60 à 80 % de la largeur** ; en gros plan, il peut déborder du cadre.
- Composition sur la hauteur : titre dans le tiers haut, sujet au centre, rien d'important dans les 10 % du bas ni les 8 % du haut (interfaces des réseaux).
- Pas de grands vides : si un écran a moins de 50 % de surface occupée, agrandir le sujet ou rapprocher la caméra.

## Vérifications pendant la construction

- `npx hyperframes check --json` après chaque scène.
- Un fichier `<scene>.motion.json` avec `keepsMoving` sur chaque scène et `appearsBy` sur le hook (≤ 0,5 s) : `check` refuse alors une scène figée.
- `npx hyperframes snapshot --composition <id> --frames 8` : regarder chaque scène comme une planche ; si 3 images de suite sont identiques, la scène est un diaporama.
- Sur le brouillon exporté : `python -I scripts/qc.py brouillon.mp4` (voir `validation.md`).
