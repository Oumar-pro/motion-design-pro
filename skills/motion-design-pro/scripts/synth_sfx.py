"""Génère les sons de transition absents des packs Kenney (whoosh, riser, sub drop, boom, pop, scintillement).

Sons synthétisés ici, donc sans licence tierce (domaine public / CC0).
Usage : python -I synth_sfx.py <dossier_sortie>
Sortie : WAV 48 kHz stéréo 16 bits, crête normalisée à -1 dBFS.
"""
import sys, os, math, random, struct, wave

SR = 48000


def bandpass_noise(n, f_of_t, q, rng):
    # bruit blanc filtré par un passe-bande biquad dont la fréquence suit f_of_t(t ∈ [0,1])
    out = [0.0] * n
    x1 = x2 = y1 = y2 = 0.0
    for i in range(n):
        f = f_of_t(i / n)
        w = 2 * math.pi * f / SR
        alpha = math.sin(w) / (2 * q)
        b0, b2 = alpha, -alpha
        a0, a1, a2 = 1 + alpha, -2 * math.cos(w), 1 - alpha
        x = rng.uniform(-1, 1)
        y = (b0 * x + b2 * x2 - a1 * y1 - a2 * y2) / a0
        x2, x1, y2, y1 = x1, x, y1, y
        out[i] = y
    return out


def env_ar(t, peak):
    # montée jusqu'à peak (0-1) puis descente, courbes douces
    return math.sin(math.pi / 2 * t / peak) ** 2 if t < peak else math.cos(math.pi / 2 * (t - peak) / (1 - peak)) ** 2


def write(path, left, right=None):
    right = right or left
    m = max(max(abs(v) for v in left), max(abs(v) for v in right)) or 1
    g = 10 ** (-1 / 20) / m
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<hh", int(l * g * 32767), int(r * g * 32767)) for l, r in zip(left, right)))


def whoosh(dur, f0, f1, f2, pan=True, seed=1):
    rng = random.Random(seed)
    n = int(dur * SR)
    noise = bandpass_noise(n, lambda t: f0 + (f1 - f0) * math.sin(math.pi * t) if t < 0.5 else f1 + (f2 - f1) * (t - 0.5) * 2, 1.2, rng)
    s = [noise[i] * env_ar(i / n, 0.55) for i in range(n)]
    if not pan:
        return s, s
    l = [s[i] * math.cos(math.pi / 4 * (1 + i / n * 0.8 - 0.4)) for i in range(n)]
    r = [s[i] * math.sin(math.pi / 4 * (1 + i / n * 0.8 - 0.4)) for i in range(n)]
    return l, r


def riser(dur, seed=2):
    rng = random.Random(seed)
    n = int(dur * SR)
    noise = bandpass_noise(n, lambda t: 300 * (20 ** t), 2.0, rng)
    ph = 0.0
    out = []
    for i in range(n):
        t = i / n
        ph += 2 * math.pi * (180 * (8 ** t)) / SR
        a = t ** 2.2 * (1 if t < 0.97 else (1 - t) / 0.03)
        out.append(a * (0.8 * noise[i] + 0.25 * math.sin(ph)))
    return out, out


def sub_drop(dur=0.9):
    n = int(dur * SR)
    ph = 0.0
    out = []
    for i in range(n):
        t = i / n
        ph += 2 * math.pi * (110 * (0.3 ** t)) / SR
        out.append(math.sin(ph) * min(1, t * 60) * (1 - t) ** 1.5)
    return out, out


def boom(dur=0.7, seed=3):
    rng = random.Random(seed)
    n = int(dur * SR)
    noise = bandpass_noise(n, lambda t: 140, 0.7, rng)
    ph = 0.0
    out = []
    for i in range(n):
        t = i / SR
        ph += 2 * math.pi * (55 + 90 * math.exp(-t * 30)) / SR
        out.append(math.sin(ph) * math.exp(-t * 6) + 0.6 * noise[i] * math.exp(-t * 25))
    return out, out


def pop(dur=0.09):
    n = int(dur * SR)
    ph = 0.0
    out = []
    for i in range(n):
        t = i / n
        ph += 2 * math.pi * (950 * (0.35 ** t)) / SR
        out.append(math.sin(ph) * min(1, t * 40) * (1 - t) ** 2)
    return out, out


def sparkle(dur=0.8, seed=4):
    rng = random.Random(seed)
    n = int(dur * SR)
    l, r = [0.0] * n, [0.0] * n
    for k in range(9):
        start = int(rng.uniform(0, 0.45) * SR)
        f = rng.choice([2093, 2349, 2637, 3136, 3520, 4186])
        p = rng.uniform(0.2, 0.8)
        for i in range(start, min(n, start + int(0.35 * SR))):
            t = (i - start) / SR
            v = math.sin(2 * math.pi * f * t) * math.exp(-t * 14) * 0.3
            l[i] += v * (1 - p)
            r[i] += v * p
    return l, r


def main():
    d = sys.argv[1]
    os.makedirs(d, exist_ok=True)
    sons = {
        "whoosh_court.wav": whoosh(0.35, 400, 2600, 900, seed=11),
        "whoosh_moyen.wav": whoosh(0.6, 300, 2200, 700, seed=12),
        "whoosh_long.wav": whoosh(1.0, 250, 1800, 500, seed=13),
        "whoosh_aigu.wav": whoosh(0.3, 1200, 6000, 2500, seed=14),
        "riser_1s.wav": riser(1.0),
        "riser_2s.wav": riser(2.0, seed=5),
        "sub_drop.wav": sub_drop(),
        "boom_impact.wav": boom(),
        "pop_synth.wav": pop(),
        "scintillement.wav": sparkle(),
    }
    for name, (l, r) in sons.items():
        write(os.path.join(d, name), l, r)
        print(name)


if __name__ == "__main__":
    main()
