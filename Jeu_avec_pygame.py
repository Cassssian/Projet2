import gestio # type: ignore # type: ignore

gestio.installer_bibliotheques_si_besoin(gestio.bibliotheques_a_installer)

import pygame
import sys
import copy
import time
import random
import json
from os import environ
import math
import moviepy.editor as mp
from tkinter import messagebox

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Cache le message de pygame
try:
    with open("score.json", "r") as f:
        data: list[{str, int}] = json.load(f)  # Charge les données du fichier JSON
except:
    with open("score.json", "w") as f:
        data: list[{str, int}] = [{"Partie": 0, "Score": 0}]
        # Sauvegarde les données dans le fichier JSON
        json.dump(data, f, indent=1)

if data:  # Vérifie si la liste n'est pas vide
    dernière_partie: int = data[-1]["Partie"]
    dernier_score: int = data[-1]["Score"]
    meilleure_partie: int = data[0]["Partie"]
    meilleur_score: int = data[0]["Score"]
else:
    dernière_partie: int = 0
    dernier_score: int = 0
    meilleure_partie: int = 0
    meilleur_score: int = 0

pygame.init()
musique: list[str] = random.choice(
    ["Audio/Firewhole - The Dreamkeeper.mp3", "Audio/Firewhole - Never Learn.mp3", "Audio/Firewhole - Temper.mp3",
     "Audio/Firewhole - 222† ∂∆ §§§.mp3"])
musique_defaite: str = "Audio/Firewhole - Bossfight Afterparty.mp3"
pygame.mixer.init()
pygame.mixer.music.load(musique)
pygame.mixer_music.play(loops=-1)
musique_actuelle: str = "jeu"


class Sauvegarde:
    """
    Classe pour sauvegarder et lire les scores
    """

    def __init__(self):
        """
        Constructeur de la classe
        --------------
        Pas d'arugments
        """
        self.__nom_fichier: str = "score.json"

    def sauvegarder(self, partie: int, score_partie: int) -> None:
        """
        Sauvegarde le score
        --------------
        partie_score : partie et score n° x
        """
        try:
            with open(self.__nom_fichier, "r") as f:
                scores: list[{str, int}] = json.load(f)
        except FileNotFoundError:
            scores: list[None] = []  # Si le fichier n'existe pas, commencer avec une liste vide

        # Ajouter les nouvelles données
        scores.append({"Partie": partie, "Score": score_partie})

        # Écrire les données mises à jour dans le fichier
        with open(self.__nom_fichier, "w") as f:
            json.dump(scores, f, indent=1)

    def sauvegarde_meilleur_score(self, meilleure_partie: int, meilleur_score: int):
        """
        Sauvegarde le meilleur score
        --------------
        Pas d'arguments
        """
        # Charger le fichier JSON
        with open(self.__nom_fichier, "r") as f:
            data: list[{str, int}] = json.load(f)

        try:
            # Modifier le premier dictionnaire
            data[0]['Partie'] = meilleure_partie
            data[0]['Score'] = meilleur_score

            with open(self.__nom_fichier, "w") as f:
                json.dump(data, f, indent=1)
        except:
            scores: list[None] = []
            scores.append({"Partie": meilleure_partie, "Score": meilleur_score})

            with open(self.__nom_fichier, "w") as f:
                json.dump(data, f, indent=1)

    def lire(self, mode: str) -> list[str]:
        """
        Lit le score
        --------------
        mode : mode de lecture utilsé
        """
        global meilleur_score, meilleure_partie, dernière_partie, dernier_score

        with open(self.__nom_fichier, "r") as fichier:
            data: list[{str, int}] = json.load(fichier)

        if mode == "lecture":
            if data:
                data.pop(0)

            liste_partie_score: list[str] = [f"Partie n°{partie['Partie']} : {partie['Score']} points" for partie in
                                             data]
            return liste_partie_score

        else:
            if data:
                meilleur_score = max(partie['Score'] for partie in data)
                meilleure_partie = max(partie['Partie'] for partie in data if partie['Score'] == meilleur_score)
                dernière_partie = max(partie['Partie'] for partie in data)
                dernier_score = next(partie['Score'] for partie in data if partie['Partie'] == dernière_partie)
            else:
                meilleur_score = meilleure_partie = dernière_partie = dernier_score = 0


class JeuDeLaVie:
    def __init__(self, tableau: list[str]):
        """
        Affecte un tableau à deux dimensions à l’attribut tableau

        tableau : tableau à deux dimensions
        """
        self.tab: list[str] = tableau
        self.iterations: int = 0
        self.mémo: list[str] = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.game_over: bool = False
        self.seuil_trop: int = 3
        self.temps_temp: int = 5

    def run(self):
        """
        Met à jour les cellules et continue le jeu.
        """
        nouveau_tableau: list[str] = copy.deepcopy(self.tab)
        for i in range(len(self.tab)):
            for j in range(len(self.tab[i])):
                nouveau_tableau[i][j] = self.resultat(self.valeur_case(i, j), self.total_voisins(i, j))
        self.tab: list[str] = nouveau_tableau
        if not self.game_over:
            self.iterations += 1
        self.vérifie_blocage()

    def valeur_case(self, i: int, j: int) -> int:
        """
        Renvoie la valeur de la case [i][j] ou 0 si la case n’existe pas.
        -----------------
        i: ligne de la case
        j: colonne de la case
        """
        if i < 0 or i >= len(self.tab) or j < 0 or j >= len(self.tab[i]):
            return 0
        return self.tab[i][j]

    def total_voisins(self, i: int, j: int) -> int:
        """
        Renvoie la somme des valeurs des voisins de la case [i][j].
        -----------------
        i: ligne de la case
        j: colonne de la case
        """
        voisins: list[tuple[int]] = [
            (i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1),
            (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
        total: int = 0
        for x, y in voisins:
            total += self.valeur_case(x, y)
        return total

    def resultat(self, valeur_case: int, total_voisins: int) -> int:
        """
        Renvoie la valeur suivante d'une cellule selon les règles du jeu.
        ---------------------
        valeur_case: valeur de la case
        total_voisins: somme des valeurs des voisins de la case
        """
        if valeur_case == 0 and total_voisins == 3 <= self.seuil_trop:
            return 1
        if valeur_case == 1 and (total_voisins < 2 or total_voisins > self.seuil_trop):
            return 0
        return valeur_case

    def vérifie_blocage(self):
        """
        Arrêtes le compteur itération si le jeu est bloqué ou en boucle
        """
        self.mémo.append(self.tab)
        if len(self.mémo) > 8:
            self.mémo.pop(0)
        try:
            if self.mémo[0] == self.mémo[2] and self.mémo[1] and self.mémo[3] and self.mémo[4] == self.mémo[6] and \
                    self.mémo[5] and self.mémo[7]:
                self.game_over: bool = True
        except:
            self.game_over: bool = False


class Amelioration:
    """
    Classe pour la gestion des améliorations
    """

    def __init__(self):
        """
        Constructeur de la classe
        --------------
        Pas d'argument
        """
        self.available_upgrades: list[str] = ['Augmenter la taille des cellules',
                                              'Réduire le seuil de surpopulation (-1 pendant 5s)',
                                              'Augmenter la vitesse', 'Changer les couleurs',
                                              'Réduire le nombre des cellules']
        self.nb_upgrades: list[int] = [random.randint(0, len(self.available_upgrades) - 1) for i in range(3)]
        self.current_upgrades: list[str] = [self.available_upgrades[i] for i in self.nb_upgrades]  # Améliorations aléatoires affichées
        self.upgrade_costs: list[int] = [10, 20, 5, 2, 15]  # Coût par amélioration
        self.current_costs = [self.upgrade_costs[self.available_upgrades.index(upgrade)] for upgrade in self.current_upgrades]
        self.upgrade_gifs: dict[str, str] = {  # Associer des GIFs à chaque amélioration
            'Augmenter la taille des cellules': 'Img/Gif/taille.gif',
            'Réduire le seuil de surpopulation (-1 pendant 5s)': 'Img/Gif/population.gif',
            'Augmenter la vitesse': 'Img/Gif/vitesse.gif',
            'Changer les couleurs': 'Img/Gif/couleur.gif',
            'Réduire le nombre des cellules': 'Img/Gif/coût.gif'
        }
        self.gif_frames: dict[None] = {}
        self.gif_index: int = 0
        self.frame_delay: int = 0  # Délai pour changer de frame (nombre de ticks)
        self.tick_count: int = 0
        self.button_width = int(width * 0.2)
        self.button_height = int(height * 0.5)
        self.gif_size = (self.button_width - 10, int(self.button_height * 0.3))
        self.seuil_timer = None

        # Charger les GIFs pour chaque amélioration
        for upgrade in self.current_upgrades:
            self.gif_frames[upgrade] = self.load_gif(self.upgrade_gifs[upgrade])

    def display_menu(self, screen):
        """
        Affiche le menu des améliorations.
        --------------
        screen: surface de Pygame
        """
        amelioration_window_width = int(width * 0.8)
        amelioration_window_height = int(height * 0.8)
        amelioration_window_x = (width - amelioration_window_width) // 2
        amelioration_window_y = (height - amelioration_window_height) // 2

        pygame.draw.rect(screen, BLACK, (amelioration_window_x, amelioration_window_y, amelioration_window_width, amelioration_window_height))

        font = pygame.font.SysFont(None, 36)

        for i, upgrade in enumerate(self.current_upgrades):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_x = amelioration_window_x + int(amelioration_window_width * 0.05) + i * (self.button_width + int(amelioration_window_width * 0.05))
            button_y = amelioration_window_y + int(amelioration_window_height * 0.1)
            button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)

            if button_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

            pygame.draw.rect(screen, BLACK, button_rect, 2)

            gif_frames = self.gif_frames[upgrade]
            current_frame = gif_frames[self.gif_index % len(gif_frames)]
            screen.blit(current_frame, (button_rect.x + 5, button_rect.y + 5))

            pygame.draw.line(screen, (0, 0, 0), (button_rect.x, button_rect.y + self.gif_size[1] + 10),
                            (button_rect.right, button_rect.y + self.gif_size[1] + 10), 3)

            self.draw_text_in_rect(screen, upgrade, font, button_rect, BLACK,
                                button_rect.y + self.gif_size[1] + int(self.button_height * 0.15))

            cost_text = f"Coût: {self.current_costs[i]} du stock"
            self.draw_text_in_rect(screen, cost_text, font, button_rect, BLACK,
                                button_rect.bottom - int(self.button_height * 0.1))

        self.gif_index += 1


    def load_gif(self, gif_path : str) -> list:
        """
        Charge un GIF et renvoie une liste de frames
        --------------
        gif_path: Chemin du GIF
        """
        clip = mp.VideoFileClip(gif_path)
        frames = []

        for frame in clip.iter_frames():
            frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], 'RGB')
            frame_surface = pygame.transform.scale(frame_surface, self.gif_size)
            frames.append(frame_surface)

        return frames

    def handle_click(self, x, y, points) -> int:
        """
        Gère les clics sur les boutons d'amélioration.
        --------------
        x: Coordonnée x de la souris
        y: Coordonnée y de la souris
        points: Nombre de points disponibles
        """
        amelioration_window_width = int(width * 0.8)
        amelioration_window_height = int(height * 0.8)
        amelioration_window_x = (width - amelioration_window_width) // 2
        amelioration_window_y = (height - amelioration_window_height) // 2

        for i in range(len(self.current_upgrades)):
            button_x = amelioration_window_x + int(amelioration_window_width * 0.05) + i * (
                        self.button_width + int(amelioration_window_width * 0.05))
            button_y = amelioration_window_y + int(amelioration_window_height * 0.1)
            button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)

            if button_rect.collidepoint(x, y):
                selected_upgrade = self.current_upgrades[i]

                if points >= self.current_costs[i]:  # Vérifiez si vous avez assez de points
                    points -= self.current_costs[i]  # Déduire le coût
                    self.apply_upgrade(selected_upgrade)  # Appliquer l'amélioration
                    upgrade_index = self.available_upgrades.index(selected_upgrade)
                    self.upgrade_costs[upgrade_index] += 5


                    # Remplacer l'amélioration sélectionnée avec une nouvelle
                    new_upgrade_index = random.randint(0, len(self.available_upgrades) - 1)
                    new_upgrade = self.available_upgrades[new_upgrade_index]

                    # Assurez-vous que la nouvelle amélioration n'est pas déjà présente
                    while new_upgrade in self.current_upgrades:
                        new_upgrade_index = random.randint(0, len(self.available_upgrades) - 1)
                        new_upgrade = self.available_upgrades[new_upgrade_index]
                        self.current_costs[i] = self.upgrade_costs[self.available_upgrades.index(new_upgrade)]

                    # Mettre à jour l'amélioration
                    self.current_upgrades[i] = new_upgrade
                    # Recharger le GIF pour la nouvelle amélioration
                    self.gif_frames[new_upgrade] = self.load_gif(self.upgrade_gifs[new_upgrade])

                    for j, upgrade in enumerate(self.current_upgrades):
                        if upgrade == selected_upgrade:
                            self.current_costs[j] = self.upgrade_costs[upgrade_index]

                    break

                elif points < self.current_costs[i]:
                    messagebox.showinfo("Pas assez de points",
                                        "Vous n'avez pas assez de points pour pouvoir sélectionner cette amélioration")
    

        return points  # Retourner les points mis à jour

    def apply_upgrade(self, upgrade):
        """
        Applique l'amélioration sélectionnée
        --------------
        upgrade: Amélioration sélectionnée
        """
        global cell_size, rows, cols, BLUE, SPEED
        if upgrade == 'Augmenter la taille des cellules':
            cell_size += 2
            rows = max(1, grid_height // cell_size)
            cols = max(1, grid_width // cell_size)
            game.tab = [[game.tab[i][j] if i < len(game.tab) and j < len(game.tab[i]) else 0
                         for j in range(cols)] for i in range(rows)]

        elif upgrade == 'Réduire le seuil de surpopulation (-1 pendant 5s)':
            game.seuil_trop += 1
            self.seuil_timer = True  # Set end time for the effect

        elif upgrade == 'Augmenter la vitesse':
            SPEED += 1  # Accélérer le jeu

        elif upgrade == 'Changer les couleurs':
            BLUE = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        elif upgrade == 'Réduire le nombre des cellules':
            self.reduce_cell()

    def reduce_cell(self):
        """
        Réduit le nombre de cellules dans self.tab.
        """
        if len(game.tab) > 1:  # S'il y a plus d'une ligne, on retire la dernière
            game.tab.pop()
        for i in range(len(game.tab)):
            if len(game.tab[i]) > 1:  # S'il y a plus d'une colonne, on retire la dernière colonne
                game.tab[i].pop()

        # Mise à jour des variables rows et cols
        global rows, cols
        rows = len(game.tab)
        cols = len(game.tab[0]) if rows > 0 else 0

    # Fonction pour découper le texte
    def wrap_text(self, text, font, max_width) -> list[str]:
        """
        Fonction pour découper le texte automatiquement
        --------------
        text: Texte à découper
        font: Police de caractères
        max_width: Largeur maximale du rectangle
        """
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        lines.append(' '.join(current_line))  # Ajouter la dernière ligne
        return lines

    # Fonction pour dessiner et centrer le texte dans un rectangle
    def draw_text_in_rect(self, screen, text, font, rect, color, custom_y=None):
        """
        Fonction pour dessiner et centrer le texte dans un rectangle
        --------------
        screen: Surface de jeu
        text: Texte à dessiner
        font: Police de caractères
        rect: Rectangle dans lequel dessiner le texte
        color: Couleur du texte
        custom_y: Coordonnée y personnalisée (par défaut None)
        """
        wrapped_lines = self.wrap_text(text, font, rect.width)
        total_height = len(wrapped_lines) * font.get_linesize()

        if custom_y is None:
            y_offset = rect.y + (rect.height - total_height) // 2
        else:
            y_offset = custom_y

        if y_offset < rect.y:
            y_offset = rect.y  # Ajuster si trop haut
        elif y_offset + total_height > rect.y + rect.height:
            y_offset = rect.y + rect.height - total_height  # Ajuster si trop bas

        for line in wrapped_lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(rect.x + rect.width // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += font.get_linesize()  # Déplacer vers la ligne suivante

class Regle:
    """
    Classe pour afficher les règles
    """
    def __init__(self):
        """
        Initialise les règles
        """
        self.rules_text : list[str]= ["Règles du jeu de la vie :", "1. Une cellule vivante avec moins de deux","voisines vivantes meurt (sous-population).", 
                                      "2. Une cellule vivante avec deux ou trois voisines vivantes survit.",
                                      "3. Une cellule vivante avec plus de trois voisines vivantes meurt (surpopulation).", 
                                      "4. Une cellule morte avec exactement trois voisines","vivantes devient une cellule vivante (reproduction)."]
    
    def draw_rules(self, screen):
        # Define the rules window size
        rules_window_width = int(width * 0.8)
        rules_window_height = int(height * 0.8)
        rules_window_x = (width - rules_window_width) // 2
        rules_window_y = (height - rules_window_height) // 2

        # Create a surface for the rules
        rules_surface = pygame.Surface((rules_window_width, rules_window_height))
        rules_surface.fill((0, 0, 0))  # Black background

        # Define font and colors
        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 48)
        text_color = (255, 255, 255)  # White text

        # Draw title
        title = title_font.render("Règles du jeu de la vie", True, text_color)
        title_rect = title.get_rect(center=(rules_window_width // 2, 40))
        rules_surface.blit(title, title_rect)

        # Draw rules
        y_offset = 100
        for rule in self.rules_text:
            rule_surface = font.render(rule, True, text_color)
            rule_rect = rule_surface.get_rect(center=(rules_window_width // 2, y_offset))
            rules_surface.blit(rule_surface, rule_rect)
            y_offset += 50

        # Draw the rules surface on the main screen
        screen.blit(rules_surface, (rules_window_x, rules_window_y))

    def wrap_text(self, text, font, max_width) -> list[str]:
        """
        Fonction pour découper le texte automatiquement
        --------------
        text: Texte à découper
        font: Police de caractères
        max_width: Largeur maximale du rectangle
        """
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))  # Ajouter la dernière ligne
        return lines
    

# width, height = 1050, 600 # Voit si c'est mieux ou pas
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jeu de la Vie - Solo")
pygame.font.init()
font: object = pygame.font.Font(None, 36)

# Update grid and cell size calculation
grid_width: int = int(width * 0.75)
grid_height: int = height
rows: int = 45
cols: int = int(rows * (grid_width / grid_height))
cell_size: int = min(grid_width // cols, grid_height // rows)
grid: list[int] = [[0 for _ in range(cols)] for _ in range(rows)]
game: object = JeuDeLaVie(grid)
save_class: object = Sauvegarde()
upgrade_menu: object = Amelioration()

WHITE: tuple[int] = (255, 255, 255)
BLACK: tuple[int] = (0, 0, 0)
BLUE: tuple[int] = (0, 128, 255)
BUTTON_COLOR: tuple[int] = (200, 200, 200)
BUTTON_HOVER_COLOR: tuple[int] = (150, 150, 150)

clock: object = pygame.time.Clock()
running: bool = True
paused: bool = True
stock: int = 20
iterations: int = 0
last_stock_update: object = time.time()
affiche_save: bool = False
show_upgrade_menu: bool = False
show_rules : bool = False
partie: list[None] = []
scroll_y: int = 0
score: int = max(0, (game.iterations - 4))
SPEED: int = 3
rules : object = Regle()


def get_rainbow_color(offset: int, time_offset: int) -> tuple[int]:
    """
    Génère une couleur arc-en-ciel en fonction de l'offset de la lettre.
    ----------
    offset : décalage de la lettre
    time_offset : décalage de temps pour l'animation
    """
    hue: int = (offset + time_offset) % 360  # Fait varier la teinte sur une échelle de 360 degrés
    r: int = int(255 * (math.sin(math.radians(hue)) + 1) / 2)  # Convertit la teinte en rouge
    g: int = int(255 * (math.sin(math.radians(hue + 120)) + 1) / 2)  # Décalage de 120 pour le vert
    b: int = int(255 * (math.sin(math.radians(hue + 240)) + 1) / 2)  # Décalage de 240 pour le bleu
    return (r, g, b)


def draw_grid():
    """
    Dessine la grille et les informations à l'écran avec des animations pour le meilleur score.
    """
    global paused, meilleur_score, affiche_save, partie

    for i in range(len(game.tab)):  # Boucle sur le nombre de lignes actuelles de game.tab
        for j in range(len(game.tab[i])):  # Boucle sur le nombre de colonnes actuelles de chaque ligne
            color = BLUE
            pygame.draw.rect(window, color if game.tab[i][j] == 1 else WHITE,
                             (j * cell_size, i * cell_size, cell_size, cell_size))
            pygame.draw.rect(window, BLACK, (j * cell_size, i * cell_size, cell_size, cell_size), 1)

    info_x = grid_width + 20
    info_y = 20
    line_height = int(height * 0.05)

    # Affichage du statut et du score courant
    status_text: str = "En pause" if paused else "En route"
    status_surface = font.render(f"Statut: {status_text}", True, WHITE)
    window.blit(status_surface, (info_x, info_y))

    iterations_surface = font.render(f"Score: {max(0, (game.iterations - 4))}", True, WHITE)
    window.blit(iterations_surface, (info_x, info_y + line_height))

    stock_surface = font.render(f"Stock: {stock}", True, WHITE)
    window.blit(stock_surface, (info_x, info_y + 2 * line_height))

    keybind_text: list[str] = upgrade_menu.wrap_text("Mettre en pause : ESPACE", font, width * 0.2)
    rules_text: list[str] = upgrade_menu.wrap_text(
        "Objectif : Garder un environnement en constant mouvement (c'est à dire que la configuration doit toujours évoluer)",
        font, width * 0.2)

    # Affichage des instructions
    y_offset: int = info_y + 3 * line_height

    for line in keybind_text:
        keybind = font.render(line, True, WHITE)
        window.blit(keybind, (info_x, y_offset))
        y_offset += line_height // 2

    y_offset += line_height

    for line in rules_text:
        rules = font.render(line, True, WHITE)
        window.blit(rules, (info_x, y_offset))
        y_offset += line_height // 2

    if meilleur_score != 0:
        # Texte du meilleur score
        score_text: str = f"Meilleur score : {meilleur_score}"

        # Variable pour animer l'effet de dégradé RGB
        time_offset: int = pygame.time.get_ticks() // 10  # Utilise le temps pour faire avancer les couleurs

        # Position initiale pour dessiner les lettres
        x_offset: int = info_x
        texte_y: int = height - line_height * 2

        # Parcours de chaque lettre pour appliquer un dégradé
        for i, letter in enumerate(score_text):
            letter_color: tuple[int] = get_rainbow_color(i * 20, time_offset)  # Couleur arc-en-ciel pour chaque lettre
            letter_surface = font.render(letter, True, letter_color)
            window.blit(letter_surface, (x_offset, texte_y))  # Affiche la lettre à la position donnée
            x_offset += letter_surface.get_width()  # Ajuste la position x pour la lettre suivante

    else:
        texte: str = "Pas de meilleur score"
        texte_surface = font.render(texte, True, WHITE)
        window.blit(texte_surface, (info_x, height - line_height * 2))

    # Charger et dessiner le bouton de sauvegarde
    bouton_sauvegarde = pygame.image.load("Img/sauvegarde.png")
    bouton_sauvegarde = pygame.transform.scale_by(bouton_sauvegarde, 0.03)
    bouton_sauvegarde_rect = bouton_sauvegarde.get_rect(topleft=(width - int(width * 0.04), int(height * 0.02)))

    window.blit(bouton_sauvegarde, bouton_sauvegarde_rect.topleft)

    # Gérer les événements de la souris ici
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:  # Si le bouton gauche de la souris est cliqué
        if bouton_sauvegarde_rect.collidepoint(mouse_x, mouse_y):
            if not paused:
                paused = True
            partie = save_class.lire("lecture")
            affiche_save = True


def show_save(partie_liste: list[str], meilleur: int) -> None:
    """
    Affiche la fenêtre de sauvegarde avec une petite taille.
    ---------
    partie_liste : liste des parties sauvegardées
    meilleur : meilleur partie avec le meilleur score
    """
    global affiche_save, scroll_y

    save_window_width: int = int(width * 0.8)
    save_window_height: int = int(height * 0.8)
    save_window_x: int = (width - save_window_width) // 2
    save_window_y: int = (height - save_window_height) // 2

    save_surface = pygame.Surface((save_window_width, save_window_height))
    save_surface.fill(BLACK)
    nb: int = 1

    if partie_liste != []:
        y: int = scroll_y + 20
        for ligne in partie_liste:
            if nb == meilleur:
                score_text: str = ligne

                # Variable pour animer l'effet de dégradé RGB
                time_offset: int = pygame.time.get_ticks() // 10  # Utilise le temps pour faire avancer les couleurs

                # Position initiale pour dessiner les lettres
                x_offset: int = 15
                y_offset: int = y

                # Parcours de chaque lettre pour appliquer un dégradé
                for i, letter in enumerate(score_text):
                    letter_color: tuple[int] = get_rainbow_color(i * 20,
                                                                 time_offset)  # Couleur arc-en-ciel pour chaque lettre
                    texte = font.render(letter, True, letter_color)
                    save_surface.blit(texte, (x_offset, y_offset))  # Affiche la lettre à la position donnée
                    x_offset += texte.get_width()  # Ajuste la position x pour la lettre suivante

                y += texte.get_height() + 10

            else:
                texte = font.render(ligne, True, WHITE)
                save_surface.blit(texte, (15, y))
                y += texte.get_height() + 10
            nb += 1

    else:
        texte = font.render("Pas de sauvegarde encore effectuée", True, WHITE)
        save_surface.blit(texte, (15, 15))

    window.blit(save_surface, (save_window_x, save_window_y))


def musique_defaite_fonction(musique: str, musique_actuelle: str):
    """
    Fonction qui permet de changer la musique du jeu pour la musique de la fenêtre de décès
    ---------
    musique : chemin de la musique
    musique_actuelle : musique actuelle qui ne doit pas être jouée
    """
    if musique_actuelle == "jeu":
        pygame.mixer_music.load(musique)
        pygame.mixer_music.play(loops=-1)


def defaite():
    """
    Fonction qui affiche l'écran de défaite.
    """
    global musique_actuelle, meilleur_score, score
    musique_defaite_fonction(musique_defaite, musique_actuelle)
    musique_actuelle = "defaite"
    window.fill(BLACK)

    if meilleur_score > score:
        score_surface = font.render(f"Votre score: {score}", True, WHITE)
        window.blit(score_surface, (width // 2 - score_surface.get_width() // 2, height // 2))
        R_label = font.render(f"\"Q\" pour quitter ou \"R\" pour recommencer", True, WHITE)
        window.blit(R_label, (width // 2 - R_label.get_width() // 2, height // 2 + 50))
        pygame.display.flip()

    else:
        # Texte du meilleur score
        score_text: str = f"Nouveau meilleur score : {score}"

        # Variable pour animer l'effet de dégradé RGB
        time_offset: int = pygame.time.get_ticks() // 10  # Utilise le temps pour faire avancer les couleurs

        # Position initiale pour dessiner les lettres
        texte_x_defaite: float = width // 2 - width * 0.155
        texte_y_defaite: int = height // 2

        # Parcours de chaque lettre pour appliquer un dégradé
        for i, letter in enumerate(score_text):
            letter_color: tuple[int] = get_rainbow_color(i * 20, time_offset)  # Couleur arc-en-ciel pour chaque lettre
            letter_surface = font.render(letter, True, letter_color)
            window.blit(letter_surface,
                        (texte_x_defaite + (width * 0.075), texte_y_defaite))  # Affiche la lettre à la position donnée
            texte_x_defaite += letter_surface.get_width()  # Ajuste la position x pour la lettre suivante

        R_label = font.render(f"\"Q\" pour quitter ou \"R\" pour recommencer", True, WHITE)
        window.blit(R_label, (width // 2 - R_label.get_width() // 2, height // 2 + 50))


def restart_game():
    """
    Réinitialise le jeu après une défaite.
    """
    global musique_actuelle, paused, stock, SPEED, BLUE, grid_width, grid_height, rows, cols, cell_size, grid, game, upgrade_menu, show_rules, rules
    musique_actuelle = "jeu"
    pygame.mixer.music.load(musique)
    pygame.mixer_music.play(loops=-1)
    grid_width = int(width * 0.75)
    grid_height = height
    rows = 45
    cols = int(rows * (grid_width / grid_height))
    cell_size = min(grid_width // cols, grid_height // rows)
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    game = JeuDeLaVie(grid)

    game.tab = [[0 for _ in range(cols)] for _ in range(rows)]
    game.iterations = 0
    game.mémo = []  # Vider la mémoire des anciens états
    game.game_over = False
    paused = True
    stock = 20
    SPEED = 3
    BLUE = (0, 128, 255)
    show_rules = False

    upgrade_menu = Amelioration()
    upgrade_menu.upgrade_costs = [10, 20, 5, 2, 15]

    rules = Regle()
    
    


def save():
    """
    Sauvegarde le score dans un fichier JSON.
    """
    global score

    save_class.lire("sauvegarde")
    try:

        global meilleur_score, meilleure_partie

        if meilleur_score < score:
            meilleur_score = score
            meilleure_partie = dernière_partie + 1
            save_class.sauvegarde_meilleur_score(meilleure_partie, meilleur_score)

        save_class.sauvegarder(dernière_partie + 1, score)
    except:
        save_class.sauvegarde_meilleur_score(1, score)
        save_class.sauvegarder(1, score)

def quit_game():
    global running, game, upgrade_menu, save_class
    save()
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    running = False

while running:
    score = max(0, game.iterations - 4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if affiche_save:  # Si la fenêtre des sauvegardes est ouverte
            # Gestion de la molette de défilement uniquement dans la fenêtre des sauvegardes
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Molette haut
                    scroll_y = min(scroll_y + 15, 0)  # Limite à 0 pour éviter de trop remonter
                elif event.button == 5:  # Molette bas
                    scroll_y -= 15

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    affiche_save = False  # Fermer la fenêtre de sauvegarde

        if show_upgrade_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_a:
                    show_upgrade_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                stock = upgrade_menu.handle_click(x, y, stock)

        if show_rules:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_g:
                    show_rules = False

        if upgrade_menu.seuil_timer and not paused:
            timer = time.time() + 5
            if time.time() > timer:
                game.seuil_trop -= 1
                upgrade_menu.seuil_timer = None

        else:  # Si le jeu est actif et que la fenêtre de sauvegarde est fermée
            if game.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        save()
                        quit_game()
                    elif event.key == pygame.K_r:
                        save()
                        restart_game()

            if not game.game_over and not show_upgrade_menu and not affiche_save:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x < grid_width and paused:
                        row = y // cell_size
                        col = x // cell_size
                        if game.tab[row][col] == 0 and stock > 0:
                            game.tab[row][col] = 1
                            stock -= 1
                        elif game.tab[row][col] == 1:
                            game.tab[row][col] = 0
                            stock += 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not game.game_over and not show_upgrade_menu:
                        paused = not paused
                    if event.key == pygame.K_a:
                        show_upgrade_menu = not show_upgrade_menu
                    if event.key == pygame.K_g:
                        show_rules = not show_rules

    if affiche_save and not show_upgrade_menu and not show_rules:  # Si la fenêtre des sauvegardes est active
        show_save(partie, meilleure_partie)

    elif show_upgrade_menu and not affiche_save and not show_rules:
        upgrade_menu.display_menu(window)
    
    elif show_rules and not show_upgrade_menu and not affiche_save:
        rules.draw_rules(window)

    else:  # Si le jeu est actif
        if not game.game_over:
            if not paused:
                current_time = time.time()
                if current_time - last_stock_update >= 5:
                    stock += 1
                    last_stock_update = current_time

                iterations += 1
                game.run()

            window.fill(BLACK)
            draw_grid()

        else:
            defaite()

    pygame.display.flip()
    clock.tick(SPEED)

import main_menu # type: ignore