import pygame
import settings
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        super().__init__()
        #moving variables
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
        self.frame_index = 0
        self.is_jumping = False
        self.in_air = True
        self.jump_count = 0
        self.attacking = False
        self.combo_counter = 0
        self.combo_time = 0
        self.combo_duration = 0

        # Load animations
        for action in ['idle', 'walk', 'run', 'jump', 'attack_1', 'attack_2', 'attack_3', 'dead']:
            temp_list = []
            frames_num = len(os.listdir(f'public/assets/new_animations/{self.char_type}/{action}'))
            for i in range(frames_num):
                img = pygame.image.load(f'public/assets/new_animations/{self.char_type}/{action}/{i}_.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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
        else:
            return

    def attack(self, targets):
        if not self.attacking:
            self.attacking = True
            self.combo_time = pygame.time.get_ticks()

            # Determina quale animazione di attacco usare in base al combo_counter
            if self.combo_counter == 0:
                self.update_action(4)  # attack_1
            elif self.combo_counter == 1:
                self.update_action(5)  # attack_2
            elif self.combo_counter == 2:
                self.update_action(6)  # attack_3

            self.frame_index = 0

            # Calcola la durata dell'animazione corrente
            num_frames = len(self.animation_list[self.action])
            attack_duration = settings.ANIMATION_COOLDOWN * num_frames
            self.combo_duration = attack_duration + 500

            # Crea una hitbox per l'attacco
            attack_rect = pygame.Rect(self.rect.centerx - (self.rect.width // 2) * self.direction, 
                                    self.rect.y, 
                                    self.rect.width, 
                                    self.rect.height)

            # Se il bersaglio è un gruppo (più nemici), itera su di essi
            if isinstance(targets, pygame.sprite.Group):
                for target in targets:
                    if attack_rect.colliderect(target.rect) and target.alive:
                        target.health -= 10  # Infligge danno
                        if target.health <= 0:
                            target.alive = False
                            target.update_action(7)  # Passa all'animazione "dead"
            else:  # Altrimenti, è un singolo bersaglio (come l'eroe)
                if attack_rect.colliderect(targets.rect) and targets.alive:
                    targets.health -= 10
                    if targets.health <= 0:
                        targets.alive = False
                        targets.update_action(7)



    def update_animation(self):
        if pygame.time.get_ticks() - self.update_time > settings.ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            # Se il nemico è morto e l'azione non è già impostata su "dead", aggiorna l'azione
            if not self.alive and self.action != 7:  # Supponendo che l'azione "dead" sia all'indice 7
                self.update_action(7)
            
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.attacking:
                    self.attacking = False
                    self.combo_counter += 1
                    if self.combo_counter > 2:
                        self.combo_counter = 0  # Reset combo dopo il terzo attacco
                    self.update_action(0)  # Ritorna all'azione "idle" dopo l'attacco

                # Se l'animazione "dead" è finita, non ripeterla
                if self.action == 7:  # L'animazione "dead"
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

            self.image = self.animation_list[self.action][self.frame_index]

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def reset_combo(self):
        # Reset combo if too much time has passed
        if pygame.time.get_ticks() - self.combo_time > self.combo_duration:
            self.combo_counter = 0

    def enemy_ai(self, player):
        if self.alive and player.alive:
            # Determina la direzione verso il giocatore
            if self.rect.x < player.rect.x:
                self.moving_right = True
                self.moving_left = False
                self.flip = False
            elif self.rect.x > player.rect.x:
                self.moving_right = False
                self.moving_left = True
                self.flip = True

            # Determina la distanza dal giocatore
            distance = abs(self.rect.x - player.rect.x)

            # Se il nemico è abbastanza vicino, attacca
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
        # Determina la larghezza della barra della salute in base alla salute corrente
        bar_width = self.rect.width / 2
        health_ratio = self.health / 100
        health_bar_width = int(bar_width * health_ratio)
        bar_height = 5

        # Determina la posizione della barra della salute (sopra la testa del personaggio)
        bar_x = self.rect.x
        bar_y = self.rect.y - bar_height - 5  # 5 pixels sopra la testa

        # Disegna la barra della salute
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Bar full
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_bar_width, bar_height))  # Current health


    def draw(self, screen):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        mask = pygame.mask.from_surface(flipped_image)
        offset = mask.get_bounding_rects()[0].x  # Get the exact offset of the non-empty part
        if self.flip:
            screen.blit(flipped_image, (self.rect.x - offset, self.rect.y))
        else:
            screen.blit(flipped_image, self.rect)
        
        # Disegna la barra della salute sopra la testa del personaggio
        self.draw_health_bar(screen)
