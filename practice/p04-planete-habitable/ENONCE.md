# A la recherche d'une nouvelle planète habitable

Après avoir reçu et déchiffré le message de l’exercice : « Le message codé », vous devez rejoindre la planète habitée en suivant les instructions données dans le message.

Pour cela, vous avez la carte de la galaxie au format JSON sous forme de vecteur. Vous devez trouver le plus court chemin en respectant les consignes de l’équipe d’exploration vers la nouvelle planète habitable.

**Input**

Fichier galaxie.json : La carte de la galaxie au format JSON

**Output**

La liste des planètes traversées pour rejoindre la planète habitable

**Exemple**

Input :

Une galaxie de 3 planètes :

```json
{
"Lyraosus": {
    "Thalis": 569
},
"Zenoisium": {
    "Terre": 859,
    "Thalis": 222
},
"Thalis": {
    "Lyraosus": 569,
    "Zenoisium": 222
},
"Terre": {
    "Zenoisium": 859
}
}
```

Output :

Si la planète cible est Thalis et qu’il n’y a aucune contrainte, on aura :
``Terre,Zenoisium,Thalis``