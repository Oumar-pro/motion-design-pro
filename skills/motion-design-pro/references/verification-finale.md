# Vérification finale : rien ne part sans elle

La vérification finale a lieu **deux fois** : sur le brouillon, avant de présenter le dossier de pré-rendu (porte 4), puis sur le fichier final, avant de le livrer. Une vidéo qui n'a pas passé cette vérification n'est jamais présentée comme terminée.

## 1. Lancer le vérificateur

```bash
python -I <skill>/scripts/verifie.py video.mp4 --script script.txt --duree 30 --format 9:16 --whisper-model <chemin>/ggml-base.bin --rapport rapport-verification.md
```

- `--script` : le texte exact de la voix off (un fichier texte). Sert au contrôle anti-IA et à la comparaison voix / script.
- `--whisper-model` (ou variable `WHISPER_MODEL`) : modèle whisper.cpp pour le filtre `whisper` de FFmpeg. Sans lui, la comparaison voix / script est sautée et passe en vérification manuelle.
- Le rapport Markdown se joint au dossier de pré-rendu et à la livraison.

Sans terminal (claude.ai) : faire la même liste à la main sur les planches d'images et l'écoute, et proposer à l'utilisateur de lancer `verifie.py` sur son PC.

## 2. Ce qui est vérifié automatiquement

| Groupe | Contrôle | Bloquant si | Conseil si |
|---|---|---|---|
| Technique | Format | Rapport largeur/hauteur différent du format demandé | |
| | Résolution | | Petit côté < 1080 px |
| | Cadence | | Autre que 24, 25, 30, 50, 60 i/s |
| | Codec | | Autre que H.264 / yuv420p (lecture sur téléphone et réseaux) |
| | Durée | Écart > 2 s avec la cible | Écart de 0,5 à 2 s |
| Image | Images fixes | > 60 % | > 40 % |
| | Plus longue tenue immobile (hors 4 dernières s) | > 2,5 s | > 1,5 s |
| | Densité d'animation | < 0,5 /s | < 0,65 /s |
| | Fondus / sorties dominants | > 50 % | > 35 % |
| | Écrans noirs | Tout écran noir après 0,15 s | |
| | Images figées hors fin | Toute image figée ≥ 2 s | |
| Son | Piste audio | Absente | |
| | Volume intégré | Hors -16 à -12 LUFS | Hors -15 à -13 LUFS |
| | Crête | | Au-dessus de -1 dBFS |
| | Silences complets | Tout silence ≥ 0,8 s après 0,3 s | |
| | Fin de vidéo audible | 3 dernières secondes sous -40 dB | |
| | Fond musical continu | | Graves absents sur > 25 % de la durée |
| | Coupes franches avec un son | | Une coupe sans impact sonore à ± 0,1 s |
| Texte | Tics d'écriture IA | | Au moins une alerte `anti_ia.py` |
| Voix | Voix conforme au script | | Une phrase du script à moins de 60 % retrouvée dans la transcription |

Seuils calibrés sur les 13 références et les essais du studio (`metrics.md`). Le modèle Whisper « base » se trompe sur les noms propres et les mots rares : une alerte « voix » signifie **réécouter ce passage**, pas forcément refaire la voix.

## 3. Ce qui se vérifie à la main (le script ne peut pas le faire)

Cocher chaque ligne dans le rapport avant le rendu final :
- [ ] Coordonnées, prix, nom de marque, URL et appel à l'action identiques, lettre par lettre, à ce que le client a fourni.
- [ ] Orthographe de chaque texte à l'écran ; noms propres ; citations, versets et chiffres validés par le client.
- [ ] Hook compréhensible son coupé, en moins de 2,5 s.
- [ ] Écoute de contrôle de la voix, au casque, en entier (`voix-off.md` §8).
- [ ] Licences : voix (plan commercial), musique, effets (`SOURCES_SFX.md`), polices, photos, droits des personnes filmées.
- [ ] Aucune vraie donnée personnelle visible (noms, numéros, messages) dans les captures.
- [ ] Aucune police de secours (Times, Arial) sur aucune image.
- [ ] Zones de sécurité : texte important hors des 8 % du haut et des 10 % du bas en 9:16 (interfaces des réseaux).
- [ ] Anti « look IA » visuel (`anti-ia.md` §3) sur la planche d'images.
- [ ] Lecture sur un vrai téléphone, luminosité moyenne, à bout de bras : tout se lit.

## 4. Planche d'images

En plus du rapport, produire une planche (6 à 8 images par scène, ou 36 images réparties sur toute la vidéo) et la regarder :
```bash
ffmpeg -i video.mp4 -vf "fps=36/DUREE,scale=240:-2,tile=9x4" -frames:v 1 planche.png
```
Refuser si : trois images de suite identiques hors fin, texte coupé par le bord, éléments qui se chevauchent, élément clé hors du carré central, police de secours, faux texte ou charabia dans l'interface.

## 5. Verdict et suite

| Verdict | Suite |
|---|---|
| **A REPRENDRE** (au moins un BLOQUANT) | Corriger, refaire le brouillon, relancer. Ne rien présenter, ne rien rendre. |
| **OK AVEC CONSEILS** | Corriger chaque conseil ou écrire pourquoi il est voulu (ex. fin tenue immobile). Puis vérifications manuelles. |
| **OK** + toutes les cases manuelles cochées | Présenter le dossier de pré-rendu (porte 4) avec le rapport. Rendu final seulement après le oui écrit. |

Après le rendu final : relancer `verifie.py` sur le fichier livré (un rendu peut différer du brouillon : encodage, son, durée). Livrer avec le rapport.
