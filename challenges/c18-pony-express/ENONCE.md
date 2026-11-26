# Pony Express

- id CTFd: 18
- Points actuels: 23
- Type: bonusmalus
- Essais max: 0 (0 = illimité, mais malus possible sur mauvaise réponse)
- Indices:
- aucun

## Énoncé (brut, HTML inclus)

Le chef des messagers du Pony Express souhaite améliorer le service postal du Far West. Pour cela, il vous confie la carte des pistes empruntées par ses cavaliers.

Chaque piste est à sens unique: un cavalier peut l'emprunter uniquement dans le sens indiqué sur la carte. Le nombre inscrit sur chaque piste correspond à la durée en minutes nécessaire pour la parcourir.

Votre mission est d'aider le chef du Pony Express à établir des zones postales pour son réseau.

<br>
Une zone postale est un groupe de villages liés entre eux:

- depuis n'importe quel village de la zone, on peut rejoindre tous les autres,<br>
- et pour chaque trajet, un trajet de retour existe aussi (pas forcément par la même piste).

Si deux zones partagent un ou plusieurs villages, elles font partie de la même zone postale.

La longueur d'une zone postale est définie comme le plus grand aller-retour minimal entre deux villages de cette zone:

max_{u,v} (plus_court_chemin(u->v) + plus_court_chemin(v->u))

Une zone est valide si cette longueur est inférieure ou égale a 8 jours.

---
Les données d'entrée sont sous la forme:
```
[Nombre de villages]
---
[ID village de depart],[ID village d'arrivée],[Temps de trajet en minutes]
...
```

---
La réponse attendue est au format:
[nombre total de zones valides];[longueur zone valide 1];[longueur zone valide 2];...

Les longueurs doivent etre triées dans l'ordre croissant. Exemple: `3;50;200;1400`

Petit exemple complet:

Avec le fichier d'entrée:
```
7
---
1,2,100
2,1,100
2,3,120
3,2,120
4,5,6000
5,4,6000
6,7,200
7,6,200
```
La sortie attendue est:
2;400;440

