# Pack Motion Design Pro

Le studio de pubs motion de la formation **Motion Design Pro avec l'IA** (Oumar Moutari).

## Installation (pour l'élève)

Dans Claude (onglet Code), colle ce message :

```
Installe le pack Motion Design Pro depuis
https://github.com/oumar-ai/motion-design-pro
Suis les instructions du README, puis vérifie que tout fonctionne.
```

Claude fait le reste.

## Instructions pour Claude

1. Clone ce dépôt dans un dossier temporaire.
2. Lance le script d'installation :
   - Windows : `powershell -ExecutionPolicy Bypass -File install.ps1`
   - Mac : `bash install.sh`
3. Vérifie que ces éléments répondent : `node --version`, `ffmpeg -version`, `python --version`, et que le dossier `~/.claude/skills/motion-design-pro` existe avec son fichier `SKILL.md`.
4. Si un outil manque, installe-le et explique en une phrase à l'utilisateur ce que tu as fait.
5. Termine par : « Le studio est prêt. Redémarre Claude, puis tape : Fais-moi une vidéo motion pour [ton produit]. »

## Contenu

- `skills/motion-design-pro` : les règles du studio (collecte, script, voix, animation, son, vérification) et 42 effets sonores libres de droits.
- `install.ps1` / `install.sh` : installation automatique des skills et des outils (Node.js, FFmpeg, Python, HyperFrames).
