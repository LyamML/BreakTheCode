---
id: p06
title: L'attaque surprise des rebelles
ctfd_id: 27
points: 53
tags: [Optimisation, Graphes]
status: solved
answer: answer.txt (score 242)
confidence: haute
---

# p06 — L'attaque surprise des rebelles

## Réponse

**Score 242**, poids 100/100, 16 sauts (fichier complet : [answer.txt](answer.txt)).

**Optimum prouvé** par deux méthodes indépendantes qui donnent le même résultat :
- `solve.py` : DP exacte (planète, poids exact) → 242
- `check_ilp.py` : ILP `scipy.optimize.milp` (HiGHS, gap 0) → 242, statut *Optimal*

Référence : l'`ExempleSolution` fourni est valide et vaut **97** (même chemin, moins
d'armes). On fait 2,5× mieux.

## Interprétation de l'énoncé

- Arêtes **orientées** (`departure,arrival`).
- Le graphe est un **DAG** (vérifié par DFS) : aucune planète ne peut être revisitée,
  la question « peut-on repasser » ne se pose pas.
- Rien à ramasser sur Nebulor (départ) ni Xevora (arrivée) : aucune arme n'y est.
  Le format ne permet d'ailleurs pas de ramasser au départ.
- Le poids ne fait qu'augmenter : vérifier le poids final ≤ 100 suffit.
- Format : on garde la ligne d'en-tête de l'exemple, `N/A` quand on ne prend rien, la
  dernière ligne est juste `Xevora`.
- Sur l'archive le score ne peut pas être validé : on ne sait pas si l'en-tête est
  attendu. Le jour J, copier exactement le format de l'exemple.

## Approche

1. Ne garder que les planètes **utiles** : atteignables depuis Nebulor ET qui
   mènent à Xevora (36 sur 100).
2. Ordre topologique. `best[v][w]` = valeur max en partant de `v` avec un poids exact `w`.
   Arrivée sur `v` = max des `best[u]` des prédécesseurs, puis knapsack 0/1 sur les
   armes de `v`.
3. Reconstruction : prédécesseur choisi par poids + tables du knapsack par planète.

Complexité O((V + E + objets) × 101) : instantané (< 0,5 s).

## Ce qui a marché

- Analyser la structure du graphe avant de coder (cycles ? doublons ? nœuds utiles ?).
  « DAG » ramène tout à une DP simple.
- Le validateur indépendant (`validate.py`) a aussi servi à noter l'exemple fourni : 97.
  Ça dit tout de suite qu'un score « correct » est bien plus haut.

## Ce qui n'a pas marché / pièges

- **PuLP 4.x a cassé son API** (`LpVariable(..., cat=)` n'existe plus, `LpStatus`
  disparu, variables via `prob.add_variable`). Perdu ~3 min. → utiliser
  **`scipy.optimize.milp`** (HiGHS inclus dans scipy, API stable), ou épingler `pulp<4`.
- PuLP 4 n'embarque plus CBC : `pip install highspy` nécessaire. Encore une raison
  de prendre scipy.

## Vérifications faites

- `python -I validate.py answer.txt` → VALIDE, score 242, poids 100.
- `python -I validate.py data/ExempleSolution` → VALIDE, score 97.
- `python -I check_ilp.py` → Optimal, 242.

## Temps / difficulté réelle

~10 min avec les vérifications. Difficulté réelle : facile dès qu'on voit que c'est un DAG.

## Leçons pour le jour J

- **Graphe + sac à dos sur un DAG** → DP sur (nœud, capacité) en ordre topologique.
  Patron dans `solve.py`, réutilisable tel quel.
- Toujours écrire **validate.py** (simulateur des règles + score) avant de soumettre :
  c'est la seule vérification possible quand la plateforme ne donne pas le score.
- Sur un challenge d'optimisation, **prouver l'optimum** par une 2e méthode (ILP vs DP)
  ou une borne supérieure. Le classement se fait au score.
