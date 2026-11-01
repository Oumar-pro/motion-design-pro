---
name: motion-design-pro
description: Studio de vidéos motion design publicitaires (pub d'appli, de produit, de marque, d'école, d'entreprise, 10 à 60 s, 16:9 ou 9:16) au niveau de 13 références mesurées image par image. Couvre la collecte des infos et visuels, le script voix off + texte à l'écran, le storyboard, les animations et transitions chiffrées (HyperFrames, Remotion, After Effects), la voix (ElevenLabs), la musique et les effets sonores, l'anti « look IA », et une vérification finale automatique obligatoire avant tout rendu. Utilise ce skill dès que l'utilisateur demande une vidéo motion, une pub animée, une vidéo d'appli ou de produit, un kinetic text, une vidéo promo, un script ou un storyboard de motion, ou veut améliorer, vérifier ou corriger une vidéo motion existante, même formulé vaguement (« fais-moi une vidéo motion », « une pub pour mon appli », « vérifie ma vidéo »). Commencer TOUJOURS par la collecte et ne JAMAIS lancer de rendu final ou de génération payante sans vérification finale et validation écrite.
---

# Motion Design Pro

Studio de pubs motion courtes. Le niveau visé est celui des références (Sama, Push, Wave, AMF, Safe Home, 3X, Pocketsflow, Telegram, Nexo). Toutes les valeurs viennent de mesures (`references/metrics.md`).

## Quand utiliser ce skill

| Oui | Non (ou autre skill d'abord) |
|---|---|
| Pub ou promo animée d'une appli, d'un produit, d'une marque, d'un service | Montage de vidéos filmées (interview, vlog) sans motion : skill `hyperframes` seul |
| Vidéo d'appli : parcours, fonctionnalités, tutoriel animé | Diaporama ou présentation à projeter en direct : skill `slideshow` |
| Kinetic text, titre animé, fin de vidéo avec logo | Animation de personnage ou dessin animé long : `hyperframes` (types/character) |
| Améliorer, vérifier ou corriger une vidéo motion existante | Simple conversion, découpe ou compression d'un fichier : FFmpeg directement |
| Script, storyboard ou brief d'une vidéo motion | Image fixe (affiche, post) : `canvas-design` |

Pour une vidéo existante à corriger : lancer d'abord `scripts/verifie.py` dessus, montrer le rapport, puis reprendre le workflow à l'étape concernée.

## Les trois règles qui ne se discutent pas

1. **Collecte complète avant tout.** Demande vague ou incomplète : pas de script ni de storyboard. Questions par rondes (`references/questionnaire.md`, 4 par ronde au plus), chaque visuel demandé un par un avec son format, défauts proposés quand l'utilisateur ne sait pas, récapitulatif `templates/brief.md` (✅ / ⏳ / provisoire). Bloquants : produit et offre, objectif et appel à l'action, cible, format et durée, langue et voix off, logo, visuels du produit.
2. **Quatre validations, rien de payant avant** (`references/validation.md`) : Brief → Script et concept → Échantillon de voix → Dossier de pré-rendu. Présenter, puis attendre un oui explicite à chaque porte. Pas de voix complète, pas de musique générée, pas de rendu final sans ce oui.
3. **Vérification finale obligatoire** (`references/verification-finale.md`) : `scripts/verifie.py` sur le brouillon avant la porte 4, puis sur le fichier final avant la livraison. Un seul BLOQUANT = on corrige, on ne présente pas. Les vérifications manuelles du rapport sont cochées une par une.

## Workflow

1. **Collecte** → porte 1.
2. **Concept et hook** : une des 4 familles (question au spectateur, rupture de format, forme ou logo qui s'assemble, mascotte ; `patterns.md` §1), 2 variantes de première phrase.
3. **Script** deux colonnes (voix | texte écran | visuel | durée) écrit pour l'oreille (`voix-off.md` §5) et sans tics IA (`anti-ia.md`) ; `scripts/anti_ia.py` sans alerte → porte 2.
4. **Voix** : échantillon 5-10 s dans 2-3 voix françaises natives (`voix-off.md`) → porte 3.
5. **Storyboard** (`templates/storyboard.md`) : chaque scène a une entrée, une action pendant la tenue, une transition causée par un objet, ses sons.
6. **Construction** : HyperFrames (`production-html.md`, après le skill `hyperframes`), Remotion, Three.js, Rapier (`boite-a-outils.md`) ou After Effects (`after-effects.md`). Vraie interface filmée avec OBS plutôt que reconstruite.
7. **Son** : voix traitée, musique sur toute la durée, effets du pack `assets/sfx/` sur chaque transition et apparition, mix à -14 LUFS (`audio.md`) ; temps forts de la musique avec `scripts/beats.py`.
8. **Vérification finale du brouillon** : `verifie.py` + planche d'images + vérifications manuelles.
9. **Dossier de pré-rendu** avec le rapport → porte 4.
10. **Rendu final** après le oui, puis `verifie.py` sur le fichier livré, rapport joint.

## À faire

- Hook en 2,4 s : une idée adressée au spectateur, écrite mot par mot sur la voix, mot clé surligné, mouvement dès la première image.
- Une idée par écran ; phrases fortes coupées en deux écrans.
- Caméra qui dérive en continu ; interface qui agit pendant les tenues (curseur en arc, appui du clic, saisie, coches, compteurs).
- Transitions causées par un objet (morph, zoom dans un mot, iris, vague, bandes, inversion clair/sombre), 3 à 5 types par film, chacune sur un temps fort avec un son.
- Ease par rôle : entrées expo-out, déplacements expo in-out, sorties expo-in, rebond seulement sur ce qui « pop » ; 6 à 14 images à 30 i/s.
- Palette 1 accent + 2 neutres, ni noir ni blanc purs ; sans-serif grasse, 3 niveaux de texte.
- En 9:16 : titre à 6-9 % de la hauteur, sujet à 60-80 % de la largeur, rien d'important dans les 8 % du haut et 10 % du bas.
- Voix humaine ou synthèse premium validée sur échantillon ; mots à l'écran calés sur la voix.
- Musique du début à la dernière image, baissée sous la voix ; -14 LUFS, crête ≤ -1 dBTP.
- Détails vrais et locaux : prénoms, devise, lieux, langue locale, vraie interface.
- Fin tenue 3-5 s : logo, accroche, bouton, contacts ajoutés un par un, avec son.

## À éviter

- Une scène = un écran qui apparaît en fondu puis attend (effet PowerPoint).
- Fondus enchaînés entre scènes ; le même « fondu + montée » sur tout.
- Titres qui flottent ou respirent après s'être posés ; rebond sur toute l'interface.
- Petits éléments au milieu d'un grand vide ; captures basse définition agrandies.
- Voix de synthèse sur appareil (Kokoro) en version finale ; points de suspension dans le texte de la voix.
- Fin muette, silences, musique qui s'arrête avant la dernière image.
- Tics IA : tiret cadratin, « ce n'est pas X, c'est Y », triades en série, émojis, mots gonflés (`anti-ia.md`).
- Faux texte, visages générés, dégradé violet par défaut, clichés (fusée, ampoule, poignée de main).
- Vraies données personnelles dans les captures ; son ou police sans licence.
- Mélanger plusieurs moteurs d'animation dans un même projet.

## Pièges déjà rencontrés (et la parade)

| Piège | Parade |
|---|---|
| Première vidéo Nassib : 86 % d'images fixes, fondus, hook de 4 s | Règles anti-diaporama de `production-html.md`, contrôle `verifie.py` |
| Voix robotique (Kokoro) | Voix française native premium, `voix-off.md` |
| Connecteur ElevenLabs « qui ne fait pas de voix » | Les outils `agents_*` sont pour les agents vocaux ; la voix off passe par `creative_list_voices` et `creative_generate_speech` (à charger si absents) |
| Plan ElevenLabs gratuit utilisé pour une pub | Gratuit = tests seulement ; voix finale sur un plan commercial |
| Contrôle trop sévère sur une vidéo à 60 i/s | `qc.py` et `verifie.py` analysent à 30 i/s |
| Captures client de 253×512 px floues en gros plan | Demander des captures natives ou filmer avec OBS ; sinon reconstruire avec des données fictives |
| Pauses bizarres dans la voix | Pas de points de suspension ; virgule, point ou un seul `<break>` par phrase |
| Verset ou citation reformulé | Texte exact fourni par le client, marqué « à valider » |
| Vidéo AmanaTa sans musique, fin muette 4,5 s | Contrôles « silences », « fin audible » et « fond musical » de `verifie.py` |
| Scène qui ne s'anime pas au rendu, ou point de zoom décalé | Identifiants uniques, coordonnées fixes plutôt que mesurées pendant le rendu, planche d'images de chaque scène |
| Simulation physique différente à chaque export | Pré-calculer la simulation (Rapier), graine fixe |
| Dernière image d'une transition grise ou vide | Planche aux frontières de scène ; finir la transition sur la couleur de la scène suivante |

## Outils et skills : ce que c'est, quand l'utiliser

Avant d'utiliser un outil, vérifier qu'il est disponible dans la session (connecteur visible, commande installée). S'il manque, le dire à l'utilisateur et proposer l'alternative de la dernière colonne.

**Autres skills**

| Skill | Ce que c'est | Quand l'utiliser | Sinon |
|---|---|---|---|
| `hyperframes` | Fabrique la vidéo en HTML/GSAP, rendue image par image | Moteur par défaut de chaque projet : le lire avant d'écrire une scène | Remotion |
| `hyperframes-cli` | Commandes du projet : init, check, snapshot, preview, render | Créer le projet, vérifier, faire les planches d'images, l'aperçu et le rendu | |
| `hyperframes-registry` | ~450 blocs prêts (transitions, titres, caméras, particules) | Avant de coder à la main une transition ou un effet connu | Recettes de `production-html.md` |
| `media-use` | Trouve ou fabrique les médias : musique, voix, sons, images, détourage, étalonnage | Musique (catalogue HeyGen), détourage de packshot, traitement d'une capture terne | Pack `assets/sfx/`, Pixabay |
| `figma` | Récupère logos, couleurs et écrans depuis un lien Figma | Le client donne un lien figma.com | Exports PNG/SVG demandés au client |
| `remotion-to-hyperframes` | Convertit un projet Remotion ou After Effects vers HyperFrames | Réutiliser une ancienne vidéo du studio dans HyperFrames | |
| `slideshow` | Présentation à projeter en direct | Si le client veut une présentation, pas une vidéo | |

**Connecteurs (MCP)**

| Connecteur | Ce que c'est | Quand l'utiliser | Attention |
|---|---|---|---|
| ElevenLabs, outils `creative_*` | Voix off : `creative_list_voices` (choisir), `creative_generate_speech` (générer), `creative_transcribe_audio` (horodater) | Échantillon de la porte 3, puis voix finale après le oui (`voix-off.md` §9) | Les outils `agents_*` sont pour des agents téléphoniques, pas pour la voix off. Chaque appel est facturé : estimer d'abord, ne jamais relancer pour réessayer. Plan gratuit = non commercial |
| ElevenLabs complet (`https://api.elevenlabs.io/v1/mcp`) | Ajoute la musique et les effets générés | Musique sur mesure de durée exacte | Plan payant pour une pub |
| HyperFrames / HeyGen | Projets hébergés, rendu dans le cloud | Quand on travaille sans terminal (claude.ai) | Aucun `render_video` avant le oui de la porte 4 |
| Google Drive (`search_files`, `read_file_content`, `download_file_content`) | Cherche et lit les fichiers du Drive de l'utilisateur ; `download_file_content` récupère le contenu d'un fichier (logo, capture, charte, musique) | Le client a déposé ses visuels sur Drive | Ne télécharger que les fichiers du projet, et les ranger dans `assets/` |

**Scripts du skill** (`python -I <skill>/scripts/<nom>`)

| Script | Ce que c'est | Quand |
|---|---|---|
| `verifie.py` | Vérification finale complète, rapport Markdown | Brouillon avant la porte 4, fichier final avant livraison, toute vidéo existante à corriger |
| `qc.py` | Mesure du mouvement et du volume seul | Contrôle rapide pendant la construction |
| `anti_ia.py` | Repère les tics d'écriture IA | Script avant la porte 2, légendes avant livraison |
| `beats.py` | Tempo et temps forts d'une musique (librosa) | Dès que la musique est choisie, pour caler les transitions |
| `voix_elevenlabs.py` | Voix par l'API ElevenLabs, 3 prises, horodatage des mots | Seulement sans connecteur ElevenLabs, avec `ELEVENLABS_API_KEY` |
| `sfx.py` | Cherche un son : pack, dossier perso, Freesound CC0 | Quand un son manque dans le catalogue |
| `synth_sfx.py` | Génère whoosh, risers, impacts | Ajuster la durée ou la couleur d'un son de transition |

**Logiciels et bibliothèques externes** (détails : `boite-a-outils.md`)

| Outil | Ce que c'est | Quand l'utiliser |
|---|---|---|
| OBS Studio (+ scrcpy) | Enregistreur d'écran | Filmer la vraie appli ou le vrai site du client |
| LosslessCut | Découpe sans réencoder | Garder les bons passages d'un enregistrement OBS |
| Remotion (+ Remotion Skills) | Moteur vidéo en React | Si on préfère React à HyperFrames ; gratuit en solo |
| Three.js | 3D dans le navigateur | Téléphone, produit ou logo en 3D |
| Rapier | Physique 3D | Objets qui tombent ou s'empilent (simulation pré-calculée) |
| Lottie | Lecteur d'animations vectorielles | Logo ou icône animés livrés par un designer |
| Blender (MCP for Blender) | Studio 3D | Packshot 3D de qualité cinéma, plan héros |
| Whisper / WhisperX | Transcription avec horodatage | Caler les mots sur la voix, vérifier la voix contre le script |
| librosa | Analyse musicale | Temps forts de la musique (`beats.py`) |
| Tone.js | Synthé dans le navigateur | Sons sur mesure calés sur le BPM |
| Voice Studio, CosyVoice | Voix locales open source | Tests seulement ; licence et écoute de contrôle obligatoires |
| FFmpeg | Couteau suisse audio/vidéo | Mesures, conversion, mix, export |
| After Effects | Logiciel de motion | Si l'utilisateur travaille dedans (`after-effects.md`) |

Sans terminal (claude.ai) : les scripts ne tournent pas. Faire la vérification à la main avec `verification-finale.md` et proposer à l'utilisateur de lancer `verifie.py` sur son PC.

## Fichiers

**Références**
- `questionnaire.md` : questions et visuels à demander.
- `validation.md` : les 4 portes et le dossier de pré-rendu.
- `verification-finale.md` : la vérification avant rendu, automatique et manuelle.
- `patterns.md` : patterns des références et anti-patterns.
- `metrics.md` : mesures chiffrées des références et des essais.
- `production-html.md` : recettes HyperFrames/GSAP, anti-diaporama, 9:16, rigueur d'atelier.
- `after-effects.md` : courbes, durées, rebonds pour After Effects.
- `boite-a-outils.md` : OBS, Remotion, Three.js, Rapier, Whisper/WhisperX, librosa, Tone.js, Voice Studio, et les autres outils évalués.
- `audio.md` : musique, niveaux, effets sonores. `voix-off.md` : voix sans effet robot.
- `anti-ia.md` : tics de texte, de voix et d'image à bannir.
- `corpus.md` : les 13 vidéos de référence.

**Scripts** (`python -I <skill>/scripts/...`)
- `verifie.py` : vérification finale complète, rapport Markdown.
- `qc.py` : contrôle du mouvement et du volume seul.
- `anti_ia.py` : tics d'écriture IA dans un script ou une légende.
- `beats.py` : tempo et temps forts d'une musique (librosa).
- `voix_elevenlabs.py` : voix par l'API ElevenLabs, horodatage des mots.
- `sfx.py`, `synth_sfx.py` : trouver ou générer des effets sonores.

**Assets et modèles** : `assets/sfx/` (42 sons libres de droits, `CATALOGUE.md`), `templates/brief.md`, `templates/storyboard.md`.
