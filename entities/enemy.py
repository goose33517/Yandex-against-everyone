import arcade
import math
import random
from settings import *


class Enemy:
    """Базовый класс врага"""

    _enemies = {}  # Словарь для связи спрайтов с объектами врагов

    def __init__(self, enemy_type, scale=0.4):
        self.enemy_type = enemy_type
        self.health = 1
        self.damage = ENEMY_DAMAGE
        self.speed = 2
        self.patrol_range = 100
        self.start_x = 0
        self.start_y = 0
        self.direction = random.choice([-1, 1])
        self.patrol_timer = 0
        self.physics_engine = None

        # Загрузка текстур в зависимости от типа
        texture_path = None
        if enemy_type == 'google':
            try:
                texture_path = GameSettings.get_image_path("enemies", "google_boss_stand.jpg")
            except:
                pass
        elif enemy_type == 'microsoft':
            try:
                texture_path = GameSettings.get_image_path("enemies", "microsoft_robot.jpg")
            except:
                pass
        elif enemy_type == 'apple':
            try:
                texture_path = GameSettings.get_image_path("enemies", "apple_enemy.jpg")
            except:
                pass
        elif enemy_type == 'telegram':
            try:
                texture_path = GameSettings.get_image_path("enemies", "telegram_plane.jpg")
            except:
                pass
        elif enemy_type == 'vk':
            try:
                texture_path = GameSettings.get_image_path("enemies", "vk_bird.jpg")
            except:
                pass

        if texture_path:
            try:
                self.sprite = arcade.Sprite(texture_path, scale)
            except:
                self.sprite = arcade.SpriteCircle(30, arcade.color.RED)
        else:
            self.sprite = arcade.SpriteCircle(30, arcade.color.RED)

        Enemy._enemies[self.sprite] = self

    @classmethod
    def create_enemy(cls, enemy_type):
        """Создание врага по типу"""
        enemy = cls(enemy_type)

        if enemy_type == 'google':
            enemy.health = 2
            enemy.speed = 1.5
        elif enemy_type == 'microsoft':
            enemy.health = 1
            enemy.speed = 2
        elif enemy_type == 'apple':
            enemy.health = 1
            enemy.speed = 3
        elif enemy_type == 'telegram':
            enemy.health = 1
            enemy.speed = 4
        elif enemy_type == 'vk':
            enemy.health = 1
            enemy.speed = 3.5

        return enemy

    @classmethod
    def get_enemy_from_sprite(cls, sprite):
        """Получение объекта врага по спрайту"""
        return cls._enemies.get(sprite)

    def update(self, delta_time):
        """Обновление состояния врага"""
        self.patrol_timer += delta_time

        if self.start_x == 0:
            self.start_x = self.sprite.center_x
            self.start_y = self.sprite.center_y

        # ПРОСТАЯ ЛОГИКА: просто двигаемся в текущем направлении
        # Изменение направления теперь происходит в screens.py
        self.sprite.change_x = self.speed * self.direction

        # Для летающих врагов
        if self.enemy_type in ['telegram', 'vk']:
            self.sprite.change_y = math.sin(self.patrol_timer) * 1.5
        else:
            self.sprite.change_y = 0

        # Обновление физики если есть движок
        if self.physics_engine:
            self.physics_engine.update()

        # Ограничение выхода за пределы экрана
        if self.sprite.center_x < 50:
            self.sprite.center_x = 50
            self.direction = 1  # Разворачиваем вправо
        elif self.sprite.center_x > SCREEN_WIDTH - 50:
            self.sprite.center_x = SCREEN_WIDTH - 50
            self.direction = -1  # Разворачиваем влево

        # Для летающих врагов ограничиваем по вертикали
        if self.enemy_type in ['telegram', 'vk']:
            if self.sprite.center_y < 100:
                self.sprite.center_y = 100
            elif self.sprite.center_y > SCREEN_HEIGHT - 100:
                self.sprite.center_y = SCREEN_HEIGHT - 100

    def setup_physics(self, platforms):
        """Настройка физики для врага"""
        if self.enemy_type not in ['telegram', 'vk']:
            try:
                self.physics_engine = arcade.PhysicsEnginePlatformer(
                    self.sprite,
                    gravity_constant=GRAVITY,
                    walls=platforms
                )
            except:
                self.physics_engine = None

    def take_damage(self, damage):
        """Получение урона"""
        self.health -= damage
        return self.health <= 0