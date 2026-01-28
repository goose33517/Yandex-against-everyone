import json
import os
from settings import SAVE_FILE


class SaveSystem:
    """Система сохранения игры"""

    def __init__(self):
        self.save_file = SAVE_FILE

    def save(self, data):
        """Сохранение данных"""
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load(self):
        """Загрузка данных"""
        if not os.path.exists(self.save_file):
            return None

        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def save_progress(self, level, score):
        """Сохранение прогресса"""
        data = self.load() or {}

        data['current_level'] = level
        data['total_score'] = data.get('total_score', 0) + score

        if 'level_scores' not in data:
            data['level_scores'] = {}

        level_key = f'level_{level}'
        if level_key not in data['level_scores'] or score > data['level_scores'][level_key]:
            data['level_scores'][level_key] = score

        return self.save(data)

    def get_progress(self):
        """Получение прогресса"""
        data = self.load()
        if not data:
            return {'current_level': 1, 'total_score': 0, 'level_scores': {}}

        return data