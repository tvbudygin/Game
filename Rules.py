class Rules_c:
    def __init__(self):
        self.rules = """Правила Тетриса:

    Цель:
    
        Очистить горизонтальные линии, заполняя их падающими фигурами. 
        Игра заканчивается, если фигуры достигают верха поля.
        Игровое поле:
        - Фигуры появляются сверху и падают вниз.
    
    Управление:
    
        - стрелка вправо / влево: перемещение влево/вправо.
        - стрелка вверх: вращение.
        - стрелка вниз: ускорение падения.
    
    Основные правила:
    
        1. Заполненные линии исчезают, верхние блоки опускаются.
        2. Игра заканчивается, если поле заполнено.
    
    Советы:
    
        - Оставляйте место для длинной фигуры (I) для "Тетриса".
        - Старайтесь избегать пустот между блоками."""

    def rulse_f(self):
        import pygame
        size1 = (1000, 750)
        pygame.display.set_caption("Правила Тетриса")
        screen1 = pygame.display.set_mode(size1)
        running1 = True

        # шрифт и размер текста
        font = pygame.font.Font(None, 35)

        while running1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE)):
                    running1 = False
            screen1.fill((0, 0, 0))
            # отступ сверху
            y_o = 30
            # идем построчно
            for i in self.rules.splitlines():
                # делаем "картинку"
                text_surface = font.render(i, True, (255, 204, 0))
                # выводим ее и смещаем каждую строку вниз
                screen1.blit(text_surface, (25, y_o))
                # добовляем к остпупу 25
                y_o += 25

            pygame.display.flip()
