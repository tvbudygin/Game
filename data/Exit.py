class Exit_c:
    def exit_f(self):
        import pygame
        size1 = w, h = (600, 300)
        pygame.display.set_caption("GOODBYE")
        screen1 = pygame.display.set_mode(size1)

        font = pygame.font.Font(None, 150)
        font1 = pygame.font.Font(None, 35)
        # отчет секунд
        down_time = 3
        # время начала отчета в милисикундах, возврщает време с начала иницилизации pygame
        start_ticks = pygame.time.get_ticks()
        running1 = True
        while running1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running1 = False
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE):
                    return True
            # вычесляем оставшееся время
            seconds_left = down_time - (pygame.time.get_ticks() - start_ticks) // 1000
            # если время меньше нуля, заканчиваем
            if seconds_left <= 1:
                running1 = False
            screen1.fill((0, 0, 0))
            # делаем картинку
            text = font.render(str(seconds_left), True, (255, 204, 0))
            text2 = font1.render("press ESC or Пробел, чтобы вернуться", True, (255, 255, 255))
            # создаем "прямоугольник" из надписи с центром
            text_r = text.get_rect(center=(w // 2, h // 2))
            text_r1 = text2.get_rect(center=(w - 280, h - 50))
            # выводим
            screen1.blit(text, text_r.topleft)
            screen1.blit(text2, text_r1.topleft)

            pygame.display.flip()
        return False
