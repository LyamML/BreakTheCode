---
owner: lyam
status: solved
points: 17
tags: "Très facile, Recherche dans une chaine de caractères"
answer: "shw"
confidence: haute
---

# p01 — Hal, c'est quoi le code ? (17 pts, « Très facile »)

## Réponse

```
shw
```

Confiance : **élevée**.

## Interprétation de l'énoncé

- « La chaîne qui se répète le plus » + « 3 lettres minuscules » → sous-chaîne de
  longueur exactement 3 la plus fréquente.
- Chevauchements : ça ne change rien ici (`shw` = 12 avec ou sans chevauchement).
- Casse : le fichier ne contient que des minuscules (50 000 caractères, pas
  d'espaces ni de ponctuation), donc pas de question.
- Égalités : aucune. `shw` = 12, les suivants (`xyo`, `prq`, `bcu`, `pzn`) = 11.
- L'exemple `ABCDEBCDABDC → BCD` est vérifié (BCD = 2, le reste = 1).

## Approche

`Counter` sur une fenêtre glissante de 3 caractères, puis `most_common`. O(n).

## Ce qui a marché

- Vérifier d'abord le format du fichier (longueur, caractères présents) avant de
  compter.
- Contrôle croisé avec un comptage sans chevauchement (`re.findall`), et
  vérification qu'il n'y a pas d'égalité en tête avant de répondre.

## Ce qui n'a pas marché / pièges

- Aucun échec. Le piège possible (« un seul essai ») est l'ambiguïté chevauchement
  / égalité : ici les deux définitions donnent la même réponse, mais il faut
  **le vérifier** avant de soumettre.

## Vérifications faites

Exemple de l'énoncé, deux définitions de comptage, absence d'égalité.

## Temps / difficulté réelle

Environ 2 minutes. Trivial.

## Leçons pour le jour J

- Sur un challenge facile qui limite les essais, calcule la réponse avec **chaque
  interprétation plausible** : si elles concordent, soumets ; sinon, signale-le à
  l'humain.
- Toujours afficher le top 5 avec les comptes, pas seulement le premier : ça
  montre tout de suite les égalités.
