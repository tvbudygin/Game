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


class MusicPlayer:
    def __init__(self, game_music_path):
        self.game_music_path = game_music_path
        self.current_music = None
        pygame.mixer.init()

    def play_game_music(self):
        if self.current_music != self.game_music_path:
            pygame.mixer.music.load(self.game_music_path)
            pygame.mixer.music.play(-1)
            self.current_music = self.game_music_path

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None


class Menu:
    def __init__(self, music_player):
        self.score = 0  # Инициализация счета
        self.grid = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.music_player = music_player

    def get_random_shape(self):
        return random.choice(SHAPES)

    def draw_shape(self, shape, x, y, color):
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    pygame.draw.rect(screen, color,
                                     (x + col * BLOCK_SIZE, y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def check_lines(self):
        lines_to_clear = []
        for row in range(len(self.grid)):
            if all(self.grid[row]):
                lines_to_clear.append(row)

        for row in lines_to_clear:
            del self.grid[row]
            self.grid.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
            self.score += 100

    def update_grid(self, shape, x, y):
        grid_x = x // BLOCK_SIZE
        grid_y = y // BLOCK_SIZE

        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    self.grid[grid_y + row][grid_x + col] = 1

    def game_loop(self):
        clock = pygame.time.Clock()
        running = True
        current_shape = self.get_random_shape()
        current_x = (SCREEN_WIDTH // 2) - (len(current_shape[0]) * BLOCK_SIZE // 2)
        current_y = 0
        color = random.choice(COLORS)

        # Запуск музыки
        self.music_player.play_game_music()

        while running:
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_shape(current_shape, current_x, current_y, color)
            current_y += BLOCK_SIZE

            if current_y + len(current_shape) * BLOCK_SIZE > SCREEN_HEIGHT or \
                    any(self.grid[(current_y + row * BLOCK_SIZE) // BLOCK_SIZE][
                            (current_x + col * BLOCK_SIZE) // BLOCK_SIZE]
                        for row in range(len(current_shape)) for col in range(len(current_shape[row])) if
                        current_shape[row][col]):
                self.update_grid(current_shape, current_x, current_y - BLOCK_SIZE)
                self.check_lines()
                current_shape = self.get_random_shape()
                current_x = (SCREEN_WIDTH // 2) - (len(current_shape[0]) * BLOCK_SIZE // 2)
                current_y = 0
                color = random.choice(COLORS)

            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col]:
                        pygame.draw.rect(screen, WHITE, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH - 150, 20))
            pygame.display.flip()
            clock.tick(10)

        self.music_player.stop_music()
        pygame.quit()


class Score:
    def __init__(self):
        self.score = 0  # Начальный счет
        self.font = pygame.font.SysFont("Arial", 30)  # Шрифт для отображения

    def increase_score(self, points):
        """Увеличиваем счет на определенное количество очков."""
        self.score += points

    def draw_score(self, screen):
        """Отображаем текущий счет на экране."""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  # Рисуем счет в левом верхнем углу


if __name__ == "__main__":
    music_player = MusicPlayer("game_music.mp3")
    game = Menu(music_player)
    game.game_loop()
