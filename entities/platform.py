import arcade
from settings import *


class Platform:
    """Класс платформы"""

    def __init__(self):
        try:
            self.sprite = arcade.Sprite(
                GameSettings.get_image_path("platforms", "platform_tile.jpg"),
                TILE_SCALING
            )
        except Exception as e:
            print(f"Error loading platform texture: {e}")
            self.sprite = arcade.SpriteSolidColor(64, 32, arcade.color.BROWN)

        self.sprite.change_x = 0
        self.sprite.change_y = 0


class MovingPlatform:
    """Класс движущейся платформы"""

    def __init__(self, start_x, start_y, move_range=100, move_speed=2, horizontal=True):
        self.start_x = start_x
        self.start_y = start_y
        self.move_range = move_range
        self.move_speed = move_speed
        self.horizontal = horizontal
        self.direction = 1

        try:
            self.sprite = arcade.Sprite(
                GameSettings.get_image_path("platforms", "platform_tile.jpg"),
                TILE_SCALING
            )
        except Exception as e:
            print(f"Error loading moving platform texture: {e}")
            self.sprite = arcade.SpriteSolidColor(64, 32, arcade.color.BLUE)

        self.sprite.center_x = start_x
        self.sprite.center_y = start_y

        self.change_x = move_speed if horizontal else 0
        self.change_y = 0 if horizontal else move_speed

    def update(self, delta_time):
        """Обновление позиции платформы"""
        if self.horizontal:
            self.sprite.center_x += self.change_x * self.direction

            if self.sprite.center_x > self.start_x + self.move_range:
                self.direction = -1
            elif self.sprite.center_x < self.start_x - self.move_range:
                self.direction = 1
        else:
            self.sprite.center_y += self.change_y * self.direction

            if self.sprite.center_y > self.start_y + self.move_range:
                self.direction = -1
            elif self.sprite.center_y < self.start_y - self.move_range:
                self.direction = 1