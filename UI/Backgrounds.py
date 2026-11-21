import pygame
from Settings.Settings import settings
from Colors.Color import Color

def create_background() -> pygame.Surface:
    surface = pygame.Surface((settings.screen.Width, settings.hud.Game_height))
    for chord_y in range(settings.hud.Game_height):
        offset = abs(chord_y - settings.hud.Half_of_game_height)
        shade = get_shade(settings.raycasting.Walls_height / (2 * offset))
        base = Color.Ceiling_color if chord_y < settings.hud.Half_of_game_height else Color.Floor_color

        r_shade = 0
        g_shade = 0
        b_shade = 0
        for r, g, b in base:
            r_shade = int(r * shade)
            g_shade = int(g * shade)
            b_shade = int(b * shade)

        color = (r_shade, g_shade, b_shade)
        pygame.draw.line(surface, color, (0, chord_y), (settings.screen.Width, chord_y))

    return surface.convert()

def create_vignette() -> pygame.Surface:
    overlay = pygame.Surface((settings.screen.Width, settings.hud.Game_height), pygame.SRCALPHA)
    chord_x, chord_y = settings.screen.Width // 2, settings.hud.Half_of_game_height
    max_r = int((settings.screen.Width ** 2 + settings.hud.Half_of_game_height ** 2) ** 0.5 / 2)
    for r in range(max_r, 0, -20):
        alpha = int(120 * (1 - r / max_r) ** 2)
        pygame.draw.circle(overlay, (0, 0, 0, alpha), (chord_x, chord_y), r)
    return overlay

def get_shade(depth):
    return max(0, 1 - depth / settings.view.Distance) ** 1.5