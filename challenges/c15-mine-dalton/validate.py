"""Controle independant : (1) transcription vs pixels de salle_D.png, (2) second solveur
(DFS memoise sur (case, t, masque) avec reconstruction du chemin), (3) rejeu du chemin,
(4) variantes d'interpretation."""
import sys
from functools import lru_cache
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from solve import GRID, STICKS  # noqa: E402

# (1) pixels
im = Image.open(HERE / "data" / "salle_D.png").convert("RGB")
for r in range(19):
    for c in range(19):
        x, y = 125 + 65 * c, 280 + 65 * r
        R, G, B = im.getpixel((x - 22, y + 5))
        bord = im.getpixel((x - 28, y))
        red = bord[0] > 140 and bord[1] < 90
        ch = GRID[r][c]
        if (r, c) == (0, 0):
            kind = 'E'
        elif R > 150 and G < 80:
            kind = 'X'
        elif R < 80:
            kind = '#'
        elif R > 140 and G < 130 and B < 60:
            kind = 'gold'
        else:
            kind = '.'
        exp = {'#': '#', 'E': 'E', 'X': 'X', '.': '.', 'D': '.'}.get(ch, 'gold')
        assert kind == exp, (r, c, ch, kind)
        if ch != 'X':
            assert red == ((r, c) in STICKS), (r, c)
print("transcription conforme aux pixels (361 cases, 30 batons)")

grid = [row.replace('D', '.') for row in GRID]
R = C = 19


def build(sticks, radius=True):
    col = {}
    for (r, c), t in sticks.items():
        cells = [(r, c)] + ([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)] if radius else [])
        for p in cells:
            col[p] = min(col.get(p, 10 ** 9), t)
    return col


def run(sticks, radius=True, strict=True, t0=0, T=400):
    col = build(sticks, radius)
    alive = (lambda p, t: t < col.get(p, 10 ** 9)) if strict else (lambda p, t: t <= col.get(p, 10 ** 9))
    nug = {(r, c): int(grid[r][c]) for r in range(R) for c in range(C) if grid[r][c].isdigit()}
    X = (18, 18)
    sys.setrecursionlimit(100000)

    @lru_cache(maxsize=None)
    def f(p, t, m):
        # meilleur nombre de pepites atteignable en finissant a X ; -1 si impossible
        if p == X:
            return bin(m).count('1')
        if t >= T:
            return -1
        best = -1
        r, c = p
        for q in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= q[0] < R and 0 <= q[1] < C and grid[q[0]][q[1]] != '#' and alive(q, t + 1):
                m2 = m | (1 << (nug[q] - 1) if q in nug else 0)
                best = max(best, f(q, t + 1, m2))
        return best

    res = f((0, 0), t0, 0)
    # chemin
    path = [(0, 0)]
    p, t, m = (0, 0), t0, 0
    while p != X and res >= 0:
        r, c = p
        for q in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= q[0] < R and 0 <= q[1] < C and grid[q[0]][q[1]] != '#' and alive(q, t + 1):
                m2 = m | (1 << (nug[q] - 1) if q in nug else 0)
                if f(q, t + 1, m2) == res:
                    p, t, m = q, t + 1, m2
                    path.append(q)
                    break
    got = sorted(nug[q] for q in set(path) if q in nug)
    return res, path, got, col


res, path, got, col = run(STICKS)
print("solveur 2 :", res, "pepites", got, "longueur", len(path) - 1)
# (3) rejeu
for t, p in enumerate(path):
    assert grid[p[0]][p[1]] != '#' and t < col.get(p, 10 ** 9), (t, p)
for a, b in zip(path, path[1:]):
    assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
print("chemin rejoue OK")
print("chemin :", path)
assert res == int((HERE / "answer.txt").read_text())
# (4) variantes
print("variante t<=t (non strict) :", run(STICKS, strict=False)[0])
print("variante sans voisins      :", run(STICKS, radius=False)[0])
print("variante depart t=1        :", run(STICKS, t0=1)[0])
for k in STICKS:  # sensibilite +-1 sur chaque minuteur
    for d in (-1, 1):
        s2 = dict(STICKS); s2[k] += d
        v = run(s2)[0]
        if v != res:
            print("  sensible :", k, STICKS[k], "->", STICKS[k] + d, ":", v)
