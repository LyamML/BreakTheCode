from pathlib import Path

d = Path(__file__).parent
ts = []
for s in (d / "data" / "challenge_Rennes.txt").read_text().split():
    h, m, x = s.split(":")
    ts.append(round((int(h) * 3600 + int(m) * 60 + float(x)) * 1000))
# tirs parasites : millisecondes hors grille .200/.700
clean = [t for t in ts if t % 500 == 200]
gaps = [b - a for a, b in zip(clean, clean[1:])]
bits = "".join("0" if g == 1000 else "1" for g in gaps)  # 1.0 s -> 0, 1.5 s -> 1
word = "".join(chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8))
print(bits, word)
(d / "answer.txt").write_text(word + "\n")
