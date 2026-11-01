# Anti « look IA » : texte, voix et image

Une pub qui « sent l'IA » perd la confiance du spectateur en une seconde. Ce guide liste les tics à bannir dans **tout ce que le skill écrit ou fabrique** : script, voix off, texte à l'écran, sous-titres, légendes de post, messages au client, et l'image elle-même.

Aucun de ces signes, pris seul, ne prouve qu'un texte vient d'une IA (des écrivains utilisent le tiret cadratin depuis toujours). C'est leur **répétition systématique** qui trahit. On les bannit donc par défaut, et on garde une exception seulement quand elle est voulue.

Sources : vidéo « Le tiret cadratin » (dossier de l'utilisateur, 31/10/2026), étude Pangram (9 signaux), page Wikipedia « Signs of AI writing », guides cités en bas.

## 1. Texte : les tics à bannir

| Tic | Exemple à éviter | À la place |
|---|---|---|
| **Tiret cadratin** « — » (aucune touche du clavier ne le tape) | « Nassib — le bon partenaire » | Virgule, point, deux-points, parenthèses : « Nassib. Le bon partenaire. » |
| **« Ce n'est pas X, c'est Y »** / « Pas seulement X, mais Y » / « Non seulement… mais aussi… » | « Ce n'est pas une appli, c'est une révolution. » | Dire Y directement : « Une appli pensée pour le mariage. » Exception : un vrai contraste porteur du message (« Pas un match. Un mariage. ») utilisé **une seule fois** par vidéo |
| **Listes toujours par trois** | « Rapide, simple et sécurisé. » à chaque phrase | 2, 4 ou 1 élément ; varier. Une triade par vidéo au maximum |
| **Émoji devant chaque titre** ou émojis « fonctionnels » (✅ 🚀 💡 ✨) | « 🚀 Lance-toi » | Pas d'émoji dans le texte à l'écran ni dans les titres ; une icône dessinée si besoin |
| **Formules d'ouverture de chatbot** | « Bien sûr ! », « Excellente question », « Voici… » | Entrer directement dans le sujet |
| **Question rhétorique + réponse immédiate** en série | « Le résultat ? Un gain de temps. Le secret ? … » | Une seule fois au maximum, sinon une affirmation |
| **« Imaginez… » / « Dans un monde où… » / « Que vous soyez X ou Y… »** | « Dans un monde où tout va vite… » | Une situation concrète : « Le taxi, le marché, la recharge… » |
| **Mots gonflés** | véritable, incontournable, révolutionner, révolutionnaire, plongez, découvrez, sublimer, libérer le potentiel, au cœur de, sans compromis, fluide, transformer, élever, booster, un jeu d'enfant, en toute sérénité, l'avenir de… | Le mot simple et concret que dirait le client : « payer », « envoyer à maman », « en 2 minutes » |
| **Parallélismes parfaits** et chaque phrase qui finit en punchline | « Simple. Rapide. Sécurisé. Puissant. » | Varier la longueur des phrases ; une seule chute forte par scène |
| **Mise en forme résiduelle** | astérisques `**gras**` visibles, `##`, puces dans une légende, caractères `─ → •` collés dans un texte courant | Texte propre ; flèches et puces seulement dans l'interface dessinée |
| **Listes à puces à la place de phrases** | Une légende de post découpée en 6 puces | Deux ou trois phrases normales |
| **Généralités sans détail** | « Une solution adaptée à vos besoins » | Un chiffre, un lieu, un prénom, un prix réel fournis par le client |

**Règle d'or** : écrire comme parle la cible. Pour une pub locale : prénoms locaux, FCFA, quartiers, expressions réelles (« à maman », « sans internet ») et, si le client en a, une phrase en langue locale.

## 2. Voix : les signes « voix générée »

Voir `voix-off.md` §8 (écoute de contrôle). En résumé : débit constant, même mélodie à chaque phrase, chiffres mal lus, liaisons fausses, ton qui change entre les blocs, absence de respiration. Le texte du §1 aggrave tout : un script plein de triades et de « ce n'est pas X, c'est Y » sonne robotique même avec une bonne voix.

## 3. Image et animation : les signes « vidéo générée »

| Signe | À la place |
|---|---|
| Même entrée sur tout (fondu + montée de 20 px, `power2.out` 0,5 s partout) | Ease choisi par rôle (`after-effects.md`), entrées variées d'une scène à l'autre |
| Titres qui flottent, respirent ou grossissent lentement après s'être posés | Titre posé = immobile ; le mouvement passe à l'interface ou à la caméra |
| Rebond sur toute l'interface, anneaux autour de chaque clic | Rebond seulement sur ce qui « pop » ; un clic = appui 1 → 0,96 → 1 |
| Toutes les scènes de la même durée, tout centré, tout symétrique | Rythme varié (2 à 4 s), compositions décalées, grille éditoriale |
| Dégradé violet-bleu par défaut, verre givré partout, blobs 3D génériques | La palette du client ; un effet de matière seulement s'il sert la marque |
| Police Inter centrée partout, aucune hiérarchie | 3 niveaux de texte (`patterns.md` §3), mot clé avec un vrai traitement |
| Fausse interface avec du charabia, « Lorem ipsum », « John Doe » | Vraie interface du client ou reconstruction fidèle avec des textes plausibles et locaux |
| Images générées : peau plastique, mains déformées, texte illisible dans l'image, regard vide | Vraies photos du client ; sinon photos libres de droits ; pas de visage généré en gros plan |
| Icônes émoji à la place d'icônes | Jeu d'icônes cohérent (même trait, même épaisseur) |
| Musique de stock générique, sons identiques répétés | Musique choisie pour le rythme du montage ; alterner 2 variantes de chaque son (`assets/sfx/CATALOGUE.md`) |
| Perfection lisse sans aucun détail humain | Un détail « fait main » : soulignement tracé à la main, grain léger, une imperfection voulue |
| Clichés de pub (poignée de main, ampoule, fusée, globe qui tourne) | Une scène vraie de la cible (le marché, le taxi, la boutique, la famille) |

## 4. Règle à copier-coller

À coller dans les instructions de tout outil d'écriture ou de génération utilisé pour le projet (script, légendes, voix, prompts d'image) :

```text
Écris comme un humain qui parle à sa cible, pas comme une IA :
- jamais de tiret cadratin (—) : virgule, point, deux-points ou parenthèses à la place ;
- jamais de formule « ce n'est pas X, c'est Y », « pas seulement… mais… », « non seulement… mais aussi… » ;
- pas de listes systématiques par trois ; varie le nombre d'éléments ;
- aucun émoji devant les titres ni dans le texte à l'écran ;
- pas de « Imaginez », « Dans un monde où », « Que vous soyez… », « Découvrez », « Plongez », « véritable », « incontournable », « révolutionner », « au cœur de », « sans compromis » ;
- pas de question rhétorique suivie de sa réponse en série ;
- pas d'astérisques, de dièses ni de puces dans un texte courant ;
- des phrases de longueurs variées, des mots simples, des détails concrets et locaux (prénoms, lieux, prix, situations réelles).
```

## 5. Contrôle automatique

`python -I scripts/anti_ia.py <fichier_script.txt|md>` repère dans un texte : tirets cadratins, formules « ce n'est pas… c'est », triades, émojis, ouvertures de chatbot, mots gonflés, mise en forme résiduelle. À lancer sur le script avant la porte 2 et sur les légendes avant livraison. Zéro alerte attendue, ou chaque alerte justifiée.

## Sources
- [Pangram : les 9 signaux de l'écriture IA (synthèse)](https://pasqualepillitteri.it/fr/news/13026/9-signaux-ecriture-ia-pangram)
- [Le nouveau em-dash : 9 signes de l'écriture IA](https://pasqualepillitteri.it/fr/news/11196/nouveau-em-dash-9-signes-ecriture-ia)
- [12 signes d'un texte écrit par l'IA](https://pasqualepillitteri.it/fr/news/404/reconnaitre-texte-ecrit-ia-detector-checker)
- [Blog du Modérateur : le tiret cadratin](https://www.blogdumoderateur.com/tiret-cadratin-mort-vive-tiret-cadratin/)
- [Slate : détecter l'IA dans les textes](https://www.slate.fr/tech-internet/intelligence-artificielle-ia-chatbot-chatgpt-texte-litterature-internet-ecriture)
- [How to spot AI writing, according to Wikipedia](https://www.beutlerink.com/blog/how-to-spot-ai-writing)
- [FlowingData : Signs of AI writing on Wikipedia](https://flowingdata.com/2025/10/20/signs-of-ai-writing-on-wikipedia/)
- [Guilty by Punctuation (critique du tiret comme preuve)](https://linguistically.substack.com/p/guilty-by-punctuation)
- [Dissolve : clichés vidéo à éviter](https://communication.dissolve.com/tips/video-cliches-to-avoid-like-the-plague)
- [Invideo : rendre une pub IA intentionnelle](https://invideo.io/faq/how-do-you-make-ai-generated-video-ads-feel-intentional/)
- Skill `hyperframes`, `references/motion.md` : « Defaults that look generated »
