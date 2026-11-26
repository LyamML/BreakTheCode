"""p05 — Un message codé : décodeur Morse audio générique (.wav).

- Détecte seul l'unité de temps (durée du plus court "bip").
- Seuil d'amplitude automatique, fenêtre glissante de 10 ms.
- Gère le Morse étendu français (É, È, À, Ç...).
- Classe les silences par rapport à l'unité : <2u = intra-lettre, <4u = lettre,
  >=4u = mot. (Ce fichier utilise 1u / 2u / 4u au lieu des 1/3/7 standard ;
  les silences de 3u sont des fins de phrase.)

Usage : python -I solve.py [message.wav] [--details]
"""
import re
import sys
import wave
from pathlib import Path

import numpy as np

MORSE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
    "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
    "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z",
    "-----": "0", ".----": "1", "..---": "2", "...--": "3", "....-": "4",
    ".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9",
    ".-.-.-": ".", "--..--": ",", "..--..": "?", ".----.": "'", "-.-.--": "!",
    "-..-.": "/", "-.--.": "(", "-.--.-": ")", ".-...": "&", "---...": ":",
    "-.-.-.": ";", "-...-": "=", ".-.-.": "+", "-....-": "-", "..--.-": "_",
    ".-..-.": '"', ".--.-.": "@",
    # Morse étendu (accents)
    "..-..": "É", ".-..-": "È", ".--.-": "À", "-.-..": "Ç", "..--": "Ü",
    "---.": "Ö", ".-.-": "Ä", "--.--": "Ñ",
}


def runs_from_wav(path, win_ms=10):
    with wave.open(str(path)) as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    dtype = {1: np.uint8, 2: np.int16, 4: np.int32}[sw]
    x = np.frombuffer(raw, dtype=dtype).astype(float)
    if sw == 1:
        x -= 128
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    win = int(sr * win_ms / 1000)
    env = np.abs(x[: len(x) // win * win]).reshape(-1, win).mean(axis=1)
    on = env > env.max() * 0.3
    runs, cur, length = [], on[0], 0
    for v in on:
        if v == cur:
            length += 1
        else:
            runs.append((bool(cur), length))
            cur, length = v, 1
    runs.append((bool(cur), length))
    return runs


def decode(runs, sentence_mark=" "):
    unit = min(l for o, l in runs if o)
    out, sym = [], ""
    # ignore leading/trailing silence
    while runs and not runs[0][0]:
        runs = runs[1:]
    for on, l in runs:
        u = l / unit
        if on:
            sym += "." if u < 2 else "-"
            continue
        if u < 1.5:
            continue
        out.append(MORSE.get(sym, f"[{sym}]"))
        sym = ""
        if 2.5 <= u < 3.5:
            out.append(sentence_mark)
        elif u >= 3.5:
            out.append(" ")
    if sym:
        out.append(MORSE.get(sym, f"[{sym}]"))
    return "".join(out).strip()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = Path(args[0]) if args else Path(__file__).parent / "data" / "message.wav"
    text = decode(runs_from_wav(path))
    m = re.search(r"ARRIV\S*\s+SUR\s+LA\s+PLAN\S+\s+([A-Z]+)", text)
    planet = m.group(1).capitalize() if m else "?"
    print(planet)
    (Path(__file__).parent / "answer.txt").write_text(planet + "\n", encoding="utf-8")
    (Path(__file__).parent / "message.txt").write_text(text + "\n", encoding="utf-8")
    if "--details" in sys.argv:
        print("\n" + text)


if __name__ == "__main__":
    main()
