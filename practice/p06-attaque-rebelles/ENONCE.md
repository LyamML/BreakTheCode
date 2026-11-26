# L'attaque surprise des rebelles

Les rebelles attaquent une base de l'empire !
Une bataille a éclaté sur la planète Xevora à l'autre bout de la galaxie et votre armée a besoin de renforts.
Vous êtes un officier de l'empire et le commandant d'un croiseur interstellaire impérial.
Vous êtes actuellement sur la planète Nebulor à bord de votre vaisseau.
Vous recevez un message de l'empereur qui vous ordonne de rejoindre le front sur Xevora pour prêter main forte aux troupes impériales.
Il vous donne pour mission d'amener le plus de puissance de feu possible sur Xevora pour repousser l'offensive des rebelles.

Votre croiseur possède une carte stellaire de la région.
Elle se présente sous la forme d'une liste de couples de planètes.
Chaque couple représente un chemin entre une planète de départ et une planète d'arrivée.
Si vous vous trouvez sur la planète de départ, vous pouvez rejoindre la planète d'arrivée.
Voici un exemple :

departure,arrival
Terre,Mars → Il est possible de rejoindre Mars à partir de la Terre.
Mercure,Vénus → Il est possible de rejoindre Vénus à partir de Mercure.

Chaque planète abrite une station de l'empire dans laquelle vous trouverez des armes.
Chaque arme a une valeur (qui correspond à sa puissance de feu) et un poids.
Votre croiseur possède un inventaire qui détaille le contenu de ces stations.
Il se présente de la façon suivante :

id,planet,value,weight
28,Uranus,5,50 → L'arme d'identifiant 28 est disponible sur Uranus. Elle a une valeur de 5 et un poids de 50.
35,Uranus,18,100 → L'arme d'identifiant 35 est disponible sur Uranus. Elle a une valeur de 18 et un poids de 100.
37,Neptune,50,250 → L'arme d'identifiant 37 est disponible sur Neptune. Elle a une valeur de 50 et un poids de 250.

Votre croiseur peut supporter un poids maximal de 100.
On considère que le poids du vaisseau est de 0 dans la situation initiale.

Vous devez donc vous rendre sur Xevora en récupérant des armes sur les planètes par lesquelles vous passerez.
Votre objectif est de maximiser la puissance de feu des armes que vous allez ramasser.
Mais vous ne pouvez pas excéder la limite de poids de votre vaisseau.

Votre réponse à l'exercice doit être construite avec la liste des planètes que vous visitez.
Et pour chaque planète visitée, vous devez préciser la liste des armes que vous voulez prendre.
Merci de respecter le formalisme décrit dans l'exemple ci-dessous :

next planet,weapons to pick on next planet(separated by ;)
Vénus,3;5 → Vous allez jusqu'à Vénus (en partant de Nebulor) et vous prenez les armes d'identifiant 3 et 5 sur cette planète.
Mercure,N/A → Ensuite, vous allez jusqu'à Mercure et vous ne prenez aucune arme.
Mars,11 → Ensuite, vous allez jusqu'à Mars et vous prenez l'arme d'identifiant 11.
Xevora → Enfin, vous allez jusqu'à Xevora.

Pour que cette solution soit considérée comme valide, il faut qu'il existe des chemins entre Nebulor et Vénus, entre Vénus et Mercure, entre Mercure et Mars et entre Mars et Xevora.
Il faut aussi que les armes d'identifiant 3 et 5 soient sur Vénus et que l'arme d'identifiant 11 soit sur Mars.
Si la solution est valide, on peut déterminer son score.
On le calcule en additionnant les valeurs de toutes les armes que vous avez récupérées.
Dans l'exemple, le score correspond donc à la somme des valeurs des armes d'identifiant 3,5 et 11.

Vous devez donc fournir une solution valide avec le meilleur score possible.