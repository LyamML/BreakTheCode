---
owner: kevin
status: submitted
points: "33"
tags: "simulation, bonusmalus"
answer: "226"
confidence: haute
---

# Notes

## Réponse

```
226
```

## Interprétation de l'énoncé

- Cible (59,86) ; 195 balles (ligne 1 = cible, séparateur espace). Flag = plus petite valeur de t (entier).
- Mise à jour : pos += v, puis si coordonnée <0 ou >99, la vitesse de cet axe s'inverse (la position hors salle est conservée). Les 2 exemples de l'énoncé sont reproduits par assert dans solve.py.
- Règle "aucun tir direct" : variante "toutes balles" et variante "balle ayant déjà rebondi" donnent la même réponse : 226 (balle d'indice 160, 0-based parmi les tireurs), qui a rebondi. Aucune balle sur la cible à t=0.
- Scanner de pièges : 0 alerte.

## Approche

Simulation directe de 200000 pas (solve.py).

## Ce qui a marché

Simulation pure Python + vérification numpy vectorisée indépendante (verify_numpy.py) : même t=226, même balle, rebondie.

## Ce qui n'a pas marché / pièges

np.loadtxt échoue (1re ligne à 2 colonnes). Le dossier du challenge n'était pas dans le worktree (non commité sur main) : copié depuis le checkout principal.

## Vérifications faites

Exemples énoncé, 2 implémentations, deux variantes de la règle "tir direct", t=0.
