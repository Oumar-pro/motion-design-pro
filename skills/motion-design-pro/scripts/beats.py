"""Tempo, temps forts et attaques d'une musique, pour caler les transitions.

Usage : python beats.py <musique.mp3|wav> [sortie.json]
Besoin : pip install librosa
Sortie : beats.json avec tempo (BPM), temps forts (s), un temps fort sur 4 (début de mesure probable), attaques (s).
"""
import sys, json
import librosa


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "beats.json"
    y, sr = librosa.load(src, sr=None, mono=True)
    tempo, frames = librosa.beat.beat_track(y=y, sr=sr)
    temps = [round(float(t), 3) for t in librosa.frames_to_time(frames, sr=sr)]
    attaques = [round(float(t), 3) for t in librosa.onset.onset_detect(y=y, sr=sr, units="time")]
    res = {
        "fichier": src,
        "duree_s": round(len(y) / sr, 2),
        "tempo_bpm": round(float(tempo[0] if hasattr(tempo, "__len__") else tempo), 1),
        "temps_forts_s": temps,
        "mesures_s": temps[::4],
        "attaques_s": attaques,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(f"{res['tempo_bpm']} BPM, {len(temps)} temps forts, {len(attaques)} attaques -> {out}")


if __name__ == "__main__":
    main()
