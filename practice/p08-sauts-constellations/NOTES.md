---
id: p08
title: Sauts de Constellations
points: 63
tags: [Difficile, Constellation, Visuel, Projection]
status: solved
answer: "285 515 493 108"
confidence: haute
---

# p08 — Sauts de Constellations

## Réponse

```
285 515 493 108
```

Non vérifiable sur l'archive. Confiance haute : chaque étape est justifiée par la
structure du graphe (segments) et vérifiée sur un rendu, et l'étape 4 tombe sur la seule
étoile « orpheline » du dataset.

## Interprétation de l'énoncé

- Format du fichier : `i s c`, puis `i` instructions texte, `s` étoiles (`x y z`, id = n°
  de ligne à partir de 1), puis `c` blocs constellation (nom / `n m` / ids / `m` segments).
- Le vaisseau part de (0,0,0) ; après chaque instruction il **se déplace sur l'étoile
  trouvée**, et on recalcule le ciel depuis là (l'étoile où l'on est disparaît du ciel).
- Seules les étoiles à ≤ 1000 al sont visibles : ça sert surtout à savoir **quelle
  constellation est visible depuis où** (depuis l'origine, l'Épée, Dark Vador et le
  Dinosaure sont invisibles ; ils apparaissent après les sauts).
- Réponse : les ids trouvés, séparés par un espace.

Les 4 instructions du dataset :
1. « l'étoile entre les deux yeux de Marvin »
2. « l'étoile faisant la liaison entre l'oeil du Dalek et sa tige »
3. « la pointe de l'Epée de Damoclès »
4. « l'oeil du dino » — le dinosaure n'a pas d'oeil, « sa composition aurait changé ».

## Approche

1. `sky.py` : parser + rendu PNG. Pour chaque constellation, **projection gnomonique
   (plan tangent) centrée sur la direction moyenne de ses étoiles**, vue de l'intérieur,
   avec les ids écrits à côté de chaque étoile. Les étoiles hors constellation visibles
   dans le cadre sont en rouge (utile pour l'étape 4).
2. Validation sur l'exemple Grande Ourse : le rendu montre la casserole, l'étoile 1 est
   bien au bout de la tige (réponse attendue 1). ✅
3. Pour chaque étape : rendu depuis la position courante, lecture de l'image, choix de
   l'étoile, contrôle par les segments (`solve.py` vérifie que les segments invoqués
   existent et que l'étoile est à ≤ 1000 al).
   - Étape 1 (origine) : yeux = triangles 517-534-489 et 563-608-326, pont 534-285-563 →
     **285** (c'est aussi l'étoile de Marvin la plus proche du milieu des deux yeux).
   - Étape 2 (depuis 285) : oeil = triangle 352-374-515 au bout de la tige 515-593 → **515**.
   - Étape 3 (depuis 515) : épée verticale, lame jusqu'à 493, pommeau 34-471-507 → **493**.
   - Étape 4 (depuis 493) : le dinosaure (68 étoiles, toutes reliées) n'a pas d'oeil. Une
     analyse du dataset montre que **l'étoile 108 est la seule des 612 qui n'appartient à
     aucune constellation**, et dans le rendu (miroir horizontal) elle tombe au milieu de
     la tête du dinosaure → **108**.

## Ce qui a marché

- **Projection gnomonique par constellation** plutôt que la carte θ/φ de l'énoncé : pas
  de distorsion, pas de coupure à ±180°, cadrage automatique sur la constellation.
- **Écrire les ids sur le rendu** : on lit directement la réponse sur l'image.
- **Analyse structurelle du dataset** (étoiles sans segment, étoiles hors de toute
  constellation, segments hors liste) : elle a donné l'étape 4 en une commande. Le
  « piège narratif » (composition changée) pointait vers une anomalie des données.
- **Planche de 8 orientations** (4 rotations × miroir) : l'orientation sur le ciel est
  arbitraire ; le dinosaure n'est lisible qu'en miroir.

## Ce qui n'a pas marché / pièges

- Premier rendu depuis une étoile : **NaN** car l'étoile où se trouve le vaisseau est à
  distance 0. Il faut l'exclure de la projection.
- Le rendu du dinosaure en orientation par défaut est illisible ; ne pas conclure sans
  essayer rotations et miroir.
- Des étoiles d'autres constellations se projettent par-dessus (les étoiles de l'épée
  tombent dans le dinosaure vu depuis 493) : les distinguer par couleur.
- Les étoiles sans segment du Dalek (24) et de R2D2 (3) sont des décorations, pas des
  anomalies : seule « hors de toute constellation » était le signal.

## Vérifications faites

- Exemple Grande Ourse : étoile 1 = bout de la tige.
- `solve.py` vérifie : segments invoqués présents, étoile choisie dans la constellation
  (étapes 1-3), distance ≤ 1000 al depuis la position courante (678, 650, 836, 730 al),
  constellation visible, et que 108 est bien l'unique étoile orpheline.
- Étape 1 : vérification numérique (étoile la plus proche du milieu des deux yeux = 285).

## Temps / difficulté réelle

~30 min avec l'outil de rendu. Difficulté réelle : moyenne une fois l'outil écrit ; sans
visualisation, impossible.

## Leçons pour le jour J

- Challenge « Visuel » → **rendre en PNG et regarder** (Read sur l'image), ids annotés.
- Pour un ciel / une sphère : projection gnomonique centrée sur l'objet ; tester les
  8 orientations (rotations + miroir) avant d'interpréter une forme.
- Quand le texte dit « il manque quelque chose » / « ça a changé », chercher
  **l'anomalie dans les données** (élément orphelin, doublon, hors liste) avant tout.
- `sky.py` est réutilisable tel quel pour tout problème de points 3D projetés.
