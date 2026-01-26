import arcade
from settings import *


class Player:
    """Класс игрока"""

    def __init__(self):
        self.game_screen = None
        self.health = PLAYER_START_HEALTH
        self.speed_multiplier = 1.0
        self.speed_boost_time = 0
        self.bullet_speed = 10
        self.bullet_damage = 1

        try:
            self.sprite = arcade.Sprite(
                GameSettings.get_image_path("player", "yandex_stand.jpg"),
                CHARACTER_SCALING
            )
        except Exception as e:
            print(f"Error loading player texture: {e}")
            self.sprite = arcade.SpriteCircle(30, arcade.color.YELLOW)

        self.walk_textures = []
        for i in range(2):
            try:
                texture_path = GameSettings.get_image_path("player", f"yandex_walk_{'right' if i == 0 else 'left'}.jpg")
                texture = arcade.load_texture(texture_path)
                self.walk_textures.append(texture)
            except Exception as e:
                print(f"Error loading walk texture {i}: {e}")

        try:
            self.stand_texture = arcade.load_texture(
                GameSettings.get_image_path("player", "yandex_stand.jpg")
            )
        except Exception as e:
            print(f"Error loading stand texture: {e}")
            self.stand_texture = None

        if self.stand_texture:
            self.sprite.texture = self.stand_texture

        self.current_texture = 0
        self.texture_change_timer = 0
        self.facing_right = True

        self.sprite.change_x = 0
        self.sprite.change_y = 0

        self.bullets = arcade.SpriteList()
        self.shoot_cooldown = 0.3
        self.shoot_timer = 0

        self.jump_count = 0
        self.max_jumps = 2

    def update(self, delta_time):
        """Обновление состояния игрока"""
        if self.speed_boost_time > 0:
            self.speed_boost_time -= delta_time
            if self.speed_boost_time <= 0:
                self.speed_multiplier = 1.0

        if self.shoot_timer > 0:
            self.shoot_timer -= delta_time

        # Анимация ходьбы
        if abs(self.sprite.change_x) > 0.1 and len(self.walk_textures) >= 2:
            self.texture_change_timer += delta_time
            if self.texture_change_timer > 0.1:
                self.texture_change_timer = 0
                self.current_texture = (self.current_texture + 1) % 2
                if self.facing_right:
                    self.sprite.texture = self.walk_textures[0]
                else:
                    self.sprite.texture = self.walk_textures[1]
        elif self.stand_texture:
            self.sprite.texture = self.stand_texture

        # Удаляем пули, вышедшие за пределы видимой области
        for bullet in self.bullets:
            # Простая проверка - удаляем пули, которые далеко улетели
            if abs(bullet.center_x - self.sprite.center_x) > SCREEN_WIDTH * 2:
                bullet.remove_from_sprite_lists()

    def move_left(self, speed):
        """Движение влево"""
        self.sprite.change_x = -speed * self.speed_multiplier
        self.facing_right = False

    def move_right(self, speed):
        """Движение вправо"""
        self.sprite.change_x = speed * self.speed_multiplier
        self.facing_right = True

    def stop_moving_left(self):
        """Остановка движения влево"""
        if self.sprite.change_x < 0:
            self.sprite.change_x = 0

    def stop_moving_right(self):
        """Остановка движения вправо"""
        if self.sprite.change_x > 0:
            self.sprite.change_x = 0

    def jump(self, speed):
        """Прыжок"""
        if self.game_screen and self.game_screen.physics_engine:
            if self.game_screen.physics_engine.can_jump():
                self.sprite.change_y = speed

    def shoot(self):
        """Выстрел"""
        if self.shoot_timer <= 0:
            bullet = arcade.SpriteCircle(10, arcade.color.YELLOW)
            bullet.center_x = self.sprite.center_x
            bullet.center_y = self.sprite.center_y

            direction = 1 if self.facing_right else -1
            bullet.change_x = self.bullet_speed * direction
            bullet.change_y = 0

            self.bullets.append(bullet)
            self.shoot_timer = self.shoot_cooldown
            return True
        return False

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        self.health = max(0, self.health)

    def add_health(self, amount):
        """Добавление здоровья"""
        self.health = min(PLAYER_START_HEALTH, self.health + amount)

    def add_speed_boost(self, multiplier, duration):
        """Добавление ускорения"""
        self.speed_multiplier = multiplier
        self.speed_boost_time = duration