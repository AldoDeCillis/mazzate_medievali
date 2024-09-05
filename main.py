import pygame
from player import Player
import settings

pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

background = pygame.image.load(settings.BACKGROUND_PATH)

# Create player instance
hero = Player('hero', settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, 1, 4)

# Creazione di più nemici
# settings.player_group.add(Player('enemy', 200, settings.SCREEN_HEIGHT // 2, 1, 4))
# settings.player_group.add(Player('enemy', 400, settings.SCREEN_HEIGHT // 2, 1, 4))

def draw_bg():
    screen.blit(background, (0, 0))
    pygame.draw.line(screen, 'black', (0, settings.SCREEN_HEIGHT), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

# Game loop
while True:
    clock.tick(settings.FPS)

    draw_bg()

    if hero.alive:
        # Reset combo if too much time has passed since the last attack
        hero.reset_combo()

        # Handle movement and action states
        if hero.attacking:
            hero.update_action(4 + hero.combo_counter)  # Ensure the correct attack animation is active if attacking
        elif hero.in_air:
            hero.update_action(3)  # Jumping
        elif hero.moving_left or hero.moving_right or hero.moving_up or hero.moving_down:
            if hero.speed > 4:
                hero.update_action(2)  # Running
            else:
                hero.update_action(1)  # Walking
        else:
            hero.update_action(0)  # Idle

    hero.move(hero.moving_left, hero.moving_right, hero.moving_up, hero.moving_down)
    hero.update_animation()
    hero.draw(screen)

    # Enemy behavior
    for enemy in settings.player_group:
        if enemy.alive:
            enemy.enemy_ai(hero)  # AI del nemico che gestisce il movimento e l'attacco
            enemy.move(enemy.moving_left, enemy.moving_right, False, False)  # Il nemico si muove solo orizzontalmente
            # Handle movement and action states
            if enemy.attacking:
                enemy.update_action(4 + enemy.combo_counter)  # Ensure the correct attack animation is active if attacking
            elif enemy.in_air:
                enemy.update_action(3)  # Jumping
            elif enemy.moving_left or enemy.moving_right or enemy.moving_up or enemy.moving_down:
                if enemy.speed > 4:
                    enemy.update_action(2)  # Running
                else:
                    enemy.update_action(1)  # Walking
            else:
                enemy.update_action(0)  # Idle
        else:
            enemy.update_action(7)
        enemy.update_animation()
        enemy.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                hero.moving_left = True
            if event.key == pygame.K_RIGHT:
                hero.moving_right = True
            if event.key == pygame.K_UP:
                hero.moving_up = True
            if event.key == pygame.K_DOWN:
                hero.moving_down = True
            if event.key == pygame.K_LSHIFT:
                hero.speed = 6  # Running
            if event.key == pygame.K_SPACE and hero.alive and not hero.is_jumping:
                hero.is_jumping = True
            if event.key == pygame.K_a and hero.alive and not hero.attacking:
                hero.attack(settings.player_group)  # Passa il gruppo di nemici come bersagli

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                hero.moving_left = False
            if event.key == pygame.K_RIGHT:
                hero.moving_right = False
            if event.key == pygame.K_UP:
                hero.moving_up = False
            if event.key == pygame.K_DOWN:
                hero.moving_down = False
            if event.key == pygame.K_LSHIFT:
                hero.speed = 4  # Normal speed

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
