import pygame

from Colors.Color import Color
from Errors.TextSizeError import TextSizeError
from Logging.Logger import Logger
from Models.Display import Display

class TextWriter:
    font_cache: dict[tuple[int, bool], pygame.font.Font] = {}
    font_name: str = "arial"

    @classmethod
    def get_font(cls, text_size: int, bold: bool = False) -> pygame.font.Font:
        pygame.init()
        key = (text_size, bold)
        if key not in cls.font_cache:
            cls.font_cache[key] = pygame.font.SysFont(cls.font_name, text_size, bold)
        return cls.font_cache[key]

    @staticmethod
    def draw_text(
        screen: pygame.Surface,
        text: str,
        position: tuple[int, int] | Display,
        text_size: int = 24,
        color: Color = Color.White,
        bold: bool = False,
        center: bool = False,
    ) -> pygame.Rect:
        """position - точка (x, y); Display принимается для совместимости и читается
        как (width, height). center=True значит "поставить центр текста в эту точку",
        поэтому координата - центр, а не угол: get_rect(center=...) сам всё считает,
        `display.width` целиком как координата уводил текст за правый край экрана.
        """
        try:
            size = int(text_size)
        except (TypeError, ValueError):
            size = 0
        if size <= 0:
            Logger.error(f"TextWriter.draw_text: UI size couldn't be 0: {text_size!r}")
            raise TextSizeError(f"UI size must be a positive integer, got {text_size!r}")

        x, y = (position.width, position.height) if isinstance(position, Display) else position
        surface = TextWriter.get_font(size, bold).render(str(text), True, color)
        rect = surface.get_rect(center=(x, y)) if center else surface.get_rect(topleft=(x, y))
        screen.blit(surface, rect)
        return rect
