---
owner: lyam
status: solved
points: 25
tags: "Physique, Filtrage CSV"
answer: "63.08712°N;67.860798°E"
confidence: moyenne
---

# p02 — Planet Landing (25 pts)

## Réponse

```
63.08712°N;67.860798°E
```

Confiance : **moyenne**. La réponse change selon la précision de G (voir
ci-dessous). Ordre d'essai recommandé si plusieurs essais sont permis :

| G utilisé | Points valides | Réponse |
|---|---|---|
| `6.674e-11` (valeur la plus courante dans le code) | 5 | `63.08712°N;67.860798°E` |
| `6.6743e-11` (CODATA 2018, `scipy.constants.G`) | 3 | `-1.051834°N;-124.251353°E` |
| `6.67e-11` (valeur des manuels de lycée français) | 10 | `70.123838°N;37.565791°E` |

## Interprétation de l'énoncé

Formules extraites des images base64 de l'énoncé (`formulas/f1.png`, `f2.png`) :
- Force : `F = G * m1 * m2 / d²`
- Freinage : `a_braking = v0² / (2 * h0)`
- Durée : **image manquante**. Le fichier « Durée de conoissage » est
  octet pour octet le même que celui de la force (même MD5). On en déduit
  `t = 2h / v0` (décélération uniforme de v0 jusqu'à 0, cohérent avec la formule
  de freinage).

Choix retenus :
- `d = R + h` : distance au centre de la planète au démarrage. Avec `d = h`, ou
  avec `GM = g·R²` (9.81 × 6 500 000²), **aucun** point n'est valide : ces
  pistes sont éliminées. La donnée `g = 9.81` sert donc de leurre.
- Unités : R = 6 500 km = 6.5e6 m, navette = 10 t = 1e4 kg, h en m.
- « vitesse maximale de freinage < 0.015 m/s » désigne en fait une
  **décélération** (m/s²) : on l'applique à `a`.
- Plusieurs points valides : on prend le **plus petit t** (« le plus rapidement
  possible »).
- Format : la latitude est donnée en `°N` et la longitude en `°E`, donc S et W
  deviennent négatifs. On garde le texte décimal tel qu'il est dans le CSV (aucun
  arrondi ni reformatage du float).

## Approche

Filtrer les 1000 lignes sur les 3 contraintes, trier par t, prendre le premier.

## Ce qui a marché

- Extraire les images base64 de l'énoncé et les regarder : les formules ne sont
  écrites nulle part ailleurs.
- Comparer les hash des images : c'est comme ça qu'on voit tout de suite que la
  formule de durée manque.
- Tester plusieurs modèles physiques. Celui qui laisse 0 candidat est faux :
  c'est un bon moyen d'en éliminer.

## Ce qui n'a pas marché / pièges

- **Sensibilité à G** : le meilleur point a F = 93 497,3 N avec G = 6.674e-11,
  mais F = 93 501,5 N avec G = 6.6743e-11. Il passe ou non selon le 4e chiffre
  de G. Les données sont générées pour tomber pile sur la limite.
- La donnée `g = 9.81` ne sert à rien (si on l'utilise, aucun point n'est
  valide).
- Les coordonnées contiennent des espaces (`82.97942° N`). Il faut parser le
  texte, pas le convertir en float puis le réécrire.

## Vérifications faites

- 3 modèles de distance/gravité testés, un seul donne des candidats.
- 5 valeurs de G testées : la réponse change, d'où le tableau ci-dessus.
- Le premier candidat respecte les 3 contraintes, avec une marge de 2,7 N sur F.

## Temps / difficulté réelle

Environ 10 minutes. Le calcul est facile, la difficulté est entièrement dans
l'ambiguïté des constantes.

## Leçons pour le jour J

- **Toujours faire un test de sensibilité aux constantes** (G, π, g, arrondis)
  quand une contrainte est un seuil. Si le gagnant change, présente le tableau à
  l'humain avant de soumettre.
- Les formules peuvent être des **images base64 dans l'énoncé** : les extraire
  avec une regex `data:image/png;base64,` puis les lire avec Read.
- Une donnée de l'énoncé peut être un **leurre** (ici g = 9.81).
- Toujours garder les chaînes numériques **telles qu'elles sont dans la source**
  pour la réponse.
