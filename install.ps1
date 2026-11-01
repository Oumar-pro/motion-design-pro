# Installation du pack Motion Design Pro (Windows)
# Lancement : powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Continue"
Write-Host "== Pack Motion Design Pro : installation ==" -ForegroundColor Cyan

# 1. Skills dans le dossier de Claude
$dest = Join-Path $HOME ".claude\skills"
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item -Recurse -Force (Join-Path $PSScriptRoot "skills\*") $dest
Write-Host "[ok] Skill motion-design-pro copie dans $dest"

# 2. Outils (winget, deja present sur Windows 10 et 11)
function Install-IfMissing($cmd, $id) {
  if (Get-Command $cmd -ErrorAction SilentlyContinue) { Write-Host "[ok] $cmd deja installe" }
  else {
    Write-Host "[..] Installation de $id"
    winget install --id $id -e --silent --accept-source-agreements --accept-package-agreements
  }
}
Install-IfMissing "node"   "OpenJS.NodeJS.LTS"
Install-IfMissing "ffmpeg" "Gyan.FFmpeg"
Install-IfMissing "python" "Python.Python.3.12"

# Rafraichir le PATH de cette session
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")

# 3. Skills HyperFrames (moteur video)
Write-Host "[..] Installation des skills HyperFrames"
npx -y skills add heygen-com/hyperframes

# 4. Bibliotheque Python pour caler la musique
python -m pip install --quiet librosa

Write-Host "== Installation terminee. Redemarre Claude, puis tape : Fais-moi une video motion ==" -ForegroundColor Green
