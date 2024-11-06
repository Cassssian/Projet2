import gestio
gestio.installer_bibliotheques_si_besoin(gestio.bibliotheques_a_installer)
import pygame
import cv2
import random
from tkinter import messagebox
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Cache le message de pygame
pygame.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jeu de la Vie")
pygame.font.init()
pygame.mixer.init()

if random.random() < 0.6:
    musique_pas_goated = "Audio/Menu C R.mp3"
    pygame.mixer.music.load(musique_pas_goated)
elif 0.6 < random.random() < 0.8:
    musique_pas_goated = "Audio/Fortnite  Lobby Classic Lobby Music.mp3"
    pygame.mixer.music.load(musique_pas_goated)
else:
    goated_musique = "Audio/Firewhole - Elevator Meme Music Remix.mp3"
    pygame.mixer.music.load(goated_musique)
pygame.mixer_music.play(loops=-1)

font = pygame.font.Font(None, 50)
button_color = (20, 20, 180)
button_color2 = (255, 100, 20)
text_color = (255, 255, 255)


def draw_button(rect, text, color):
    pygame.draw.rect(window, color, rect, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)


video = cv2.VideoCapture('Bg.mp4')

solo_rect = pygame.Rect(width*1/4-100, height//2 + 70, 200, 50)
multi_rect = pygame.Rect(width*3/4-100, height//2 + 70, 200, 50)

continuer = True
while continuer:
    ret, frame = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video.read()

    frame = cv2.resize(frame, (width, height))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(frame)
    window.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))

    draw_button(solo_rect, "Solo Mode", button_color)
    draw_button(multi_rect, "Fight Mode", button_color2)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            if solo_rect.collidepoint(x, y):
                if not os.path.exists("Touche.txt"):
                    messagebox.showinfo("Touches", "Voici les touches que vous pouvez utiliser au cours de ce mode de jeu :\n\n\t- Touche \"A\": Accéder au menu des améliorations\n\n\t- Touche \"G\": Accéder au menu des règles\n\n\t- Touche \"Esc\": Retour sur le jeu")
                    with open("Touche.txt", "w", encoding="utf8") as f:
                        f.write("Voici les touches que vous pouvez utiliser au cours de ce mode de jeu :\n\n\t- Touche \"A\": Accéder au menu des améliorations\n\n\t- Touche \"G\": Accéder au menu des règles\n\n\t- Touche \"Esc\": Retour sur le jeu")
                import Jeu_avec_pygame
            elif multi_rect.collidepoint(x, y):
                if not os.path.exists("Règles.txt"):
                    messagebox.showinfo("Règles", "Vous jouez en 1vs1 contre un ordinateur (cases rouges). Vous disposez de 5 cartes différentes à déposer dans la partie correspondante de la grille, chaque carte coûte un certain nombre de pixel indiqué (votre stock étant représenté par la barre verte), vous avez 5 minutes pour qu'une case bleue atteint le bord gauche de l'écran")
                    with open("Règles.txt", "w", encoding="utf8") as f:
                        f.write("Règles :\n\nVous jouez en 1vs1 contre un ordinateur (cases rouges). Vous disposez de 5 cartes différentes à déposer dans la partie\ncorrespondante de la grille, chaque carte coûte un certain nombre de pixel indiqué (votre stock étant représenté par la barre\nverte), vous avez 5 minutes pour qu'une case bleue atteint le bord gauche de l'écran")
                import FightMode
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

video.release()
pygame.quit()
