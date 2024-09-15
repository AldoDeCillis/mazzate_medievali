import pygame
import settings

# Variabili per i font
font = None
small_font = None

# Opzioni del menu
menu_options = ["Start Game", "Options"]
selected_option = 0  # 0: Start Game, 1: Options

# Funzione per inizializzare i font (da chiamare dopo pygame.init())
def init_fonts():
    global font, small_font
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

# Funzione per disegnare il menu
def draw_menu(screen):
    screen.fill((0, 0, 0))  # Sfondo nero
    # Titolo del gioco
    title = font.render("My Game", True, (255, 255, 255))
    screen.blit(title, (settings.SCREEN_WIDTH // 2 - title.get_width() // 2, settings.SCREEN_HEIGHT // 4))
    
    # Opzioni del menu
    for i, option in enumerate(menu_options):
        text = small_font.render(option, True, (255, 255, 255))
        screen.blit(text, (settings.SCREEN_WIDTH // 2 - text.get_width() // 2, settings.SCREEN_HEIGHT // 2 + i * 40))
    
    # Indicatore dell'opzione selezionata
    dot_y = settings.SCREEN_HEIGHT // 2 + selected_option * 40
    pygame.draw.circle(screen, (255, 0, 0), (settings.SCREEN_WIDTH // 2 - 100, dot_y + 20), 10)

# Funzione per gestire l'input del menu
def handle_menu_input():
    global selected_option
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            if event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            if event.key == pygame.K_RETURN:
                if selected_option == 0:  # Start Game
                    return True  # Avvia il gioco
                elif selected_option == 1:  # Options
                    print("Options selected")
    return False
