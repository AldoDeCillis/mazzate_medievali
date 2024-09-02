# main.py
import pygame
from player import Player
import settings

pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

background = pygame.image.load(settings.BACKGROUND_PATH)

# Hero action variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Create player instance
hero = Player('hero', settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, 1, 4)

def draw_bg():
    screen.blit(background, (0, 0))
    pygame.draw.line(screen, 'black', (0, settings.SCREEN_HEIGHT), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

# Game loop
while True:
    clock.tick(settings.FPS)

    draw_bg()

    if hero.alive:
        # Se il giocatore è in salto
        if hero.in_air:
            hero.update_action(3)  # Cambia in "jump" se sta saltando
        # Se il giocatore sta correndo (con LSHIFT premuto)
        elif moving_left or moving_right or moving_up or moving_down:
            if hero.speed > 4:  # Controlla se la velocità è maggiore di quella normale
                hero.update_action(2)  # Cambia in "run" se c'è movimento rapido
            else:
                hero.update_action(1)  # Cambia in "walk" se c'è movimento normale
        else:
            hero.update_action(0)  # Cambia in "idle" se non c'è movimento

    hero.move(moving_left, moving_right, moving_up, moving_down)
    hero.update_animation()
    hero.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_UP:
                moving_up = True
            if event.key == pygame.K_DOWN:
                moving_down = True
            if event.key == pygame.K_LSHIFT:
                hero.speed = 6  # Aumenta la velocità per la corsa
            if event.key == pygame.K_SPACE and hero.alive and not hero.is_jumping:
                hero.is_jumping = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_DOWN:
                moving_down = False
            if event.key == pygame.K_LSHIFT:
                hero.speed = 4  # Ripristina la velocità normale
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
