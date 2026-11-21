"""Потолок, пол и виньетка 3D-вида.

get_shade здесь - та же функция, что была в ray_casting.py: туман по дальности один
для стен и для пола/потолка. Держать две копии нельзя, поэтому при переносе рендера
(часть человека 1) переносить её надо в модуль сцены, а отсюда - импортировать.
"""
import pygame

from Colors.Color import Color
from Settings.Settings import settings


def get_shade(depth: float) -> float:
    """Насколько ярко видеть точку на расстоянии depth (в клетках): 1 - близко, 0 - темно."""
    return max(0.0, 1 - depth / settings.view.Distance) ** 1.5


def create_background() -> pygame.Surface:
    """Потолок и пол. Чем дальше от игрока, тем темнее; создаётся один раз."""
    width = settings.screen.Width
    game_height = settings.screen.Game_height
    half = settings.screen.Half_of_game_height
    surface = pygame.Surface((width, game_height))

    for chord_y in range(game_height):
        # +0.5 - чтобы на строке горизонта не было деления на ноль
        offset = abs(chord_y - half) + 0.5
        shade = get_shade(settings.raycasting.Walls_height / (2 * offset))
        base = Color.Ceiling_color if chord_y < half else Color.Floor_color
        color = tuple(int(channel * shade) for channel in base)
        pygame.draw.line(surface, color, (0, chord_y), (width, chord_y))

    return surface.convert() if pygame.get_init() else surface


def create_vignette() -> pygame.Surface:
    """Тёмные края экрана. Создаётся один раз, потом просто выводится.

    Кольца (не залитые круги) идущие от центра к краям с растущей плотностью:
    залитый круг всегда красит и центр, поэтому прежний вариант затемнял середину
    экрана и оставлял углы чистыми - то есть был анти-виньеткой.
    """
    width = settings.screen.Width
    game_height = settings.screen.Game_height
    overlay = pygame.Surface((width, game_height), pygame.SRCALPHA)
    chord_x, chord_y = width // 2, game_height // 2
    max_r = int((width ** 2 + game_height ** 2) ** 0.5 / 2)
    step = 20

    for radius in range(step, max_r + step, step):
        alpha = int(120 * (radius / max_r) ** 2)
        pygame.draw.circle(overlay, (0, 0, 0, alpha), (chord_x, chord_y), radius, width=step)

    return overlay
