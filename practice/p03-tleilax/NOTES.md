---
owner: lyam
status: solved
points: 27
tags: "Déchiffrage, Manipulation de tableau"
answer: "3458H2B"
confidence: haute
---

# p03 — C'est une oeuvre d'un grand maître Tleilax (27 pts)

## Réponse

```
3458H2B
```

Confiance : **haute**. Le texte est parfaitement lisible, et les 91 `X` de la grille
sont tous utilisés par les 7 glyphes : il ne reste aucun « signature » ni résidu.

## Interprétation de l'énoncé

- Le fichier fait 20 lignes × 100 colonnes. Il contient des espaces, des lettres
  `a`–`e` et des `X`.
- « I. Ajout d'une pigmentation de Alpha à Echo » : `a`…`e` (alphabet OTAN A→E)
  sont du **bruit**. Seuls les `X` forment le dessin.
- « II. De gauche à droite, descente de plus en plus » : la colonne j est décalée
  (cycliquement) vers le bas de j.
- « III. De haut en bas, glissement de plus en plus sur la droite » : la ligne i
  est décalée (cycliquement) vers la droite de i.
- Ce qui marche en pratique : **appliquer III puis II tels qu'ils sont écrits**
  (ligne i rotation à droite de i, puis colonne j rotation vers le bas de j).
  Les inscriptions décrivent donc la remise en forme, avec l'ordre inversé par
  rapport à la liste (et non le brouillage à inverser). Plutôt que de raisonner
  sur le sens, on a fait une recherche exhaustive.
- « Un tableau tleilax n'est jamais signé » : il n'y a rien à ignorer, tous les X
  appartiennent à la réponse (91/91 vérifié).
- Fichier nommé `R_Cest_une_oeuvre_de_masheikhs.txt` alors que l'énoncé annonce
  « B C'est une oeuvre… » : c'est sans importance.

## Approche

1. Garder seulement les `X`.
2. Recherche exhaustive : décalage de lignes `a·i` et de colonnes `b·j` pour
   a, b ∈ [-5, 5], dans les deux ordres (242 essais). Score = nombre de paires de
   `X` voisins (haut-bas et gauche-droite). Le texte forme des traits continus, donc
   le bon déchiffrement maximise ce score.
3. Le meilleur (score 84, contre 81 pour le suivant) donne un texte net en police
   4×5 : `3 4 5 8 H 2 B`.

## Ce qui a marché

- **Ne garder que le symbole « encre »** : avant ça, rien n'est lisible.
- **Recherche exhaustive des paramètres + score de lisibilité** au lieu de deviner
  le sens des décalages. Mes 2 premières tentatives « raisonnées » (inverser chaque
  opération dans l'ordre inverse) donnaient un résultat illisible.
- Afficher le rendu en `#`/`.` et le lire à l'œil.

## Ce qui n'a pas marché / pièges

- Inverser naïvement le brouillage (sens opposé, ordre inverse) : résultat
  illisible. Le texte de l'énoncé est ambigu sur « brouillage » vs « remise en
  forme ».
- Ma transcription manuelle de la police (stockée colonne par colonne) avait 2
  glyphes faux (`??58H2B`) : vérifier la table de glyphes en relançant le script.
- Il n'y a pas d'exemple : seul le rendu visuel permet de valider.

## Vérifications faites

- Le score maximal est unique et se détache (84 contre 81, et le 2e candidat
  n'est pas lisible).
- Le nombre de X utilisés par les glyphes (13+9+14+16+12+14+13 = 91) est égal au
  nombre total de X de la grille.
- Relecture visuelle glyphe par glyphe.

## Temps / difficulté réelle

Environ 10 minutes, dont 5 perdues à raisonner sur le sens des décalages avant de
passer à la recherche exhaustive.

## Leçons pour le jour J

- Grille brouillée par permutations : **recherche exhaustive sur un petit espace de
  paramètres + score automatique** (adjacence, entropie, mots du dictionnaire).
  C'est plus rapide et plus sûr que de déduire le sens des opérations.
- Le bruit est souvent un sous-alphabet nommé de façon détournée (« Alpha à Echo »
  = a–e).
- Pour valider un résultat visuel, compter les pixels utilisés : si tout le signal
  est expliqué, rien n'est caché.
