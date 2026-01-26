import os
import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Яндекс-Марио"
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.0
PLAYER_JUMP_SPEED = 20

# Настройки камеры
CAMERA_LERP = 0.12  # Плавность следования камеры
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)  # Мёртвая зона по ширине
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)  # Мёртвая зона по высоте

LAYER_NAME_PLATFORMS = "platforms"
LAYER_NAME_MOVING_PLATFORMS = "moving_platforms"
LAYER_NAME_ENEMIES = "enemies"
LAYER_NAME_POWERUPS = "powerups"
LAYER_NAME_LADDERS = "ladders"
LAYER_NAME_PLAYER = "player"
LAYER_NAME_BACKGROUND = "background"

PLAYER_START_HEALTH = 3
ENEMY_DAMAGE = 1
COIN_SCORE = 10
POWERUP_DURATION = 10

SAVE_FILE = "yandex_mario_save.json"

BACKGROUND_COLOR = arcade.csscolor.CORNFLOWER_BLUE
UI_COLOR = arcade.color.YELLOW
TEXT_COLOR = arcade.color.BLACK


class GameSettings:
    @staticmethod
    def get_asset_path(*path_parts):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "assets", *path_parts)

    @staticmethod
    def get_image_path(category, filename):
        return GameSettings.get_asset_path("images", category, filename)

    @staticmethod
    def get_sound_path(filename):
        return GameSettings.get_asset_path("sounds", filename)