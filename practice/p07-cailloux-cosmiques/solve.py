"""p07 — Alerte cailloux cosmiques : nombre de champs d'astéroïdes.

Usage : python -I solve.py data [--all]

Chaque pixel blanc (255) des 10 images est un astéroïde en (z, y, x), les images
étant espacées de 1 px. Deux astéroïdes à distance euclidienne <= 5 sont dans le
même champ (lien simple, transitif) -> composantes connexes.

Méthode exacte sans KD-tree (scipy.spatial / scipy.linalg peuvent être bloqués
par la politique Windows) : on étiquette d'abord les composantes 26-connexes
(distance <= sqrt(3) < 5, donc forcément même champ), puis pour chaque vecteur
de décalage d de norme <= R on fait un ET entre le volume et le volume décalé :
chaque couple de pixels blancs trouvé unit deux composantes (union-find).
"""
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))  # chemins relatifs au dossier du challenge
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def load(folder: Path) -> np.ndarray:
    files = sorted(folder.glob("image_*.png"))
    return np.stack([np.array(Image.open(f).convert("L")) > 127 for f in files])


def count_fields(vol: np.ndarray, r: float, metric: str = "eucl", strict: bool = False) -> int:
    lab, n = ndimage.label(vol, structure=np.ones((3, 3, 3)))
    parent = np.arange(n + 1)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    R = int(np.floor(r))
    Z, Y, X = vol.shape
    for dz in range(0, R + 1):
        for dy in range(-R, R + 1):
            for dx in range(-R, R + 1):
                # demi-espace pour ne traiter chaque paire qu'une fois
                if (dz, dy, dx) <= (0, 0, 0):
                    continue
                if metric == "eucl":
                    d = (dz * dz + dy * dy + dx * dx) ** 0.5
                elif metric == "cheb":
                    d = max(abs(dz), abs(dy), abs(dx))
                else:  # manhattan
                    d = abs(dz) + abs(dy) + abs(dx)
                if d > r or (strict and d >= r) or dz >= Z:
                    continue
                a = lab[0:Z - dz, max(0, -dy):Y - max(0, dy), max(0, -dx):X - max(0, dx)]
                b = lab[dz:Z, max(0, dy):Y + min(0, dy), max(0, dx):X + min(0, dx)]
                m = (a > 0) & (b > 0) & (a != b)
                if not m.any():
                    continue
                pairs = np.unique(np.stack([a[m], b[m]], 1), axis=0)
                for p, q in pairs:
                    rp, rq = find(p), find(q)
                    if rp != rq:
                        parent[rp] = rq
    return len({find(i) for i in range(1, n + 1)})


def main() -> None:
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "data")
    vol = load(folder)
    if "--all" in sys.argv:
        print("pixels blancs:", int(vol.sum()))
        print("26-connexe (contact):", ndimage.label(vol, np.ones((3, 3, 3)))[1])
        for lab_, r, met, st in [
            ("euclidienne <= 5", 5, "eucl", False),
            ("euclidienne < 5", 5, "eucl", True),
            ("chebyshev <= 5", 5, "cheb", False),
            ("manhattan <= 5", 5, "manh", False),
            ("euclidienne <= 10 (diametre)", 10, "eucl", False),
            ("euclidienne <= 2.5 (rayon/2)", 2.5, "eucl", False),
        ]:
            print(f"{lab_}: {count_fields(vol, r, met, st)}")
        s = sum(count_fields(vol[z:z + 1], 5) for z in range(vol.shape[0]))
        print("2D par image, eucl <= 5, somme:", s)
    else:
        ans = str(count_fields(vol, 5))
        print(ans)
        (Path(__file__).resolve().parent / "answer.txt").write_text(ans + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
