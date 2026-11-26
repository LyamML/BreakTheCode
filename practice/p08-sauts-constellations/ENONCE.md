# Sauts de Constellations

Vous êtes entré en possession d'un disque de données contenant, selon vos informations, des instructions pour atteindre une planète regorgeante de ressources.
Celle-ci sera cependant difficile à trouver : le disque date probablement de plusieurs siècles, et à l'époque les pilotes de vaisseaux spaciaux se fiaient à leur vue pour naviguer entre les étoiles.

Vous faites décrypter le disque par votre ordinateur de bord. Après examen, il s'avère que son contenu se rapproche à bien des égards d'une carte au trésor.
Il est fait mention de constellations, et des instructions ciblent certaines de leurs étoiles, entre lesquelles il faut naviguer pour arriver à la destination tant convoitée.

Heureusement, votre ordinateur possède une base de données des étoiles et des constellations de la galaxie.
Bonne nouvelle, les noms des constellations n'ont pas l'air d'avoir beaucoup changé depuis l'époque du disque de données, et de même pour la position des étoiles dans ce coin réduit de l'univers.

En parcourant le manuel d'utilisation de l'appareil, vous trouvez même comment activer le Plannificateur de Voyage Interstellaire.
Avec ceci, vous n'avez pas besoin de vous déplacer physiquement d'une étoile à l'autre; l'ordinateur vous simule la vision que vous auriez de la voûte céleste depuis une position donnée.

Cela vous sera absolument nécessaire pour visualiser les constellations, qui ne prennent forme que si l'observateur se tient à une position précise, vraisemblablement sur une planète habitable voisine d'une étoile.
Vous considérez que les étoiles à plus de 1000 années-lumière de l'observateur ne sont pas visibles à l'oeil nu, ce qui permettra d'éliminer les constellations trop lointaines de la simulation et ainsi d'éviter de surcharger votre vision.

Vous scrutez l'hologramme que projette l'ordinateur de bord ...

## Entrée

On définit un système de coordonnées cartésiennes (x, y, z) en 3 dimensions, une unité correspondant à une année-lumière.
Votre position de départ est en `(x, y, z) = (0, 0, 0)`, donc à l'origine de ce repère.

L'entrée est un fichier contenant les données sur les étoiles et les constellations de la galaxie, organisées en lignes. Le séparateur est l'espace.

- 1ère ligne : `i s c` avec `i` le nombre d'instructions, `s` le nombre d'étoiles, `c` le nombre de constellations (trois nombres entiers).
- Les `i` lignes suivantes : une ligne par instruction (texte). Suivez les dans l'ordre jusqu'à atteindre votre destination.
- Les `s` lignes suivantes : `x y z` la position de chaque étoile dans le repère cartésien (trois nombres flottants). La première étoile a pour identifiant `1`, la deuxième `2`, etc.
- Les `c` blocs suivants (des regroupements de lignes), un bloc par constellation :
    - 1ère ligne : le nom de la constellation (texte).
    - 2ème ligne : `n m` avec `n` le nombre d'étoiles composant la constellation, `m` le nombre de segments les reliant pour former la constellation (deux nombres entiers).
    - 3ème ligne : `s1 s2 s3 ... sn` la liste des identifiants des `n` étoiles composant la constellation (`n` nombres entiers).
    - Les `m` lignes suivantes : `s1 s2` le couple d'identifiants des étoiles à relier afin de tracer la constellation (deux nombres entiers). Certaines étoiles peuvent être reliées à aucune autre, ou à plusieurs autres.

## Sortie

La liste des identifiants des étoiles trouvées à partir de chaque instruction, dans l'ordre : des nombres entiers séparés par un espace. Par exemple `1 5 7 11` .

## Exemple

L'exemple suivant comporte une seule instruction, 7 étoiles et une seule constellation (avec 7 segments) : la Grande Ourse (aussi nommée la Grande Casserole).

Il peut être difficile de trouver la bonne étoile en reportant simplement les coordonnées dans un espace 3D.
Une des manières de procéder est de projeter les étoiles (et les relier en ligne droite) sur la voûte céleste, pour un observateur étant ici à l'origine (mais étant amené à se déplacer avec un jeu de données plus complet).

Voir 'exemple-cartesien.png' dans les fichiers joints.

La conversion des coordonnées cartésiennes `(x, y, z)` en coordonnées sphériques `(r, theta, phi)` permet de dessiner les constellations dans un repère 2D; nous pourrons alors considérer deux axes pour `theta` (ordonnées) et `phi` (abscisses).

Voir 'exemple-spherique.png' dans les fichiers joints.

Les repères sont quelque peu arbitraires, vous pouvez les adapter à votre convenance. Nous utilisons ici la convention physique, avec `r` la distance radiale, `theta` la colatitude (entre 0 et π) et `phi` la longitude (entre -π et π).
Le vaisseau étant situé à l'origine `(0, 0, 0)` du repère cartésien après recalcul des coordonnées en s'étant déplacé à chaque instruction, il s'agit alors de repères locaux au vaisseau.

Voir 'exemple-systeme_de_coordonnees.png' dans les fichiers joints.

Les coordonnées projetées des étoiles doivent paraître suffisamment proches pour pouvoir être regroupées dans la même constellation.
Ainsi une constellation ne se dispersera pas sur toute la voûte céleste. Attention cependant, elle peut être située dans **n'importe quelle direction**.

Le jeu de données de l'exemple est le suivant :

```txt
1 7 1
Rendez vous à l'étoile se trouvant au bout de la tige de la "grande casserole"
338.3905780631833 162.31002365250987 -62.047077044377254
402.4971009494973 102.3175855201485 -4.087226068962925
318.88794399138186 27.650917636487826 -3.825497544164767
218.27070344064245 -23.574831163873704 0.6182996869474933
416.8366006196655 -187.10978611626473 96.16801626973358
648.5897087242948 -329.82346692439285 11.260322027616029
424.6728358388315 -93.75744596729236 -50.37697336825302
Grande Ourse (Grande Casserole)
7 7
1 2 3 4 5 6 7
1 2
2 3
3 4
4 5
4 7
5 6
6 7
```

Il faut ici trouver l'étoile d'identifiant 1.
S'il y avait eu une seconde instruction, il aurait fallu déplacer le vaisseau aux coordonnées (cartésiennes) de cette étoile, puis recalculer les coordonnées et chercher la seconde étoile, et ainsi de suite.

Imaginons que le fichier d'entrée comporte 4 instructions, et que nous trouvons les étoiles 1, 5, 7 et 11 en suivant respectivement les instructions 1, 2, 3 et 4. La réponse attendue est alors `1 5 7 11`.

Note : les coordonnées des étoiles sont ici fictives, et d'ailleurs en réalité certaines sont en fait des galaxies, bien plus éloignées que dans cet exercice.