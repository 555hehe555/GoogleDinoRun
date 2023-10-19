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

back = (153, 0, 153)
mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Run")
mw.fill(back)
clock = pygame.time.Clock()

dinosaur_img = pygame.image.load("./imegs/dino/dino.png")
cactus_img = pygame.image.load("./imegs/cactus/cactus_big.png")
small_cactus_img = pygame.image.load("./imegs/cactus/cactus_smol.png")
sand_img = pygame.image.load("./imegs/textures/sand.png")
sky_img = pygame.image.load("./imegs/textures/sky.png")
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
restart_img = pygame.image.load("./imegs/buttons/restart.png")
pause_img = pygame.image.load("./imegs/buttons/pause.png")
resume_img = pygame.image.load("./imegs/buttons/enter.png")

# music
jump_sound = pygame.mixer.Sound("./sounds/jamp.mp3")
run_sound = pygame.mixer.Sound("./sounds/run_test.mp3")
background_sound = pygame.mixer.Sound("./sounds/portal_radio_tune.mp3")
jump_sound.set_volume(0.3)
background_sound.set_volume(0.1)

def draw_text(text, size, color, x, y, align="topleft"):
    font = pygame.font.SysFont('Arial', size)
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
    dinosaur = Dinosaur(initial_dinosaur_x, initial_dinosaur_y)
    cacti = []
    score = 0
    start_time = time.time()
    game_over = False


# menu.append_option('Start', start_game)
# menu.append_option('Quit', quit)

class Dinosaur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x  # Початкова позиція динозавра
        self.width = 50
        self.height = 40
        self.velocity = 0
        self.gravity = 0.75
        self.jumping = False

    def draw(self):
        mw.blit(dinosaur_img, (self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.velocity = 0
            self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity = -15
            self.jumping = True
            jump_sound.play()

class Cactus:
    def __init__(self, x, image, speed):
        self.x = x
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - image.get_height()
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.speed = speed

    def draw(self):
        mw.blit(self.image, (self.x, self.y))

    def update(self):
        self.x -= self.speed

countdown_timer = 0
show_countdown = True
resume_timer = 0
paused = False
pause_timer = 0
pause_cooldown = False

darken_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
darken_surface.set_alpha(128)
darken_surface.fill((0, 0, 0))

def draw_pause_screen():
    global pause_timer, paused, pause_cooldown
    mw.blit(darken_surface, (0, 0))
    draw_text("Pause", 50, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, align="center")
    mw.blit(resume_img, (SCREEN_WIDTH // 2 - resume_img.get_width() // 2, SCREEN_HEIGHT // 2))

    pause_timer -= 1 / 60
    if pause_timer <= 0:
        pause_timer = 0
        pause_cooldown = True

    if not paused:
        pause_cooldown = False
        pause_timer = 3
        paused = True

def draw_countdown():
    global countdown_timer, paused, game_over, pause_timer
    mw.blit(darken_surface, (0, 0))
    draw_text(str(int(countdown_timer) + 1), 100, (255, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, align="center")
    countdown_timer -= 1 / 60
    if countdown_timer <= 0:
        countdown_timer = 0
        paused = False
        game_over = False

    pause_timer -= 1 / 60
    if pause_timer <= 0:
        pause_timer = 1
        paused = not paused

def handle_pause_input():
    global paused, show_countdown, countdown_timer, resume_timer
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        paused = not paused
        if paused:
            show_countdown = False
            resume_timer = 3
        else:
            show_countdown = True

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

try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

score = 0
start_time = time.time()
dinosaur = Dinosaur(100, SCREEN_HEIGHT - GROUND_HEIGHT - 40)
cacti = []
restart_delay = 1.5

def draw_restart_screen():
    draw_text("Game Over", 50, (83, 83, 83), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, align="center")
    mw.blit(restart_img, (SCREEN_WIDTH // 2 - restart_img.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
restart_timer = 0

while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
    mw.blit(sky_img, (0, 0))
    mw.blit(sand_img, (0, SCREEN_HEIGHT - GROUND_HEIGHT - SAND_HEIGHT + sand_offset))
    dinosaur.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not game_over:
                paused = not paused
                if paused:
                    show_countdown = False
                    resume_timer = 3
                else:
                    show_countdown = True


    handle_resume_input()

    if not game_over and not paused:
        spawn_counter += 1
        if spawn_counter >= next_cactus_time:
            if random.randint(0, 1) == 0:
                cactus = Cactus(SCREEN_WIDTH, cactus_img, random.randint(3, 7))
            else:
                cactus = Cactus(SCREEN_WIDTH, small_cactus_img, random.randint(3, 7))

            cacti.append(cactus)
            spawn_counter = 0
            next_cactus_time = random.randint(60, 120)


        keys = pygame.key.get_pressed()


        if keys[pygame.K_SPACE]:
            run_sound.stop()
            dinosaur.jump()

        if not dinosaur.jumping and run_sound.get_num_channels() == 0:
            run_sound.play()

        dinosaur.update()
        for cactus in cacti:
            cactus.update()

        for cactus in cacti:
            if dinosaur is not None and dinosaur.x < cactus.x + cactus.width and dinosaur.x + dinosaur.width > cactus.x and \
                    dinosaur.y < cactus.y + cactus.height and dinosaur.y + dinosaur.height > cactus.y:
                game_over = True

        elapsed_time = int(time.time() - start_time)
        score = elapsed_time

    if game_over:
        draw_restart_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and restart_timer <= 0:
            start_game()
            restart_timer = restart_delay
            background_sound.stop()
            # Після рестарту гри
            game_over = False
            dinosaur.x = 10  # Початкова позиція динозавра
            dinosaur.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40

    if restart_timer > 0:
        restart_timer -= 1 / 60

    for cactus in cacti:
        cactus.draw()

    if paused:
        draw_pause_screen()
        if background_sound.get_num_channels() == 0:
            background_sound.play()
    elif not game_over:
        score_x = 0
        if score_x <= 10:
            score_x = 77
        elif score <= 100:
            score_x =87

        draw_text(f"Score: {score}", 20, (83, 83, 83), score_x, 10, align="topright")
        draw_text(f"High Score: {high_score}", 20, (83, 83, 83), 10, 30, align="topleft")
        mw.blit(pause_img, (SCREEN_WIDTH - pause_img.get_width() - 10, 10))

    if not paused:
        background_sound.stop()

    pygame.display.flip()
    clock.tick(60)

# Збереження рекорду в файл
if score > high_score:
    with open("highscore.txt", "w") as file:
        file.write(str(score))

pygame.quit()
sys.exit()
