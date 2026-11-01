# Mesures chiffrées des références

Mesuré le 30/10/2026 avec ffmpeg (différences entre images à 96×54, détection de coupes, EBU R128, transcription Whisper). Les seuils de `scripts/qc.py` en sont tirés.

## Mouvement

| # | Vidéo | Images fixes | Plus longue tenue immobile | Animations/s | Ease-out / in-out / in | Durée médiane | Coupes |
|---|---|---|---|---|---|---|---|
| V1 | School | 60 % | 2,5 s (ouverture ciel) | 0,57 | 35 / 35 / 30 % | 267 ms | 1 |
| V2 | Sama | 57 % | 1,03 s | 0,80 | 63 / 29 / 8 % | 267 ms | 10 |
| V3 | Telegram | 27 % | 0,77 s | 0,75 | 41 / 41 / 18 % | 383 ms | 4 |
| V4 | Pocketsflow | 27 % | 0,38 s | 1,46 | 23 / 73 / 5 % | 183 ms | 2 |
| V5 | x-downloader | 19 % | - | 0,19* | 56 / 22 / 22 % | 400 ms | 5 |
| V6 | Nexo (Claude) | 28 % | 0,58 s | 0,95 | 45 / 36 / 18 % | 300 ms | 0 |
| V7 | Push | 33 % | 1,23 s | 0,66 | 35 / 35 / 31 % | 450 ms | 2 |
| V8 | AMF | 37 % | 0,90 s | 0,96 | 57 / 37 / 7 % | 333 ms | 2 |
| V9 | Safe Home | 44 % | 1,03 s | 0,62 | 17 / 65 / 17 % | 333 ms | 6 |
| V10 | Nexo AE (Uber) | 31 % | 0,50 s | 0,76 | 63 / 13 / 25 % | 450 ms | 5 |
| V11 | Energi 3X | 6 % | 0,40 s | 0,73 | 28 / 32 / 40 % | 233 ms | 12 |
| V12 | Wave (9:16) | 20 % | 0,90 s | 0,90 | 21 / 67 / 12 % | 333 ms | 1 |
| V13 | Thé 3X | 11 % | 1,63 s | 0,66 | 70 / 25 / 5 % | 233 ms | 10 |
| **Médiane** | | **31 %** | **0,9 s** | **0,76** | **41 / 37 / 18 %** | **333 ms** | **4** |
| ✗ | **Test « Nassib »** | **86 %** | **4,37 s** | **0,23** | **25 / 13 / 62 %** | **200 ms** | 3 |

*V5 : deux versions empilées dans la même image, densité non comparable.

## Son

| # | Volume intégré | Écart de volume (LRA) | Crête | Impacts/s | Tempo estimé | Voix off |
|---|---|---|---|---|---|---|
| V1 | -14,1 LUFS | 2,7 LU | -0,2 | 3,9 | 120 | FR, mots clés |
| V2 | -14,2 | 4,9 | -1,7 | 4,3 | 146 | FR tutoiement, identique |
| V3 | -14,1 | 1,8 | -1,9 | 3,8 | 125 | non |
| V4 | -14,3 | 2,1 | -0,6 | 3,0 | 150 | EN, identique |
| V6 | -18,4 | 5,8 | -3,4 | 3,3 | 97 | non (démo) |
| V7 | -14,1 | 3,4 | -0,2 | 4,4 | 92 | FR tutoiement, mixte |
| V8 | -14,2 | 2,0 | -0,3 | 4,4 | 120 | FR vouvoiement, mots clés |
| V9 | -14,1 | 2,3 | -0,4 | 4,7 | 120 | FR vouvoiement, identique |
| V10 | -12,2 | 2,9 | +0,5 | 2,8 | 118 | chanson |
| V11 | -14,1 | 2,1 | -1,4 | 4,3 | 125 | FR slogan, mots clés |
| V12 | -14,2 | 2,3 | -0,7 | 4,4 | 120 | FR + bambara, mots clés |
| V13 | -14,1 | 2,6 | -2,2 | 5,0 | 122 | FR, identique |
| ✗ Test | **-17,5** | 1,9 | -3,3 | 4,1 | 102 | voix de synthèse robotique |

## Mesures de formes isolées
- Pop d'un point (V11) : 0 → 26 → 16 → 18 px, +44 % / -11 %, stable en 4 images.
- Balayage circulaire (V10, V11) : le diamètre double à chaque image, plein écran en 4 images (expo-in).
- Déplacement latéral (V6) : dépassement ~18 %, retour en ~200 ms.
- Rebond de balle (V6) : chute accélérée 0,5 → 12 px/image, remontée décélérée.

## Ce que dit le contre-exemple
Le test « Nassib » avait de bonnes idées (texte mot par mot, surlignage, mot barré, compteur 0 → 98 %, inversion sombre, fin complète), mais :
- chaque scène = un écran qui apparaît en fondu puis attend (86 % d'images fixes, tenue de 4,4 s dès l'ouverture) ;
- aucune transition causée par un objet, aucune caméra ;
- éléments petits au milieu d'un grand vide en 9:16 (texte secondaire ~3 % de la hauteur, téléphone ~50 % de la largeur, moitié basse de l'écran souvent vide) ;
- hook de 4,3 s (citation) au lieu d'une phrase adressée au spectateur en 2,4 s ;
- voix de synthèse robotique, volume 3,5 dB sous les références, effets sonores non calés sur les transitions.
