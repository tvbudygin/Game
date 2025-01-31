import os
import sys
import pygame
import random

ALL_SPRITES = pygame.sprite.Group()
ALL_SPRITES1 = pygame.sprite.Group()

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# переменная состояние, где сейчас находится игра, меню правила или сама игра
sostoanie = "menu"
# устанавливаем "имя"
pygame.display.set_caption("Тетрис")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Размеры блоков
BLOCK_SIZE = 30

# цвета фигур
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (100, 100, 100),
    (255, 255, 255),
    (128, 128, 128),
    (128, 0, 0),
    (0, 128, 0),
    (0, 0, 128),
    (128, 128, 0),
    (128, 0, 128),
    (0, 128, 128)
]

# Тетромино: фигуры
SHAPES = [
    [[1, 1, 1, 1]],  # линия
    [[1, 1], [1, 1]],  # квадрат
    [[0, 1, 0], [1, 1, 1]],  # T-образная
    [[1, 1, 0], [0, 1, 1]],  # Z-образная
    [[0, 1, 1], [1, 1, 0]],  # S-образная
    [[1, 0, 0], [1, 1, 1]],  # L-образная
    [[0, 0, 1], [1, 1, 1]],  # J-образная
]


# функция загрузки изображений
def load_image(name):
    base_dir = os.path.dirname(__file__)  # Папка, где находится скрипт
    fullname = os.path.join(base_dir, 'images', name)
    if not os.path.isfile(fullname):
        print(f'Файл {fullname} не найден.')
        sys.exit()
    return pygame.image.load(fullname)


# создаем фон
class Fon(pygame.sprite.Sprite):
    image = load_image("fon.png")

    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.image = Fon.image
        self.rect = self.image.get_rect()


# добавляем кнопку игры
class Play(pygame.sprite.Sprite):
    image = load_image("play.png")

    def __init__(self, size):
        super().__init__(ALL_SPRITES1)
        self.image = Play.image
        self.rect = pygame.Rect(112.5, 107.5, 75, 75)


# добавляем кнопку правил
class Rules(pygame.sprite.Sprite):
    image = load_image("rules.png")

    def __init__(self, size):
        super().__init__(ALL_SPRITES1)
        self.image = Rules.image
        self.rect = pygame.Rect(112.5, 262.5, 75, 75)


# добавляем кнопку выход
class Exit(pygame.sprite.Sprite):
    image = load_image("exit.png")

    def __init__(self, size):
        super().__init__(ALL_SPRITES1)
        self.image = Exit.image
        self.rect = pygame.Rect(112.5, 417.5, 75, 75)


# класс меню игры
class Menu:
    # Инициализация шрифта для отображения счёта
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)

    # Функция для выбора случайной фигуры
    def get_random_shape(self):
        return random.choice(SHAPES)

    # Функция для рисования фигуры
    def draw_shape(self, shape, x, y, color):
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    pygame.draw.rect(screen, color,
                                     (x + col * BLOCK_SIZE, y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Функция для отображения счёта
    def draw_score(self, screen, score):
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))  # Отображаем в верхнем левом углу

    # Главная игра
    def game_loop(self):
        clock = pygame.time.Clock()
        running = True
        current_shape = self.get_random_shape()
        current_x = (SCREEN_WIDTH // 2) - (len(current_shape[0]) * BLOCK_SIZE // 2)
        current_y = 0
        c = COLORS[random.randint(0, 14)]
        color = pygame.Color(c[0], c[1], c[2])

        # Инициализация счёта
        score = 0

        # переменные для проверки появления других фигур
        k = False
        k1 = False

        # координаты кнопок
        rect_play = pygame.Rect(112.5, 107.5, 75, 75)
        rect_rules = pygame.Rect(112.5, 262.5, 75, 75)
        rect_exit = pygame.Rect(112.5, 417.5, 75, 75)

        while running:
            global sostoanie

            if sostoanie == "menu":
                screen.fill(BLACK)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if rect_play.collidepoint(mouse_pos):
                            sostoanie = "game"
                        if rect_exit.collidepoint(mouse_pos):
                            sostoanie = "exit"
                        if rect_rules.collidepoint(mouse_pos):
                            sostoanie = "rules"

                ALL_SPRITES.draw(screen)

                # Рисуем текущую падающую фигуру
                self.draw_shape(current_shape, current_x, current_y, color)
                current_y += BLOCK_SIZE

                # Если фигура достигла низа экрана, создаем новую фигуру
                if current_y + len(current_shape) * BLOCK_SIZE > SCREEN_HEIGHT:
                    current_shape = self.get_random_shape()
                    current_x = (SCREEN_WIDTH // 2) - (len(current_shape[0]) * BLOCK_SIZE // 2)
                    current_y = 0
                    color = COLORS[random.randint(0, 14)]
                    score += 10  # Увеличиваем счёт

                # Отображаем счёт
                self.draw_score(screen, score)

                # Обработка второй фигуры
                if (current_y + len(current_shape) * BLOCK_SIZE) * 1.25 > SCREEN_HEIGHT and not k:
                    current_shape1 = self.get_random_shape()
                    current_x1 = 5
                    current_y1 = 0
                    color1 = COLORS[random.randint(0, 14)]
                    k = True

                if k:
                    self.draw_shape(current_shape1, current_x1, current_y1, color1)
                    current_y1 += BLOCK_SIZE
                    if current_y1 + len(current_shape) * BLOCK_SIZE > SCREEN_HEIGHT:
                        k = False

                # Обработка третьей фигуры
                if (current_y + len(current_shape) * BLOCK_SIZE) * 2 > SCREEN_HEIGHT and not k1:
                    current_shape2 = self.get_random_shape()
                    current_x2 = SCREEN_WIDTH - (len(current_shape[0]) * BLOCK_SIZE) - 5
                    current_y2 = 0
                    color2 = COLORS[random.randint(0, 14)]
                    k1 = True

                if k1:
                    self.draw_shape(current_shape2, current_x2, current_y2, color2)
                    current_y2 += BLOCK_SIZE
                    if current_y2 + len(current_shape) * BLOCK_SIZE > SCREEN_HEIGHT:
                        k1 = False

                ALL_SPRITES1.draw(screen)
                pygame.display.flip()

                clock.tick(10)

            elif sostoanie == "rules":
                from Rules import Rules_c
                a = Rules_c()
                a.rulse_f()
                sostoanie = "menu"
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.display.set_caption("Тетрис")

            elif sostoanie == "exit":
                from Exit import Exit_c
                a = Exit_c()
                b = a.exit_f()
                if not b:
                    running = False
                else:
                    sostoanie = "menu"
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.set_caption("Тетрис")

            elif sostoanie == "game":
                from Rezvushkin import game_loop
                game_loop()
                from Kuznetsov import Score
                Score()
                sostoanie = "menu"
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.display.set_caption("Тетрис")

        pygame.quit()


# создаем фон и кнопки
fon = Fon()
play = Play((SCREEN_WIDTH, SCREEN_HEIGHT))
rules = Rules((SCREEN_WIDTH, SCREEN_HEIGHT))
exits = Exit((SCREEN_WIDTH, SCREEN_HEIGHT))
# Запуск игры
game = Menu()
game.game_loop()
