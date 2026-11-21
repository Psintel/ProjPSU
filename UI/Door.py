"""Дверь между комнатами: экран темнеет (останется только дверь) -> дверь уезжает в
стену на чёрном фоне -> action() (смена комнаты/победа) -> новая сцена проявляется.

Порт transition.py один-в-один по поведению, кроме трёх мест:
  * состояние вынесено в Models/DoorStates, направление - в Side;
  * якорь: rect центрируется по Half_of_game_height (линия горизонта 3D-вида), а не по
    всему экрану - с Height=1080 нижняя половина двери уезжала за край и на HUD;
  * action() вызывается ровно один раз и обнуляется, transition-колбэк не должен
    пережить переход.
"""
from enum import Enum

import pygame

from Models.DoorStates import DoorStates
from Settings.Settings import settings
from UI.Fade import Fade


class Side(int, Enum):
    """Куда уезжает дверь. int - потому что направление множится на прогресс анимации."""

    Dir_left = -1
    Dir_right = 1


class Door:
    def __init__(self, image: pygame.Surface) -> None:
        self.image = image
        self.rect = pygame.Rect(0, 0, *settings.door.Animation_size)
        self.rect.center = (settings.screen.Width // 2, settings.screen.Half_of_game_height)
        self.state = DoorStates.Idle
        self.timer = 0.0
        self.direction = Side.Dir_left
        self.action = None

    @property
    def active(self) -> bool:
        return self.state != DoorStates.Idle

    @property
    def blackout(self) -> bool:
        """True, когда экран полностью чёрный и игру рисовать не нужно."""
        return self.state == DoorStates.Opening

    def start(self, action, direction: Side = Side.Dir_left) -> None:
        self.state = DoorStates.Darken
        self.timer = 0.0
        self.direction = Side(direction)
        self.action = action

    def update(self, dt: float) -> None:
        """dt - секунды (clock.tick(FPS) / 1000), не миллисекунды."""
        if not self.active:
            return

        self.timer += dt
        if self.state == DoorStates.Darken and self.timer >= settings.door.Fade_time:
            self.state, self.timer = DoorStates.Opening, 0.0
        elif self.state == DoorStates.Opening and self.timer >= settings.door.Opening_time:
            action, self.action = self.action, None
            if action:
                action()
            self.state, self.timer = DoorStates.Fade_in, 0.0
        elif self.state == DoorStates.Fade_in and self.timer >= settings.door.Fade_time:
            self.state, self.timer = DoorStates.Idle, 0.0

    def draw(self, screen: pygame.Surface) -> None:
        """Вызывать ПОСЛЕ отрисовки игры и HUD (или на чёрном экране при blackout)."""
        if self.state == DoorStates.Darken:
            t = min(self.timer / settings.door.Fade_time, 1.0)
            Fade.draw_fade(screen, t)
            self.draw_door(screen, 0.0, int(255 * t))
        elif self.state == DoorStates.Opening:
            self.draw_door(screen, self.timer / settings.door.Opening_time)
        elif self.state == DoorStates.Fade_in:
            Fade.draw_fade(screen, max(0.0, 1.0 - self.timer / settings.door.Fade_time))

    def draw_door(self, screen: pygame.Surface, progress: float, alpha: int = 255) -> None:
        progress = min(progress, 1.0)
        progress = progress * progress * (3 - 2 * progress)    # плавный старт и остановка

        self.image.set_alpha(alpha)
        screen.set_clip(self.rect)                             # дверь уезжает "в стену"
        offset = int(self.direction * progress * self.rect.width)
        screen.blit(self.image, (self.rect.x + offset, self.rect.y))
        screen.set_clip(None)
        if alpha == 255:
            pygame.draw.rect(screen, (40, 20, 10), self.rect, 6)   # рамка
