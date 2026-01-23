import arcade
from settings import PLAYER_MOVE_SPEED, PLAYER_JUMP_SPEED, PLAYER_MAX_HEALTH, IMAGE_PATH

class Player(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()
        self.speed = PLAYER_MOVE_SPEED
        self.jump_speed = PLAYER_JUMP_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.coins = 0
        self.score = 0
        self._load_textures()

    def _load_textures(self):
        stand_path = IMAGE_PATH / "player" / "yandex_stand.png"
        walk_left_path = IMAGE_PATH / "player" / "yandex_walk_left.png"
        walk_right_path = IMAGE_PATH / "player" / "yandex_walk_right.png"

        self.stand_right_textures = [arcade.load_texture(stand_path, scale=2.0)]
        self.stand_left_textures = [arcade.load_texture(stand_path, flipped_horizontally=True, scale=2.0)]
        self.walk_right_textures = [arcade.load_texture(walk_right_path, scale=2.0)]
        self.walk_left_textures = [arcade.load_texture(walk_left_path, scale=2.0)]

        self.texture = self.stand_right_textures[0]

    def update(self):
        super().update()
        super().update_animation()

    def take_hit(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def add_coin(self, amount=1):
        self.coins += amount
        self.score += COIN_SCORE

    def add_score(self, value):
        self.score += value
