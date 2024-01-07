import pygame

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 30
SAND_HEIGHT = 10
font1 = ".\Press_Start_2P\PressStart2P-Regular.ttf"

back = (153, 0, 153)
mw = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Run")

musik = True


class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = filename

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Dinosaur:
    def __init__(self, name_img, jump_song, x, y):
        self.x = x
        self.y = y
        self.start_x = x  # Початкова позиція динозавра
        self.width = 50
        self.height = 40
        self.velocity = 0
        self.gravity = 0.75
        self.jumping = False
        self.name_img = name_img
        self.jump_song = jump_song

    def draw(self):
        mw.blit(self.name_img, (self.x, self.y))

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
            if musik:
                self.jump_song.play()


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


class Menu:
    def __init__(self):
        self._options = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        option_surface = pygame.font.Font(font1, 20).render(option, True, (83, 83, 83))
        self._options.append(option_surface)
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()
