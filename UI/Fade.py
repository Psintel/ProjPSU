import pygame

from Settings.Settings import settings


class Fade:
    """Слой затемнения на весь экран. 0 - ничего не видно кроме игры, 1 - чёрный экран."""

    _surface: pygame.Surface | None = None

    @classmethod
    def get_surface(cls) -> pygame.Surface:
        """Создаём лениво: pygame.Surface до pygame.init() даёт неконвертированную
        поверхность, а размер экрана на момент импорта модуля ещё неизвестен.
        """
        if cls._surface is None:
            surface = pygame.Surface((settings.screen.Width, settings.screen.Height))
            surface.fill((0, 0, 0))
            cls._surface = surface.convert() if pygame.get_init() else surface
        return cls._surface

    @classmethod
    def draw_fade(cls, screen: pygame.Surface, scale: float) -> None:
        if scale > 0:
            surface = cls.get_surface()
            surface.set_alpha(int(255 * min(scale, 1)))
            screen.blit(surface, (0, 0))
