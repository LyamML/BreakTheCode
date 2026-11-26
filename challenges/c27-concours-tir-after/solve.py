"""c27 Concours de tir : After party.
Lit data/bullets.data.zip en memoire (zipfile, rien n'est extrait ni execute),
simule chaque archive jusqu'a t avec les regles de c24, et trace les positions
de toutes les balles a t sur une grille 100x100 -> portrait.png.
Usage : python3 -I solve.py
"""
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
ZIP = HERE / "data" / "bullets.data.zip"


def position_at(b, t):
    x, y, vx, vy = b
    for _ in range(t):
        x += vx
        y += vy
        if x < 0 or x > 99:
            vx = -vx
        if y < 0 or y > 99:
            vy = -vy
    return x, y


def main():
    pts = []
    with zipfile.ZipFile(ZIP) as z:
        names = [n for n in z.namelist() if n.endswith(".txt")]
        for n in names:
            lines = [l.split() for l in z.read(n).decode().splitlines() if l.strip()]
            t = int(lines[0][0])
            for l in lines[1:]:
                pts.append(position_at(tuple(map(int, l)), t))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    print(f"{len(names)} archives, {len(pts)} balles, {len(set(pts))} positions distinctes,"
          f" x in [{min(xs)},{max(xs)}], y in [{min(ys)},{max(ys)}]")
    img = np.full((100, 100), 255, np.uint8)
    for x, y in pts:
        img[y, x] = 0  # ligne = y (y vers le bas) : portrait a l'endroit
    Image.fromarray(img).resize((600, 600), Image.NEAREST).save(HERE / "portrait.png")
    Image.fromarray(img[::-1]).resize((600, 600), Image.NEAREST).save(HERE / "portrait_yup.png")
    # Identification visuelle (portrait d'Abraham Lincoln) : aucun texte dans l'image.
    answer = "Abraham Lincoln"
    (HERE / "answer.txt").write_text(answer + "\n")
    print(answer)


if __name__ == "__main__":
    main()
