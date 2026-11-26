"""Outils p08 : parsing du dataset + rendu de la voûte céleste depuis une position.

Usage :
  python -I sky.py <dataset> <pos: x,y,z | star-id> <out_dir> [--max-dist 1000]

Produit dans out_dir :
  - all_sky.png : projection équirectangulaire (phi en abscisse, inversée comme dans
    l'exemple de l'énoncé = vue de l'intérieur ; theta en ordonnée).
  - <constellation>.png : projection gnomonique (plan tangent) centrée sur la
    constellation, sans distorsion, avec les ids d'étoiles. Étoiles > max-dist en gris,
    étoiles hors constellation proches en rouge.
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def parse(path):
    lines = [l.rstrip("\r\n") for l in Path(path).read_text(encoding="utf-8").splitlines()]
    it = iter(lines)

    def nxt():
        while True:
            l = next(it)
            if l.strip():
                return l

    i, s, c = map(int, nxt().split())
    instr = [nxt() for _ in range(i)]
    stars = np.array([list(map(float, nxt().split())) for _ in range(s)])
    consts = []
    for _ in range(c):
        name = nxt().strip()
        n, m = map(int, nxt().split())
        ids = list(map(int, nxt().split()))
        assert len(ids) == n, (name, n, len(ids))
        edges = [tuple(map(int, nxt().split())) for _ in range(m)]
        consts.append({"name": name, "ids": ids, "edges": edges})
    return instr, stars, consts


def spherical(v):
    r = np.linalg.norm(v, axis=-1) if v.ndim > 1 else np.linalg.norm(v)
    theta = np.arccos(np.clip(v[..., 2] / np.maximum(r, 1e-12), -1, 1))
    phi = np.arctan2(v[..., 1], v[..., 0])
    return r, theta, phi


def gnomonic(dirs, center):
    """Projette des directions unitaires sur le plan tangent à `center` (vue de l'intérieur)."""
    c = center / np.linalg.norm(center)
    up0 = np.array([0.0, 0.0, 1.0])
    if abs(c @ up0) > 0.95:
        up0 = np.array([1.0, 0.0, 0.0])
    e_up = up0 - (up0 @ c) * c
    e_up /= np.linalg.norm(e_up)
    e_right = np.cross(c, e_up)  # vue depuis l'intérieur de la sphère
    d = dirs / np.maximum(np.linalg.norm(dirs, axis=1, keepdims=True), 1e-9)
    cosang = d @ c
    x = (d @ e_right) / np.maximum(cosang, 1e-6)
    y = (d @ e_up) / np.maximum(cosang, 1e-6)
    return np.stack([x, y], 1), cosang


def render_constellation(stars, pos, const, out_png, max_dist=1000.0, size=900):
    rel = stars - pos
    dist = np.linalg.norm(rel, axis=1)
    ids = np.array(const["ids"]) - 1
    ids = ids[dist[ids] > 1e-9]  # l'étoile où se trouve le vaisseau n'est pas visible
    center = (rel[ids] / dist[ids, None]).mean(0)
    proj, cosang = gnomonic(rel, center)
    p = proj[ids]
    lo, hi = p.min(0), p.max(0)
    span = max(hi - lo) * 1.15 + 1e-9
    mid = (lo + hi) / 2

    def to_px(q):
        return ((q[:, 0] - mid[0]) / span + 0.5) * size, (0.5 - (q[:, 1] - mid[1]) / span) * size

    img = Image.new("RGB", (size, size + 40), "white")
    dr = ImageDraw.Draw(img)
    X, Y = to_px(proj)
    inset = set(ids.tolist())
    # étoiles hors constellation visibles dans le cadre
    for k in range(len(stars)):
        if k in inset or cosang[k] <= 0 or dist[k] < 1e-9:
            continue
        if 0 <= X[k] < size and 0 <= Y[k] < size:
            col = (220, 0, 0) if dist[k] <= max_dist else (255, 180, 180)
            dr.ellipse([X[k] - 3, Y[k] - 3, X[k] + 3, Y[k] + 3], fill=col)
            dr.text((X[k] + 4, Y[k] - 12), str(k + 1), fill=col)
    for a, b in const["edges"]:
        a, b = a - 1, b - 1
        if a not in inset or b not in inset or cosang[a] <= 0 or cosang[b] <= 0:
            continue
        vis = dist[a] <= max_dist and dist[b] <= max_dist
        dr.line([X[a], Y[a], X[b], Y[b]], fill=(0, 0, 200) if vis else (200, 200, 230), width=2)
    for k in ids:
        if cosang[k] <= 0:
            continue
        vis = dist[k] <= max_dist
        col = (0, 0, 0) if vis else (170, 170, 170)
        dr.ellipse([X[k] - 4, Y[k] - 4, X[k] + 4, Y[k] + 4], fill=col)
        dr.text((X[k] + 5, Y[k] - 12), str(k + 1), fill=col)
    nvis = int((dist[ids] <= max_dist).sum())
    dr.text((10, size + 10),
            f"{const['name']}  visibles {nvis}/{len(ids)}  dist min/med/max "
            f"{dist[ids].min():.0f}/{np.median(dist[ids]):.0f}/{dist[ids].max():.0f}",
            fill=(0, 0, 0))
    img.save(out_png)
    return nvis


def render_all_sky(stars, pos, consts, out_png, max_dist=1000.0, W=1800, H=900):
    rel = stars - pos
    r, th, ph = spherical(rel)
    img = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(img)
    X = (1 - (ph + math.pi) / (2 * math.pi)) * W  # phi inversé (vue de l'intérieur)
    Y = th / math.pi * H
    palette = [(200, 0, 0), (0, 120, 0), (0, 0, 200), (160, 0, 160), (0, 140, 140), (200, 120, 0),
               (90, 90, 90), (120, 60, 0)]
    for k in range(len(stars)):
        if 0 < r[k] <= max_dist:
            dr.point((X[k], Y[k]), fill=(150, 150, 150))
    for ci, c in enumerate(consts):
        col = palette[ci % len(palette)]
        for a, b in c["edges"]:
            a, b = a - 1, b - 1
            if r[a] <= max_dist and r[b] <= max_dist and abs(X[a] - X[b]) < W / 2:
                dr.line([X[a], Y[a], X[b], Y[b]], fill=col, width=1)
        ids = np.array(c["ids"]) - 1
        vis = ids[r[ids] <= max_dist]
        if len(vis):
            dr.text((X[vis].mean(), Y[vis].mean()), c["name"], fill=col)
    img.save(out_png)


def main():
    ds, pos_arg, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    max_dist = float(sys.argv[sys.argv.index("--max-dist") + 1]) if "--max-dist" in sys.argv else 1000.0
    instr, stars, consts = parse(ds)
    pos = stars[int(pos_arg) - 1] if "," not in pos_arg else np.array(list(map(float, pos_arg.split(","))))
    out.mkdir(parents=True, exist_ok=True)
    render_all_sky(stars, pos, consts, out / "all_sky.png", max_dist)
    for c in consts:
        safe = "".join(ch if ch.isalnum() else "_" for ch in c["name"])
        nvis = render_constellation(stars, pos, c, out / f"{safe}.png", max_dist)
        print(f"{c['name']:<35} visibles {nvis}/{len(c['ids'])}")


if __name__ == "__main__":
    main()
