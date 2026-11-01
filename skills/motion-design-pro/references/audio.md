# Voix off et sound design

## Voix off
- Pub commerciale : voix off par défaut (10 vidéos sur 12 sonores en ont une). Texte animé + musique seule : réservé aux démos de marque ou au style « vitrine ».
- Démarre à 0,0-0,3 s, sans intro musicale.
- Phrases de 2 à 3 s, une idée par phrase = un écran.
- Débit : 2,5 à 3,3 mots/s ; pour 30 s, script de 65 à 85 mots.
- Ton : tutoiement pour appli grand public (Sama, Push, Wave), vouvoiement pour institution/B2B (AMF, Safe Home, école).
- Accroche ou slogan final en langue locale si pertinent (« Ika wari yi tayé »).

**Guide complet anti-voix robotique : `voix-off.md`** (choix de la voix, modèle, réglages ElevenLabs, écriture pour l'oreille, prises, montage, écoute de contrôle). Génération : `scripts/voix_elevenlabs.py` (bloc par bloc, 3 prises, horodatage de chaque mot).

### Qualité de la voix (la voix robotique tue la vidéo)
Ordre de préférence :
1. **Voix humaine enregistrée** par l'utilisateur ou un comédien (demander un WAV, pièce calme, micro proche).
2. **Voix de synthèse haut de gamme** (voix HeyGen, voix clonée de l'utilisateur, ou autre service premium que l'utilisateur possède), en français natif, style publicitaire.
3. **Jamais** une voix de synthèse sur appareil (ex. Kokoro via `npx hyperframes tts`) pour une vidéo finale en français : seulement pour caler le minutage d'un brouillon, en le disant à l'utilisateur.

Toujours faire valider un échantillon de 5 à 10 s avant de générer la voix complète (`validation.md`, porte 3).

Réglages pour une voix de synthèse : style « publicité / narration énergique », stabilité moyenne (pas trop monotone), vitesse 1,05-1,1, ponctuation écrite pour forcer les pauses (« Ton argent… mérite un plan. »), mots étrangers ou locaux écrits phonétiquement si mal prononcés, une phrase par génération pour corriger facilement.

### Traitement de la voix
- Coupe-bas 80-100 Hz, léger creux 200-400 Hz si la voix sonne « boîte », présence +2-3 dB vers 3-5 kHz, dé-esseur si besoin.
- Compression 3:1 à 4:1, la voix doit rester devant la musique sans pomper.
- Pas de silence au début ; respirations conservées mais baissées.

## Lien texte / voix
- **Mode A, texte quasi identique** : chaque mot apparaît quand il est prononcé (transcription horodatée, ex. Whisper). Pour un public en lecture muette, un tutoriel ou une accroche.
- **Mode B, mots clés** : la voix raconte, l'écran garde 2 à 5 mots par phrase avec le mot fort surligné. Pour un argumentaire dense.
- Toujours : la première phrase est en mode A.

## Musique
- 120 BPM par défaut (majorité du corpus) ; 145-150 BPM pour du très énergique ; 90-100 BPM pour du posé/premium.
- Volume compressé et stable (écart de volume LRA 2 à 5 LU dans les références), baissé sous la voix (ducking -10 à -14 dB, soit environ 0,14 de volume sous la voix).
- Montée de volume au virage du récit ; baisse ou arrêt net sur la fin.

## Niveaux (mesurés sur les références)
- **Volume intégré : -14 LUFS** (12 références sur 13 entre -14,1 et -14,3). Accepté : -15,5 à -13.
- Crête vraie : -1 dBTP au maximum.
- Vérifier avec `scripts/qc.py` ou `npx hyperframes audio <video> --json` ; normaliser avec `npx hyperframes normalize-audio`.

## Calage
- Transitions de scène sur un temps fort (une par mesure : toutes les 2 s à 120 BPM).
- Apparitions de mots sur la voix ; à défaut, sur les croches (0,25 s à 120 BPM).
- Impact sonore à 0,0-0,1 s (le son démarre avec l'image).

## Effets sonores : obligatoires
Générer la liste depuis la timeline : **chaque transition** reçoit un whoosh ou un impact placé à ± 1 image de la coupe, **chaque apparition importante** (mot clé, bouton, chiffre, notification, logo) reçoit son son. Les effets restent 6 à 10 dB sous la voix. Le contrôle `scripts/qc.py` indique combien de coupes ont un impact sonore à moins de 0,1 s : viser toutes.

| Événement visuel | SFX |
|---|---|
| Mot qui apparaît | tic / pop doux très court |
| Surlignage | swish court ou marqueur |
| Bouton cliqué | clic d'interface |
| Disque, bande, vague (transition) | whoosh + impact sur la coupe |
| Zoom dans une lettre | riser court → whoosh |
| Chiffre qui défile | tic-tic de compteur, ding à l'arrivée |
| Notification / message | son de notification |
| Logo final | impact grave + scintillement |
| Inversion clair/sombre | sub drop ou baisse soudaine de musique |

### Où prendre les sons (dans cet ordre)
1. **Pack du skill** : `assets/sfx/` (42 sons, catalogue dans `assets/sfx/CATALOGUE.md`). Kenney CC0 + sons de transition synthétisés. Couvre tout le tableau ci-dessus, hors connexion et sans risque de licence. `python -I scripts/sfx.py liste` ou `sfx.py cherche whoosh`.
2. **Dossier personnel de l'utilisateur** (ex. bundle Sonniss GDC, libre de droits, usage commercial sans crédit, interdit pour entraîner une IA) : si la variable `SFX_DIR` pointe dessus, `sfx.py cherche <mot>` le fouille aussi.
3. **Freesound, CC0 uniquement** : quand un son précis manque (caisse enregistreuse, foule, moteur…). Besoin d'une clé gratuite `FREESOUND_API_KEY` (https://freesound.org/apiv2/apply). `sfx.py freesound "cash register"` liste les résultats CC0, `sfx.py telecharge <id> <dossier_projet>` télécharge l'aperçu HQ (MP3) et l'inscrit dans `SOURCES_SFX.md` du projet. Mots-clés en anglais.
4. Sons fournis par l'utilisateur.

Ne jamais utiliser un son dont la licence n'est pas CC0 ou explicitement libre de droits commerciaux. Dans le plan sonore (porte 4), indiquer pour chaque son : fichier, instant, source, licence.

Les sons synthétisés peuvent être ajustés (durée, couleur) en modifiant `scripts/synth_sfx.py` puis `python -I scripts/synth_sfx.py <dossier>`.
