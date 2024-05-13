import sys
import time

import pygame.mixer

from classes import *

# Screen dimensions
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 30
SAND_HEIGHT = 10
font1 = ".\\Press_Start_2P\\PressStart2P-Regular.ttf"
local_time = time.localtime()
month = local_time.tm_mon

if 3 < month < 11:
    sand_img = pygame.image.load("./imegs/textures/sand.png").convert()
    sky_img = pygame.image.load("./imegs/textures/nebo.png").convert()
else:
    sand_img = pygame.image.load("./imegs/textures/sand_new_Year.png").convert()
    sky_img = pygame.image.load("./imegs/textures/nebo_new_Year.png").convert()
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
plus_img = pygame.image.load("./imegs/buttons/plus.png").convert()
minus_img = pygame.image.load("./imegs/buttons/minus.png").convert()

# Background color and window initialization
mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Run")

# music
jump_sound = pygame.mixer.Sound("./sounds/jamp.mp3")
run_sound = pygame.mixer.Sound("./sounds/run_test.mp3")
background_sound = pygame.mixer.Sound("./sounds/portal_radio_tune.mp3")
sounds_sound = pygame.mixer.Sound("./sounds/sounds.mp3")
click_sound = pygame.mixer.Sound("./sounds/click.mp3")
switch_sound = pygame.mixer.Sound("./sounds/switching.mp3")

jamp_volm = 30
background_volm = 10
run_volm = 100
switch_volm = 100
click_volm = 50

running = True
sand_offset = 0


def run_mysic_volm():
    global running
    running = True


# Quit function
def quit_game():
    global running
    running = False


menu = Menu()


def switch_menu_func():
    from menu import menu_run, create_settings_option
    menu_run()


text_list = ["jamp", "run", "background", "switch", "click"]
volm_list = [jamp_volm, run_volm, background_volm, switch_volm, click_volm]
sound_list = [jump_sound, run_sound, background_sound, switch_sound, click_sound]


# Add options to the menu
def create_menu_option():
    menu._options = []
    menu.append_option("Back to menu", switch_menu_func)
    for text in text_list:
        menu.append_option(text, lambda: print())


create_menu_option()

back_to_menu_obg = Area(100, 45, 240, 20)

plus_obg_jamp = Picture(plus_img, (100 + (len(text_list[0])) * 20), 50 + 1 * 50, 32, 32)
minus_obg_jamp = Picture(minus_img, (100 + (len(text_list[0])) * 20) + 100, 50 + 1 * 50, 32, 32)

plus_obg_run = Picture(plus_img, (100 + (len(text_list[1])) * 20), 50 + 2 * 50, 32, 32)
minus_obg_run = Picture(minus_img, (100 + (len(text_list[1])) * 20) + 100, 50 + 2 * 50, 32, 32)

plus_obg_background = Picture(plus_img, (100 + (len(text_list[2])) * 20), 50 + 3 * 50, 32, 32)
minus_obg_background = Picture(minus_img, (100 + (len(text_list[2])) * 20) + 100, 50 + 3 * 50, 32, 32)

plus_obg_switch = Picture(plus_img, (100 + (len(text_list[3])) * 20), 50 + 4 * 50, 32, 32)
minus_obg_switch = Picture(minus_img, (100 + (len(text_list[3])) * 20) + 100, 50 + 4 * 50, 32, 32)

plus_obg_click = Picture(plus_img, (100 + (len(text_list[4])) * 20), 50 + 5 * 50, 32, 32)
minus_obg_click = Picture(minus_img, (100 + (len(text_list[4])) * 20) + 100, 50 + 5 * 50, 32, 32)

menu_select = 0


def start_mysic_volm_menu():
    global switch_music_btn, running, jamp_volm, run_volm, background_volm, click_volm, switch_volm, menu_select
    while running:
        if menu_select > 5:
            menu_select = 5
        elif menu_select < 0:
            menu_select = 0
        volm_list = [jamp_volm, run_volm, background_volm, switch_volm, click_volm]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP:
                    menu.switch(-1)
                    menu_select -= 1
                elif event.key == pygame.K_DOWN:
                    menu.switch(1)
                    menu_select += 1
                elif event.key == pygame.K_SPACE and menu_select == 0:
                    menu.select()

                if event.key == pygame.K_LEFT and menu_select == 1 or pygame.K_RIGHT and menu_select == 1:
                    pygame.mixer.stop()
                    if event.key == pygame.K_LEFT and jamp_volm < 100:
                        jamp_volm += 10
                    elif event.key == pygame.K_RIGHT and jamp_volm > 0:
                        jamp_volm -= 10
                    jump_sound.set_volume(jamp_volm / 100)
                    # volm_list = [jamp_volm, run_volm, background_volm, switch_volm, click_volm]
                    # volm_list[0] = jamp_volm
                if event.key == pygame.K_LEFT and menu_select == 2 or pygame.K_RIGHT and menu_select == 2:
                    pygame.mixer.stop()
                    if event.key == pygame.K_LEFT and run_volm < 100:
                        run_volm += 10
                    elif event.key == pygame.K_RIGHT and run_volm > 0:
                        run_volm -= 10
                    run_sound.set_volume(run_volm / 100)
                    volm_list = [jamp_volm, run_volm, background_volm, switch_volm, click_volm]

                if event.key == pygame.K_LEFT and menu_select == 3 or pygame.K_RIGHT and menu_select == 3:
                    pygame.mixer.stop()
                    if event.key == pygame.K_LEFT and background_volm < 100:
                        background_volm += 10
                    elif event.key == pygame.K_RIGHT and background_volm > 0:
                        background_volm -= 10
                    background_sound.set_volume(background_volm / 100)
                    volm_list = [jamp_volm, run_volm, background_volm, switch_volm, click_volm]

                if event.key == pygame.K_LEFT and menu_select == 4 or pygame.K_RIGHT and menu_select == 4:
                    pygame.mixer.stop()
                    if event.key == pygame.K_LEFT and switch_volm < 100:
                        switch_volm += 10
                    elif event.key == pygame.K_RIGHT and switch_volm > 0:
                        switch_volm -= 10
                    switch_sound.set_volume(switch_volm / 100)
                    volm_list = [jamp_volm, run_volm, background_volm, switch_volm, click_volm]

                if event.key == pygame.K_LEFT and menu_select == 5 or pygame.K_RIGHT and menu_select == 5:
                    pygame.mixer.stop()
                    if event.key == pygame.K_LEFT and click_volm < 100:
                        click_volm += 10
                    if event.key == pygame.K_RIGHT and click_volm > 0:
                        click_volm -= 10
                    click_sound.set_volume(click_volm / 100)
                    volm_list = [jamp_volm, run_volm, background_volm, switch_volm, click_volm]

                if event.key == pygame.K_v:
                    from mysic_func import change_music_state
                    change_music_state(switch_music_btn)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                from mysic_func import click_on_switch_music_btn
                click_on_switch_music_btn(switch_music_btn, event, 10)
                pygame.mixer.stop()
                if back_to_menu_obg.collidepoint(event.pos[0], event.pos[1]):
                    switch_menu_func()

                if plus_obg_jamp.collidepoint(event.pos[0], event.pos[1]) and jamp_volm < 100:
                    jamp_volm += 10
                    jump_sound.set_volume(jamp_volm / 100)
                    jump_sound.play()
                elif plus_obg_jamp.collidepoint(event.pos[0], event.pos[1]):
                    jump_sound.play()
                if minus_obg_jamp.collidepoint(event.pos[0], event.pos[1]) and jamp_volm > 0:
                    jamp_volm -= 10
                    jump_sound.set_volume(jamp_volm / 100)
                    jump_sound.play()

                if plus_obg_run.collidepoint(event.pos[0], event.pos[1]) and run_volm < 100:
                    run_volm += 10
                    run_sound.set_volume(run_volm / 100)
                    run_sound.play()
                elif minus_obg_run.collidepoint(event.pos[0], event.pos[1]):
                    run_sound.play()
                if minus_obg_run.collidepoint(event.pos[0], event.pos[1]) and run_volm > 0:
                    run_volm -= 10
                    run_sound.set_volume(run_volm / 100)
                    run_sound.play()

                if plus_obg_background.collidepoint(event.pos[0], event.pos[1]) and background_volm < 100:
                    background_volm += 10
                    background_sound.set_volume(background_volm / 100)
                    background_sound.play()
                elif plus_obg_background.collidepoint(event.pos[0], event.pos[1]):
                    background_sound.play()
                if minus_obg_background.collidepoint(event.pos[0], event.pos[1]) and background_volm > 0:
                    background_volm -= 10
                    background_sound.set_volume(background_volm / 100)
                    background_sound.play()

                if plus_obg_switch.collidepoint(event.pos[0], event.pos[1]) and switch_volm < 100:
                    switch_volm += 10
                    switch_sound.set_volume(switch_volm / 100)
                    switch_sound.play()
                elif minus_obg_switch.collidepoint(event.pos[0], event.pos[1]):
                    switch_sound.play()
                if minus_obg_switch.collidepoint(event.pos[0], event.pos[1]) and switch_volm > 0:
                    switch_volm -= 10
                    switch_sound.set_volume(switch_volm / 100)
                    switch_sound.play()

                if plus_obg_click.collidepoint(event.pos[0], event.pos[1]) and click_volm < 100:
                    click_volm += 10
                    click_sound.set_volume(jamp_volm / 100)
                    click_sound.play()
                elif plus_obg_click.collidepoint(event.pos[0], event.pos[1]):
                    click_sound.play()
                if minus_obg_click.collidepoint(event.pos[0], event.pos[1]) and click_volm > 0:
                    click_volm -= 10
                    click_sound.set_volume(click_volm / 100)
                    click_sound.play()

        mw.blit(sky_img, (0, 0))
        mw.blit(sand_img, (0, SCREEN_HEIGHT - GROUND_HEIGHT - SAND_HEIGHT + sand_offset))

        plus_obg_jamp.draw()
        draw_text(str(jamp_volm), 20, (83, 83, 83), (100 + (len(text_list[0])) * 20) + 40, 55 + 1 * 50) if volm_list[
                                                                                                                  0] == 100 else \
            draw_text(str(jamp_volm), 25, (83, 83, 83), (100 + (len(text_list[0])) * 20) + 43, 55 + 1 * 50)
        minus_obg_jamp.draw()

        plus_obg_run.draw()
        draw_text(str(volm_list[1]), 20, (83, 83, 83), (100 + (len(text_list[1])) * 20) + 40, 55 + 2 * 50) if volm_list[
                                                                                                                  1] == 100 else \
            draw_text(str(volm_list[1]), 25, (83, 83, 83), (100 + (len(text_list[1])) * 20) + 43, 55 + 2 * 50)
        minus_obg_run.draw()

        plus_obg_background.draw()
        draw_text(str(volm_list[2]), 20, (83, 83, 83), (100 + (len(text_list[2])) * 20) + 40, 55 + 3 * 50) if volm_list[
                                                                                                                  2] == 100 else \
            draw_text(str(volm_list[2]), 25, (83, 83, 83), (100 + (len(text_list[2])) * 20) + 43, 55 + 3 * 50)
        minus_obg_background.draw()

        plus_obg_switch.draw()
        draw_text(str(volm_list[3]), 20, (83, 83, 83), (100 + (len(text_list[3])) * 20) + 40, 55 + 4 * 50) if volm_list[
                                                                                                                  3] == 100 else \
            draw_text(str(volm_list[3]), 25, (83, 83, 83), (100 + (len(text_list[3])) * 20) + 43, 55 + 4 * 50)
        minus_obg_switch.draw()

        plus_obg_click.draw()
        draw_text(str(volm_list[4]), 20, (83, 83, 83), (100 + (len(text_list[4])) * 20) + 40, 55 + 5 * 50) if volm_list[
                                                                                                                  4] == 100 else \
            draw_text(str(volm_list[4]), 25, (83, 83, 83), (100 + (len(text_list[4])) * 20) + 43, 55 + 5 * 50)
        minus_obg_click.draw()

        darken_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        darken_surface.set_alpha(128)
        darken_surface.fill((0, 0, 0))

        from classes import switch_music_btn
        from mysic_func import create_switch_music_btn
        create_switch_music_btn(switch_music_btn, 10)

        # Draw the menu
        for i, option_surface in enumerate(menu._options):
            option_rect = option_surface.get_rect()
            option_rect.topleft = (100, 50 + i * 50)
            if i == menu.current_option_index:
                pygame.draw.rect(mw, (0, 204, 204), option_rect)
            mw.blit(option_surface, option_rect)

        pygame.display.flip()

    sys.exit()
    pygame.quit()
