"""Vérification indépendante (numpy vectorisé) de solve.py."""
import sys
from pathlib import Path
import numpy as np

L = (Path(__file__).parent / "data/bullets.data.txt").read_text().split("\n")
xc, yc = map(int, L[0].split())
B = np.array([list(map(int, l.split())) for l in L[1:] if l.strip()])
x, y, vx, vy = [B[:, i].copy() for i in range(4)]
bn = np.zeros(len(B), bool)
for t in range(5000):
    h = np.where((x == xc) & (y == yc))[0]
    if len(h):
        print(t, "indices", h, "rebondi", bn[h])
        break
    x = x + vx
    y = y + vy
    ox = (x < 0) | (x > 99)
    oy = (y < 0) | (y > 99)
    vx = np.where(ox, -vx, vx)
    vy = np.where(oy, -vy, vy)
    bn |= ox | oy
