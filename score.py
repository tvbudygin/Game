import pygame


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
        screen.blit(score_text, (300, 20))  # Рисуем счет в правой части экрана