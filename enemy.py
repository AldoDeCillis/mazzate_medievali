import pygame
from player import Player

class Enemy(Player):
    def __init__(self, char_type, x, y, scale, speed):
        super().__init__(char_type, x, y, scale, speed)

    def enemy_ai(self, player):
        if self.alive and player.alive:
            if self.rect.x < player.rect.x:
                self.moving_right = True
                self.moving_left = False
                self.flip = False
            elif self.rect.x > player.rect.x:
                self.moving_right = False
                self.moving_left = True
                self.flip = True

            distance = abs(self.rect.x - player.rect.x)

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
