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

# Цвета фигур
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

# Класс для фигур
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = (SCREEN_WIDTH // 2) - (len(shape[0]) * BLOCK_SIZE // 2)
        self.y = 0

    def draw(self):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    pygame.draw.rect(screen, self.color, (self.x + col * BLOCK_SIZE, self.y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def move_piece(self, dx):
        new_x = self.x + dx
        if new_x < 0:
            new_x = 0
        elif new_x + len(self.shape[0]) * BLOCK_SIZE > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH - len(self.shape[0]) * BLOCK_SIZE
        self.x = new_x

# Функция для выбора случайной фигуры
def get_random_shape():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return Tetromino(shape, color)

# Главная игра
def game_loop():
    clock = pygame.time.Clock()
    running = True
    current_tetromino = get_random_shape()

    while running:
        screen.fill(BLACK)

        # Отслеживание событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move_piece(-BLOCK_SIZE)
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move_piece(BLOCK_SIZE)

        # Рисуем падающую фигуру
        current_tetromino.draw()

        # Обновляем позицию фигуры
        current_tetromino.y += BLOCK_SIZE

        # Если фигура достигла низа экрана, создаем новую
        if current_tetromino.y + len(current_tetromino.shape) * BLOCK_SIZE > SCREEN_HEIGHT:
            current_tetromino = get_random_shape()

        pygame.display.flip()

        # Задержка, чтобы фигуры падали не слишком быстро
        clock.tick(10)

    pygame.quit()

# Запуск игры
game_loop()