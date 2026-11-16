import pygame
from Logging.Logger import Logger
from typing import Any
from Colors.Color import Color
from Models.Display import Display
from Errors import TextSizeError

class TextWriter:
    font_cache = {}

    @staticmethod
    def __get_font(text_size: int, bold: Any):
        key = (text_size, bold)
        if key not in TextWriter.font_cache:
            TextWriter.font_cache[key] = pygame.font.SysFont("Arial", text_size, bold)
        return TextWriter.font_cache[key]

    @staticmethod
    def draw_text(screen: pygame.Surface, text: str, display: Display, text_size: int, color: Color, bold: Any, center: Any):
        if text_size <= 0:
            Logger.error("Text size couldn't be 0")
            raise TextSizeError

        surface = TextWriter.__get_font(text_size, bold).render(text, True, color)
        if center:
            rect = surface.get_rect(center=(display.width, display.height))
        else:
            rect = surface.get_rect(topleft=(display.width, display.height))

        screen.blit(surface, rect)

