---
owner: kevin
status: failed
points: "17"
tags: "bonusmalus, chaîne c26"
answer: "ANNAPOLIS"
confidence: haute
---

# Notes

## Réponse

Flag à soumettre (copier-coller exact) :

```
ANNAPOLIS
```

## Interprétation

- Entrée : grille 10x10 de caractères ASCII imprimables (dans ENONCE.md, pas de fichier data/).
- Contexte c26 : message caché « horizontalement ou verticalement », « pas toujours en
  langage humain ». Le 1er message donnait la colonne 5 = `KGLOOSCAPF`, flag `GLOOSCAP`
  (un caractère de bruit à chaque bout).
- Flag attendu : le mot caché, en majuscules comme le précédent.
- Scan de pièges : aucune consigne cachée dans l'énoncé (pas de HTML/texte invisible).
  Hint « Avis d'Archibald » (3 pts) non débloqué, inutile.

## Solution

Décalage de César sur les 95 ASCII imprimables (32..126), testé pour les 95 décalages,
sur les 10 lignes et 10 colonnes, à l'endroit et en miroir (80 lectures x 95).
Une seule lecture contient un mot : **ligne 7 (8e ligne), décalage −8** :

`VIVVIXWTQ[` → `NANNAPOLIS` → bruit `N` + **ANNAPOLIS**.

Le `[` → `S` montre que le décalage porte sur l'ASCII (pas un ROT sur 26 lettres).
Annapolis (Nouvelle-Écosse, vallée d'Annapolis) est le territoire mi'kmaq/wabanaki de
la légende de Glooscap : cohérent avec le 1er message.

## Vérifications

- Recherche exhaustive : seule la ligne 7 produit ≥ 8 majuscules consécutives, et
  seul le décalage −8 donne un mot. Toute la grille décalée de −8 reste du bruit sauf
  la ligne 7 (message unique).
- Format : même convention que c26 (bruit retiré, majuscules).

## Variantes

1. `ANNAPOLIS` (retenue) — bruit au 1er caractère, comme K/F autour de GLOOSCAP.
2. `NANNAPOLIS` — ligne brute complète ; peu probable (pas un mot).

## Pièges / leçons

- Les pistes Vigenère « V.G. », XOR avec la grille 1, base64 étaient des fausses pistes :
  un simple César ASCII ligne par ligne suffit. Toujours brute-forcer les 95 décalages
  sur chaque ligne/colonne avant les hypothèses complexes.
