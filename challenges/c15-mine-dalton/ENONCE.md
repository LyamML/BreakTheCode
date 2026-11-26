# La mine des Dalton

- id CTFd: 15
- Points actuels: 39
- Type: bonusmalus
- Essais max: 0 (0 = illimité, mais malus possible sur mauvaise réponse)
- Indices:
- hint 16 « Relire le plan » coût 3 (NON débloqué)
- hint 17 « Méthode » coût 9 (NON débloqué)

## Énoncé (brut, HTML inclus)

La nouvelle est arrivée par le dernier train en provenance de
Coffeyville : les Dalton ont encore frappé, cette fois sur la
concession minière de Placer Gulch. Ils sont repartis avec tout l'or
qu'ils pouvaient porter — et ont laissé derrière eux quelque chose de
bien plus inquiétant que des coffres vides.

Le contremaître de la mine, un dénommé Hollis, a été le premier à
redescendre dans les galeries. C'est lui qui a trouvé les bâtons de
dynamite, disposés un peu partout, chacun avec son propre mécanisme
d'horlogerie. Pas assez pour tout faire sauter d'un coup. Juste assez
pour condamner la mine, galerie après galerie, le temps que la
poussière retombe sur le passage des Dalton.

« Il reste de l'or là-dedans, » a-t-il dit aux hommes rassemblés à
l'entrée. « Et je ne suis pas décidé à le laisser aux rats. ».

Quelqu'un lui a tendu un plan de la mine, avec l'emplacement de
chaque bâton marqué à l'encre encore fraîche. Hollis l'a étudié un
long moment sans rien dire.

« Je ne pourrai pas tout récupérer, » a-t-il fini par admettre.
« Mais je peux calculer combien. Et c'est déjà plus que ce que les
Dalton s'attendent à me laisser. ».

Il a plié le plan, l'a glissé dans sa veste, et s'est dirigé vers
l'entrée du puits.

---

**Les règles du plan retrouvé par Hollis :**

La mine est une grille. `#` est un mur, `.` une galerie libre, `E`
l'entrée, `X` la sortie, et les chiffres `1` à `9` des pépites d'or
numérotées. Hollis avance d'une case par seconde, jamais en diagonale,
et ne s'arrête jamais — ramasser l'or ne lui coûte aucun temps.

Chaque bâton de dynamite explose à un instant `t` marqué sur le plan :
à cet instant, sa case ET ses voisines directes (haut/bas/gauche/
droite) s'effondrent définitivement. Une case reste franchissable tant
que le temps reste strictement inférieur à `t`.

Le flag est le nombre maximal de pépites que Hollis peut ramasser en
ressortant vivant de la mine.

