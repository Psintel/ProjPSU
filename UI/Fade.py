import pygame
from Settings.Settings import settings

class Fade:
    fade_surface = pygame.Surface(settings.screen.Width, settings.screen.Height)

    @staticmethod
    def draw_fade(screen: pygame.Surface, scale: float):
        if scale > 0:
            Fade.fade_surface.set_alpha(int(255 * min(scale, 1)))
            screen.blit(Fade.fade_surface, (0, 0))

