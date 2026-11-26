---
id: p07
title: Alerte cailloux cosmiques
points: 59
tags: [Facile, Clustering, Visuel]
status: solved
answer: "447"
confidence: haute
---

# p07 — Alerte cailloux cosmiques

## Réponse

```
447
```

Non vérifiable sur l'archive (pas de compte connecté). Confiance haute : la seule
interprétation fidèle au texte donne 447, et la variante stricte `< 5` donne aussi 447.

## Interprétation de l'énoncé

- 10 images 500×500 en niveaux de gris, **strictement binaires** (0 / 255) → pas de
  question de seuil (> 127 suffit).
- « Suite d'images situées à une distance 1px représentant un espace en 3 dimensions » :
  on empile les images, coordonnées `(z, y, x)` avec `z` = index de l'image, pas de 1.
- « chaque pixel blanc représente un astéroïde » : **chaque pixel** est un astéroïde
  (pas chaque tache). 70 050 astéroïdes.
- « amas d'astéroïdes situés dans un rayon maximum de 5px les uns des autres » : lien
  simple transitif (A–B ≤ 5 et B–C ≤ 5 → A, B, C même champ) = composantes connexes du
  graphe « distance ≤ 5 ». Distance euclidienne 3D (on parle de rayon → boule).
- « Un astéroïde isolé est compté comme un champ » → les singletons comptent.

## Toutes les variantes calculées (`python -I solve.py data --all`)

| Interprétation | Champs |
|---|---|
| **Euclidienne 3D ≤ 5 (retenue)** | **447** |
| Euclidienne 3D < 5 | 447 |
| Chebyshev ≤ 5 (cube) | 429 |
| Manhattan ≤ 5 | 455 |
| Euclidienne ≤ 10 (rayon pris comme diamètre ×2) | 352 |
| Euclidienne ≤ 2.5 | 501 |
| Simple contact 26-connexe | 547 |
| 2D image par image, somme | 621 |

≤ 5 et < 5 donnent le même résultat : aucun couple déterminant n'est à exactement 5.

## Approche

1. Charger les 10 PNG → volume booléen `10×500×500`.
2. `scipy.ndimage.label` en 26-connexité : deux pixels qui se touchent sont à ≤ √3 < 5,
   donc dans le même champ. 547 composantes, ce qui réduit énormément le travail.
3. Pour chaque vecteur `d` (demi-espace) de norme ≤ 5 (~260 vecteurs), ET entre le
   volume étiqueté et sa version décalée de `d` : chaque paire d'étiquettes différentes
   trouvée est unie (union-find). Exact, ~3 s par variante.

## Ce qui a marché

- Regarder une image d'abord (Read sur le PNG) : on voit des taches + des pixels
  isolés, ce qui montre tout de suite que « astéroïde = pixel », pas « astéroïde = tache ».
- Pré-étiqueter en 26-connexe puis unir par décalages : exact, rapide, numpy pur.
- Calculer toutes les variantes d'un coup : on voit qu'elles divergent (429 → 621),
  donc l'interprétation compte vraiment, et que `≤`/`<` ne change rien.

## Ce qui n'a pas marché / pièges

- **`scipy.spatial.cKDTree` est inutilisable sur ce poste** : son import charge
  `scipy.linalg` → `_flapack`, DLL **bloquée par la stratégie de contrôle d'application
  Windows** (`ImportError: DLL load failed ... Une stratégie de contrôle d'application a
  bloqué ce fichier`). `scipy.ndimage` fonctionne. Tout ce qui importe `scipy.linalg`
  (spatial, optimize, sparse.csgraph probablement) est à tester avant de compter dessus.
- Un KD-tree sur 70 000 points avec r = 5 génère ~10 M paires : faisable mais lourd ; la
  pré-réduction par composantes 26-connexes est bien plus efficace.

## Vérifications faites

- Brute force O(n²) en Python pur sur 4 sous-volumes 10×90×90 (de 13 à 14 496 points) :
  même nombre de champs que la méthode par décalages à chaque fois.
- Valeurs de pixels inspectées : uniquement 0 et 255 dans les 10 images.

## Temps / difficulté réelle

~15 min dont 5 perdues sur le blocage scipy. Difficulté réelle : facile, une fois qu'on a
tranché l'interprétation.

## Leçons pour le jour J

- Sur une question de clustering, **lister et calculer toutes les métriques** possibles
  et regarder si elles divergent. Ici elles divergent → c'est le texte qui tranche
  (« rayon » = boule euclidienne, chaque pixel = un objet).
- Composantes connexes avec un seuil de distance sur une grille : `ndimage.label` puis
  union-find par décalages ; pas besoin de KD-tree.
- Tester dès le début `python -c "import scipy.spatial"` : si c'est bloqué, le savoir
  avant d'écrire le code.
