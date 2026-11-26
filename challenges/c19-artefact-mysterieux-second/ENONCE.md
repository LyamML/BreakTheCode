# L'artefact mystérieux - Second message

- id CTFd: 19
- Points actuels: 17
- Type: bonusmalus
- Essais max: 0 (malus possible)
- Indices: hint 18 « Avis d'Archibald » coût 3 (NON débloqué)
- Débloqué par c26 (Premier message, flag validé : GLOOSCAP)

## Énoncé

Ayant bruyamment exulté votre joie d'avoir déchiffré le premier message, l'artefact tressaille et un second mélange de symboles apparaît :

```txt
['L', 'f', '%', '?', '1', 'D', 'M', '"', 'F', 'J']
['a', 'l', '6', 'B', 'G', ';', 'K', '"', '+', 'b']
['K', 'a', ')', 'm', "'", 'Y', '6', '=', '&', 'v']
['k', '-', '@', '`', 'a', 'H', '9', 'a', '\\', 'N']
['Y', '$', 'P', '|', '3', '=', 'V', '3', '0', 'u']
['i', 'T', 'U', '}', '6', '?', '}', 's', '*', 'X']
['&', '(', '7', 'l', '*', 'A', 'S', ':', 'S', 'w']
['V', 'I', 'V', 'V', 'I', 'X', 'W', 'T', 'Q', '[']
['y', "'", 'd', '8', 'N', 'R', '!', 'M', ':', '!']
['3', 'K', 's', 'k', '^', '-', '+', 'R', 'p', 'S']
```

(Le `'\\'` est une repr Python : un seul antislash.)

## Contexte du premier message (c26)

Un totem amérindien ; un expert « Archibald V.G. » dit qu'activé par les rayons lunaires il reflète des symboles rangés ; des messages cachés horizontalement ou verticalement, « pas toujours écrits en langage humain ». Le premier message était une grille 10x10 de cellules encodées en ASCII décimal sur 3 couches ; une fois décodée, la colonne 5 lue de haut en bas donnait KGLOOSCAPF → flag GLOOSCAP (validé).
