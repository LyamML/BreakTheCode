---
owner: lyam
status: failed
points: "26"
tags: "bonusmalus"
answer: ""
confidence: ""
---

# c17 L'opérateur fantôme

## Réponse

Non trouvée pendant l'event (0 essai soumis, donc aucun malus).

## Solution (connue après coup)

Le challenge se résolvait **dans la salle** : il fallait chuchoter **« Où aura lieu la fête »**
à un organisateur **portant une étoile de shérif**. Il répondait par l'adresse, dont le nom de
rue était le flag (format `rue du saloon`, sans déterminant).

Lecture de l'énoncé a posteriori :
- « l'Opérateur Fantôme est toujours en ville » → c'est quelqu'un de présent dans la salle ;
- « ces messages passent sous les yeux de tout le monde » → la clé était visible ou dite sur place ;
- « le lieu du prochain sabotage » → dans le code des conspirateurs, le sabotage devient « la fête ».

Source exacte de la phrase non confirmée : à demander aux organisateurs.

## Ce qui n'a pas marché / pièges

- Image invisible de l'énoncé (`/files/media/indice_operateur_fantome.txt`) : appât, elle
  contient seulement « Bien essayé, mais c'est non… vous êtes sur la bonne voie ».
- ~40 min de fouille de la plateforme, sans résultat : HTML/JSON du challenge, en-têtes HTTP,
  flux `/events`, `/plugins/countdown/times`, notifications, robots.txt, CSS/JS du thème,
  logo/bannière/favicon, utilisateurs et équipes, DNS, stéganographie du texte (acrostiches,
  accents, caractères invisibles), fichiers des autres challenges, réseaux Wi-Fi.
- Demandes aux orgas sans la bonne phrase (« c'est vous l'opérateur fantôme », lampe torche,
  « Bandit », « Reno ») : refusées.

## Indices qu'on avait

- Normale Surchauffe l'a validé à 19:29 (UTC), 9 min après le début, sans dépendre d'un
  autre challenge : la clé était accessible tout de suite.
- Certains orgas portaient une étoile de shérif, d'autres non.

## Leçon

Énoncé sans fichier + « toujours en ville » / « sous les yeux de tout le monde » →
envoyer tout de suite un humain dans la salle, et parler aux orgas avec le vocabulaire
du récit. Voir `docs/PLAYBOOK.md`, section 6.
