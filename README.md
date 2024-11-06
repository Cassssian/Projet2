<b>
<p align="center">
<span style="font-size:3em">Jeu de la vie</span>
</p>

<p align="center">
<span style="font-size:2em">DucceschKleinsansklien Industries® & FluchInfo ®</span>
</p>
<b>
<br>

---

## Description
Ce projet implémente le célèbre "Jeu de la Vie" conçu par le mathématicien britannique John Conway en 1970. C'est un automate cellulaire qui simule l'évolution de cellules sur une grille en deux dimensions.

## Règles du jeu
1. Une cellule morte avec exactement trois voisines vivantes devient vivante.
2. Une cellule vivante avec deux ou trois voisines vivantes reste vivante.
3. Dans tous les autres cas, la cellule meurt ou reste morte.

## Fonctionnalités

- Visualisation de l'évolution des cellules
- Contrôle de la vitesse de simulation
- Possibilité de pause/reprise
- Grande variété d'améliorations disponibles

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/Zynix52/Projet-2.git
   ```

2. Naviguez dans le dossier du projet :

    ```bash
    cd Projet-2
    ```

## Utilisation

1. Exécutez le programme `main_menu.py`

2. Choisissez votre mode (soit `Solo Mode`ou `Fight Mode`)
*(si c'est la première fois que vous y jouez, vous aurez une fenêtre qui vous expliquera chaque cas)*

3. Jouez !

## Contrôles

Pour le `Solo Mode`:

- `Espace` : Pause/Reprise
- `A` : Fenêtre d'amélioration
- `G` : Fenêtre des règles
- `Esc` : Retour au jeu (ferme la fenêtre active)


Pour le `Fight Mode`:

- Juste besoin de cliquer sur l'item que l'on veut *(veuillez faire attention à vos pixels ! <u>Méfiez-vous</u>)*

## Structure du projet

- `Jeu_avec_pygame.py` : Fichier principal contenant la logique du jeu et l'interface graphique

- `README.md` : Documentation du projet

- `FightMode.py`: Fichier pour le "combat" contre le bot à la manière de ~~***clash royale***~~

- `gestio.py` : Fichier pour gérer automatiquement sur chaque bécane les bibliothèques à installer ou mettre à jour

- `Jeu_de_la_vie.py` : Fichier avec la logique principale du ***Jeu de la Vie***

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Auteurs

- [DucceschKleinsansklien Industries®](https://github.com/Zynix52)
- [FluchInfo®](https://github.com/AxelF52)


Amusez-vous bien avec le Jeu de la Vie !

