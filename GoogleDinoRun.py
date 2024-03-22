import random
import time
import sys
import pygame
from classes import Cactus, Dinosaur, Picture

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 30
SAND_HEIGHT = 10
font1 = ".\Press_Start_2P\PressStart2P-Regular.ttf"
local_time = time.localtime()
month = local_time.tm_mon

if month > 3 and month < 11:
    dinosaur_img = pygame.image.load("./imegs/dino/dino_k.png").convert_alpha()
    cactus_img = pygame.image.load("./imegs/cactus/cactus_big.png").convert_alpha()
    small_cactus_img = pygame.image.load("./imegs/cactus/cactus_smol.png").convert_alpha()
    sand_img = pygame.image.load("./imegs/textures/sand.png").convert()
    sky_img = pygame.image.load("./imegs/textures/nebo.png").convert()
else:
    dinosaur_img = pygame.image.load("./imegs/dino/dino_k_new_Year.png").convert_alpha()
    cactus_img = pygame.image.load("./imegs/cactus/cactus_big_new_Year.png").convert_alpha()
    small_cactus_img = pygame.image.load("./imegs/cactus/cactus_smol_new_Year.png").convert_alpha()
    sand_img = pygame.image.load("./imegs/textures/sand_new_Year.png").convert()
    sky_img = pygame.image.load("./imegs/textures/nebo_new_Year.png").convert()
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
restart_img = pygame.image.load("./imegs/buttons/restart.png").convert()
pause_img = pygame.image.load("./imegs/buttons/pause.png").convert()
resume_img = pygame.image.load("./imegs/buttons/enter.png").convert()
menu_img = pygame.image.load("./imegs/buttons/dth.png").convert()
music_on_img = pygame.image.load("./imegs/buttons/musik_on.png").convert()
music_off_img = pygame.image.load("./imegs/buttons/musik_off.png").convert()

# music
jump_sound = pygame.mixer.Sound("./sounds/jamp.mp3")
run_sound = pygame.mixer.Sound("./sounds/run_test.mp3")
background_sound = pygame.mixer.Sound("./sounds/portal_radio_tune.mp3")
sounds_sounds = pygame.mixer.Sound("./sounds/sounds.mp3")
jump_sound.set_volume(0.3)
background_sound.set_volume(0.1)
sounds_sounds.set_volume(0)

mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

debag = True
global_debag = True

def draw_text(text, size, color, x, y, align="topleft"):
    font = pygame.font.Font(font1, size)
    label = font.render(text, True, color)
    text_rect = label.get_rect(**{align: (x, y)})
    mw.blit(label, text_rect)


# Функція для початку гри
def start_game():
    global game_over, dinosaur, cacti, score, start_time

    # Зберегти початкову позицію динозавра
    initial_dinosaur_x = 10
    initial_dinosaur_y = SCREEN_HEIGHT - GROUND_HEIGHT - 40

    # Ініціалізуємо гру знову
    dinosaur = Dinosaur(dinosaur_img, initial_dinosaur_x, initial_dinosaur_y)
    cacti = []
    score = 0
    game_over = False


music_state_img = music_on_img

pause_btn = Picture(pause_img, (SCREEN_WIDTH - pause_img.get_width() - 10), (pause_img.get_height() - 10),
                    pause_img.get_width(),
                    pause_img.get_height())
restart_btn = Picture(restart_img, (SCREEN_WIDTH // 2 - restart_img.get_width() // 2), (SCREEN_HEIGHT // 2 + 70),
                      restart_img.get_width(), restart_img.get_height())
resume_btn = Picture(resume_img, (SCREEN_WIDTH // 2 - resume_img.get_width() // 2), (SCREEN_HEIGHT // 2),
                     resume_img.get_width(), resume_img.get_height())
menu_btn = Picture(menu_img, (SCREEN_WIDTH - menu_img.get_width() - 10), (menu_img.get_height() - 10),
                   menu_img.get_width(), menu_img.get_height())
music_btn = Picture(music_state_img, (SCREEN_WIDTH - music_state_img.get_width() - 67),
                    (music_state_img.get_height() - 10), music_state_img.get_width(),
                    music_state_img.get_height())

countdown_timer = 0
show_countdown = True
resume_timer = 0
paused = False
pause_timer = 0
pause_cooldown = False

game_on = True

darken_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
darken_surface.set_alpha(128)
darken_surface.fill((0, 0, 0))


def switch_btn_size(btn_name, is_show):
    if is_show:
        if btn_name == resume_btn:
            btn_name.rect.size = (128, 32)
        else:
            btn_name.rect.size = (32, 32)
    else:
        btn_name.rect.size = (0, 0)


def draw_pause_screen():
    global pause_timer, paused, pause_cooldown
    mw.blit(darken_surface, (0, 0))
    draw_text("Pause", 25, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, align="center")
    resume_btn.fill()
    resume_btn.draw()
    menu_btn.fill()
    menu_btn.draw()

    pause_timer -= 1 / 60
    if pause_timer <= 0:
        pause_timer = 0
        pause_cooldown = True

    if not paused:
        pause_cooldown = False
        pause_timer = 3
        paused = True



def handle_resume_input():
    global show_countdown, countdown_timer
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        show_countdown = True


speed = 5
spawn_counter = 0
sand_offset = 0
next_cactus_time = random.randint(60, 120)
game_over = False
silent_game_over = False

try:
    with open("highscore.dat", "r") as file:
        high_score = int(file.read())
except:
    open("highscore.dat", "w").close()
    high_score = 0

score = 0
start_time = None
dinosaur = Dinosaur(dinosaur_img, 100, SCREEN_HEIGHT - GROUND_HEIGHT - 40)
cacti = []
restart_delay = 1.5


def draw_restart_screen():
    draw_text("Game Over", 30, (83, 83, 83), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, align="center")
    restart_btn.fill()
    restart_btn.draw()
    menu_btn.fill()
    menu_btn.draw()
    draw_text(f"Score: {score}", 15, (83, 83, 83), 10, 10)
    draw_text(f"High Score: {high_score}", 15, (83, 83, 83), 10, 30)


restart_timer = 0
paused_score = 0
show_menu = True
elapsed_time = 0


def game_cicle():
    # noinspection PyGlobalUndefined
    global show_menu, game_on, score, high_score, paused_score, switch_btn_size, debag, show_countdown, resume_timer, \
        music, silent_game_over, elapsed_time, jump_sound, music_btn, switch_music_btn
    show_menu = False
    start_time = time.time()
    while not pygame.key.get_pressed()[pygame.K_ESCAPE] and game_on:
        mw.blit(sky_img, (0, 0))
        mw.blit(sand_img, (0, SCREEN_HEIGHT - GROUND_HEIGHT - SAND_HEIGHT + sand_offset))
        dinosaur.draw()
        global game_over, paused, spawn_counter, next_cactus_time, restart_timer
        a = clock.get_fps()
        print(a)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if menu_btn.collidepoint(event.pos[0], event.pos[1]):
                    paused = False
                    game_over = True
                    background_sound.stop()

                    from menu import menu_run
                    menu_run()
                    game_on = False

                if pause_btn.collidepoint(event.pos[0], event.pos[1]) and not game_over:
                    paused = not paused
                    if paused:
                        show_countdown = False
                        resume_timer = 3
                    else:
                        show_countdown = True

                if resume_btn.collidepoint(event.pos[0], event.pos[1]):
                    paused = False

                if restart_btn.collidepoint(event.pos[0], event.pos[1]) and restart_timer <= 0:
                    start_game()
                    restart_timer = restart_delay
                    background_sound.stop()
                    # Після рестарту гри
                    game_over = False
                    paused_score = 0
                    start_time = time.time()
                    dinosaur.x = 100  # Початкова позиція динозавра
                    dinosaur.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40


                from mysic_func import click_on_switch_music_btn
                if paused:
                    click_on_switch_music_btn(switch_music_btn, event, 74)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not game_over:
                    paused = not paused
                    if paused:
                        show_countdown = False
                        resume_timer = 3
                    else:
                        show_countdown = True

                if event.key == pygame.K_m:
                    paused = False
                    silent_game_over = True
                    background_sound.stop()
                    from menu import menu_run
                    menu_run()
                    game_on = False


                elif event.key == pygame.K_v and paused:
                    from mysic_func import change_music_state
                    change_music_state(switch_music_btn)

                if global_debag:
                    if event.key == pygame.K_g:
                        game_over = True

                    if event.key == pygame.K_r:
                        silent_game_over = True

                    if event.key == pygame.K_c:
                        if debag:
                            debag = False
                        else:
                            debag = True

                    if event.key == pygame.K_h:
                        with open("highscore.dat", "w"):
                            high_score = 0


        handle_resume_input()

        from classes import switch_music_btn
        if switch_music_btn:
            import classes as cl
            cl.music = True
        else:
            import classes as cl
            cl.music = False

        if not game_over and not paused:
            switch_btn_size(music_btn, False)
            switch_btn_size(resume_btn, False)
            switch_btn_size(restart_btn, False)
            switch_btn_size(menu_btn, False)

            spawn_counter += 1
            if spawn_counter >= next_cactus_time:
                if random.randint(0, 1) == 0:
                    cactus = Cactus(SCREEN_WIDTH, cactus_img, random.randint(5, 10))
                else:
                    cactus = Cactus(SCREEN_WIDTH, small_cactus_img, random.randint(5, 10))

                cacti.append(cactus)
                spawn_counter = 0
                next_cactus_time = random.randint(60, 120)

            keys = pygame.key.get_pressed()
            from classes import music
            print(music)

            if not dinosaur.jumping and run_sound.get_num_channels() == 0 and music:
                run_sound.play()

            dinosaur.update()
            for cactus in cacti:
                cactus.update()
                cactus.draw()

                if dinosaur is not None and dinosaur.x < cactus.x + cactus.width and dinosaur.x + dinosaur.width > cactus.x and \
                        dinosaur.y < cactus.y + cactus.height and dinosaur.y + dinosaur.height > cactus.y:
                    if debag:
                        game_over = True
                    else:
                        game_over = False

            if sounds_sounds.get_num_channels() == 0:
                sounds_sounds.play()
                paused_score += 0.5

            elapsed_time_int = int(paused_score)
            elapsed_time_float = float(paused_score)
            score = elapsed_time_int

            if keys[pygame.K_SPACE] and elapsed_time_float >= 0.5:
                run_sound.stop()
                dinosaur.jump()
                if jump_sound.get_num_channels() == 0 and music:
                    jump_sound.play()

            if dinosaur.y == (SCREEN_HEIGHT - GROUND_HEIGHT - 40):
                jump_sound.stop()

        if game_over:
            switch_btn_size(resume_btn, False)
            switch_btn_size(restart_btn, True)
            switch_btn_size(menu_btn, True)
            switch_btn_size(pause_btn, False)

            for cactus in cacti:
                cactus.draw()

            draw_restart_screen()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and restart_timer <= 0:
                start_game()
                restart_timer = restart_delay
                background_sound.stop()
                # Після рестарту гри
                game_over = False
                paused_score = 0
                start_time = time.time()
                dinosaur.x = 100  # Початкова позиція динозавра
                dinosaur.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40

        if silent_game_over:
            switch_btn_size(resume_btn, False)
            switch_btn_size(restart_btn, True)
            switch_btn_size(menu_btn, True)
            switch_btn_size(pause_btn, False)

            if restart_timer <= 0:
                jump_sound.stop()
                start_game()
                restart_timer = restart_delay
                background_sound.stop()
                # Після рестарту гри
                silent_game_over = False
                paused_score = 0
                elapsed_time = 0

                dinosaur.x = 100  # Початкова позиція динозавра
                dinosaur.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40

        if restart_timer > 0:
            restart_timer -= 1 / 60


        if paused:
            switch_btn_size(music_btn, True)
            switch_btn_size(resume_btn, True)
            switch_btn_size(restart_btn, False)
            switch_btn_size(menu_btn, True)
            switch_btn_size(pause_btn, False)

            for cactus in cacti:
                cactus.draw()

            draw_pause_screen()



            from classes import switch_music_btn
            from mysic_func import create_switch_music_btn
            if paused:
                create_switch_music_btn(switch_music_btn, 74)

            from classes import music
            if not music:
                background_sound.stop()

            if background_sound.get_num_channels() == 0 and music:
                background_sound.play()


        elif not game_over:
            switch_btn_size(pause_btn, True)

            pause_btn.fill()
            pause_btn.draw()
            pause_btn.rect.size = (pause_img.get_width(), pause_img.get_height())
            draw_text(f"Score: {score}", 15, (83, 83, 83), 10, 10)
            draw_text(f"High Score: {high_score}", 15, (83, 83, 83), 10, 30)

        if not paused:
            background_sound.stop()

        pygame.display.flip()
        clock.tick(60)

        # Збереження рекорду в файл
        if score > high_score and game_over:
            high_score = score
            with open("highscore.dat", "w") as file:
                file.write(str(high_score))
    pygame.quit()
    sys.exit()
