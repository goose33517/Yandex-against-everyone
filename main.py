import arcade
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR
from core.screens import GameScreen


class YandexMarioGame(arcade.Window):
    """Главный класс игры"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUND_COLOR)

        self.game_screen = None
        self.game_over = False
        self.level_complete = False
        self.current_level_score = 0
        self.total_score = 0

        self.current_screen = "menu"
        self.current_level = 1

        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        """Загрузка звуков"""
        try:
            sound_path = os.path.join("assets", "sounds", "jump.mp3")
            if os.path.exists(sound_path):
                self.sounds['jump'] = arcade.load_sound(sound_path)
        except:
            self.sounds['jump'] = None

        try:
            sound_path = os.path.join("assets", "sounds", "coin.mp3")
            if os.path.exists(sound_path):
                self.sounds['coin'] = arcade.load_sound(sound_path)
        except:
            self.sounds['coin'] = None

        try:
            sound_path = os.path.join("assets", "sounds", "shoot.mp3")
            if os.path.exists(sound_path):
                self.sounds['shoot'] = arcade.load_sound(sound_path)
        except:
            self.sounds['shoot'] = None

        try:
            sound_path = os.path.join("assets", "sounds", "hit.mp3")
            if os.path.exists(sound_path):
                self.sounds['hit'] = arcade.load_sound(sound_path)
        except:
            self.sounds['hit'] = None

    def setup(self):
        """Настройка игры"""
        self.game_screen = GameScreen(self)

    def start_game(self, level=None):
        """Начать игру"""
        if level:
            self.current_level = level
        self.current_screen = "game"
        self.game_over = False
        self.level_complete = False
        self.current_level_score = 0

        try:
            self.game_screen.setup(self.current_level)
            self.game_screen.game_sounds = self.sounds
        except Exception as e:
            print(f"Ошибка запуска игры: {e}")
            self.current_screen = "menu"

    def show_game_over(self, score):
        """Показать экран завершения игры"""
        self.game_over = True
        self.current_screen = "game_over"
        self.current_level_score = score

    def show_level_complete(self, score):
        """Показать экран завершения уровня"""
        self.level_complete = True
        self.current_screen = "level_complete"
        self.current_level_score = score
        self.total_score += score

    def next_level(self):
        """Перейти на следующий уровень"""
        if self.current_level < 4:
            self.current_level += 1
            self.start_game(self.current_level)
        else:
            self.current_screen = "menu"

    def on_draw(self):
        """Отрисовка"""
        self.clear()

        if self.current_screen == "menu":
            arcade.draw_text(
                "Яндекс-Марио",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 100,
                arcade.color.YELLOW,
                60,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                "Нажмите ПРОБЕЛ чтобы начать",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.WHITE,
                30,
                anchor_x="center"
            )

            arcade.draw_text(
                f"Текущий уровень: {self.current_level}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50,
                arcade.color.LIGHT_GRAY,
                20,
                anchor_x="center"
            )

            arcade.draw_text(
                f"Общий счет: {self.total_score}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 100,
                arcade.color.YELLOW,
                24,
                anchor_x="center"
            )

            arcade.draw_text(
                "ESC - выход",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 150,
                arcade.color.LIGHT_GRAY,
                20,
                anchor_x="center"
            )
        elif self.current_screen == "game":
            try:
                self.game_screen.on_draw()
            except Exception as e:
                print(f"Ошибка отрисовки игры: {e}")
                self.current_screen = "menu"
        elif self.current_screen == "game_over":
            arcade.draw_text(
                "ИГРА ОКОНЧЕНА",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 200,
                arcade.color.RED,
                60,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                f"Уровень: {self.current_level}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 50,
                arcade.color.WHITE,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                f"Счет: {self.current_level_score}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.YELLOW,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                f"Общий счет: {self.total_score}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50,
                arcade.color.YELLOW,
                30,
                anchor_x="center"
            )

            arcade.draw_text(
                "Нажмите ПРОБЕЛ чтобы повторить",
                SCREEN_WIDTH // 2,
                200,
                arcade.color.LIGHT_GRAY,
                24,
                anchor_x="center"
            )

            arcade.draw_text(
                "ESC - выход в меню",
                SCREEN_WIDTH // 2,
                150,
                arcade.color.LIGHT_GRAY,
                20,
                anchor_x="center"
            )
        elif self.current_screen == "level_complete":
            arcade.draw_text(
                "УРОВЕНЬ ПРОЙДЕН!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 200,
                arcade.color.GREEN,
                60,
                anchor_x="center",
                bold=True
            )

            arcade.draw_text(
                f"Уровень: {self.current_level}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 50,
                arcade.color.WHITE,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                f"Счет уровня: {self.current_level_score}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.YELLOW,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                f"Общий счет: {self.total_score}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50,
                arcade.color.YELLOW,
                30,
                anchor_x="center"
            )

            if self.current_level < 4:
                arcade.draw_text(
                    "Нажмите ПРОБЕЛ для следующего уровня",
                    SCREEN_WIDTH // 2,
                    200,
                    arcade.color.LIGHT_GRAY,
                    24,
                    anchor_x="center"
                )
            else:
                arcade.draw_text(
                    "ИГРА ПРОЙДЕНА!",
                    SCREEN_WIDTH // 2,
                    250,
                    arcade.color.GOLD,
                    50,
                    anchor_x="center",
                    bold=True
                )
                arcade.draw_text(
                    "Нажмите ESC для выхода в меню",
                    SCREEN_WIDTH // 2,
                    150,
                    arcade.color.LIGHT_GRAY,
                    24,
                    anchor_x="center"
                )

    def on_update(self, delta_time):
        """Обновление логики"""
        if self.current_screen == "game":
            try:
                self.game_screen.on_update(delta_time)
            except Exception as e:
                print(f"Ошибка обновления игры: {e}")
                self.current_screen = "menu"

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if key == arcade.key.ESCAPE:
            if self.current_screen == "menu":
                arcade.close_window()
            else:
                self.current_screen = "menu"
                self.game_over = False
                self.level_complete = False

        if self.current_screen == "menu" and key == arcade.key.SPACE:
            self.start_game(1)
        elif self.current_screen == "game":
            try:
                self.game_screen.on_key_press(key, modifiers)
            except Exception as e:
                print(f"Ошибка обработки клавиши: {e}")
        elif self.current_screen == "game_over" and key == arcade.key.SPACE:
            self.start_game(self.current_level)
        elif self.current_screen == "level_complete" and key == arcade.key.SPACE:
            if self.current_level < 4:
                self.next_level()

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if self.current_screen == "game":
            try:
                self.game_screen.on_key_release(key, modifiers)
            except Exception as e:
                print(f"Ошибка отпускания клавиши: {e}")


def main():
    """Главная функция"""
    window = YandexMarioGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()