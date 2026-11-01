#!/usr/bin/env bash
# Installation du pack Motion Design Pro (Mac)
# Lancement : bash install.sh

echo "== Pack Motion Design Pro : installation =="
DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. Skills dans le dossier de Claude
mkdir -p "$HOME/.claude/skills"
cp -R "$DIR/skills/"* "$HOME/.claude/skills/"
echo "[ok] Skill motion-design-pro copie"

# 2. Outils (Homebrew)
if ! command -v brew >/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
for pkg in node ffmpeg python; do
  command -v "$pkg" >/dev/null || brew install "$pkg"
done

# 3. Skills HyperFrames (moteur video)
npx -y skills add heygen-com/hyperframes

# 4. Bibliotheque Python pour caler la musique
python3 -m pip install --quiet librosa

echo "== Installation terminee. Redemarre Claude, puis tape : Fais-moi une video motion =="
