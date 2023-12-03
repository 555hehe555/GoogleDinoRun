import pygame
import sys

pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 30
SAND_HEIGHT = 10
font1 = ".\Press_Start_2P\PressStart2P-Regular.ttf"

# Load imagesm
dinosaur_img = pygame.image.load("./imegs/dino/dino_k.png")
sand_img = pygame.image.load("./imegs/textures/sand.png")
sky_img = pygame.image.load("./imegs/textures/sky.png")
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
musik_on_img = pygame.image.load("./imegs/buttons/musik_on.png")
musik_off_img = pygame.image.load("./imegs/buttons/musik_off.png")

# Background color and window initialization
background = (153, 0, 153)
mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Run")
mw.fill(background)
clock = pygame.time.Clock()

# Variables for game execution control
running = True
sand_offset = 0

class Menu:
    def __init__(self):
        self._options = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        option_surface = pygame.font.Font(font1, 20).render(option, True, (255, 255, 255))
        self._options.append(option_surface)
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

# Quit function
def quit_game():
    global running
    running = False
menu = Menu()

# Add options to the menu
def create_menu_option():
    from GoogleDinoRun_test import game_cicle

    menu.append_option("Start Game", game_cicle)
    menu.append_option("Quit", quit_game)
    menu.append_option("about developers", lambda: print("about developers..."))

create_menu_option()

def menu_run():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP:
                    menu.switch(-1)
                elif event.key == pygame.K_DOWN:
                    menu.switch(1)
                elif event.key == pygame.K_SPACE:
                    menu.select()

        mw.blit(sky_img, (0, 0))
        mw.blit(sand_img, (0, SCREEN_HEIGHT - GROUND_HEIGHT - SAND_HEIGHT + sand_offset))
        mw.blit(musik_on_img, (700, 10))

        # Draw the menu
        for i, option_surface in enumerate(menu._options):
            option_rect = option_surface.get_rect()
            option_rect.topleft = (100, 70 + i * 70)
            if i == menu._current_option_index:
                pygame.draw.rect(mw, (9, 100, 0), option_rect)
            mw.blit(option_surface, option_rect)

        pygame.display.flip()

    sys.exit()
    pygame.quit()

menu_run()
# if show_menu != False:
#     print("menu is running")
#     menu_run()