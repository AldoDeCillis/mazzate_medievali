import pygame
from player import Player
from enemy import Enemy
import settings
import game  # Import del modulo game

# Carica lo sfondo
background = pygame.image.load(settings.BACKGROUND_PATH)

# Crea un'istanza del player
hero = Player('hero', settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, 1, 4)
# Crea un nemico
skeleton = Enemy('skeleton', 0, settings.SCREEN_HEIGHT // 2, 1, 4)

# Aggiungi il nemico al gruppo
settings.player_group.add(skeleton)

def draw_bg():
    settings.screen.blit(background, (0, 0))
    pygame.draw.line(settings.screen, 'black', (0, settings.SCREEN_HEIGHT), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), 2)

# Avvia il gioco
if __name__ == "__main__":
    game.run_game_loop(hero, draw_bg)
