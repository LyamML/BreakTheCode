# Concours de tir : feu !

- id CTFd: 24
- Points actuels: 33
- Type: bonusmalus
- Essais max: 0 (0 = illimité, mais malus possible sur mauvaise réponse)
- Indices:
- aucun

## Énoncé (brut, HTML inclus)

La ville de Fort Davis organise cette année son 127ème concours de tir. C'est un concours un peu particulier qui se tient en intérieur !

La salle du concours fait 100m sur 100m, et la cible est disposée quelque part dans la salle, loin des bords.

Ce qui rend ce concours très spécial, ce sont les murs de la salle ! Ils sont capables de renvoyer les projectiles avec très peu de dispersion d'énergie (c'est sans doute grace à leur revêtement en fibre de cactus ...).
D'ailleurs cette particularité a inspiré une règle de ce concours : aucun tir direct ne pourra être validé. Ca rend ce concours incroyablement difficile, et aussi très dangereux ...


Chaque participant au concours a droit à une unique balle qui pourra être tirée à partir de n'importe quelle position, dans n'importe quelle direction.

Chaque participant se positionne donc dans la salle à l'endroit de son choix et choisit une direction. Et au signal, tout le monde tire en même temps !

Il reste cependant un problème : comment déterminer le vainqueur ? Impossible de suivre à l'oeil nu près de 200 balles qui ricochent à l'infini sur les murs ...


L'organisation doit donc, à partir des informations dont elle dispose, reconstituer la trajectoire de chaque balle tirée et déterminer laquelle atteindra la cible en premier.


Ces informations sont stockées dans un fichier (dont nous nous sommes procurés une copie) au format suivant :


La première ligne contient les coordonnées (xc, yc) de la cible

Les lignes suivantes sont au format : x, y, vx, vy qui décrit la position initiale du tireur (x,y) ainsi que la vitesse selon l'axe x (vx) et selon l'axe y (vy)


On simule le champ de tir par intervalles de temps


A t=0 chaque balle se trouve en (x0, y0) (données du fichier en entrée)

A t=1 chaque balle se trouve en (x1, y1) = (x0+vx, y0+vy)

A t=2 chaque balle se trouve en (x2, y2) = (x1+vx, y1+vy)

...

A t=n chaque balle se trouve en (xn, yn) = (x[n-1]+vx, y[n-1]+vy)


La salle fait 100m par 100m, chaque position x ou y étant numérotée de 0 à 99.


La gestion des rebonds est aussi un peu spéciale : due à la grande épaisseur de fibres de cactus, les balles s'enfoncent dans les couches d'isolants avant de rebondir. Ainsi, lorsqu'une composante x ou y des coordonnées d'une balle est strictement inférieure à zéro (ou strictement supérieure à 99), la position "hors de la salle" est comptabilisée, et la vitesse associée vx ou vy s'inverse.


Par exemple, si une balle a comme position (x, y) = (0, 1) et comme vitesse (vx, vy) = (-1, 3) alors sa prochaine position à t+1 sera (x, y) = (0+(-1), 1+3) = (-1, 4).

Sa position en x étant négative, elle rebondit et sa vitesse vx s'inverse et passe de -1 à 1. Sa position en y étant comprise entre 0 et 99 la vitesse verticale vy ne change pas et reste à 3. Sa nouvelle vitesse à t+1 sera alors de (1, 3). Sa position à t+2 sera (0, 7)


Autre exemple : si la position d'une balle est (98, 99) et sa vitesse (3, 3) sa position à t+1 sera de (101, 102) et sa vitesse de (-3, -3) : les deux composantes x et y sont supérieurs à 99 et les composantes de la vitesse s'inversent. A t+2 sa position sera alors de (98, 99) et sa vitesse toujours de (-3,-3). A t+3 sa position sera de (95,96) et sa vitesse reste à (-3, -3)


En simulant l'ensemble des trajectoires, pouvez-vous déterminer la plus petite valeur de t pour laquelle une balle se trouve à la position exacte (xc, yc) de la cible ?

