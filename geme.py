import pygame
import random
import time

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 30
SAND_HEIGHT = 10

back = (153, 0, 153)
mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Run")
mw.fill(back)
clock = pygame.time.Clock()

dinosaur_img = pygame.image.load("dino.png")
cactus_img = pygame.image.load("cactus_bigpng.png")
small_cactus_img = pygame.image.load("cactus_smol.png")
sand_img = pygame.image.load("sand.png")
sky_img = pygame.image.load("sky.png")
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
restart_img = pygame.image.load("restart.png")
pause_img = pygame.image.load("pause.png")
resume_img = pygame.image.load("enter.png")

def draw_text(text, size, color, x, y, align="topleft"):
    font = pygame.font.SysFont('Arial', size)
    label = font.render(text, True, color)
    text_rect = label.get_rect(**{align: (x, y)})
    mw.blit(label, text_rect)

class Dinosaur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
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

class Cactus:
    def __init__(self, x, image,
                 speed):
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

countdown_timer = 0  # Час таймера
show_countdown = True  # Показувати таймер на початку гри
resume_timer = 0  # Таймер для продовження гри після паузи
paused = False
pause_timer = 0
pause_cooldown = False
countdown_timer = 0

darken_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
darken_surface.set_alpha(128)
darken_surface.fill((0, 0, 0))

def draw_pause_screen():
    global pause_timer, paused, pause_cooldown
    mw.blit(darken_surface, (0, 0))  # Виводимо темніший екран
    draw_text("Пауза", 50, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, align="center")
    mw.blit(resume_img, (SCREEN_WIDTH // 2 - resume_img.get_width() // 2, SCREEN_HEIGHT // 2))

    # Оновлюємо таймер паузи
    pause_timer -= 1 / 60
    if pause_timer <= 0:
        pause_timer = 0
        pause_cooldown = True

    if not paused:
        pause_cooldown = False
        pause_timer = 3  # Запускаємо таймер паузи знову після виходу з паузи
        paused = True


# noinspection PyUnusedLocal
def draw_countdown():
    global countdown_timer, paused, game_over
    mw.blit(darken_surface, (0, 0))  # Виводимо темніший екран
    draw_text(str(int(countdown_timer) + 1), 100, (255, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, align="center")
    countdown_timer -= 1 / 60
    if countdown_timer <= 0:
        countdown_timer = 0
        paused = False
        game_over = False

    # Оновлюємо таймер паузи
    pause_timer -= 1 / 60
    if pause_timer <= 0:
        pause_timer = 1  # Скидаємо таймер на 1 секунду для наступного входу в паузу
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

# Завантаження рекорду з файлу
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

score = 0
start_time = time.time()
dinosaur = Dinosaur(100, SCREEN_HEIGHT - GROUND_HEIGHT - 40)
cacti = []
restart_delay = 1.5  # Затримка часу (у секундах) перед перезапуском гри після Game Over

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
            quit()

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
                print(1)
            else:
                cactus = Cactus(SCREEN_WIDTH, small_cactus_img, random.randint(3, 7))
                print(2)

            cacti.append(cactus)
            spawn_counter = 0
            next_cactus_time = random.randint(60, 120)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            dinosaur.jump()

        dinosaur.update()
        for cactus in cacti:
            cactus.update()

        for cactus in cacti:
            if dinosaur.x < cactus.x + cactus.width and dinosaur.x + dinosaur.width > cactus.x and \
                    dinosaur.y < cactus.y + cactus.height and dinosaur.y + dinosaur.height > cactus.y:
                game_over = True

        elapsed_time = int(time.time() - start_time)
        score = elapsed_time

    if game_over:
        draw_restart_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and restart_timer <= 0:
            dinosaur = Dinosaur(100, SCREEN_HEIGHT - GROUND_HEIGHT - 40)
            cacti = []
            spawn_counter = 0
            next_cactus_time = random.randint(60, 120)
            start_time = time.time()
            game_over = False
            restart_timer = restart_delay

    # Зменшуємо таймер перезапуску
    if restart_timer > 0:
        restart_timer -= 1 / 60


    for cactus in cacti:
        cactus.draw()

    if paused:
        draw_pause_screen()
    elif not game_over:
        draw_text(f"Очки: {score}", 20, (83, 83, 83), 67, 10, align="topright")
        draw_text(f"Рекорд: {high_score}", 20, (83, 83, 83), 10, 30, align="topleft")
        mw.blit(pause_img, (SCREEN_WIDTH - pause_img.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()
