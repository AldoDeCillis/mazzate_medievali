import pygame
import settings
import menu

def run_game_loop(hero, draw_bg):
    menu.init_fonts()  # Inizializza i font

    game_running = False
    while True:
        settings.clock.tick(settings.FPS)

        if not game_running:
            menu.draw_menu(settings.screen)
            game_running = menu.handle_menu_input()
        else:
            # Gestione degli eventi di input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
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
                        hero.speed = 6  # Corsa
                    if event.key == pygame.K_SPACE and hero.alive and not hero.is_jumping:
                        hero.is_jumping = True
                    if event.key == pygame.K_a and hero.alive and not hero.attacking:
                        hero.attack(settings.player_group)

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
                        hero.speed = 4  # Velocità normale

            draw_bg()
            
            hero.move(hero.moving_left, hero.moving_right, hero.moving_up, hero.moving_down)
            hero.update()
            if hero.alive:
                hero.reset_combo()
                if hero.attacking:
                    hero.update_action(4 + hero.combo_counter)
                elif hero.in_air:
                    hero.update_action(3)
                elif hero.moving_left or hero.moving_right or hero.moving_up or hero.moving_down:
                    if hero.speed > 4:
                        hero.update_action(2)
                    else:
                        hero.update_action(1)
                else:
                    hero.update_action(0)
            hero.update_animation()
            hero.draw(settings.screen)

            for enemy in settings.player_group:
                if enemy.alive:
                    enemy.enemy_ai(hero)
                    enemy.move(enemy.moving_left, enemy.moving_right, False, False)
                    enemy.update()
                    if enemy.attacking:
                        enemy.update_action(4 + enemy.combo_counter)
                    elif enemy.in_air:
                        enemy.update_action(3)
                    elif enemy.moving_left or enemy.moving_right:
                        if enemy.speed > 4:
                            enemy.update_action(2)
                        else:
                            enemy.update_action(1)
                    else:
                        enemy.update_action(0)
                enemy.update_animation()
                enemy.draw(settings.screen)

        pygame.display.update()
