from classes import *
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
dinosaur_img = pygame.image.load("./imegs/dino/dino_k_new_Year.png")
sand_img = pygame.image.load("./imegs/textures/sand_new_Year.png")
sky_img = pygame.image.load("./imegs/textures/nebo_new_Year.png")
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
music_on_img = pygame.image.load("./imegs/buttons/musik_on.png")
music_off_img = pygame.image.load("./imegs/buttons/musik_off.png")

# Background color and window initialization
background = (153, 0, 153)
mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Run")
mw.fill(background)
clock = pygame.time.Clock()

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
    menu.append_option("about developers", lambda: print("about developers..."))


create_menu_option()



def menu_run():
    global running, music, music_btns
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
                    if switch_music_btn:
                        import classes as cl
                        cl.switch_music_btn = False
                        cl.music = False
                    else:
                        import classes as cl
                        cl.switch_music_btn = True
                        cl.music = True

            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # if musik_btn.collidepoint(event.pos[0], event.pos[1]):
                #     change_music_state()

        mw.blit(sky_img, (0, 0))
        mw.blit(sand_img, (0, SCREEN_HEIGHT - GROUND_HEIGHT - SAND_HEIGHT + sand_offset))

        # musik_btn.fill()
        # musik_btn.draw()
        from classes import switch_music_btn
        if switch_music_btn:
            print(1)
            music_on_btn = Picture(music_on_img, (SCREEN_WIDTH - music_on_img.get_width() - 10),
                                   (music_on_img.get_height() - 10), music_on_img.get_width(),
                                   music_on_img.get_height())
            music_btns = [music_on_btn]
        else:
            print(2)
            music_off_btn = Picture(music_off_img, (SCREEN_WIDTH - music_off_img.get_width() - 10),
                                    (music_off_img.get_height() - 10), music_off_img.get_width(),
                                    music_off_img.get_height())
            music_btns = [music_off_btn]
        print(f"debag{music_btns}")
        for music_btn in music_btns:
            music_btn.fill()
            music_btn.draw()

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
