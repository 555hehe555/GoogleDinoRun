from classes import *
import pygame
import random
import time
import sys

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 30
SAND_HEIGHT = 10
font1 = ".\Press_Start_2P\PressStart2P-Regular.ttf"

dinosaur_img = pygame.image.load("./imegs/dino/dino_k_new_Year.png")
cactus_img = pygame.image.load("./imegs/cactus/cactus_big_new_Year.png")
small_cactus_img = pygame.image.load("./imegs/cactus/cactus_smol_new_Year.png")
sand_img = pygame.image.load("./imegs/textures/sand_new_Year.png")
sky_img = pygame.image.load("./imegs/textures/nebo_new_Year.png")
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
restart_img = pygame.image.load("./imegs/buttons/restart.png")
pause_img = pygame.image.load("./imegs/buttons/pause.png")
resume_img = pygame.image.load("./imegs/buttons/enter.png")
menu_img = pygame.image.load("./imegs/buttons/dth.png")
musik_on_img = pygame.image.load("./imegs/buttons/musik_on.png")
musik_off_img = pygame.image.load("./imegs/buttons/musik_off.png")

# music
jump_sound = pygame.mixer.Sound("./sounds/jamp.mp3")
run_sound = pygame.mixer.Sound("./sounds/run_test.mp3")
background_sound = pygame.mixer.Sound("./sounds/portal_radio_tune.mp3")
sounds_sounds = pygame.mixer.Sound("./sounds/sounds.mp3")
jump_sound.set_volume(0.3)
background_sound.set_volume(0.1)
sounds_sounds.set_volume(0)

back = (153, 0, 153)
mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Run")
mw.fill(back)
clock = pygame.time.Clock()

debag = True


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
    dinosaur = Dinosaur(dinosaur_img, jump_sound, initial_dinosaur_x, initial_dinosaur_y)
    cacti = []
    score = 0
    start_time = time.time()
    game_over = False


musik_state_img = musik_on_img

pause_btn = Picture(pause_img, (SCREEN_WIDTH - pause_img.get_width() - 10), (pause_img.get_height() - 10),
                    pause_img.get_width(),
                    pause_img.get_height())
restart_btn = Picture(restart_img, (SCREEN_WIDTH // 2 - restart_img.get_width() // 2), (SCREEN_HEIGHT // 2 + 70),
                      restart_img.get_width(), restart_img.get_height())
resume_btn = Picture(resume_img, (SCREEN_WIDTH // 2 - resume_img.get_width() // 2), (SCREEN_HEIGHT // 2),
                     resume_img.get_width(), resume_img.get_height())
menu_btn = Picture(menu_img, (SCREEN_WIDTH - menu_img.get_width() - 10), (menu_img.get_height() - 10),
                   menu_img.get_width(), menu_img.get_height())

musik_btn = Picture(musik_state_img, (SCREEN_WIDTH - musik_state_img.get_width() - 67),
                    (musik_state_img.get_height() - 10), musik_state_img.get_width(),
                    musik_state_img.get_height())


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


def switch_btn_size(btn_name, btn_img, is_show):
    if is_show:
        btn_name.rect.size = (btn_img.get_width(), btn_img.get_height())
    else:
        btn_name.rect.size = (0, 0)


def draw_pause_screen():
    global pause_timer, paused, pause_cooldown
    mw.blit(darken_surface, (0, 0))
    draw_text("Pause", 25, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, align="center")
    # mw.blit(resume_img, (SCREEN_WIDTH // 2 - resume_img.get_width() // 2, SCREEN_HEIGHT // 2))
    resume_btn.fill()
    resume_btn.draw()
    # mw.blit(menu_img, (700, 10))
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
start_time = time.time()
dinosaur = Dinosaur(dinosaur_img, jump_sound, 100, SCREEN_HEIGHT - GROUND_HEIGHT - 40)
cacti = []
restart_delay = 1.5


def draw_restart_screen(score_x):
    draw_text("Game Over", 30, (83, 83, 83), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, align="center")
    # mw.blit(restart_img, (SCREEN_WIDTH // 2 - restart_img.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    restart_btn.fill()
    restart_btn.draw()
    # mw.blit(menu_img, (700, 10))
    menu_btn.fill()
    menu_btn.draw()
    draw_text(f"Score: {score}", 15, (83, 83, 83), score_x, 10, align="topright")
    draw_text(f"High Score: {high_score}", 15, (83, 83, 83), 10, 30, align="topleft")


restart_timer = 0
paused_score = 0
show_menu = True
elapsed_time_int, elapsed_time_float = 0, 0

def game_cicle():
    global show_menu, game_on, score, high_score, paused_score, switch_btn_size, debag, show_countdown, resume_timer, musik_state_img, musik, silent_game_over, elapsed_time_int, elapsed_time_float
    show_menu = False
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

                    dinosaur.x = 100  # Початкова позиція динозавра
                    dinosaur.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40

                if musik_btn.collidepoint(event.pos[0], event.pos[1]):
                    print("v preset")
                    if musik:
                        musik = False
                        musik_state_img = musik_off_img
                        print(f"debag musik - {musik}")
                    else:
                        musik = True
                        musik_state_img = musik_on_img
                        print(f"debag musik - {musik}")

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

                elif event.key == pygame.K_v:
                    print("v preset")
                    if musik:
                        musik = False
                        musik_state_img = musik_off_img
                        print(f"debag musik - {musik}")
                    else:
                        musik = True
                        musik_state_img = musik_on_img
                        print(f"debag musik - {musik}")

                if event.key == pygame.K_g:
                    game_over = True

                if event.key == pygame.K_r:
                    silent_game_over = True

                if event.key == pygame.K_c:
                    if debag:
                        debag = False
                    else:
                        debag = True

        handle_resume_input()

        if not game_over and not paused:
            switch_btn_size(musik_btn, musik_state_img, False)
            switch_btn_size(resume_btn, resume_img, False)
            switch_btn_size(restart_btn, restart_img, False)
            switch_btn_size(menu_btn, menu_img, False)

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

            if not dinosaur.jumping and run_sound.get_num_channels() == 0 and musik:
                run_sound.play()

            dinosaur.update()
            for cactus in cacti:
                cactus.update()

            for cactus in cacti:
                if dinosaur is not None and dinosaur.x < cactus.x + cactus.width and dinosaur.x + dinosaur.width > cactus.x and \
                        dinosaur.y < cactus.y + cactus.height and dinosaur.y + dinosaur.height > cactus.y:
                    if debag:
                        game_over = True
                    else:
                        game_over = False

            # print(f'score-{int(round(time.time()-1703358308.059905,0)-round(start_time-1703358307.5885847,0))}, paused_score-{paused_score}')

            elapsed_time_int = int(time.time() - start_time - paused_score)
            elapsed_time_float = float(time.time() - start_time - paused_score)
            elapsed_time_float = round(elapsed_time_float, 1)
            score = elapsed_time_int

            if keys[pygame.K_SPACE] and elapsed_time_float > 0.5:
                run_sound.stop()
                dinosaur.jump()

        score_x = 0
        if score_x <= 10:
            score_x = 165
        elif score <= 100:
            score_x = 253
        # score_x = SCREEN_HEIGHT - GROUND_HEIGHT - 340

        if game_over:
            switch_btn_size(resume_btn, resume_img, False)
            switch_btn_size(restart_btn, restart_img, True)
            switch_btn_size(menu_btn, menu_img, True)
            switch_btn_size(pause_btn, pause_img, False)

            draw_restart_screen(score_x)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and restart_timer <= 0:
                start_game()
                restart_timer = restart_delay
                background_sound.stop()
                # Після рестарту гри
                game_over = False
                paused_score = 0

                dinosaur.x = 100  # Початкова позиція динозавра
                dinosaur.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40

        if silent_game_over:
            switch_btn_size(resume_btn, resume_img, False)
            switch_btn_size(restart_btn, restart_img, True)
            switch_btn_size(menu_btn, menu_img, True)
            switch_btn_size(pause_btn, pause_img, False)

            if restart_timer <= 0:
                jump_sound.stop()
                start_game()
                restart_timer = restart_delay
                background_sound.stop()
                # Після рестарту гри
                silent_game_over = False
                paused_score = 0
                elapsed_time_int = 0
                elapsed_time_float = 0

                dinosaur.x = 100  # Початкова позиція динозавра
                dinosaur.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40


        if restart_timer > 0:
            restart_timer -= 1 / 60

        for cactus in cacti:
            cactus.draw()

        if paused:
            switch_btn_size(musik_btn, musik_state_img, True)
            switch_btn_size(resume_btn, resume_img, True)
            switch_btn_size(restart_btn, restart_img, False)
            switch_btn_size(menu_btn, menu_img, True)
            switch_btn_size(pause_btn, pause_img, False)
            draw_pause_screen()

            musik_btn.fill()
            musik_btn.draw()

            if background_sound.get_num_channels() == 0 and musik:
                background_sound.play()

            while sounds_sounds.get_num_channels() == 0:
                sounds_sounds.play()
                paused_score += 1
                # print(f"paused_score-{paused_score}")



        elif not game_over:
            switch_btn_size(pause_btn, pause_img, True)

            pause_btn.fill()
            pause_btn.draw()
            pause_btn.rect.size = (pause_img.get_width(), pause_img.get_height())
            draw_text(f"Score: {score}", 15, (83, 83, 83), score_x, 10, align="topright")
            draw_text(f"High Score: {high_score}", 15, (83, 83, 83), 10, 30, align="topleft")
            # mw.blit(pause_img, (SCREEN_WIDTH - pause_img.get_width() - 10, 10))

        if not paused:
            background_sound.stop()

        pygame.display.flip()
        clock.tick(60)

        # Збереження рекорду в файл
        if score > high_score and game_over:
            high_score = score
            with open("highscore.dat", "w") as file:
                file.write(str(high_score))
        # pygame.draw.rect(mw, (255, 0, 0), pause_btn.rect)  # Заливка області м'яча червоним кольором
        # pygame.draw.rect(mw, (255, 0, 0), resume_btn.rect)  # Заливка області м'яча червоним кольором
    pygame.quit()
    sys.exit()
