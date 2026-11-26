"""Verification independante : decodage generique (on reapplique "codes decimaux ->
caracteres" jusqu'a obtenir un seul caractere), puis recherche exhaustive dans les
8 directions de toute suite de >= 5 lettres, et controle de answer.txt."""
import re
from pathlib import Path

HERE = Path(__file__).parent
text = (HERE / "ENONCE.md").read_text(encoding="utf-8")
cells = re.findall(r"'([0-9-]+)'", text)
assert len(cells) == 100


def to_chars(s):
    # couche 1 : codes separes par '-' (et '--')
    return "".join(chr(int(x)) for x in s.replace("--", "-").split("-"))


def full(cell):
    s = to_chars(cell)
    while len(s) > 1:
        # couche suivante : chiffres -> codes ASCII decimaux de 2 ou 3 chiffres (32..126)
        out, i = "", 0
        if len(s) <= 3 and 32 <= int(s) <= 126:
            return chr(int(s))
        while i < len(s):
            for w in (2, 3):
                v = s[i:i + w]
                if len(v) == w and 32 <= int(v) <= 126 and not (w == 3 and int(s[i:i + 2]) >= 32):
                    out += chr(int(v)); i += w; break
            else:
                raise ValueError(s)
        s = out
    return s


G = [[full(cells[10 * r + c]) for c in range(10)] for r in range(10)]
found = []
for r in range(10):
    for c in range(10):
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]:
            s, rr, cc = "", r, c
            while 0 <= rr < 10 and 0 <= cc < 10 and G[rr][cc].isalpha():
                s += G[rr][cc]; rr += dr; cc += dc
            if len(s) >= 5:
                found.append((r, c, dr, dc, s))
print(found)
ans = (HERE / "answer.txt").read_text(encoding="utf-8").strip()
assert any(ans in s for *_, s in found), "answer.txt introuvable dans la grille"
print("OK : answer.txt =", ans, "present dans la grille")
