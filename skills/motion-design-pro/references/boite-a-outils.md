# Boîte à outils

Outils retenus par l'utilisateur (31/10/2026), avec leur place dans la chaîne de production. Règle commune : **chaque image doit dépendre uniquement du temps de la vidéo** (rendu image par image, qu'on peut rejouer dans n'importe quel ordre). Pas d'horloge, pas de `requestAnimationFrame`, pas d'aléatoire sans graine.

| Étape | Outil | Rôle |
|---|---|---|
| Capturer | **OBS Studio** | Filmer la vraie appli ou le vrai site du client |
| Animer | **HyperFrames** ou **Remotion** | Moteur vidéo (un seul par projet) |
| 3D | **Three.js** | Téléphone, produit, logo en 3D |
| Physique | **Rapier** | Objets qui tombent, s'empilent, rebondissent pour de vrai |
| Voix | ElevenLabs, **Voice Studio** (local) | Voix off |
| Transcrire, synchroniser | **Whisper** (faster-whisper) | Instant de chaque mot, vérification de la voix |
| Analyser la musique | **librosa** | Tempo et temps forts pour caler les transitions |
| Sons sur mesure | **Tone.js** | Risers, ticks, stingers calés sur le BPM |
| Finir | FFmpeg, `scripts/qc.py` | Mix, export, contrôle |

## Autres outils évalués (liste « 20 skills », 31/10/2026)

| Outil | Verdict | Quand |
|---|---|---|
| **Remotion Skills** (remotion-dev/skills) | ✅ Installer si on utilise Remotion | Skills officiels pour agents : à lire avant d'écrire du Remotion, nos règles de style restent prioritaires |
| **WhisperX** | ✅ Préféré pour la synchro | Alignement mot par mot plus précis que Whisper seul : instant d'apparition de chaque mot |
| **LosslessCut** | ✅ | Couper les enregistrements OBS sans réencoder (garder les bons passages) |
| **Lottie** (lottie-web) | ✅ Si fourni | Logo ou icônes animés livrés par le designer (fichier .json / .lottie). Piloter l'image Lottie depuis le temps de la vidéo (`goToAndStop`), jamais en lecture libre |
| **MCP for Blender** | ⚠️ Pour la 3D produit | Claude construit une scène Blender (packshot, canette qui tourne) ; rendu en images puis intégré. Long à rendre : réservé aux plans héros |
| **three-gpu-pathtracer** | ⚠️ Plans héros 3D | Reflets et lumière réalistes dans Three.js ; lent, mais le rendu image par image le permet |
| **postprocessing** (pmndrs) | ⚠️ Avec mesure | Bloom, profondeur de champ, étalonnage sur une scène Three.js. Trop de bloom = « look IA » (`anti-ia.md`) |
| **three.quarks** | ⚠️ Avec mesure | Particules et traînées 3D ; seulement si elles servent l'action (étincelle qui guide le regard) |
| **Tweakpane** | ⚠️ Pendant le réglage | Curseurs en direct pour régler une scène ; retirer avant le rendu |
| **Jolt Physics** | ➖ Doublon | Rapier suffit ; même règle de simulation pré-calculée |
| **Anime.js, Motion** (motiondivision) | ➖ Doublon | GSAP (HyperFrames) ou Remotion font déjà le travail ; ne pas mélanger les moteurs d'animation |
| **Manim** | ➖ Hors sujet pub | Schémas et équations animés : utile pour une vidéo explicative technique, pas pour une pub |
| **CosyVoice** | ➖ À tester seulement | Voix multilingue open source ; français et licence à vérifier, écoute de contrôle `voix-off.md` §8 obligatoire |
| **ComfyUI** | ❌ Pas pour des personnes ou du texte | Risque « look IA » et licences floues ; au mieux pour des fonds ou textures abstraits |

## OBS Studio : la vraie interface

La vraie appli filmée vaut mieux que n'importe quelle reconstruction (anti « look IA », `anti-ia.md`).
- Téléphone Android : le recopier sur le PC avec **scrcpy** (gratuit), puis le filmer dans OBS. iPhone : enregistrement d'écran natif.
- Canevas OBS à la résolution native du téléphone (ex. 1080×2400), **60 i/s**, encodeur matériel en qualité constante (CQP/CRF ~16-18), enregistrement en **MKV** puis « Remux » en MP4 (un MKV survit à un plantage).
- Avant de filmer : compte de démonstration avec **prénoms et montants fictifs mais plausibles** (jamais de vraies données personnelles), barre d'état propre (batterie pleine, heure ronde, pas de notifications), mode sombre ou clair selon la charte.
- Gestes lents et nets, une action à la fois, 1 s d'arrêt entre deux écrans : on accélère et on recadre ensuite dans le moteur vidéo (zoom de caméra sur le bouton, etc.).
- Dans la vidéo : le film d'écran va **dans** le cadre du téléphone, et la caméra du moteur fait les zooms. Ne jamais zoomer à plus de 150 % d'une capture (flou).

## Remotion : le moteur React

- **Licence** : gratuit pour un **individu**, y compris pour des vidéos commerciales de clients ; payant pour une entreprise de plus de 3 personnes. La licence doit changer avec Remotion 5.0 : la revérifier à chaque nouvelle version majeure. Source : `LICENSE.md` du dépôt remotion-dev/remotion.
- Choisir **HyperFrames ou Remotion par projet**, pas les deux. Remotion si l'utilisateur veut du React et des composants réutilisables entre projets ; HyperFrames pour l'aperçu Studio et le connecteur.
- Démarrer : `npx create-video@latest`, puis `npx remotion studio` (aperçu) et `npx remotion render` (export).
- Traduction de nos presets (`after-effects.md`) :
  - ENTRÉE : `interpolate(frame, [d, d + 10], [0, 1], {easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateLeft: "clamp", extrapolateRight: "clamp"})`
  - DÉPLACEMENT : `Easing.bezier(0.83, 0, 0.17, 1)` ; SORTIE : `Easing.bezier(0.7, 0, 0.84, 0)`
  - POP : `spring({frame: frame - d, fps, config: {damping: 10, stiffness: 180}})` (dépassement visible) ; sans rebond : `damping: 200`.
- Une scène = un `<Sequence>` ; caméra = un `<AbsoluteFill>` parent animé ; textes, chiffres, couleurs dans un seul fichier de config (`production-html.md`, rigueur d'atelier).
- Polices : `@remotion/google-fonts` ou `staticFile()` + `delayRender()` jusqu'à `document.fonts.ready`.
- Son : `<Audio>` avec `volume` en fonction de la frame pour le ducking ; effets sonores du pack `assets/sfx/` dans `public/`.
- Après le rendu : `scripts/qc.py` fonctionne sur n'importe quel MP4.

## Three.js : la 3D

- Usages : téléphone en 3D qui pivote, produit (canette, boîte) qui tourne, logo en relief, plateau qui défile en profondeur.
- Dans Remotion : `@remotion/three` (`<ThreeCanvas>`), la rotation calculée depuis `useCurrentFrame()`. Dans HyperFrames : runtime 3D du skill `hyperframes` (`references/runtimes.md`).
- Interdit : `clock.getDelta()`, `requestAnimationFrame`, boucles d'animation propres à Three.js. Tout se calcule depuis le temps de la vidéo.
- Modèles en glTF/GLB, éclairage simple (une lumière principale + environnement doux), pas de matières « plastique brillant » génériques.
- 3D au service d'un message : un mouvement de caméra lent et un seul objet héros, pas un décor 3D chargé.

## Rapier : la physique

- Usages : cartes ou pièces qui tombent et s'empilent, notifications qui s'entassent, canettes qui roulent. Paquet JavaScript `@dimforge/rapier3d-compat` (ou `rapier2d-compat` pour de la 2D).
- **Piège principal** : le rendu saute d'image en image dans n'importe quel ordre. On ne simule donc pas pendant le rendu : on **pré-calcule (« bake »)** toute la simulation au chargement, à pas fixe (1/60 s), en enregistrant positions et rotations de chaque objet, puis chaque image lit l'état correspondant à son temps.
- Graine fixe pour toute valeur aléatoire (positions de départ), sinon le rendu change à chaque export.
- La physique fait le mouvement, la mise en scène reste nôtre : arrêt net des objets avant le texte, aucun objet qui sort du cadre sans raison.

## Voice Studio (voix locale)

Plusieurs projets portent ce nom (par exemple msrbuilds/voice-studio, interface locale qui regroupe plusieurs moteurs : Kokoro, Chatterbox, VibeVoice, Qwen3-TTS… ; ou debpalash/VoiceStudio, application de bureau). Règles, quel que soit le projet :
- La **licence de chaque moteur** compte, pas seulement celle de l'interface : certains modèles interdisent l'usage commercial. La vérifier avant une pub.
- **Kokoro** reste interdit pour une voix finale en français (`voix-off.md`). Tester les autres moteurs avec l'écoute de contrôle de `voix-off.md` §8.
- Le clonage de voix seulement avec l'accord écrit de la personne.
- Même méthode qu'avec ElevenLabs : script écrit pour l'oreille, blocs par scène, 3 prises, échantillon validé à la porte 3.

## Whisper : synchroniser et vérifier la voix

- Préférer **faster-whisper** (plus rapide) avec un modèle **large-v3** ou **medium** pour le français. Le modèle « base » (celui du filtre FFmpeg de ce poste) se trompe sur les noms et les mots rares : il sert à repérer, pas à juger.
- Horodatage par mot (`word_timestamps=True`) : sert à faire apparaître chaque mot à l'écran au moment où il est dit (mode A, `audio.md`).
- Contrôle : comparer la transcription au script ; un écart sur un mot clé, un chiffre ou un verset = réécouter ce passage.

## librosa : caler l'image sur la musique

- `scripts/beats.py musique.mp3` (librosa) donne le tempo, la liste des temps forts et des attaques en secondes, dans `beats.json`.
- Utilisation : chaque transition de scène se place sur un temps fort (à ± 1 image) ; les apparitions de mots sur les croches si la voix ne les impose pas.
- Si le tempo de la musique ne colle pas au montage, couper la musique sur une mesure, ne jamais étirer la voix.

## Tone.js : sons sur mesure

- Usages : riser qui monte exactement jusqu'à la coupe, ticks de compteur au tempo, petit motif musical sur le logo, variantes de sons pour ne pas répéter le même fichier.
- Rendu hors ligne vers un fichier WAV (`Tone.Offline`), puis placement dans le mix comme les autres sons. Pas de son généré en direct pendant le rendu vidéo.
- Caler sur le BPM du projet (`Tone.Transport.bpm`), le même que la musique.
- Tone.js ne remplace pas une vraie musique : un fond entièrement synthétique sonne « généré ». Il complète le pack `assets/sfx/`.
