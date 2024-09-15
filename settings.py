import pygame

# Dimensioni della finestra
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768 #int(SCREEN_WIDTH * 0.5)

# FPS e altre impostazioni globali
FPS = 60
BACKGROUND_PATH = 'public/assets/backgrounds/game_background_3.1.png'

# Gruppi di sprite
player_group = pygame.sprite.Group()

# Impostazioni di gioco
GRAVITY = 0.75
ANIMATION_COOLDOWN = 150

# Inizializzazione pygame e creazione della finestra
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
