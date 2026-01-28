import json
import os
from settings import *


class LevelLoader:
    """Загрузчик уровней"""

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.levels_dir = os.path.join(project_root, "levels")

        if not os.path.exists(self.levels_dir):
            os.makedirs(self.levels_dir)
            self.create_default_levels()

    def create_default_levels(self):
        """Создание уровней по умолчанию"""
        for level_num in range(1, 5):
            level_data = self.create_default_level(level_num)
            filename = os.path.join(self.levels_dir, f"level{level_num}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(level_data, f, ensure_ascii=False, indent=2)

    def create_default_level(self, level_number):
        """Создание уровня по умолчанию"""
        # Большой мир для камеры
        world_width = SCREEN_WIDTH * 3

        level_data = {
            "name": f"Уровень {level_number}",
            "player_start": [300, 200],  # Начинаем не с самого края
            "platforms": [],
            "enemies": [],
            "powerups": [],
            "moving_platforms": [],
            "world_width": world_width,
            "world_height": SCREEN_HEIGHT
        }

        # Создаем очень длинную основную платформу для камеры
        for i in range(60):  # В 3 раза больше
            level_data["platforms"].append({
                "x": i * GRID_PIXEL_SIZE,
                "y": 100,
                "width": 1
            })

        if level_number == 1:
            # Офис Яндекса - растягиваем
            level_data["platforms"].extend([
                {"x": 400, "y": 200, "width": 5},
                {"x": 800, "y": 300, "width": 5},
                {"x": 1200, "y": 250, "width": 4},
                {"x": 1600, "y": 200, "width": 6},
                {"x": 2200, "y": 300, "width": 4},
                {"x": 2800, "y": 250, "width": 5}
            ])

            level_data["enemies"].extend([
                {"x": 300, "y": 250, "type": "google", "patrol_range": 100},
                {"x": 700, "y": 350, "type": "google", "patrol_range": 80},
                {"x": 1100, "y": 350, "type": "microsoft", "patrol_range": 60},
                {"x": 1500, "y": 250, "type": "google", "patrol_range": 100},
                {"x": 1900, "y": 350, "type": "apple", "patrol_range": 70},
                {"x": 2300, "y": 280, "type": "microsoft", "patrol_range": 90},
                {"x": 2700, "y": 320, "type": "google", "patrol_range": 120}
            ])

        elif level_number == 2:
            # Кремниевая долина - больше платформ
            level_data["platforms"].extend([
                {"x": 300, "y": 200, "width": 4},
                {"x": 700, "y": 300, "width": 4},
                {"x": 1100, "y": 250, "width": 4},
                {"x": 1500, "y": 200, "width": 5},
                {"x": 1900, "y": 300, "width": 6},
                {"x": 2300, "y": 250, "width": 4},
                {"x": 2700, "y": 200, "width": 5}
            ])

            level_data["moving_platforms"].extend([
                {"x": 400, "y": 150, "move_range": 200, "move_speed": 2, "horizontal": True},
                {"x": 900, "y": 350, "move_range": 150, "move_speed": 1.5, "horizontal": False},
                {"x": 1400, "y": 180, "move_range": 180, "move_speed": 2.2, "horizontal": True},
                {"x": 2000, "y": 280, "move_range": 220, "move_speed": 1.8, "horizontal": True},
                {"x": 2600, "y": 220, "move_range": 160, "move_speed": 2.0, "horizontal": False}
            ])

            level_data["enemies"].extend([
                {"x": 250, "y": 250, "type": "microsoft", "patrol_range": 80},
                {"x": 650, "y": 300, "type": "apple", "patrol_range": 60},
                {"x": 1050, "y": 400, "type": "microsoft", "patrol_range": 70},
                {"x": 1450, "y": 300, "type": "google", "patrol_range": 90},
                {"x": 1850, "y": 280, "type": "apple", "patrol_range": 100},
                {"x": 2250, "y": 350, "type": "microsoft", "patrol_range": 80},
                {"x": 2650, "y": 320, "type": "telegram", "patrol_range": 150}
            ])

        elif level_number == 3:
            # Облачный сервер - еще больше
            level_data["platforms"].extend([
                {"x": 200, "y": 180, "width": 4},
                {"x": 600, "y": 260, "width": 4},
                {"x": 1000, "y": 200, "width": 4},
                {"x": 1400, "y": 280, "width": 4},
                {"x": 1800, "y": 150, "width": 5},
                {"x": 2200, "y": 220, "width": 6},
                {"x": 2600, "y": 180, "width": 4},
                {"x": 3000, "y": 250, "width": 5}
            ])

            level_data["moving_platforms"].extend([
                {"x": 300, "y": 230, "move_range": 100, "move_speed": 3, "horizontal": True},
                {"x": 700, "y": 310, "move_range": 120, "move_speed": 2, "horizontal": False},
                {"x": 1100, "y": 250, "move_range": 150, "move_speed": 2.5, "horizontal": True},
                {"x": 1700, "y": 200, "move_range": 180, "move_speed": 2, "horizontal": True},
                {"x": 2100, "y": 270, "move_range": 140, "move_speed": 1.8, "horizontal": False},
                {"x": 2500, "y": 220, "move_range": 160, "move_speed": 2.2, "horizontal": True},
                {"x": 2900, "y": 190, "move_range": 130, "move_speed": 1.9, "horizontal": False}
            ])

            level_data["enemies"].extend([
                {"x": 150, "y": 230, "type": "apple", "patrol_range": 50},
                {"x": 550, "y": 310, "type": "telegram", "patrol_range": 120},
                {"x": 950, "y": 360, "type": "vk", "patrol_range": 100},
                {"x": 1350, "y": 300, "type": "apple", "patrol_range": 60},
                {"x": 1750, "y": 200, "type": "microsoft", "patrol_range": 80},
                {"x": 2150, "y": 250, "type": "telegram", "patrol_range": 150},
                {"x": 2550, "y": 320, "type": "vk", "patrol_range": 120},
                {"x": 2950, "y": 280, "type": "apple", "patrol_range": 90}
            ])

        elif level_number == 4:
            # Финальный босс - самый большой
            level_data["platforms"].extend([
                {"x": 400, "y": 250, "width": 6},
                {"x": 900, "y": 350, "width": 6},
                {"x": 1400, "y": 300, "width": 5},
                {"x": 1900, "y": 250, "width": 8},
                {"x": 2400, "y": 400, "width": 6},
                {"x": 2900, "y": 320, "width": 7}
            ])

            level_data["moving_platforms"].extend([
                {"x": 200, "y": 180, "move_range": 150, "move_speed": 2, "horizontal": True},
                {"x": 700, "y": 300, "move_range": 100, "move_speed": 1.5, "horizontal": False},
                {"x": 1200, "y": 400, "move_range": 200, "move_speed": 2.5, "horizontal": True},
                {"x": 1700, "y": 280, "move_range": 180, "move_speed": 2.2, "horizontal": True},
                {"x": 2200, "y": 350, "move_range": 160, "move_speed": 1.8, "horizontal": False},
                {"x": 2700, "y": 220, "move_range": 190, "move_speed": 2.3, "horizontal": True}
            ])

            level_data["enemies"].extend([
                {"x": 600, "y": 400, "type": "google", "patrol_range": 200},
                {"x": 300, "y": 300, "type": "microsoft", "patrol_range": 120},
                {"x": 1100, "y": 350, "type": "apple", "patrol_range": 100},
                {"x": 450, "y": 450, "type": "telegram", "patrol_range": 150},
                {"x": 950, "y": 450, "type": "vk", "patrol_range": 130},
                {"x": 1500, "y": 380, "type": "google", "patrol_range": 180},
                {"x": 1900, "y": 420, "type": "microsoft", "patrol_range": 140},
                {"x": 2300, "y": 350, "type": "apple", "patrol_range": 160},
                {"x": 2800, "y": 380, "type": "google", "patrol_range": 200, "is_boss": True}
            ])

        # Распределяем бонусы по всему огромному уровню
        for i in range(15):
            level_data["powerups"].append({
                "x": 200 + i * 200,
                "y": 250 if level_number == 1 else 300,
                "type": "coin"
            })

        if level_number > 1:
            for i in range(4):
                level_data["powerups"].append({
                    "x": 400 + i * 400,
                    "y": 300,
                    "type": "heart"
                })

        if level_number >= 2:
            for i in range(4):
                level_data["powerups"].append({
                    "x": 600 + i * 500,
                    "y": 350,
                    "type": "speed"
                })

        return level_data

    def load_level(self, level_number):
        """Загрузка уровня из JSON файла"""
        filename = os.path.join(self.levels_dir, f"level{level_number}.json")

        if not os.path.exists(filename):
            print(f"Level file {filename} not found, creating default level")
            level_data = self.create_default_level(level_number)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(level_data, f, ensure_ascii=False, indent=2)
            return level_data

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                level_data = json.load(f)
            return level_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {filename}: {e}")
            return self.create_default_level(level_number)
        except Exception as e:
            print(f"Error loading level {level_number}: {e}")
            return self.create_default_level(level_number)