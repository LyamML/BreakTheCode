---
owner: kevin
status: submitted
points: "47"
tags: ""
answer: "GLOOSCAP"
confidence: haute
---

# Notes

## Réponse

Flag à soumettre (copier-coller exact) :

```
GLOOSCAP
```

Variantes de format (si refus, ne pas resoumettre sans l'humain) : `Glooscap`, `glooscap`
(casse ; le message dans la grille est en majuscules), orthographes alternatives du
personnage (Gluskap, Glooskap) : NON, la grille écrit exactement GLOOSCAP.

## Interprétation de l'énoncé

- Pas de fichier : grille 10x10 dans ENONCE.md. Type `bonusmalus` : malus si mauvaise réponse.
- Format de flag non précisé → le message trouvé tel quel.
- Scanner : 0 alerte. Aucune consigne cachée dans l'énoncé.
- « pas toujours écrits en langage humain » = la grille est encodée en couches (codes ASCII).

## Approche

Chaque cellule : décodage en 3 couches.
1. `'53-53--52-57'` : `--` sépare des groupes, `-` des codes ASCII décimaux → `'5549'`.
2. `'5549'` : paires de chiffres = codes ASCII → `'71'`.
3. `'71'` → `chr(71)` = `G`.

Grille finale (lignes) :

```
M 5 j C U K S } 0 :
P @ A 2 = G K P & O
" g Y j = L R 7 H J
% P " Q V O 4 \ h l
F x J E P O 5 \ Y ~
^ ~ d M F S ] 1 % _
n y y $ T C 4 # v v
, v " D   A 5 \ { v
i R d 3 [ P J k q J
] b l ~ X F : u [ >
```

Colonne 5 (0-indexée), de haut en bas : `K G L O O S C A P F` → **GLOOSCAP** (lignes 1 à 8),
héros/esprit légendaire des peuples Wabanaki/Mi'kmaq : cohérent avec « campement
amérindien » et « esprits ancestraux ».

## Ce qui a marché

Décodage direct + lecture des colonnes.

## Ce qui n'a pas marché / pièges

- Recherche de mots dictionnaire (8 directions, sens inverse), base64, ROT47 et décalages
  ASCII sur toutes les lignes/colonnes/diagonales : rien d'autre de significatif
  (`PROP`, `SCAP` = bruit/inclus).
- Colonne 6 `SKR45]45J:` non interprétée : peut-être le support d'un « second message »
  (challenge suivant de la série) — à signaler si un « deuxième message » apparaît.

## Vérifications faites

- `solve.py` (décodage couche par couche) et `validate.py` (décodage générique
  indépendant, codes 2/3 chiffres, recherche dans les 8 directions) donnent la même
  grille ; GLOOSCAP est la seule suite de lettres formant un mot réel.
- Contrôle manuel : R1C5 `53-53--52-57` → `5549` → `71` → `G` ; R8C5 `53-54--52-56` →
  `5648` → `80` → `P`.

## Journal

| Heure | Action | Résultat |
|---|---|---|
| J | Décodage + recherche | GLOOSCAP |
