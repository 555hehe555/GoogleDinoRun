import pygame
from classes import SCREEN_WIDTH, Picture


def create_switch_music_btn(switch_music_btn, x):
    music_btn_img_path = "./imegs/buttons/musik_on.png" if switch_music_btn else "./imegs/buttons/musik_off.png "
    music_btn_img = pygame.image.load(music_btn_img_path)
    music_btn = Picture(music_btn_img, (SCREEN_WIDTH - music_btn_img.get_width() - x),
                        (music_btn_img.get_height() - 10), music_btn_img.get_width(),
                        music_btn_img.get_height())
    music_btn.fill()
    music_btn.draw()

    return music_btn


def change_music_state(switch_music_btn):
    if switch_music_btn:
        import classes as cl
        cl.switch_music_btn = False
        cl.music = False
    else:
        import classes as cl
        cl.switch_music_btn = True
        cl.music = True

def click_on_switch_music_btn(switch_music_btn, event, x):
    music_btn = create_switch_music_btn(switch_music_btn, x)
    if music_btn.collidepoint(event.pos[0], event.pos[1]):
        change_music_state(switch_music_btn)
