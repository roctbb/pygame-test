import pygame
from pygame import *
from game_platform import *
from player import Player

WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("RPG")

    bg = Ground(0, 0)

    timer = pygame.time.Clock()
    hero = Player(155, 155)
    left = right = up = down = False

    coins_count = 0

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    coins = []  # то, во что мы будем врезаться или опираться

    entities.add(bg)

    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    level = [
        "----------------------------------",
        "-    s               s           -",
        "-      c  s     c       --       -",
        "-    s  w                c       -",
        "-            --                  -",
        "-      c  w        s             -",
        "--            w        c         -",
        "-  s       s                     -",
        "-                   ----     --- -",
        "-    w    s    -----             -",
        "--                 -----         -",
        "-       c       c                -",
        "-  c                         --- -",
        "-            s                   -",
        "-                    c           -",
        "-      ---                       -",
        "-      -----                     -",
        "-   -------         ----         -",
        "-                                -",
        "-                         -      -",
        "-           c                --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]

    print(len(level[0]) * 32)
    print(len(level) * 32)

    x = 0
    y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "s":
                entities.add(Stone(x, y))
            if col == "w":
                water = Water(x, y)
                entities.add(water)
                platforms.append(water)
            if col == "c":
                coin = Coin(x, y)
                entities.add(coin)
                coins.append(coin)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля
    entities.add(hero)
    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while True:  # Основной цикл программы
        timer.tick(30)

        for e in pygame.event.get():  # Обрабатываем события

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False

            if e.type == QUIT:
                raise SystemExit("QUIT")

        camera.update(hero)
        hero.update(left, right, up, down, platforms)

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        for coin in coins:
            if sprite.collide_rect(hero, coin):
                coins.remove(coin)
                entities.remove(coin)
                coins_count += 1

        textsurface = myfont.render(f'Coins: {coins_count}', False, (255, 255, 255))
        screen.blit(textsurface, (20, 20))

        pygame.display.update()


if __name__ == "__main__":
    main()