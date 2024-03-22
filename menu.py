import sys
import time
from classes import *


# Screen dimensions
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 30
SAND_HEIGHT = 10
font1 = ".\Press_Start_2P\PressStart2P-Regular.ttf"
local_time = time.localtime()
month = local_time.tm_mon


if month > 3 and month < 11:
    sand_img = pygame.image.load("./imegs/textures/sand.png").convert()
    sky_img = pygame.image.load("./imegs/textures/nebo.png").convert()
else:
    sand_img = pygame.image.load("./imegs/textures/sand_new_Year.png").convert()
    sky_img = pygame.image.load("./imegs/textures/nebo_new_Year.png").convert()
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Background color and window initialization
mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Run")

# Variables for game execution control
running = True
sand_offset = 0


# Quit function
def quit_game():
    global running
    running = False


menu = Menu()


# Add options to the menu
def create_menu_option():
    from GoogleDinoRun import game_cicle

    menu.append_option("Start Game", game_cicle)
    menu.append_option("Quit", quit_game)


create_menu_option()

start_game_obg = Area(100, 70, 200, 20)
quit_obg = Area(100, 140, 80, 20)

def menu_run():
    global running, music, music_btns, switch_music_btn, start_game_obg, quit_obg, game_cicle, quit_obg
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
                elif event.key == pygame.K_v:
                    from mysic_func import change_music_state
                    change_music_state(switch_music_btn)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                from mysic_func import click_on_switch_music_btn
                click_on_switch_music_btn(switch_music_btn, event, 10)

                if start_game_obg.collidepoint(event.pos[0], event.pos[1]):
                    from GoogleDinoRun import game_cicle

                    game_cicle()
                if quit_obg.collidepoint(event.pos[0], event.pos[1]):
                    quit_game()

        mw.blit(sky_img, (0, 0))
        mw.blit(sand_img, (0, SCREEN_HEIGHT - GROUND_HEIGHT - SAND_HEIGHT + sand_offset))

        from classes import switch_music_btn
        from mysic_func import create_switch_music_btn
        create_switch_music_btn(switch_music_btn, 10)

        # Draw the menu
        for i, option_surface in enumerate(menu._options):
            option_rect = option_surface.get_rect()
            option_rect.topleft = (100, 70 + i * 70)
            if i == menu._current_option_index:
                pygame.draw.rect(mw, (0, 204, 204), option_rect)
            mw.blit(option_surface, option_rect)

        pygame.display.flip()

    sys.exit()
    pygame.quit()


menu_run()
