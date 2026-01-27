import arcade
import os
import json
import math
from settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.platform import Platform, MovingPlatform
from entities.powerup import PowerUp, Coin, Heart, SpeedBoost
from core.level_loader import LevelLoader
from core.ui import UI


class GameScreen:
    """Экран игры"""

    def __init__(self, game):
        self.game = game
        self.physics_engine = None
        self.scene = None
        self.player = None
        self.ui = None
        self.level_loader = None
        self.current_level = 1
        self.score = 0
        self.level_time = 0
        self.moving_platforms = []
        self.game_sounds = {}

        # Камеры как в учебнике
        self.world_camera = arcade.camera.Camera2D()  # Камера для игрового мира
        self.gui_camera = arcade.camera.Camera2D()  # Камера для объектов интерфейса

        # Тряска камеры как в учебнике
        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,  # Трястись будет только то, что попадает в объектив мировой камеры
            max_amplitude=15.0,  # Параметры, с которыми можно поиграть
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        # Параметры камеры как в учебнике
        self.CAMERA_LERP = 0.12  # Плавность следования камеры
        self.DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)  # Размеры мёртвой зоны камеры
        self.DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)

        # Границы мира
        self.world_width = SCREEN_WIDTH * 3  # Увеличиваем мир для камеры
        self.world_height = SCREEN_HEIGHT

        self.background_sprite_list = None

    def setup(self, level):
        """Настройка уровня"""
        self.current_level = level
        self.score = 0
        self.level_time = 0
        self.moving_platforms = []
        self.background_sprite_list = None

        # Сбрасываем камеру
        self.world_camera.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.gui_camera.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Пересоздаем тряску камеры
        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        # Создаем сцену
        self.scene = arcade.Scene()

        # Загружаем фон для уровня
        self.load_background(level)

        # Загружаем уровень
        self.level_loader = LevelLoader()
        level_data = self.level_loader.load_level(level)

        if not level_data:
            print(f"Error: Level {level} not found!")
            return

        # Создаем платформы
        self.create_platforms(level_data)

        # Создаем игрока
        self.create_player(level_data)

        # Создаем врагов
        self.create_enemies(level_data)

        # Создаем бонусы
        self.create_powerups(level_data)

        # Создаем физический движок для игрока
        try:
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player.sprite,
                gravity_constant=GRAVITY,
                walls=self.scene[LAYER_NAME_PLATFORMS]
            )
        except Exception as e:
            print(f"Ошибка создания физического движка: {e}")
            self.physics_engine = None

        # Создаем UI
        self.ui = UI(self.player, self.score, self.current_level)

    def load_background(self, level):
        """Загрузка фонового изображения для уровня"""
        try:
            # Создаем SpriteList для фона
            self.background_sprite_list = arcade.SpriteList()

            # Пробуем загрузить фоновое изображение
            bg_filename = f"level{level}_bg.jpg"
            bg_path = GameSettings.get_image_path("ui", bg_filename)

            if os.path.exists(bg_path):
                # Создаем спрайт для фона
                background_sprite = arcade.Sprite(bg_path)
                background_sprite.center_x = self.world_width // 2  # Центр мира
                background_sprite.center_y = self.world_height // 2

                # Масштабируем спрайт под размер мира
                scale_x = self.world_width / background_sprite.width
                scale_y = self.world_height / background_sprite.height
                scale = max(scale_x, scale_y) * 1.1  # Немного больше для перекрытия
                background_sprite.scale = scale

                # Добавляем спрайт в список
                self.background_sprite_list.append(background_sprite)

                print(f"Загружен фон для уровня {level}: {bg_filename}")
            else:
                print(f"Фоновое изображение {bg_filename} не найдено")
                self.background_sprite_list = None
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            self.background_sprite_list = None

    def create_platforms(self, level_data):
        """Создание платформ"""
        platforms_layer = arcade.SpriteList()

        for platform_data in level_data.get('platforms', []):
            x = platform_data['x']
            y = platform_data['y']
            width = platform_data.get('width', 1)

            for i in range(width):
                platform = Platform()
                platform.sprite.center_x = x + i * GRID_PIXEL_SIZE
                platform.sprite.center_y = y
                platforms_layer.append(platform.sprite)

        # Добавляем движущиеся платформы для определенных уровней
        if self.current_level >= 2:
            for mp_data in level_data.get('moving_platforms', []):
                mp = MovingPlatform(
                    start_x=mp_data['x'],
                    start_y=mp_data['y'],
                    move_range=mp_data['move_range'],
                    move_speed=mp_data.get('move_speed', 2),
                    horizontal=mp_data.get('horizontal', True)
                )
                self.moving_platforms.append(mp)
                platforms_layer.append(mp.sprite)

        self.scene.add_sprite_list(LAYER_NAME_PLATFORMS, sprite_list=platforms_layer)

    def create_player(self, level_data):
        """Создание игрока"""
        start_x = level_data['player_start'][0]
        start_y = level_data['player_start'][1]

        self.player = Player()
        self.player.game_screen = self
        self.player.sprite.center_x = start_x
        self.player.sprite.center_y = start_y

        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player.sprite)

    def create_enemies(self, level_data):
        """Создание врагов"""
        enemies_layer = arcade.SpriteList()
        enemy_types = ['google', 'microsoft', 'apple', 'telegram', 'vk']

        for enemy_data in level_data.get('enemies', []):
            enemy_type = enemy_data.get('type', 'google')
            if enemy_type in enemy_types:
                enemy = Enemy.create_enemy(enemy_type)
                enemy.sprite.center_x = enemy_data['x']
                enemy.sprite.center_y = enemy_data['y']
                enemy.patrol_range = enemy_data.get('patrol_range', 100)
                enemy.start_x = enemy_data['x']
                # Инициализируем движение сразу
                enemy.sprite.change_x = enemy.speed * enemy.direction
                enemies_layer.append(enemy.sprite)

        self.scene.add_sprite_list(LAYER_NAME_ENEMIES, sprite_list=enemies_layer)

    def create_powerups(self, level_data):
        """Создание бонусы"""
        powerups_layer = arcade.SpriteList()

        for powerup_data in level_data.get('powerups', []):
            powerup_type = powerup_data.get('type', 'coin')
            if powerup_type == 'coin':
                powerup = Coin()
            elif powerup_type == 'heart':
                powerup = Heart()
            elif powerup_type == 'speed':
                powerup = SpeedBoost()
            else:
                continue

            powerup.sprite.center_x = powerup_data['x']
            powerup.sprite.center_y = powerup_data['y']
            powerups_layer.append(powerup.sprite)

        self.scene.add_sprite_list(LAYER_NAME_POWERUPS, sprite_list=powerups_layer)

    def on_draw(self):
        """Отрисовка игры - строго как в учебнике"""
        # 1) Мир
        self.camera_shake.update_camera()  # Запчасть от тряски камеры
        self.world_camera.use()

        if self.background_sprite_list:
            try:
                self.background_sprite_list.draw()
            except Exception as e:
                print(f"Ошибка отрисовки фона: {e}")
                self.draw_color_background()
        else:
            self.draw_color_background()

        # Рисуем сцену
        self.scene.draw()

        # Рисуем пули
        self.player.bullets.draw()

        # Для отладки: рисуем мертвую зону
        # self.draw_dead_zone()

        self.camera_shake.readjust_camera()  # И это тоже

        # 2) GUI - строго как в учебнике
        self.gui_camera.use()
        self.ui.draw()

    def draw_color_background(self):
        """Рисуем цветной фон"""
        bg_colors = {
            1: arcade.color.LIGHT_BLUE,  # Офис Яндекса
            2: arcade.color.LIGHT_GREEN,  # Кремниевая долина
            3: arcade.color.LIGHT_GRAY,  # Облачный сервер
            4: arcade.color.DARK_BLUE,  # Финальный босс
        }
        color = bg_colors.get(self.current_level, BACKGROUND_COLOR)

        # Рисуем прямоугольник на весь мир
        arcade.draw_lrbt_rectangle_filled(
            0, self.world_width, 0, self.world_height, color
        )

    def draw_dead_zone(self):
        """Рисуем мертвую зону камеры для отладки - как в учебнике"""
        cam_x, cam_y = self.world_camera.position
        arcade.draw_lrbt_rectangle_outline(
            cam_x - self.DEAD_ZONE_W // 2,
            cam_x + self.DEAD_ZONE_W // 2,
            cam_y - self.DEAD_ZONE_H // 2,
            cam_y + self.DEAD_ZONE_H // 2,
            arcade.color.AMBER, 2
        )

    def on_update(self, delta_time):
        """Обновление игры - строго по учебнику"""
        if not self.physics_engine or not self.player:
            return

        self.level_time += delta_time

        # Обновляем тряску камеры как в учебнике
        self.camera_shake.update(delta_time)

        # Обновляем физику игрока
        self.physics_engine.update()

        # Обновляем игрока
        self.player.update(delta_time)

        # Обновляем врагов
        for enemy_sprite in self.scene[LAYER_NAME_ENEMIES]:
            enemy = Enemy.get_enemy_from_sprite(enemy_sprite)
            if enemy:
                # Обновляем врага
                enemy.update(delta_time)

                # ПРОВЕРЯЕМ ГРАНИЦЫ ПАТРУЛИРОВАНИЯ ПРАВИЛЬНО
                current_x = enemy.sprite.center_x

                # Если враг вышел за правую границу патрулирования
                if current_x > enemy.start_x + enemy.patrol_range:
                    enemy.direction = -1  # Меняем направление на лево
                    enemy.sprite.change_x = enemy.speed * enemy.direction
                # Если враг вышел за левую границу патрулирования
                elif current_x < enemy.start_x - enemy.patrol_range:
                    enemy.direction = 1  # Меняем направление на право
                    enemy.sprite.change_x = enemy.speed * enemy.direction

                # Применяем движение к спрайту врага
                enemy.sprite.center_x += enemy.sprite.change_x
                enemy.sprite.center_y += enemy.sprite.change_y

        # Обновляем движущиеся платформы
        for mp in self.moving_platforms:
            mp.update(delta_time)
            if self.physics_engine.is_on_ladder():
                continue
            if arcade.check_for_collision(self.player.sprite, mp.sprite):
                self.player.sprite.center_y += mp.change_y

        # Обновляем пули
        self.player.bullets.update()

        # Проверяем столкновения пуль с врагами
        for bullet in self.player.bullets:
            hit_list = arcade.check_for_collision_with_list(bullet, self.scene[LAYER_NAME_ENEMIES])
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy_sprite in hit_list:
                    enemy_sprite.remove_from_sprite_lists()
                    self.score += COIN_SCORE
                    if self.game_sounds.get('hit'):
                        arcade.play_sound(self.game_sounds['hit'])

                    # Активируем тряску камеры как в учебнике
                    self.camera_shake.start()

        # Проверяем столкновения игрока с врагами
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player.sprite, self.scene[LAYER_NAME_ENEMIES]
        )
        if enemy_hit_list:
            for enemy_sprite in enemy_hit_list:
                enemy_sprite.remove_from_sprite_lists()
                self.player.take_damage(ENEMY_DAMAGE)
                if self.game_sounds.get('hit'):
                    arcade.play_sound(self.game_sounds['hit'])

                # Активируем тряску камеры как в учебнике
                self.camera_shake.start()

                if self.player.health <= 0:
                    # Игра окончена
                    self.game.show_game_over(self.score)
                    return

        # Проверяем столкновения с бонусами
        powerup_hit_list = arcade.check_for_collision_with_list(
            self.player.sprite, self.scene[LAYER_NAME_POWERUPS]
        )
        for powerup_sprite in powerup_hit_list:
            powerup = PowerUp.get_powerup_from_sprite(powerup_sprite)
            if powerup:
                powerup.apply(self.player)
                self.score += powerup.value
                powerup_sprite.remove_from_sprite_lists()

                if isinstance(powerup, Coin) and self.game_sounds.get('coin'):
                    arcade.play_sound(self.game_sounds['coin'])

        # Проверяем выход за пределы карты
        if self.player.sprite.center_y < -100:
            self.player.take_damage(self.player.health)  # Instant death
            self.game.show_game_over(self.score)
            return

        # Проверяем завершение уровня
        if len(self.scene[LAYER_NAME_ENEMIES]) == 0:
            self.game.show_level_complete(self.score)
            return

        # Обновляем UI
        self.ui.score = self.score
        self.ui.update()

        # Обновляем камеру - СТРОГО КАК В УЧЕБНИКЕ
        self.update_camera()

    def update_camera(self):
        """Обновление позиции камеры - СТРОГО КАК В УЧЕБНИКЕ"""
        if not self.player:
            return

        cam_x, cam_y = self.world_camera.position
        px, py = self.player.sprite.center_x, self.player.sprite.center_y

        # Мёртвая зона - как в учебнике
        dz_left = cam_x - self.DEAD_ZONE_W // 2
        dz_right = cam_x + self.DEAD_ZONE_W // 2
        dz_bottom = cam_y - self.DEAD_ZONE_H // 2
        dz_top = cam_y + self.DEAD_ZONE_H // 2

        target_x, target_y = cam_x, cam_y

        # Проверяем мёртвую зону - как в учебнике
        if px < dz_left:
            target_x = px + self.DEAD_ZONE_W // 2
        elif px > dz_right:
            target_x = px - self.DEAD_ZONE_W // 2
        if py < dz_bottom:
            target_y = py + self.DEAD_ZONE_H // 2
        elif py > dz_top:
            target_y = py - self.DEAD_ZONE_H // 2

        # Не показываем «пустоту» за краями карты - как в учебнике
        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        target_x = max(half_w, min(self.world_width - half_w, target_x))
        target_y = max(half_h, min(self.world_height - half_h, target_y))

        # Плавно к цели, аналог arcade.math.lerp_2d, но руками - КАК В УЧЕБНИКЕ
        smooth_x = (1 - self.CAMERA_LERP) * cam_x + self.CAMERA_LERP * target_x
        smooth_y = (1 - self.CAMERA_LERP) * cam_y + self.CAMERA_LERP * target_y

        self.world_camera.position = (smooth_x, smooth_y)

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine and self.physics_engine.can_jump():
                self.player.sprite.change_y = PLAYER_JUMP_SPEED
                if self.game_sounds.get('jump'):
                    arcade.play_sound(self.game_sounds['jump'])
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.move_left(PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.move_right(PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.LCTRL or key == arcade.key.RCTRL:
            if self.player.shoot() and self.game_sounds.get('shoot'):
                arcade.play_sound(self.game_sounds['shoot'])

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.stop_moving_left()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.stop_moving_right()