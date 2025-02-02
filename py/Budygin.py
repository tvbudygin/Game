import os
import sys
import pygame
import random
from Rules import Rules_c
from Exit import Exit_c

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


# фукцию загрузки изображений
def load_image(name):
    fullname = os.path.join('../data/images', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изобрадением {fullname} не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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

    def __init__(self):
        super().__init__(ALL_SPRITES1)
        self.image = Play.image
        self.rect = pygame.Rect(112.5, 107.5, 75, 75)


# добавляем кнопку правил
class Rules(pygame.sprite.Sprite):
    image = load_image("rules.png")

    def __init__(self):
        super().__init__(ALL_SPRITES1)
        self.image = Rules.image
        self.rect = pygame.Rect(112.5, 262.5, 75, 75)


# добавляем кнопку выход
class Exit(pygame.sprite.Sprite):
    image = load_image("exit.png")

    def __init__(self):
        super().__init__(ALL_SPRITES1)
        self.image = Exit.image
        self.rect = pygame.Rect(112.5, 417.5, 75, 75)


# класс меню игры
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
    def game_loop(self, sostoanie='menu', game_screnn_state='', score=0, max_score=0, inverted_mode=False):
        try:
            from Kuznetsov import MusicPlayer

            music_player = MusicPlayer("../data/music/game_music.mp3")
            music_player.play_game_music()
            # создаем фон и кнопки
            Fon()
            Play()
            Rules()
            Exit()
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            clock = pygame.time.Clock()
            running = True
            current_shape = self.get_random_shape()
            # x и y для 1 фигуры
            current_x = (SCREEN_WIDTH // 2) - (len(current_shape[0]) * BLOCK_SIZE // 2)
            current_y = 0
            # создаю цвета для каждой фигуры, так чтобы можно было поменять оттенок
            c = COLORS[random.randint(0, 14)]
            c1 = COLORS[random.randint(0, 14)]
            c2 = COLORS[random.randint(0, 14)]
            color = pygame.Color(c[0], c[1], c[2])
            color1 = pygame.Color(c1[0], c1[1], c1[2])
            color2 = pygame.Color(c2[0], c2[1], c2[2])
            # делаем все цвета разными
            while color1 != color and color1 != color2 and color2 != color:
                color1 = COLORS[random.randint(0, 14)]
                color2 = COLORS[random.randint(0, 14)]
            # переменные для проверки появилась ли другие фигуры
            k = False
            k1 = False
            # координаты кнопок
            rect_play = pygame.Rect(112.5, 107.5, 75, 75)
            rect_rules = pygame.Rect(112.5, 262.5, 75, 75)
            rect_exit = pygame.Rect(112.5, 417.5, 75, 75)

            while running:
                if pygame.get_init():
                    # если сейчас состояние меню
                    if sostoanie == "menu":
                        try:
                            screen.fill(BLACK)
                            # Отслеживание событий
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    # Получаем позицию мыши во время клика
                                    mouse_pos = event.pos
                                    # если нажали в диапозоне кнопки play, открываем другое меню
                                    if rect_play.collidepoint(mouse_pos):
                                        sostoanie = "game"
                                    # если нажали в диапозоне кнопки exit, открываем другое меню
                                    if rect_exit.collidepoint(mouse_pos):
                                        sostoanie = "exit"
                                    # если нажали в диапозоне кнопки rules, открываем лургое меню
                                    if rect_rules.collidepoint(mouse_pos):
                                        sostoanie = "rules"

                            # добовляем фон
                            ALL_SPRITES.draw(screen)

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

                            # обновляем координаты 2 фигуры и рисуем ее
                            if k:
                                self.draw_shape(current_shape1, current_x1, current_y1, color1)
                                current_y1 += BLOCK_SIZE
                                # если фигура достигла низа, то разришаем рисовать следующую
                                if current_y1 + len(current_shape) * BLOCK_SIZE > SCREEN_HEIGHT:
                                    k = False

                            # добовляем третью фигуру
                            if (current_y + len(current_shape) * BLOCK_SIZE) * 2 > SCREEN_HEIGHT and not k1:
                                current_shape2 = self.get_random_shape()
                                current_x2 = SCREEN_WIDTH - (len(current_shape[0]) * BLOCK_SIZE) - 5
                                current_y2 = 0
                                color2 = COLORS[random.randint(0, 14)]
                                k1 = True

                            # обновляем координаты 3 фигуры и рисуем ее
                            if k1:
                                self.draw_shape(current_shape2, current_x2, current_y2, color2)
                                current_y2 += BLOCK_SIZE
                                # если фигура достигла низа, то разришаем рисовать следующую
                                if current_y2 + len(current_shape) * BLOCK_SIZE > SCREEN_HEIGHT:
                                    k1 = False

                            font = pygame.font.Font(None, 36)
                            score_text = font.render(f"Max_score: {str(max_score)}", True, WHITE)
                            screen.blit(score_text, (10, 550))
                            # добавляем кнопки
                            ALL_SPRITES1.draw(screen)
                            pygame.display.flip()
                            # Задержка, чтобы фигуры падали не слишком быстро
                            clock.tick(10)
                        except Exception as e:
                            print(e)
                    # если состояние правила, открывем дургое окно
                    elif sostoanie == "rules":
                        try:
                            a = Rules_c()
                            a.rulse_f()
                            # если закрыли, то возвращаем меню
                            sostoanie = "menu"
                            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                            pygame.display.set_caption("Тетрис")
                        except Exception as e:
                            print(e)
                    elif sostoanie == "exit":
                        try:
                            a = Exit_c()
                            b = a.exit_f()
                            # закрывем все
                            if not b:
                                running = False
                            # если ззахотели вернуться, то возвращаем меню
                            else:
                                sostoanie = "menu"
                                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                                pygame.display.set_caption("Тетрис")
                        except Exception as e:
                            print(e)
                    elif sostoanie == "game":
                        try:
                            from Rezvushkin import game_loop
                            game_loop(screen_state=game_screnn_state, score=score, max_score=max_score,
                                      inverted_mode=inverted_mode)

                            # если закрыли, то возвращаем меню
                            sostoanie = "menu"
                            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                            pygame.display.set_caption("Тетрис")
                        except Exception as e:
                            print(e)
                else:
                    running = False

            pygame.quit()
            sys.exit()
        except KeyboardInterrupt:
            pygame.quit()
            sys.exit()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    game = Menu()
    game.game_loop()
