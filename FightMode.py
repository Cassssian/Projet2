import random
import pygame
import sys
import copy
import time
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

pygame.init()
pygame.mixer.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
window = pygame.display.set_mode((width, height))
pygame.font.init()
font = pygame.font.Font(None, 36)
rows, cols = 40, 85
cell_size = 15
grid = [[0 for _ in range(cols)] for _ in range(rows)]
music = random.choice(
    ["Audio\\B1.mp3", "Audio\\B2.mp3", "Audio\\B3.mp3"])
pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(0.1)
pygame.mixer_music.play(loops=-1)
game_over_music_played = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 100)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
start_time = time.time()
pause_duration = 5
stock = 10
last_stock_update = time.time()


class JeuDeLaVie:
    def __init__(self, tableau):
        self.tab = tableau
        self.iterations = 0
        self.mémoire = []
        self.game_over_var = False

    def verif_gameover(self):
        """
        getter
        """
        return self.game_over_var

    def run(self):
        """
        boucle du jeu
        """
        if not self.game_over_var:
            nouveau_tableau = copy.deepcopy(self.tab)
            for i in range(len(self.tab)):
                for j in range(len(self.tab[i])):
                    nouveau_tableau[i][j] = self.resultat(i, j)
            self.tab = nouveau_tableau
            self.game_over()

    def valeur_case(self, i, j):
        """
            Renvoie la valeur de la case [i][j] ou 0 si la case n’existe pas.
        """
        if i < 0 or i >= len(self.tab) or j < 0 or j >= len(self.tab[i]):
            return 0
        return self.tab[i][j]

    def total_voisins(self, i, j):
        """Renvoie la somme des valeurs des voisins de la case [i][j]."""
        voisins = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1),
                   (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
        total_player = 0
        total_robot = 0
        for x, y in voisins:
            if self.valeur_case(x, y) == 1:
                total_player += 1
            elif self.valeur_case(x, y) == 2:
                total_robot += 1
        return total_player, total_robot

    def resultat(self, i, j):
        """
        Renvoie la valeur suivante d’une la cellule.

        :param valeur_case: la valeur de la cellule (0 ou 1)
        :param total_voisins: la somme des valeurs des voisins
        :return: la valeur de la cellule au tour suivant

        """
        valeur_case = self.valeur_case(i, j)
        total_voisins_player, total_voisins_robot = self.total_voisins(i, j)

        if valeur_case == 0:
            if total_voisins_player == 3:
                return 1
            elif total_voisins_robot == 3:
                return 2
        elif valeur_case == 1:
            if total_voisins_player < 2 or total_voisins_player > 3:
                return 0
        elif valeur_case == 2:
            if total_voisins_robot < 2 or total_voisins_robot > 3:
                return 0
        elif valeur_case == 3:
            return 0
        elif valeur_case == -1:
            return 3

        return valeur_case

    def couleur_case(self, i, j):
        """ définie a qui appartient la case """
        valeur = self.valeur_case(i, j)
        if valeur == 1:
            return BLUE
        elif valeur == 2:
            return RED
        elif valeur == 3:
            return YELLOW
        elif valeur == -1:
            return BLACK
        else:
            return WHITE

    def game_over(self):
        """ Verfier si quelqu'un a gané"""
        for i in range(len(self.tab)):
            if self.valeur_case(i, 0) == 1:  # Column index 0 is the leftmost column
                self.game_over_var = 1

        for i in range(len(self.tab)):
            if self.valeur_case(i, len(self.tab[i]) - 1) == 2:  # Rightmost column
                self.game_over_var = 0

    def analyse(self):
        """ Compte le nb de cases bleues chez l'equipe advairss*e """
        occurence = []
        for i in range(len(self.tab) // 2 - 1):
            for j in range(len(self.tab[i])):
                if self.tab[i][j] == -1:
                    occurence.append([i, j])
        return occurence

    def draw_canon(self, row, col, color, lvl):
        """ carte helice """
        pygame.draw.circle(window, color, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), 15)
        self.shoot(row, col, lvl, color)

    def shoot(self, row, col, lvl, color):
        """ largeur """
        for step in range(int(lvl) * 10):
            col += 1

            if col >= len(self.tab[row]):
                break

            if self.tab[row][col] != 0:
                break

            if color == BLUE:
                self.tab[row][col] = 1
            elif color == RED:
                self.tab[row][col] = 2


game = JeuDeLaVie(grid)

carte_actuelle = "None"
stock = 10
last_stock_update = time.time()
cartes_dispo = ["planeur", "boule de feu", "vaisseau", "canon", "mangeur"]
cartes_affichees = cartes_dispo[:3]
carte_suivante = cartes_dispo[3]


def draw_grid():
    """
    Dessine la grille actualisée avec les cartes/les couleurs
    """
    global nb_cartes, index
    for i in range(rows):
        for j in range(cols):
            color = game.couleur_case(i, j)  # Utilisation de la méthode couleur_case
            pygame.draw.rect(window, color, (j * cell_size, i * cell_size, cell_size, cell_size))
            pygame.draw.rect(window, BLACK, (j * cell_size, i * cell_size, cell_size, cell_size), 1)  # Black grid lines

    middle_col = cols // 2
    pygame.draw.line(window, RED, (middle_col * cell_size, 0), (middle_col * cell_size, rows * cell_size), 5)

    pygame.draw.line(window, GREEN, (190, 660), ((200 + 68 * round(stock, 1)), 660), 30)
    scoreP1 = font.render("Pixels  :", True, GREEN)
    window.blit(scoreP1, (80, 648))

    for i in range(11):
        num = font.render(f"{i}", True, BLACK)
        window.blit(num, (200 + 65 * i - 5, 650))

    for i in range(3):
        image = pygame.image.load(f"Img\\{cartes_affichees[i]}.png")
        image = pygame.transform.scale(image, (64, 80))
        window.blit(image, (990 + i * 75, height - 102))

    image2 = pygame.image.load(f"Img\\{carte_suivante}.png")
    image2 = pygame.transform.scale(image2, (32, 40))
    window.blit(image2, (1220, height - 82))

    if carte_actuelle != "None":
        image = pygame.image.load(f"Img\\{carte_actuelle}.png")
        image = pygame.transform.scale(image, (64, 80))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        window.blit(image, (mouse_x, mouse_y))


total_time = 5 * 60 # 5 minutes in seconds
start_time = time.time()

def draw_timer():
    """timer"""
    elapsed_time = time.time() - start_time
    remaining_time = total_time - int(elapsed_time)

    if remaining_time < 0:
        remaining_time = 0

    minutes = remaining_time // 60
    seconds = remaining_time % 60
    if minutes > 2:
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, WHITE)
    else:
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, RED)

    window.blit(timer_text, (width//2 - 75, height - 110))

    row = random.randint(5, 35)
    col = random.randint(5, 80)

    if minutes <= 3:
        if random.random() < 0.01**minutes:
            rayon = 10
            for r in range(1, rayon + 1):
                for i in range(-r, r + 1):
                    if 0 <= row + i < rows and 0 <= col + r < cols:
                        game.tab[row + i][col + r] = -1
                    if 0 <= row + i < rows and 0 <= col - r < cols:
                        game.tab[row + i][col - r] = -1
                    if 0 <= row + r < rows and 0 <= col + i < cols:
                        game.tab[row + r][col + i] = -1
                    if 0 <= row - r < rows and 0 <= col + i < cols:
                        game.tab[row - r][col + i] = -1



def draw_game_over(val):
    """
    Interface de game_over
    """
    global game_over_music_played
    width, height = 1280, 720

    if not game_over_music_played:
        pygame.mixer.music.stop()
        if val == 0:
            pygame.mixer.music.load("Audio\\Death.mp3")
            pygame.mixer.music.play()
            sound_effect = pygame.mixer.Sound(random.choice(["Audio\\clash royale angry king emote sound.mp3", "Audio\\clash royale angry king emote sound dist.mp3"]))
            sound_effect.play()
        elif val == 1:
            pygame.mixer.music.load("Audio\\Win.mp3")
            pygame.mixer.music.play()
        game_over_music_played = True

    if val == 0:
        game_over_label = font.render("Vous avez perdu, touche \"échap\" pour quitter", True, RED)
        window.blit(game_over_label, (width // 2 + 50, height // 2))
    elif val == 1:
        game_over_label = font.render("Vous avez gagné, touche \"échap\" pour quitter", True, GREEN)
        window.blit(game_over_label, (width // 2 + 50, height // 2))


def robot():
    """
    Fonction pour les actions du robot (aléatoire mais placement statégiques)
    """
    r = random.randint(1, 20)
    if r == 1:
        lst = game.analyse()
        if 20 < len(lst) < 40:
            r2 = random.randint(1, 2)
            if r2 == 1:
                if random.random() < 0.1:
                    sound_effect = pygame.mixer.Sound(random.choice(["Audio\\GoblinSPAWN.mp3", "Audio\\GoblinSPAWN dist.mp3"]))
                    sound_effect.play()
                row = lst[random.randint(0, len(lst) - 1)][0] + 6
                col = lst[random.randint(0, len(lst) - 1)][1] - 6
                game.tab[row][col] = 2
                game.tab[row - 2][col] = 2
                game.tab[row - 2][col + 1] = 2
                game.tab[row - 1][col + 1] = 2
                game.tab[row - 1][col + 2] = 2
            else:
                row = lst[random.randint(0, len(lst) - 1)][0] + 6
                col = lst[random.randint(0, len(lst) - 1)][1] - 1
                game.tab[row][col] = 2
                if random.random() < 0.1:
                    sound_effect = pygame.mixer.Sound(random.choice(["Audio\\valkyrieSPAWN.mp3", "Audio\\valkyrieSPAWN dist.mp3"]))
                    sound_effect.play()
                game.tab[row - 1][col] = 2
                game.tab[row - 1][col + 1] = 2
                game.tab[row - 1][col + 2] = 2
                game.tab[row - 2][col + 3] = 2
                game.tab[row - 3][col + 3] = 2
                game.tab[row - 3][col + 2] = 2
        elif len(lst) < 20:
            if random.random() < 0.1:
                sound_effect = pygame.mixer.Sound(random.choice(["Audio\\MiniPEKASPAWN.mp3", "Audio\\MiniPEKASPAWN dist.mp3"]))
                sound_effect.play()
            x = random.randint(50, 400)
            y = random.randint(0, 400)
            row = y // cell_size
            col = x // cell_size
            try:
                game.tab[row][col] = 2
                game.tab[row + 1][col + 1] = 2
                game.tab[row + 2][col + 1] = 2
                game.tab[row + 3][col + 1] = 2
                game.tab[row + 3][col] = 2
                game.tab[row + 3][col - 1] = 2
                game.tab[row + 3][col - 2] = 2
                game.tab[row + 3][col - 3] = 2
                game.tab[row + 3][col - 4] = 2
                game.tab[row + 2][col - 5] = 2
            except:
                pass
        elif len(lst) >= 40:
            if random.random() < 0.1:
                sound_effect = pygame.mixer.Sound(random.choice(["Audio\\GolemSPAWN.mp3", "Audio\\GolemSPAWN dist.mp3"]))
                sound_effect.play()
            row = rows // 2
            col = cols // 4 - 20
            game.draw_canon(row, col, RED, 3)


# Initialize the game
game = JeuDeLaVie(grid)
canon = None
running = True

while running:
    current_time = time.time()
    elapsed_time = current_time - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i in range(3):
                card_rect = pygame.Rect(1000 + i * 75, height - 95, 64, 64)
                if card_rect.collidepoint((x, y)):
                    carte_actuelle = cartes_affichees[i]

                    if len(cartes_dispo) > 3:
                        cartes_affichees[i] = cartes_dispo[3]
                        cartes_dispo.pop(3)
                        cartes_dispo.append(carte_actuelle)

                    carte_suivante = cartes_dispo[3]

            row = y // cell_size
            col = x // cell_size
            middle_col = cols // 2

            if 0 <= row < rows and 0 <= col < cols:
                if carte_actuelle != "boule de feu":
                    if col >= middle_col:
                        if carte_actuelle == "planeur" and stock - 3 >= 0:
                            sound_effect = pygame.mixer.Sound(random.choice(["Audio\\GoblinSPAWN.mp3", "Audio\\GoblinSPAWN dist.mp3"]))
                            sound_effect.play()
                            game.tab[row][col] = 1
                            game.tab[row - 2][col] = 1
                            game.tab[row - 2][col - 1] = 1
                            game.tab[row - 1][col - 1] = 1
                            game.tab[row - 1][col - 2] = 1
                            stock -= 3
                            carte_actuelle = "None"
                        elif carte_actuelle == "vaisseau" and stock - 4 >= 0:
                            sound_effect = pygame.mixer.Sound(random.choice(["Audio\\MiniPEKASPAWN.mp3", "Audio\\MiniPEKASPAWN dist.mp3"]))
                            sound_effect.play()
                            try:
                                game.tab[row][col] = 1
                                game.tab[row + 1][col - 1] = 1
                                game.tab[row + 2][col - 1] = 1
                                game.tab[row + 3][col - 1] = 1
                                game.tab[row + 3][col] = 1
                                game.tab[row + 3][col + 1] = 1
                                game.tab[row + 3][col + 2] = 1
                                game.tab[row + 3][col + 3] = 1
                                game.tab[row + 3][col + 4] = 1
                                game.tab[row + 2][col + 5] = 1
                                stock -= 4
                                carte_actuelle = "None"
                            except:
                                pass
                        elif carte_actuelle == "mangeur" and stock - 2 >= 0:
                            sound_effect = pygame.mixer.Sound(random.choice(["Audio\\valkyrieSPAWN.mp3", "Audio\\valkyrieSPAWN dist.mp3"]))
                            sound_effect.play()
                            game.tab[row][col] = 1
                            game.tab[row - 1][col] = 1
                            game.tab[row - 1][col - 1] = 1
                            game.tab[row - 1][col - 2] = 1
                            game.tab[row - 2][col - 3] = 1
                            game.tab[row - 3][col - 3] = 1
                            game.tab[row - 3][col - 2] = 1
                            stock -= 2
                            carte_actuelle = "None"
                        elif carte_actuelle == "canon" and stock - 8 >= 0:
                            sound_effect = pygame.mixer.Sound(random.choice(["Audio\\GolemSPAWN.mp3", "Audio\\GolemSPAWN dist.mp3"]))
                            sound_effect.play()
                            game.draw_canon(row, col, BLUE, random.choice([1, 3]))
                            stock -= 8
                            carte_actuelle = "None"

                elif col < middle_col and stock - 6 >= 0:
                    if random.random() > 0.5:
                        sound_effect = pygame.mixer.Sound(random.choice(["Audio\\HİHİHİHA (Clash Royale Hihihiha Sesi).mp3", "Audio\\HİHİHİHA (Clash Royale Hihihiha Sesi) dist.mp3"]))
                        sound_effect.play()
                    rayon = random.randint(5, 7)
                    for r in range(1, rayon + 1):
                        for i in range(-r, r + 1):
                            if 0 <= row + i < rows and 0 <= col + r < cols:
                                game.tab[row + i][col + r] = -1
                            if 0 <= row + i < rows and 0 <= col - r < cols:
                                game.tab[row + i][col - r] = -1
                            if 0 <= row + r < rows and 0 <= col + i < cols:
                                game.tab[row + r][col + i] = -1
                            if 0 <= row - r < rows and 0 <= col + i < cols:
                                game.tab[row - r][col + i] = -1
                    stock -= 6
                    carte_actuelle = "None"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if current_time - last_stock_update >= 0.1:
        if stock < 10:
            stock += 0.1
        last_stock_update = current_time

    if random.randint(1, 50) == 1:
        music = random.choice(["Audio\\BOULIEATTACK.mp3","Audio\\COMBAT.mp3","Audio\\ELECTRO1.mp3","Audio\\ELECTRO2.mp3","Audio\\GOBLINATTACK.mp3","Audio\\PEKAATTACK.mp3","Audio\\PODEGRADER.mp3","Audio\\TIMBER.mp3", "Audio\\BOULIEATTACK.mp3","Audio\\COMBAT dist.mp3","Audio\\ELECTRO1 dist.mp3","Audio\\ELECTRO2 dist.mp3","Audio\\GOBLINATTACK dist.mp3","Audio\\PEKAATTACK dist.mp3","Audio\\PODEGRADER dist.mp3","Audio\\TIMBER dist.mp3"])
        sound_effect = pygame.mixer.Sound(music)
        sound_effect.play()

    game.run()
    robot()
    window.fill(BLACK)
    if game.verif_gameover() is False:
        draw_grid()
        draw_timer()
    else:
        window.fill(BLACK)
        draw_game_over(game.verif_gameover())

    pygame.display.flip()
    clock.tick(7.5)
