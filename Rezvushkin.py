import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 270
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((600, 600))
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


def draw():
    h = 0
    w = 0
    for i in range(SCREEN_HEIGHT // 30):
        for e in range(SCREEN_WIDTH // 30):
            color = pygame.Color(255, 255, 255)
            hsv = color.hsla
            color.hsla = (hsv[0], hsv[1], hsv[2] - 50, hsv[3])
            pygame.draw.rect(screen, color, (w, h, 30, 30), 1)
            w += 30
        h += 30
        w = 0


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
                    pygame.draw.rect(screen, self.color,
                                     (self.x + col * BLOCK_SIZE, self.y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def move_piece(self, dx):
        new_x = self.x + dx
        if new_x < 0:
            new_x = 0
        elif new_x + len(self.shape[0]) * BLOCK_SIZE > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH - len(self.shape[0]) * BLOCK_SIZE
        self.x = new_x

    def move_piece_y(self, dy):
        new_y = self.y + dy
        self.y = new_y

    def rotate(self):
        # Поворот фигуры на 90 градусов
        rows = len(self.shape)
        cols = len(self.shape[0])
        new_shape = [[0] * rows for _ in range(cols)]  # Создаем пустую матрицу с перевернутыми размерами
        print(new_shape)
        for row in range(rows):
            print(row, rows)
            for col in range(cols):
                print(col, cols)
                print(rows - 1 - row)
                new_shape[col][rows - row - 1] = self.shape[row][col]
        print(new_shape)

        # Проверяем, не выходит ли фигура за границы экрана
        if self.x + len(new_shape[0]) * BLOCK_SIZE <= SCREEN_WIDTH and self.y + len(
                new_shape) * BLOCK_SIZE <= SCREEN_HEIGHT:
            self.shape = new_shape


# Функция для выбора случайной фигуры
def get_random_shape():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return Tetromino(shape, color)


# Инициализация массива для хранения состояния экрана
def init_screen_state():
    screen_state = [[None for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    return screen_state


# Проверка столкновения с нижней частью экрана или другими фигурами
def check_collision(tetromino, screen_state):
    for row in range(len(tetromino.shape)):
        for col in range(len(tetromino.shape[row])):
            if tetromino.shape[row][col]:
                x = (tetromino.x + col * BLOCK_SIZE) // BLOCK_SIZE
                y = (tetromino.y + row * BLOCK_SIZE + BLOCK_SIZE) // BLOCK_SIZE
                if y >= len(screen_state) or screen_state[y][x] is not None:
                    return True
    return False


# Проверка достижения верха экрана
def check_top_collision(screen_state):
    for x in range(len(screen_state[0])):
        if screen_state[0][x] is not None:
            return True
    return False


# Добавление фигуры в состояние экрана
def add_to_screen_state(tetromino, screen_state):
    for row in range(len(tetromino.shape)):
        for col in range(len(tetromino.shape[row])):
            if tetromino.shape[row][col]:
                x = (tetromino.x + col * BLOCK_SIZE) // BLOCK_SIZE
                y = (tetromino.y + row * BLOCK_SIZE) // BLOCK_SIZE
                screen_state[y][x] = tetromino.color


# Рисование фигур из состояния экрана
def draw_from_screen_state(screen_state):
    for y in range(len(screen_state)):
        for x in range(len(screen_state[y])):
            if screen_state[y][x] is not None:
                pygame.draw.rect(screen, screen_state[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# Главная игра
def game_loop():
    clock = pygame.time.Clock()
    running = True
    screen_state = init_screen_state()
    current_tetromino = get_random_shape()

    while running:
        screen.fill((0, 0, 0))
        draw()
        # Отслеживание событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move_piece(-BLOCK_SIZE)
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move_piece(BLOCK_SIZE)
                elif event.key == pygame.K_DOWN:
                    current_tetromino.move_piece_y(BLOCK_SIZE)
                elif event.key == pygame.K_SPACE:
                    current_tetromino.rotate()

        # Рисуем падающую фигуру
        current_tetromino.draw()

        # Обновляем позицию фигуры
        if not check_collision(current_tetromino, screen_state):
            current_tetromino.y += BLOCK_SIZE
        else:
            add_to_screen_state(current_tetromino, screen_state)
            if check_top_collision(screen_state):  # проверка достигла ли фигура самого верха
                print("Игра окончена! Фигуры достигли верха экрана.")
                running = False
            else:
                current_tetromino = get_random_shape()

        # Рисуем фигуры из состояния экрана
        draw_from_screen_state(screen_state)
        pygame.display.flip()

        # Задержка, чтобы фигуры падали не слишком быстро
        clock.tick(4)

    pygame.quit()


# Запуск игры
game_loop()
