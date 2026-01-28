import arcade
from settings import *


class PowerUp:
    """Базовый класс бонуса"""

    _powerups = {}  # Словарь для связи спрайтов с объектами бонусов

    def __init__(self, powerup_type, value=10):
        self.powerup_type = powerup_type
        self.value = value

        if powerup_type == 'coin':
            try:
                texture_path = GameSettings.get_image_path("powerups", "coin_ruble.jpg")
                self.sprite = arcade.Sprite(texture_path, 0.3)
            except Exception as e:
                print(f"Error loading coin texture: {e}")
                self.sprite = arcade.SpriteCircle(20, arcade.color.YELLOW)
        elif powerup_type == 'heart':
            try:
                texture_path = GameSettings.get_image_path("powerups", "heart.jpg")
                self.sprite = arcade.Sprite(texture_path, 0.2)
            except Exception as e:
                print(f"Error loading heart texture: {e}")
                self.sprite = arcade.SpriteCircle(15, arcade.color.RED)
        elif powerup_type == 'speed':
            try:
                texture_path = GameSettings.get_image_path("powerups", "speed_boost.jpg")
                self.sprite = arcade.Sprite(texture_path, 0.3)
            except Exception as e:
                print(f"Error loading speed boost texture: {e}")
                self.sprite = arcade.SpriteCircle(20, arcade.color.CYAN)
        else:
            self.sprite = arcade.SpriteCircle(20, arcade.color.YELLOW)

        PowerUp._powerups[self.sprite] = self

    @classmethod
    def get_powerup_from_sprite(cls, sprite):
        """Получение объекта бонуса по спрайту"""
        return cls._powerups.get(sprite)

    def apply(self, player):
        """Применение бонуса к игроку"""
        pass


class Coin(PowerUp):
    """Класс монеты"""

    def __init__(self):
        super().__init__('coin', COIN_SCORE)
        self.rotation_speed = 2

    def apply(self, player):
        """Применение монеты"""
        pass


class Heart(PowerUp):
    """Класс сердца (дополнительная жизнь)"""

    def __init__(self):
        super().__init__('heart', 50)

    def apply(self, player):
        """Применение сердца"""
        player.add_health(1)


class SpeedBoost(PowerUp):
    """Класс ускорения"""

    def __init__(self):
        super().__init__('speed', 30)

    def apply(self, player):
        """Применение ускорения"""
        player.add_speed_boost(2.0, POWERUP_DURATION)