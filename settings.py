import pygame

# settings.py
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.5)
FPS = 60
BACKGROUND_PATH = 'public/assets/backgrounds/game_background_3.1.png'

player_group = pygame.sprite.Group()

#Game Settings
GRAVITY = 0.75
ANIMATION_COOLDOWN = 150