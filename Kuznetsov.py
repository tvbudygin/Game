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

# Функция для выбора случайной фигуры
def get_random_shape():
    return random.choice(SHAPES)

# Функция для рисования фигуры
def draw_shape(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                pygame.draw.rect(screen, WHITE, (x + col * BLOCK_SIZE, y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Главная игра
def game_loop():
    clock = pygame.time.Clock()
    running = True
    current_shape = get_random_shape()
    current_x = (SCREEN_WIDTH // 2) - (len(current_shape[0]) * BLOCK_SIZE // 2)
    current_y = 0

    while running:
        screen.fill(BLACK)

        # Отслеживание событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Рисуем падающую фигуру
        draw_shape(current_shape, current_x, current_y)

        # Обновляем  позицию фигуры
        current_y += BLOCK_SIZE

        # Если фигура достигла низа экрана, создаем новую
        if current_y + len(current_shape) * BLOCK_SIZE > SCREEN_HEIGHT:
            current_shape = get_random_shape()
            current_x = (SCREEN_WIDTH // 2) - (len(current_shape[0]) * BLOCK_SIZE // 2)
            current_y = 0

        pygame.display.flip()

        # Задержка, чтобы фигуры падали не слишком быстро
        clock.tick(10)

    pygame.quit()

# Запуск игры
game_loop()
