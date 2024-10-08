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

        for action in ['idle', 'walk', 'run', 'jump', 'attack_1', 'attack_2', 'attack_3', 'dead']:
            try:
                temp_list = []
                mask_list_temp = []
                frames_num = len(os.listdir(f'public/assets/new_animations/{self.char_type}/{action}'))
                for i in range(frames_num):
                    img = pygame.image.load(f'public/assets/new_animations/{self.char_type}/{action}/{i}_.png')
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                    # Crea una maschera per l'immagine corrente
                    mask_list_temp.append(pygame.mask.from_surface(img))
                self.animation_list.append(temp_list)
                self.mask_list.append(mask_list_temp)
                print(f'Loaded {action} animation with {frames_num} frames for {self.char_type}')  # Linea di debug
            except FileNotFoundError:
                # Se l'animazione non esiste, carica quella di default (ad esempio idle)
                print(f'Animation {action} not found for {self.char_type}')  # Linea di debug
                if action != 'idle':
                    self.animation_list.append(self.animation_list[0])  # Usa l'animazione idle come fallback
                    self.mask_list.append(self.mask_list[0])  # Usa la maschera di idle

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = self.mask_list[self.action][self.frame_index]

    def update(self):
        self.update_animation()
        self.check_alive()

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

            # Create an attack hitbox using sprite collision
            if isinstance(targets, pygame.sprite.Group):
                for target in settings.player_group:
                    if pygame.sprite.spritecollide(self, settings.player_group, False):
                        target.health -= 10  # Deal damage
                        
                        if target.health <= 0:
                            target.alive = False
            else:  # Otherwise, it's a single target (like the hero)
                if pygame.sprite.spritecollide(self, settings.player_group, False) and targets.alive:
                    targets.health -= 10
                    if targets.health <= 0:
                        targets.alive = False

    def update_animation(self):
        if pygame.time.get_ticks() - self.update_time > settings.ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if not self.alive and self.action != 7:  # 7 è l'azione 'dead'
                self.update_action(7)

            if self.frame_index >= len(self.animation_list[self.action]):
                if self.attacking:
                    self.attacking = False
                    self.combo_counter += 1
                    if self.combo_counter > 2:
                        self.combo_counter = 0  # Reset combo after the third attack
                    self.update_action(0)  # Return to "idle" action after attack

                if self.action == 7:  # Se l'azione è 'dead'
                    if self.frame_index >= len(self.animation_list[self.action]):
                        self.frame_index = len(self.animation_list[self.action]) - 1  # Blocca l'animazione sull'ultimo frame
                else:
                    self.frame_index = 0

            self.image = self.animation_list[self.action][self.frame_index]
            self.mask = self.mask_list[self.action][self.frame_index]  # Update the mask when the frame changes

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0  # Azzerare il frame_index
            self.update_time = pygame.time.get_ticks()
            self.mask = self.mask_list[self.action][self.frame_index]  # Update the mask for the new action

    def reset_combo(self):
        # Reset combo if too much time has passed
        if pygame.time.get_ticks() - self.combo_time > self.combo_duration:
            self.combo_counter = 0
            
    def check_alive(self):
        if self.health <= 0:
            self.alive = False
            self.speed = 0
            self.update_action(7)
            

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
        pygame.draw.rect(screen, (170, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Full bar
        pygame.draw.rect(screen, (0, 170, 0), (bar_x, bar_y, health_bar_width, bar_height))  # Current health

    def draw(self, screen):
        # Flip the image if needed
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        # Create mask
        self.mask = pygame.mask.from_surface(flipped_image)
        # Width of the image
        img_width = flipped_image.get_width()
        # If the character is flipped, align the image from the right side of the rect
        if self.flip:
            screen.blit(flipped_image, (self.rect.left - img_width / 2, self.rect.y))
        else:
            screen.blit(flipped_image, (self.rect.x, self.rect.y))

        self.draw_health_bar(screen)
