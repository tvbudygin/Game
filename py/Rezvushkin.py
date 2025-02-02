import pygame
import random
from Budygin import load_image

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Тетрис")
ALL_SPRITES = pygame.sprite.Group()
ALL_SPRITES1 = pygame.sprite.Group()
ALL_SPRITES2 = pygame.sprite.Group()

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


def draws():
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
    def __init__(self, shape, color, inverted_mode):
        self.shape = shape
        self.color = color
        self.x = (SCREEN_WIDTH // 2) - (len(shape[0]) * BLOCK_SIZE // 2)
        self.x = (self.x // BLOCK_SIZE) * BLOCK_SIZE
        # разное елси перевернутый экран
        if not inverted_mode:
            self.y = 0
        else:
            self.y = SCREEN_HEIGHT - (len(shape) * BLOCK_SIZE)

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

    def move_piece_y(self, dy, inverted_mode=False):
        # разное елси перевернутый экран
        if not inverted_mode:
            self.y = self.y + dy
        else:
            self.y = self.y - dy

    def rotate(self):
        # Поворот фигуры на 90 градусов
        rows = len(self.shape)
        cols = len(self.shape[0])
        new_shape = [[0] * rows for _ in range(cols)]  # Создаем пустую матрицу с перевернутыми размерами
        for row in range(rows):
            for col in range(cols):
                new_shape[col][rows - row - 1] = self.shape[row][col]

        # Проверяем, не выходит ли фигура за границы экрана
        if self.x + len(new_shape[0]) * BLOCK_SIZE <= SCREEN_WIDTH and self.y + len(
                new_shape) * BLOCK_SIZE <= SCREEN_HEIGHT:
            self.shape = new_shape


# Функция для выбора случайной фигуры
def get_random_shape(inverted_mode):
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return Tetromino(shape, color, inverted_mode)


# Инициализация массива для хранения состояния экрана
def init_screen_state():
    screen_state = [[None for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    return screen_state


# Проверка столкновения с нижней частью экрана или другими фигурами
def check_collision(tetromino, screen_state, inverted_mode=False):
    for row in range(len(tetromino.shape)):
        for col in range(len(tetromino.shape[row])):
            if tetromino.shape[row][col]:
                x = (tetromino.x + col * BLOCK_SIZE) // BLOCK_SIZE
                # разное елси перевернутый экран
                if not inverted_mode:
                    y = (tetromino.y + row * BLOCK_SIZE + BLOCK_SIZE) // BLOCK_SIZE
                    if y >= len(screen_state) or screen_state[y][x] is not None:
                        return True
                else:
                    y = (tetromino.y + row * BLOCK_SIZE - BLOCK_SIZE) // BLOCK_SIZE
                    if y < 0 or screen_state[y][x] is not None:
                        return True
    return False


# Проверка достижения верха экрана
def check_top_collision(screen_state, inverted_mode=False):
    # разное елси перевернутый экран
    if not inverted_mode:
        for x in range(len(screen_state[0])):
            if screen_state[0][x] is not None:
                return True
    else:
        for x in range(len(screen_state[0])):
            if screen_state[-1][x] is not None:
                return True
    return False


# Добавление фигуры в состояние экрана
def add_to_screen_state(tetromino, screen_state):
    for row in range(len(tetromino.shape)):
        for col in range(len(tetromino.shape[row])):
            if tetromino.shape[row][col]:
                x = (tetromino.x + col * BLOCK_SIZE) // BLOCK_SIZE
                y = (tetromino.y + row * BLOCK_SIZE) // BLOCK_SIZE
                if 0 <= y < len(screen_state) and 0 <= x < len(screen_state[0]):
                    screen_state[y][x] = tetromino.color


# Рисование фигур из состояния экрана
def draw_from_screen_state(screen_state):
    for y in range(len(screen_state)):
        for x in range(len(screen_state[y])):
            if screen_state[y][x] is not None:
                pygame.draw.rect(screen, screen_state[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# перемещение фишуры вниз
def drop(tetromino, screen_state, inverted_mode=False):
    while not check_collision(tetromino, screen_state, inverted_mode):
        # разное елси перевернутый экран
        if not inverted_mode:
            tetromino.y += BLOCK_SIZE
        else:
            tetromino.y -= BLOCK_SIZE


# функция удаления заболненых линий и подсчет их
def change_screen_state(screen_state, inverted_mode=False):
    new_screen_state = [row for row in screen_state if None in row]
    len_clear = len(screen_state) - len(new_screen_state)

    for _ in range(len_clear):
        # разное елси перевернутый экран
        if not inverted_mode:
            new_screen_state.insert(0, [None] * len(screen_state[0]))
        else:
            new_screen_state.insert(-1, [None] * len(screen_state[0]))

    return new_screen_state, len_clear


# добавляем кнопку переварачивания
class Reverses(pygame.sprite.Sprite):
    image = load_image("reverses.png")

    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.image = Reverses.image
        self.rect = pygame.Rect(475, 412.5, 75, 75)


# добавляем кнопку очищения
class Clears(pygame.sprite.Sprite):
    image = load_image("clears.png")

    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.image = Clears.image
        self.rect = pygame.Rect(350, 412.5, 75, 75)


# добавляем в spites
class Win(pygame.sprite.Sprite):
    image = load_image("win.png")

    def __init__(self):
        super().__init__(ALL_SPRITES1)
        self.image = Win.image
        self.rect = pygame.Rect(350, 150, 200, 200)


# добавляем в spites
class Fail(pygame.sprite.Sprite):
    image = load_image("fail.png")

    def __init__(self):
        super().__init__(ALL_SPRITES2)
        self.image = Fail.image
        self.rect = pygame.Rect(350, 150, 200, 200)


# добавляем в spites
class Q1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES1)
        font = pygame.font.Font(None, 36)
        self.image = font.render("PRESS Q", True, (255, 0, 0))
        self.rect = self.image.get_rect(center=(450, 100))


# добавляем в spites
class Q2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES2)
        font = pygame.font.Font(None, 36)
        self.image = font.render("PRESS Q", True, (255, 0, 0))
        self.rect = self.image.get_rect(center=(450, 100))


# Главная игра
def game_loop(screen_state='', score=0, max_score=0, inverted_mode=False):
    from Kuznetsov import MusicPlayer
    music_player = MusicPlayer("../data/music/game_music1.mp3")
    music_player.play_game_music()
    # добавялем spites
    Reverses()
    Clears()
    Win()
    Fail()
    Q1()
    Q2()
    is_paused = False  # останавливается ли экран
    # inverted_mode = False  # включён ли режим перевёрнутого тетриса
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Тетрис")
    clock = pygame.time.Clock()
    running = True
    if screen_state == '':
        screen_state = init_screen_state()
    current_tetromino = get_random_shape(inverted_mode)
    rect_clear = pygame.Rect(350, 412.5, 75, 75)
    rect_reverse = pygame.Rect(475, 412.5, 75, 75)
    show_sprites = False  # опказывать ли win/lose

    while running:
        # Отслеживание событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                from Budygin import Menu
                return Menu().game_loop(game_screnn_state=screen_state, score=score, max_score=max_score,
                                        inverted_mode=inverted_mode)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if not check_collision(current_tetromino, screen_state, inverted_mode):
                        current_tetromino.move_piece(-BLOCK_SIZE)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if not check_collision(current_tetromino, screen_state, inverted_mode):
                        current_tetromino.move_piece(BLOCK_SIZE)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not inverted_mode:
                        if not check_collision(current_tetromino, screen_state, inverted_mode):
                            current_tetromino.move_piece_y(BLOCK_SIZE, inverted_mode)
                    else:
                        if not check_collision(current_tetromino, screen_state, inverted_mode):
                            current_tetromino.rotate()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if not inverted_mode:
                        if not check_collision(current_tetromino, screen_state, inverted_mode):
                            current_tetromino.rotate()
                    else:
                        if not check_collision(current_tetromino, screen_state, inverted_mode):
                            current_tetromino.move_piece_y(BLOCK_SIZE, inverted_mode)
                elif event.key == pygame.K_SPACE:
                    if not check_collision(current_tetromino, screen_state, inverted_mode):
                        drop(current_tetromino, screen_state, inverted_mode)
                elif event.key == pygame.K_ESCAPE:
                    from Budygin import Menu
                    return Menu().game_loop(game_screnn_state=screen_state, score=score, max_score=max_score)
                # очистка
                elif event.key == pygame.K_q:
                    is_paused = False
                    show_sprites = False
                    screen_state = init_screen_state()
                    current_tetromino = get_random_shape(inverted_mode)
                    score = 0
                    music_player = MusicPlayer("../data/music/game_music1.mp3")
                    music_player.play_game_music()
                # переворот
                elif event.key == pygame.K_e:
                    inverted_mode = not inverted_mode
                    screen_state = screen_state[::-1]
                    rows = len(screen_state)
                    old_row = current_tetromino.y // BLOCK_SIZE
                    new_row = (rows - 1) - old_row
                    current_tetromino.y = new_row * BLOCK_SIZE
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Получаем позицию мыши во время клика
                mouse_pos = event.pos
                # если нажали в диапозоне кнопки clear, очищаем
                if rect_clear.collidepoint(mouse_pos):
                    screen_state = init_screen_state()
                    current_tetromino = get_random_shape(inverted_mode)
                    score = 0
                    is_paused = False
                    show_sprites = False
                    music_player = MusicPlayer("../data/music/game_music1.mp3")
                    music_player.play_game_music()
                # переворот
                if rect_reverse.collidepoint(mouse_pos):
                    inverted_mode = not inverted_mode
                    screen_state = screen_state[::-1]
                    rows = len(screen_state)
                    old_row = current_tetromino.y // BLOCK_SIZE
                    new_row = (rows - 1) - old_row
                    current_tetromino.y = new_row * BLOCK_SIZE
        if not running:
            break

        screen.fill((0, 0, 0))
        draws()
        ALL_SPRITES.draw(screen)

        if not is_paused:
            # Рисуем падающую фигуру
            current_tetromino.draw()

            # Обновляем позицию фигуры
            if not check_collision(current_tetromino, screen_state, inverted_mode):
                if not inverted_mode:
                    current_tetromino.y += BLOCK_SIZE
                else:
                    current_tetromino.y -= BLOCK_SIZE
            else:
                # добавляем и очищаем экран
                add_to_screen_state(current_tetromino, screen_state)
                # считаем очки
                if not is_paused:
                    score += 50
                screen_state, len_clear = change_screen_state(screen_state, inverted_mode)
                if len_clear == 1 or len_clear == 2:
                    score += (1000 * len_clear)
                elif len_clear == 3:
                    score += (1000 * len_clear) + 500
                elif len_clear == 4:
                    score += (1000 * (len_clear + 1))
                if max_score <= score:
                    max_score = score
                # победа
                if score >= 15000:
                    show_sprites = True
                elif check_top_collision(screen_state, inverted_mode):  # проверка достигла ли фигура самого верха
                    is_paused = True
                    show_sprites = True
                else:
                    current_tetromino = get_random_shape(inverted_mode)
        # победа/проигрышь рисуем
        if show_sprites:
            if score >= 15000:
                ALL_SPRITES1.draw(screen)
                is_paused = True
            elif check_top_collision(screen_state, inverted_mode):
                ALL_SPRITES2.draw(screen)

        # рисуем score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {str(score)}", True, WHITE)
        screen.blit(score_text, (400, 10))

        # рисуем max_score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Max_score: {str(max_score)}", True, WHITE)
        screen.blit(score_text, (390, 550))

        # Рисуем фигуры из состояния экрана
        draw_from_screen_state(screen_state)
        pygame.display.flip()

        # Задержка, чтобы фигуры падали не слишком быстро
        clock.tick(3)
    pygame.quit()


if __name__ == "__main__":
    # Запуск игры
    game_loop()
