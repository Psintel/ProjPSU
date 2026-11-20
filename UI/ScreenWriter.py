import pygame
from Colors.Color import Color
from Models.Display import Display
from UI.Fade import Fade
from TextWriter import TextWriter
from Settings.Settings import Settings

class ScreenWriter:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def draw_win_screen(self):
        Fade.draw_fade(self.screen, 0.8)
        TextWriter.draw_text(self.screen, "ВЫ СБЕЖАЛИ!", Display(Settings.screen.Width // 2, Settings.screen.Height // 2 - 40), 64, Color.Green, True, True)
        TextWriter.draw_text(self.screen, "Спасибо за игру", (Settings.screen.Width // 2, Settings.screen.Height // 2 + 40), 28, Color.White, False, True)
        TextWriter.draw_text(self.screen, "Нажмите ESC для выхода", (Settings.screen.Width // 2, Settings.screen.Height // 2 + 100), 22, Color.Gray, False,True)