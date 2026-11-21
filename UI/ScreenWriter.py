"""Экраны поверх всего: победа, титул, сообщения перед интро.

Порт intro.py (show_text_screen/show_messages/show_title_screen) и ui.draw_win_screen.
Каждый показ текста - свой короткий цикл (появление -> hold -> исчезновение) со
своей обработкой событий: возвращаем False, только если игрок закрыл окно.
Видео (Intro/IntroPlayer) и эти экраны оба рисуют на весь экран, поэтому порядок
показа задаёт один владелец цикла - GameManager, а не каждый экран сам за себя.
"""
import pygame

from Colors.Color import Color
from Models.ParametrizedLine import ParametrizedLine
from Models.Text import Text
from Settings.Settings import settings
from UI.Fade import Fade
from UI.TextWriter import TextWriter


class ScreenWriter:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def draw_win_screen(self) -> None:
        center_x = settings.screen.Width // 2
        center_y = settings.screen.Height // 2
        Fade.draw_fade(self.screen, 0.8)
        TextWriter.draw_text(self.screen, "ВЫ СБЕЖАЛИ!", (center_x, center_y - 40), 64, Color.Green, True, True)
        TextWriter.draw_text(self.screen, "Спасибо за игру", (center_x, center_y + 40), 28, center=True)
        TextWriter.draw_text(self.screen, "Нажмите ESC для выхода", (center_x, center_y + 100), 22, Color.Gray, center=True)

    def show_text_screen(self, text: Text, hold: float) -> bool:
        """Текст на чёрном фоне: плавно появляется, держится hold секунд, плавно исчезает.
        Пропуск - любая клавиша или клик.
        """
        width, height = settings.screen.Width, settings.screen.Height
        layer = pygame.Surface((width, height), pygame.SRCALPHA)

        y = height // 2 - text.height // 2
        for line in text.lines:
            TextWriter.draw_text(
                layer, line.line, (width // 2, y + line.height // 2),
                line.text_size, line.color, line.bold, True,
            )
            y += line.height
        TextWriter.draw_text(layer, "Нажмите любую клавишу", (width // 2, height - 50), 18, Color.Gray, center=True)

        return self.__disappear(layer, hold)

    def __disappear(self, layer: pygame.Surface, hold: float) -> bool:
        fade_time = settings.title.Fade_time
        clock = pygame.time.Clock()
        elapsed = 0.0
        leave_at = fade_time + hold           # когда начинать исчезать

        while True:
            elapsed += clock.tick(settings.screen.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    leave_at = min(leave_at, elapsed)

            if elapsed - leave_at >= fade_time:
                return True

            fade_in = min(elapsed / fade_time, 1.0)
            fade_out = 1.0 - max(0.0, elapsed - leave_at) / fade_time
            layer.set_alpha(int(255 * max(0.0, min(fade_in, fade_out))))

            self.screen.fill((0, 0, 0))
            self.screen.blit(layer, (0, 0))
            pygame.display.flip()

    def show_messages(self) -> bool:
        """Сообщения перед интро. False - игрок закрыл окно, игру не запускаем."""
        for lines in settings.title.Pre_intro_messages:
            text = Text(ParametrizedLine(line, 32) for line in lines)
            if not self.show_text_screen(text, settings.title.Message_hold_time):
                return False
        return True

    def show_title_screen(self) -> bool:
        """Название игры после видео."""
        text = Text([ParametrizedLine(settings.title.Text, 72, Color.Red, True)])
        for line in settings.title.Lines:
            text.add(ParametrizedLine(line, 30))
        return self.show_text_screen(text, settings.title.Hold_time)
