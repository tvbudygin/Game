import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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


class Menu:
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

    # Главная игра
    def game_loop(self):
        clock = pygame.time.Clock()
        running = True
        current_shape = self.get_random_shape()
        current_x = (SCREEN_WIDTH // 2) - (len(current_shape[0]) * BLOCK_SIZE // 2)
        current_y = 0
        c = COLORS[random.randint(0, 14)]
        c1 = COLORS[random.randint(0, 14)]
        c2 = COLORS[random.randint(0, 14)]
        color = pygame.Color(c[0], c[1], c[2])
        color1 = pygame.Color(c1[0], c1[1], c1[2])
        color2 = pygame.Color(c2[0], c2[1], c2[2])
        k = False
        k1 = False
        while color1 != color:
            color1 = COLORS[random.randint(0, 14)]

        while running:
            screen.fill(BLACK)

            # Отслеживание событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Рисуем  падающую фигуру
            self.draw_shape(current_shape, current_x, current_y, color)

            # Обновляем  позицию фигуры
            current_y += BLOCK_SIZE

            # Если фигура достигла низа экрана, создаем новую
            if current_y + len(current_shape) * BLOCK_SIZE > SCREEN_HEIGHT:
                current_shape = self.get_random_shape()
                current_x = (SCREEN_WIDTH // 2) - (len(current_shape[0]) * BLOCK_SIZE // 2)
                current_y = 0
                color = COLORS[random.randint(0, 14)]

            # добовляем вторую фигуру
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

            # добовляем третью фигуру
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

            pygame.display.flip()

            # Задержка, чтобы фигуры падали не слишком быстро
            clock.tick(10)

        pygame.quit()


# Запуск игры
game = Menu()
game.game_loop()
# конец