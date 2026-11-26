# Tournée des saloons

- id CTFd: 20
- Points actuels: 60
- Type: manual_verification
- Essais max: 0 (0 = illimité, mais malus possible sur mauvaise réponse)
- Indices:
- aucun

## Énoncé (brut, HTML inclus)

Chaque année, les aventurier(e)s du territoire s'affrontent pour un seul titre : celui ou celle qui se sera arrêté(e)
dans le plus de saloons distincts durant la nuit (5 heures maximum, temps de trajet et arrêts compris).

La légende commence et se termine toujours au même endroit, au saloon dont la réputation n'est plus à faire,
celui qui attire les plus grandes gueules et les pires bagarreurs,
celui dont la somme des pistes entrantes et sortantes est la plus grande.

Chaque piste n'est taillée dans le canyon que dans un sens, impossible de rebrousser chemin sur une même piste.
On peut aussi traverser un saloon sans s'y arrêter, sans perdre de temps à y boire un verre,
mais ses portes doivent être ouvertes dans les deux cas : un saloon fermé bloque le passage.

Les tenanciers gardent des horaires à leur convenance,
si bien qu'un saloon grand ouvert à minuit peut fermer boutique avant l'aube.

Chaque aventurier(e) choisit librement son horaire de départ, dans les limites des horaires d'ouverture
et de fermeture du saloon de départ, et doit impérativement y être de retour avant sa fermeture.

À la fin, un seul nom restera : celui ou celle qui aura osé la tournée avec le plus d'arrêts dans les saloons
en minimisant le temps de son circuit.

## Saloons

Chaque tenancier a couché sur le papier ses horaires d'ouverture et de fermeture pour l'occasion,
ainsi que le temps que vous devrez y rester pour consommer, au risque de se faire bannir les années suivantes de celui-ci.

Cette liste des saloons est disponible dans le fichier `saloons.csv`.

```csv
name,opening_hour,closing_hour,time_spent
Wild Saloon,00:15,01:45,10m0s
Crooked Rattlesnake,23:45,02:45,40m0s
Rattling Tavern,21:15,22:45,50m0s
Drunken Barrel,19:45,01:30,40m0s
```

## Carte

Les arpenteurs et arpentrices du territoire ont relevé chaque piste praticable entre les saloons,
ainsi que le temps nécessaire pour la parcourir.

Cette carte des chemins est disponible dans le fichier `map.csv`.

```csv
trail,travel_duration,starting_point,destination
Narrow Ridge,5m2s,Wild Saloon,Crooked Rattlesnake
Twisting Gulch,2m5s,Wild Saloon,Rattling Tavern
Endless Byway,1m17s,Crooked Rattlesnake,Drunken Barrel
```

## Rapport de tournée

Pour prétendre au titre, chaque aventurier(e) doit conter sa tournée aux anciens du territoire :
les saloons visités, dans l'ordre de passage, ainsi que la piste empruntée pour passer de l'un à l'autre.

Le nom gravé dans la légende ne sera connu qu'une fois chaque tournée passée au crible : seules celles
respectant les contraintes du territoire seront jugées dignes d'être notées, puis départagées par leur score.

```json
{
  "starting_hour": "21:00",
  "circuit": [
    {
      "starting_saloon": "Wild Saloon",
      "destination_saloon": "Crooked Rattlesnake",
      "trail": "Narrow Ridge",
      "stopped": true
    },
    {
      "starting_saloon": "Crooked Rattlesnake",
      "destination_saloon": "Drunken Barrel",
      "trail": "Endless Byway",
      "stopped": false
    }
  ]
}
```

La colonne `stopped` indique si l'aventurier(e) s'est arrêté(e) au saloon `destination_saloon` de la ligne.

## Classement

Le nombre de points attribué pour la résolution de cet exercice dépendra de la qualité relative de votre solution en fonction de celles des autres équipes.
Il y aura donc un classement.

- 1er : 60 points
- 2ᵉ : 52 points
- 3ᵉ : 43 points
- 4ᵉ : 35 points
- 5ᵉ : 21 points
- du 6ᵉ au 14ᵉ : 15 points
- 15ᵉ et au-delà : 10 points

