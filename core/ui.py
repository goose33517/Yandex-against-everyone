import arcade
from settings import *


class UI:
    """Пользовательский интерфейс - как в учебнике"""

    def __init__(self, player, score, level=1):
        self.player = player
        self.score = score
        self.level = level

    def draw(self):
        """Отрисовка UI - только текст как в учебнике"""
        # Просто текст без камеры
        arcade.draw_text(f"Уровень: {self.level}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)
        arcade.draw_text(f"Счет: {self.score}", 10, SCREEN_HEIGHT - 60, arcade.color.YELLOW, 16)
        arcade.draw_text(f"Здоровье: {self.player.health}", 10, SCREEN_HEIGHT - 90, arcade.color.RED, 16)

    def update(self):
        """Обновление UI"""
        pass