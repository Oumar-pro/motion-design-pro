# Validations avant rendu (ne pas brûler de crédits pour rien)

Le rendu final, la voix off complète, la musique ou les images générées peuvent consommer des crédits (HeyGen, voix de synthèse en ligne, rendu dans le cloud). **Rien de payant ni de définitif ne part avant que l'utilisateur ait validé par écrit.** Les étapes gratuites (texte, planches, aperçu local) servent à tout corriger avant.

## Les 4 portes

| Porte | Ce que tu présentes | Ce qui est interdit avant validation |
|---|---|---|
| **1. Brief** | Récapitulatif `templates/brief.md` avec ✅ / ⏳ | Écrire le script |
| **2. Script et concept** | Hook choisi + 2 variantes, script deux colonnes (voix / texte écran / visuel / durée), musique et BPM proposés | Générer voix, musique, images |
| **3. Voix** | Un **échantillon de 5 à 10 s** (la phrase du hook) dans 2 ou 3 voix candidates, ou la voix enregistrée par l'utilisateur, avec le traitement audio appliqué | Générer la voix off complète |
| **4. Dossier de pré-rendu** | Tout le contenu ci-dessous | Lancer le rendu final ou tout rendu payant |

À chaque porte : poser la question avec l'outil AskUserQuestion (ou une question claire), puis **attendre la réponse**. Une réponse vague (« ok continue ») vaut validation de la porte en cours seulement, pas des suivantes.

## Contenu du dossier de pré-rendu (porte 4)

Présenter, dans cet ordre, en une seule fois :

1. **Script final** deux colonnes, avec les timecodes réels de la voix (transcription horodatée).
2. **Storyboard visuel** : pour chaque scène, une planche de 4 à 8 images tirées de l'aperçu (`npx hyperframes snapshot --composition <id> --frames 8`, ou captures de l'aperçu), avec son timecode.
3. **Tableau des animations** : pour chaque scène, éléments animés, preset (ENTRÉE / DÉPLACEMENT / SORTIE / POP / DÉPASSEMENT), durée, décalages, ce qui bouge pendant les tenues.
4. **Tableau des transitions** : entre chaque scène, le type (morph, zoom dans une lettre, iris, bandes, vague, inversion, coupe), l'objet qui la déclenche, le temps fort musical sur lequel elle tombe.
5. **Plan sonore** : voix (choix validé à la porte 3), musique (titre, BPM, source/licence), liste des effets sonores avec leur instant (un par transition, un par apparition importante), niveaux visés (-14 LUFS, musique sous la voix).
6. **Rapport de vérification finale** sur le brouillon exporté localement : `python -I <skill>/scripts/verifie.py brouillon.mp4 --script script.txt --duree D --format F --rapport rapport-verification.md` (`verification-finale.md`). Aucun BLOQUANT ; chaque CONSEIL corrigé ou justifié ; vérifications manuelles cochées.
7. **Lien vers l'aperçu** (aperçu HyperFrames / desktop app, ou fichier brouillon) pour que l'utilisateur regarde en mouvement.
8. **Coût estimé** du rendu final (crédits ou temps), format(s) et résolution(s) qui seront rendus.

Terminer par une seule question : « Je lance le rendu final ? », avec les options « Oui, lance le rendu » / « Modifier d'abord ». Tant que la réponse n'est pas un oui explicite, ne rien rendre.

## Après le rendu final

- Relancer `scripts/qc.py` sur le fichier final et joindre le rapport.
- Si un contrôle échoue, le dire et proposer la correction ; ne pas présenter la vidéo comme terminée.
