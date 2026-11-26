---
id: p09
title: Les rebelles continuent leur offensive
ctfd_id: 28
points: 80
tags: [Optimisation, Graphes]
status: solved
answer: answer.txt (score 154)
confidence: haute
---

# p09 — Les rebelles continuent leur offensive

## Réponse

**Score 154**, 11 sauts, poids max atteint 99/100 (fichier complet : [answer.txt](answer.txt)).

- `solve.py` : ILP exact (`scipy.optimize.milp`, HiGHS, `mip_rel_gap=0`) → statut
  **Optimal**, 154, en ~5 s.
- **Borne supérieure** : même problème sans contrainte carburant (DP de p06 sur ce
  graphe) = **156**. Le carburant ne coûte donc que 2 points : on est au plus près.
- `check_dp.py` : 2e méthode exacte, indépendante de l'ILP (DP sur l'inventaire) →
  **abandonnée** : après ~25 min et 5,7 Go de RAM elle n'avait pas fini (explosion
  exponentielle des inventaires). L'optimalité repose sur l'ILP (HiGHS, écart 0) et
  la borne 156. Leçon : toujours mettre un timeout à une vérification exhaustive.

## Interprétation de l'énoncé

- Graphe orienté, **DAG** (vérifié), 27 planètes utiles sur 100, **159 chemins**
  Xevora → Crystar. Pas de revisite possible.
- Poids max **100** : pas redit dans l'énoncé de p09, repris de p06 (« la contrainte
  de poids de votre vaisseau »). À confirmer le jour J si l'énoncé est similaire.
- Le poids porté = armes + carburants **pas encore brûlés**. Contrôlé sur chaque
  planète après ramassage (c'est le moment où on est le plus lourd).
- Un carburant ramassé sur la planète courante peut payer le trajet suivant (le
  format de l'exemple le fait : `Vénus,1,3;5;7` puis `Mercure,5,N/A`).
- Valeur brûlée ≥ coût, l'excédent est perdu.
- Carburant `1` (valeur infinie, poids 0) : forcément utilisé au 1er saut (rien à
  ramasser sur Xevora). Aucun objet n'a l'id 1 dans `Items`.
- Score = armes **en soute à l'arrivée** (les carburants ne comptent pas).
- Format : en-tête de l'exemple, `N/A` si rien à ramasser, dernière ligne
  `Crystar,<carburants>` sans 3e champ.

## Approche

ILP (voir le docstring de `solve.py`) :
- `x_e` arête prise (flot unitaire Xevora → Crystar), `y_i` arme prise,
  `z_{i,e}` carburant `i` ramassé puis **brûlé sur l'arête `e`**, autorisé seulement
  si `e` part de la planète de `i` ou d'une planète en aval.
- Coût : `Σ val_i · z_{i,e} ≥ cost_e · x_e`.
- Poids à la planète `v` : armes en amont + carburants ramassés en amont et brûlés sur
  une arête au départ de `v` ou en aval ≤ 100, activé par big-M si `v` est sur le chemin.
- Ramasser un carburant sans jamais le brûler n'apporte rien : pas de variable pour ça.

Taille : quelques milliers de variables binaires, résolu en ~5 s.

## Ce qui a marché

- Modéliser le carburant par **« quel trajet il paie »** (affectation) plutôt que de
  suivre un inventaire : le poids à chaque étape devient une somme linéaire.
- Restreindre aux planètes utiles et aux couples (carburant, arête en aval) : modèle petit.
- Borne sup « sans carburant » en 10 lignes (réutilise la DP de p06) : ça prouve qu'on
  ne peut pas gagner plus de 2 points.

## Ce qui n'a pas marché / pièges

- PuLP 4 : API cassée et plus de CBC embarqué (voir p06). → `scipy.optimize.milp`.
- La DP « par inventaire » (`check_dp.py`) est **beaucoup plus lente** que l'ILP
  (énumération 2^k objets × sous-ensembles brûlés). Bonne vérification, mauvais
  outil principal sous chrono.

## Vérifications faites

- `python -I validate.py answer.txt` → VALIDE, score 154 (simulation pas à pas :
  inventaire, coûts, poids ≤ 100 après chaque ramassage, objets sur la bonne planète).
- Borne supérieure 156.
- `python -I check_dp.py` → voir Réponse.

## Temps / difficulté réelle

~25 min (modèle 10 min, validateur 5 min, vérifications). Difficulté réelle : moyenne
si on pense ILP tout de suite, difficile en DP pure.

## Leçons pour le jour J

- **Optimisation combinatoire avec plusieurs contraintes couplées → ILP direct**
  (`scipy.optimize.milp`), pas de DP maison. Une DP n'est rentable que si l'état est
  petit (p06 : nœud × capacité).
- Ressource consommable (carburant, énergie) : variable **« ressource i utilisée à
  l'étape e »** plutôt que de suivre un inventaire.
- Toujours une **borne supérieure** par relaxation (enlever une contrainte) : si elle
  est proche du score obtenu, on peut soumettre en confiance.
- Écrire **validate.py en simulant les règles à la lettre**, séparé du solveur : il
  attrape les erreurs de modélisation que le solveur ne verra jamais.
