from typing import Any

import pygame
from Colors.Color import Color
from Models.Display import Display
from Models.ParametrizedLine import ParametrizedLine
from UI.Fade import Fade
from TextWriter import TextWriter
from Settings.Settings import Settings
from Models.Text import Text

class ScreenWriter:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def draw_win_screen(self):
        Fade.draw_fade(self.screen, 0.8)
        TextWriter.draw_text(self.screen, "ВЫ СБЕЖАЛИ!", Display(Settings.screen.Width // 2, Settings.screen.Height // 2 - 40), 64, Color.Green, True, True)
        TextWriter.draw_text(self.screen, "Спасибо за игру", (Settings.screen.Width // 2, Settings.screen.Height // 2 + 40), 28, Color.White, False, True)
        TextWriter.draw_text(self.screen, "Нажмите ESC для выхода", (Settings.screen.Width // 2, Settings.screen.Height // 2 + 100), 22, Color.Gray, False,True)

    def show_text_screen(self, text: Text, hold: float) -> Any:
        screen = pygame.Surface((Settings.screen.Width, Settings.screen.Height), pygame.SRCALPHA)
        total_height = sum(int(size * 1.5) for _, size, _, _ in text.lines)
        y = Settings.screen.Height // 2 - total_height // 2
        for text, size, color, bold in text.lines:
            line_h = int(size * 1.5)
            TextWriter.draw_text(screen, text, Display(Settings.screen.Width // 2, y + line_h // 2), size, color, bold, True)
            y += line_h
        TextWriter.draw_text(screen, "Нажмите любую клавишу", Display(Settings.screen.Width // 2, Settings.screen.Height - 50), 18, Color.Gray, False, True)

        return self.__disappear(screen, hold)

    def __disappear(self, screen: pygame.Surface, hold: float) -> Any:
        clock = pygame.time.Clock()
        time = 0.0
        leave_at = Settings.title.Fade_time + hold

        while True:
            time += clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    leave_at = min(leave_at, time)

            if time - leave_at >= Settings.title.Fade_time:
                return True

            fade_in = min(time / Settings.title.Fade_time, 1.0)
            fade_out = 1.0 - max(0.0, time - leave_at) / Settings.title.Fade_time
            screen.set_alpha(int(255 * max(0.0, min(fade_in, fade_out))))

            self.screen.fill((0, 0, 0))
            self.screen.blit(screen, (0, 0))
            pygame.display.flip()

    def show_messages(self) -> Any:
        for lines in Settings.title.Pre_intro_messages:
            text = Text([ParametrizedLine(line, 32, Color.White, False) for line in lines])
            if not self.show_text_screen(text, Settings.title.Message_hold_time):
                return False
        return True

    def show_title_screen(self) -> Any:
        text = [Text(ParametrizedLine(Settings.title.Text, 72, Color.Red, True))]
        text.lines += [ParametrizedLine(line, 30, Color.White, False) for line in Settings.title.Lines]
        return self.show_text_screen(text, Settings.title.Hold_time)
