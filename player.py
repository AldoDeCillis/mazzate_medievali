import pygame
import settings
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        super().__init__()
        # Moving variables
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.alive = True
        self.health = 100
        self.update_time = pygame.time.get_ticks()
        self.speed = speed
        self.char_type = char_type
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.action = 0
        self.animation_list = []
        self.mask_list = []
        self.frame_index = 0
        self.is_jumping = False
        self.in_air = True
        self.jump_count = 0
        self.attacking = False
        self.combo_counter = 0
        self.combo_time = 0
        self.combo_duration = 0

        # Load animations and create masks
        for action in ['idle', 'walk', 'run', 'jump', 'attack_1', 'attack_2', 'attack_3', 'dead']:
            temp_list = []
            mask_list_temp = []
            frames_num = len(os.listdir(f'public/assets/new_animations/{self.char_type}/{action}'))
            for i in range(frames_num):
                img = pygame.image.load(f'public/assets/new_animations/{self.char_type}/{action}/{i}_.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
                # Create a mask for the current image
                mask_list_temp.append(pygame.mask.from_surface(img))
            self.animation_list.append(temp_list)
            self.mask_list.append(mask_list_temp)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = self.mask_list[self.action][self.frame_index]

    def move(self, moving_left, moving_right, moving_up, moving_down):
        dx = 0
        dy = 0

        if self.alive:
            if moving_left:
                dx = -self.speed
                self.direction = -1
                self.flip = True
            if moving_right:
                dx = self.speed
                self.direction = 1
                self.flip = False
            if moving_up:
                dy = -self.speed
            if moving_down:
                dy = self.speed

            if self.is_jumping and not self.in_air:
                self.vel_y = -20
                self.is_jumping = False
                self.in_air = True
                self.jump_count = 0

            # Apply gravity
            self.vel_y += settings.GRAVITY
            dy += self.vel_y
            
            # Check collision with floor
            if self.rect.bottom + dy > settings.SCREEN_HEIGHT:
                dy = settings.SCREEN_HEIGHT - self.rect.bottom
                self.vel_y = 0
                self.in_air = False

            self.rect.x += dx
            self.rect.y += dy

            # Update hitbox position to follow the player
            self.mask = self.mask_list[self.action][self.frame_index]
        else:
            return

    def attack(self, targets):
        if not self.attacking:
            self.attacking = True
            self.combo_time = pygame.time.get_ticks()

            # Determine which attack animation to use based on combo_counter
            if self.combo_counter == 0:
                self.update_action(4)  # attack_1
            elif self.combo_counter == 1:
                self.update_action(5)  # attack_2
            elif self.combo_counter == 2:
                self.update_action(6)  # attack_3

            self.frame_index = 0

            # Calculate the duration of the current animation
            num_frames = len(self.animation_list[self.action])
            attack_duration = settings.ANIMATION_COOLDOWN * num_frames
            self.combo_duration = attack_duration + 500

            # Create an attack hitbox using mask collision
            if isinstance(targets, pygame.sprite.Group):
                for target in targets:
                    offset = (target.rect.x - self.rect.x, target.rect.y - self.rect.y)
                    if self.mask.overlap(target.mask, offset) and target.alive:
                        target.health -= 10  # Deal damage
                        if target.health <= 0:
                            target.alive = False
                            target.update_action(7)  # Switch to "dead" animation
            else:  # Otherwise, it's a single target (like the hero)
                offset = (targets.rect.x - self.rect.x, targets.rect.y - self.rect.y)
                if self.mask.overlap(targets.mask, offset) and targets.alive:
                    targets.health -= 10
                    if targets.health <= 0:
                        targets.alive = False
                        targets.update_action(7)

    def update_animation(self):
        if pygame.time.get_ticks() - self.update_time > settings.ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            # If the enemy is dead and the action isn't already set to "dead", update the action
            if not self.alive and self.action != 7:
                self.update_action(7)
            
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.attacking:
                    self.attacking = False
                    self.combo_counter += 1
                    if self.combo_counter > 2:
                        self.combo_counter = 0  # Reset combo after the third attack
                    self.update_action(0)  # Return to "idle" action after attack

                # If the "dead" animation is finished, don't repeat it
                if self.action == 7:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

            self.image = self.animation_list[self.action][self.frame_index]
            self.mask = self.mask_list[self.action][self.frame_index]  # Update the mask when the frame changes

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.mask = self.mask_list[self.action][self.frame_index]  # Update the mask for the new action

    def reset_combo(self):
        # Reset combo if too much time has passed
        if pygame.time.get_ticks() - self.combo_time > self.combo_duration:
            self.combo_counter = 0

    def enemy_ai(self, player):
        if self.alive and player.alive:
            # Determine direction towards the player
            if self.rect.x < player.rect.x:
                self.moving_right = True
                self.moving_left = False
                self.flip = False
            elif self.rect.x > player.rect.x:
                self.moving_right = False
                self.moving_left = True
                self.flip = True

            # Determine distance from the player
            distance = abs(self.rect.x - player.rect.x)

            # If the enemy is close enough, attack
            if distance < 50:
                self.moving_left = False
                self.moving_right = False
                self.attack(player)
            else:
                self.moving_left = self.rect.x > player.rect.x
                self.moving_right = self.rect.x < player.rect.x
        else:
            self.moving_left = False
            self.moving_right = False

    def draw_health_bar(self, screen):
        # Determine the width of the health bar based on current health
        bar_width = self.rect.width / 4
        health_ratio = self.health / 100
        health_bar_width = int(bar_width * health_ratio)
        bar_height = 5

        # Determine the position of the health bar (above the character's head)
        bar_x = self.rect.x + bar_width / 2 + 2
        bar_y = self.rect.y - bar_height + 40  # 5 pixels above the head

        # Draw the health bar
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Full bar
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_bar_width, bar_height))  # Current health

    def draw(self, screen):
        # Disegna l'immagine del personaggio
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        mask = pygame.mask.from_surface(flipped_image)
        offset = mask.get_bounding_rects()[0].x  # Ottieni l'offset esatto della parte non vuota
        if self.flip:
            screen.blit(flipped_image, (self.rect.x - offset, self.rect.y))
        else:
            screen.blit(flipped_image, self.rect)

        # Disegna la maschera di collisione per il debug
        mask_outline = self.mask.outline()  # Ottieni i punti del contorno della maschera
        mask_outline = [(self.rect.x + p[0], self.rect.y + p[1]) for p in mask_outline]  # Adatta i punti alle coordinate globali
        if self.flip:
            mask_outline = [(self.rect.x + self.image.get_width() - p[0], p[1]) for p in mask_outline]  # Adatta i punti per l'immagine capovolta
        
        if mask_outline:
            pygame.draw.lines(screen, (0, 255, 0), True, mask_outline, 2)  # Disegna il contorno in verde

        # Disegna la barra della salute sopra la testa del personaggio
        self.draw_health_bar(screen)
