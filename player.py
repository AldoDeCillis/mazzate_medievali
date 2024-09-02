import pygame
import settings
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        super().__init__()
        self.alive = True
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
        
        # Load animations
        for action in ['idle', 'walk', 'run', 'jump']:
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

        if self.is_jumping and self.in_air == False:
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

    def update_animation(self):
        ANIMATION_COOLDOWN = 150  # Time in milliseconds between frames
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            self.image = self.animation_list[self.action][self.frame_index]

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, screen):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        mask = pygame.mask.from_surface(flipped_image)
        offset = mask.get_bounding_rects()[0].x  # Ottieni l'offset esatto della parte non vuota
        if self.flip:
            screen.blit(flipped_image, (self.rect.x - offset, self.rect.y))
        else:
            screen.blit(flipped_image, self.rect)