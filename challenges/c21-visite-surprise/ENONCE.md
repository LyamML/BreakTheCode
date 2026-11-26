# Visite surprise

- id CTFd: 21
- Points actuels: 17
- Type: bonusmalus
- Essais max: 0 (0 = illimité, mais malus possible sur mauvaise réponse)
- Indices:
- aucun

## Énoncé (brut, HTML inclus)

# Visite surprise

Un jeune Indien souhaite quitter Jiménez pour rejoindre un ami qui vit à El Paso.

Pour préparer son voyage, il décide de représenter le pays sur une carte. Il divise cette carte en différentes **zones**, chacune correspondant à la distance qu'il est capable de parcourir en une journée.

Chaque jour, il peut donc se déplacer vers le **nord, le sud, l'est ou l'ouest**, et ainsi parcourir une zone supplémentaire dans la direction choisie.

Mais le voyage est loin d'être sans danger.

### Les étapes du voyage

Sur son chemin, le jeune homme doit obligatoirement s'arrêter dans plusieurs **lieux importants**.

Dans certains d'entre eux, il doit récupérer des vivres indispensables à la poursuite de son voyage. Dans d'autres, il doit retrouver des amis ou des membres de sa famille.

Il doit impérativement se rendre dans **chacun de ces lieux**, mais il est libre de choisir l'ordre dans lequel il les visitera.

Il pourra rejoindre son ami uniquement après avoir rendu visite à tous ceux qu'il devait rencontrer et récupéré toutes les ressources nécessaires à son périple.

### Les bandits

Le pays est également parcouru par plusieurs groupes de bandits.

Chaque groupe possède son propre trajet et son propre rythme de déplacement. Certains groupes avancent chaque jour, tandis que d'autres ne se déplacent que tous les trois jours, cinq jours, ou selon toute autre périodicité.

Le comportement de chaque groupe est entièrement déterminé et peut donc être prévu par le voyageur.

Lorsqu'un groupe de bandits se trouve dans une zone, celle-ci devient **dangereuse** et le voyageur ne peut pas y terminer sa journée.

Notre jeune indien obtient d'une éclaireur les habitudes des bandits. Ils sont actuellement stationnés à Camp Grant (old site). Le premier groupe de bandits se déplace vers l'est tous les jours. Le second groupe de bandit se déplace vers l'est tous les trois jours. Le dernier groupe de bandits se déplace vers l'est tous les cinq jours. Quand ils atteignent Mesilla, les bandits font demi-tour et se déplace vers l'ouest au même rythme.

### Les événements

Le pays est également soumis à divers événements qui peuvent rendre certaines zones temporairement impraticables.

Une route peut par exemple être détruite par une catastrophe naturelle, une rivière peut sortir de son lit ou une région peut devenir trop dangereuse pour être traversée.

Ces événements ont une durée limitée : une zone peut ainsi être impraticable pendant quelques jours avant de redevenir accessible.

### Le déroulement d'une journée

Le voyage est organisé jour après jour.

Au début de chaque journée, le voyageur connaît la situation du pays ainsi que la position des différents groupes de bandits.

Il choisit alors la direction dans laquelle il souhaite se déplacer et parcourt une zone pendant la journée.

Il ne peut cependant effectuer ce déplacement que si **la zone dans laquelle il souhaite arriver est praticable au début et à la fin de la journée**.

Ainsi, s'il sait qu'un groupe de bandits occupera cette zone à la fin de la journée, il ne pourra pas s'y rendre, même si elle était parfaitement sûre au moment de son départ.

De même, il ne pourra pas partir vers une zone qui est déjà dangereuse ou impraticable au début de la journée.

À la fin de chaque journée, les événements évoluent et les différents groupes de bandits se déplacent conformément à leurs règles.

### Objectif

À partir des informations concernant la carte, le village de départ, l'ami à rejoindre, les différents lieux à visiter, les groupes de bandits et les événements pouvant affecter le pays, **déterminer le nombre minimal de jours nécessaires pour que le jeune homme rejoigne son ami après avoir visité tous les lieux qui lui sont imposés.**

Si aucun itinéraire ne permet de réaliser ce voyage, il faudra l'indiquer en saisissant 0.

