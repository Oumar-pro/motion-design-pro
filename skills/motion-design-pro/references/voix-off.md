# Voix off : éviter l'effet robot

Recherche faite le 30/10/2026 (documentation officielle ElevenLabs + guides spécialisés, sources en bas). Les réglages sont des **points de départ** : ElevenLabs rappelle que les bons réglages dépendent de chaque voix. On teste toujours sur la phrase du hook avant de générer le reste.

## 1. Choisir la source

| Source | Qualité | Usage commercial | Quand |
|---|---|---|---|
| Voix humaine enregistrée (téléphone récent, pièce calme, 15-20 cm de la bouche) | Naturelle | Oui | Marché local, ton chaleureux, budget zéro |
| ElevenLabs **gratuit** | Bonne | **Non** (usage non commercial, mention « ElevenLabs » exigée) | Tests, échantillons, brouillons |
| ElevenLabs **Starter** ou plus | Bonne à très bonne | Oui, pour l'audio généré pendant l'abonnement | Voix finale d'une pub |
| Voix de synthèse sur appareil (Kokoro…) | Robotique en français | - | Minutage d'un brouillon uniquement |

Budget : 30 s de script ≈ 450 caractères ≈ 450 crédits par prise. Avec 3 prises par bloc, une vidéo coûte ~1 500 à 2 000 crédits. Le gratuit (10 000/mois) suffit pour tous les tests ; la génération finale se fait sur un plan commercial.

## 2. Choisir la voix (la moitié du résultat)

- **Voice Library** : filtrer langue **Français**, puis l'accent qui correspond à la cible (France, Afrique de l'Ouest, Canada…). Une voix anglaise « qui parle français » sonne toujours faux.
- Préférer les voix étiquetées narration / publicité / « advertisement », avec beaucoup d'utilisations et une bonne note. Éviter les voix « conversational » ou faites pour les agents téléphoniques : plates en pub.
- Âge et énergie cohérents avec la marque (jeune et dynamique pour une appli, posée pour une école, une banque).
- Faire écouter **2 ou 3 voix** sur la même phrase à l'utilisateur (porte 3 de `validation.md`).
- Voix clonée : seulement avec l'accord de la personne dont c'est la voix.

## 3. Choisir le modèle

| Modèle | Points forts | Limites | Usage |
|---|---|---|---|
| **Multilingual v2** | Stable, français de qualité, accepte `<break time="0.5s" />`, normalise bien chiffres et devises | Moins d'émotions jouées | **Défaut pour la voix finale** |
| **v3 / v4** (expressifs) | Émotion, balises `[excited]`, `[whispers]`… | Pas de balises `<break>`, plus variable selon la voix, résultats inconsistants sous ~250 caractères | Accroche très jouée, après test |
| Flash / Turbo | Rapide, bon marché | Lit mal chiffres et devises, moins naturel | À éviter pour une pub |

## 4. Réglages de départ

| Réglage | Multilingual v2 | Pourquoi |
|---|---|---|
| Stabilité | **45-50 %** (40 % si trop plat ; 55-60 % si ça part dans tous les sens) | Bas = plus expressif mais instable ; haut = régulier mais monotone |
| Similarité (Clarity + Similarity) | **75 %** | Valeur la plus courante selon la doc officielle |
| Style (exagération) | **0 %** ; 10-20 % maximum si la voix reste plate | La doc recommande 0 : au-dessus, le modèle devient moins stable |
| Speaker boost | **Activé** | Plus fidèle à la voix (non disponible sur v3) |
| Vitesse | **1,0 à 1,08** (plage autorisée 0,7-1,2) | Au-delà, la qualité baisse ; préférer resserrer les silences au montage |

v3/v4 : choisir le mode « Natural » (ou « Creative » pour plus d'émotion), pas de similarité ni de speaker boost.

## 5. Écrire pour l'oreille (là où se joue l'effet robot)

- **Phrases courtes** : 6 à 12 mots, une idée par phrase. Une phrase trop longue est lue d'un trait, sans respiration.
- **Ponctuation = mise en scène** : le point donne la pause la plus nette ; la virgule une pause courte ; un retour à la ligne une pause plus longue. Tirets et points de suspension donnent des pauses **moins fiables**.
- **Pauses précises** (v2) : `<break time="0.4s" />`, au plus une par phrase ; trop de balises font accélérer la voix ou créent des artefacts.
- **Chiffres et sigles écrits comme on les dit** : « 25 000 FCFA » → « vingt-cinq mille francs CFA » ; téléphone en groupes « soixante-seize, zéro cinq, cinquante-sept… » ; « *755# » → « étoile sept cent cinquante-cinq dièse » ; sigles épelés « A M F » ou écrits « Ah-èm-èf » si mal lus.
- **Noms propres et mots locaux** : les écrire phonétiquement (« Sotouba », « Ika wari yi tayé » découpé en syllabes si besoin) ; sur v2, balise alias ou dictionnaire de prononciation.
- **Accent tonique** : mettre le mot clé en fin de phrase, c'est là que le français place l'emphase (« Ton argent mérite… un plan. »).
- **Émotion** (v3/v4) : une balise courte au début du bloc (`[enthusiastic]`, `[warm]`) ; tester, certaines voix les lisent mal.
- **Questions** : finir par « ? » pour obtenir l'intonation montante ; vérifier à l'écoute.

## 6. Méthode de génération

1. Générer **par bloc de scène** (1 à 3 phrases, idéalement 150-400 caractères) : assez long pour garder une intonation naturelle, assez court pour corriger un passage.
2. **3 prises par bloc**, choisir la meilleure ; noter le `seed` de la prise retenue pour la reproduire.
3. Garder **la même voix, le même modèle, les mêmes réglages** sur toute la vidéo.
4. Ne régénérer que le bloc fautif ; si un seul mot est mal prononcé, corriger l'écriture du mot plutôt que les réglages.
5. Demander les **horodatages** (`scripts/voix_elevenlabs.py`, endpoint *with-timestamps*) : ils donnent l'instant exact de chaque mot pour caler le texte animé (mode A) sans Whisper.

## 7. Montage et traitement

- Couper les silences de début et de fin ; resserrer les blancs entre phrases à **0,15-0,35 s** (une pause de pub est courte).
- Ne jamais accélérer la voix de plus de 5 % au montage (effet « chipmunk ») : réécrire le script si c'est trop long.
- Coupe-bas 80-100 Hz, léger creux 250-400 Hz si la voix sonne « carton », présence +2-3 dB vers 3-5 kHz, dé-esseur doux.
- Compression 3:1 à 4:1, puis musique baissée sous la voix (ducking -10 à -14 dB) ; mix final -14 LUFS, crête -1 dBTP (`audio.md`).
- Pas de réverbération sur une voix de pub.

## 8. Écoute de contrôle (avant la porte 3)

La voix est refusée si l'un de ces défauts s'entend :
- [ ] Débit parfaitement constant, sans respiration ni accélération sur les mots importants.
- [ ] Même mélodie de phrase répétée à chaque phrase.
- [ ] Chiffre, devise, téléphone ou nom propre mal lu.
- [ ] Liaison française oubliée ou fautive (« les‿amis », « vous‿avez »).
- [ ] Question qui ne monte pas, affirmation qui monte.
- [ ] Souffle métallique, clic, mot avalé ou doublé (artefact).
- [ ] Ton qui change d'un bloc à l'autre.

## 9. Avec le connecteur ElevenLabs (MCP)

Le connecteur ElevenLabs contient deux familles d'outils : `agents_*` (agents vocaux téléphoniques, **inutiles ici**) et `creative_*` (synthèse vocale). Si seuls les `agents_*` sont visibles, charger les autres (`get_more_tools`, ou la recherche d'outils avec « creative_generate_speech »). Ne pas conclure trop vite que la voix off est impossible.

1. **Choisir la voix** : `creative_list_voices` avec `languages: ["fr"]`, `use_cases: ["advertisement"]` (ou `narrative_story`), le genre et l'âge voulus, `voice_category: "high_quality"`, `sort: "usage_character_count_1y"`. Retenir 3 voix pour l'échantillon de la porte 3.
2. **Estimer avant de dépenser** : `creative_generate_speech` avec `estimate_only: true`, annoncer le coût à l'utilisateur.
3. **Générer** : `model_id: "eleven_multilingual_v2"` pour la voix finale (stable, accepte `<break time="0.4s" />`), ou `eleven_v4` si on veut des balises de jeu (`[warm]`, `[enthusiastic]`), sans `<break>`. `generations_count: 3` pour avoir 3 prises. Un bloc de scène par appel, toujours dans le même `flow_id` (créé avec `creative_create_flow`).
4. **Ne jamais relancer un appel « pour réessayer »** : chaque appel est facturé. Attendre le résultat avec `creative_get_flow_run_status`.
5. Le connecteur **n'expose pas** les curseurs stabilité / similarité / style / vitesse. Le rendu se règle par le choix de la voix, du modèle et l'écriture du texte (§5). Pour régler les curseurs : ouvrir l'URL renvoyée (canevas ElevenLabs) et ajuster à la main avec les valeurs du §4, ou utiliser `scripts/voix_elevenlabs.py` avec une clé API.
6. **Horodatage des mots** : `creative_transcribe_audio` sur la prise retenue (ou Whisper), pour caler le texte animé.

## Sources
- [ElevenLabs : réglages de voix (Text to Speech)](https://elevenlabs.io/docs/product-guides/playground/text-to-speech)
- [ElevenLabs : API voice settings](https://elevenlabs.io/docs/api-reference/voices/settings.md)
- [ElevenLabs : prompting et bonnes pratiques](https://elevenlabs.io/docs/best-practices/prompting)
- [ElevenLabs : ajouter des pauses](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-can-i-add-pauses.md)
- [ElevenLabs : rendre la synthèse moins robotique](https://elevenlabs.io/en/blog/how-to-make-text-to-speech-sound-less-robotic)
- [Artlist : mieux utiliser ElevenLabs](https://artlist.io/blog/?p=65717)
- [AnySpeech : 12 corrections contre la voix robotique](https://anyspeech.io/blog/how-to-make-ai-voice-sound-less-robotic)
- [Scenario : modèles ElevenLabs](https://help.scenario.com/en/articles/elevenlabs-family-the-essentials/)
- [Conditions du plan gratuit (terms.law)](https://terms.law/ai-output-rights/elevenlabs/)
