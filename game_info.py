import sys
import time

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

# Background color and window initialization
mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Run")
clock = pygame.time.Clock()

menu = Menu()


def switch_menu_func():
    from menu import menu_run
    menu_run()


# Add options to the menu
def create_menu_option():
    menu._options = []
    menu.append_option("Back to menu", switch_menu_func)


language = "uk"
running = False


def run_game_info():
    global running
    running = True
    create_menu_option()  # Створюємо меню перед початком циклу

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu.select()

        mw.fill((0, 0, 0))  # Затемнений фон

        mw.blit(sky_img, (0, 0))
        mw.blit(sand_img, (0, SCREEN_HEIGHT - GROUND_HEIGHT - SAND_HEIGHT + 0))

        # Затемнений прямокутник
        darken_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        darken_rect.set_alpha(180)  # Задаємо прозорість (0 - повністю прозорий, 255 - повністю непрозорий)
        darken_rect.fill((0, 0, 0))
        mw.blit(darken_rect, (0, 0))

        # Змінили координати виводу тексту "Опис гри GoogleDinoRun:"
        draw_text("Опис гри GoogleDinoRun:", 24, (120, 120, 120), 30, 70)

        # Додали додаткові пропуски між рядками
        description_text = [
            "",
            "GoogleDinoRun - захоплива аркадна гра, ",
            "де ти керуєш веселим динозавриком,",
            "що біжить назустріч пригодам у прерії.",
            "Твоя мета - Пробігти як умога далі.",
            "як найбільше кактусів, поки зможеш. ",
            "Наскільки далеко ти зможеш забігти?",
            "",
            "Управління:",
            "    Пробіл: стрибати",
            "    Enter: вибрати опцію у меню",
            "    М: перейти до головного меню",
            "    P: ввести/вийти з режиму паузи",
            "    V: вмикати/вимикати звук",
            "",
            "Тримай в руках контроль над своїм динозавром,",
            "стрибай високо та уникай небезпеки!",
            "Приємної гри!",
        ]

        # Змінили координати виводу тексту "Опис гри GoogleDinoRun:"
        y_offset = 100  # Змінили відступ

        for line in description_text:
            draw_text(line, 16, (120, 120, 120), 30, y_offset)
            y_offset += 20

        # Відображаємо поточний пункт меню
        option_surface = menu._options[menu.current_option_index]
        option_rect = option_surface.get_rect()
        option_rect.topleft = (70, 30)
        pygame.draw.rect(mw, (0, 204, 204), option_rect)
        mw.blit(option_surface, option_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
