---
owner: kevin
status: submitted
points: "39"
tags: ""
answer: "4"
confidence: haute
---

# Notes

## Réponse

Flag à soumettre (copier-coller exact) :

```
4
```

Pépites ramassées : 2, 4, 7, 8 (chemin de 148 s, rejoué dans `validate.py`).

## Interprétation de l'énoncé

- `mine_des_daltons.png` contient les règles et l'exemple (5x7, bâton t=12, sortie 1). `salle_D.png` contient le
  jeu de données réel (19x19, 9 pépites, 30 bâtons). La première image n'a pas de zone « D » :
  le « D » est le nombre de bâtons dans le format d'entrée (`R C K D`).
- Départ en E à t=0, une case par seconde, jamais immobile (allers-retours permis).
  Une case est franchissable à l'instant s si s < min(t des bâtons sur la case ou ses 4 voisins).
- L'exemple fixe le temps. Avec t0=0, la case (0,3) est foulée pour la dernière fois à
  l'instant 11, ce que dit le texte de l'image. Avec un réglage à 11, le détour est mortel (sortie 0).
  `solve.py` vérifie ces deux assertions.
- Trois cases portent une pépite et un bâton : 3 (t94), 8 (t30), 6 (t112).
- Arriver en X termine le trajet. La variante « on peut repasser par X » donne la même réponse, 4.

## Approche

Transcription : couleurs échantillonnées par Pillow au centre de chaque case, temps lus
sur un agrandissement (planche des 30 vignettes). BFS par couches de temps sur
(case, masque de pépites), arrêt quand les couches deviennent périodiques après le
dernier effondrement (t=186).

## Vérifications

- `validate.py` fait quatre contrôles : (1) la transcription est comparée aux pixels pour les 361 cases et les 30
  bordures de bâton ; (2) un deuxième solveur (DFS mémoïsée sur (case, t, masque), horizon
  400 s) trouve 4 ; (3) le chemin optimal est reconstruit et rejoué ; (4) les variantes sont calculées.
- Optimalité prouvée : la recherche couvre tout l'espace d'états.

## Variantes / sensibilité

| Hypothèse | Résultat |
|---|---|
| **retenue** (strict <, rayon 4-voisins, départ t=0) | **4** |
| non strict (≤) | 6 |
| explosion sans les voisins | 8 |
| départ t=1 | 3 |
| bâton (1,8) lu 49 au lieu de 48 | 6 |
| bâton (10,6) lu 29 au lieu de 30 | 3 |

Seuls les minuteurs t48 et t30 changent la réponse à ±1. Relus sur l'agrandissement, ils sont nets.
L'exemple ou l'énoncé contredit chacune des variantes d'interprétation.

## Ce qui n'a pas marché / pièges

- Aucune alerte du scanner, aucune consigne cachée.
- Piège possible : prendre l'exemple de l'image principale (sortie 1) au lieu de salle_D.
- Des pépites sont posées sur des cases piégées : ne pas les rater dans la transcription.
