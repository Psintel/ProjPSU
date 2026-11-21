from enum import Enum
import pygame
from Models.DoorStates import DoorStates
from Settings.Settings import Settings
from Fade import Fade

class Side(Enum):
    Dir_left = -1
    Dir_right = 1

class Door:
    def __init__(self, image):
        self.image = image
        self.rect = pygame.Rect(0, 0, *Settings.door.Animation_size)
        self.rect.center = (Settings.screen.Width // 2, Settings.screen.Height)
        self.state = DoorStates.Idle
        self.timer = 0.0
        self.direction = Side.Dir_left
        self.action = None

    @property
    def active(self):
        return self.state != DoorStates.Idle

    @property
    def blackout(self):
        return self.state == DoorStates.Opening

    def start(self, action, direction):
        self.state = DoorStates.Darken
        self.timer = 0.0
        self.direction = direction
        self.action = action

    def update(self, dt: int):
        self.timer += dt
        if self.state == DoorStates.Darken and self.timer >= Settings.door.Fade_time:
            self.state, self.timer = DoorStates.Opening, 0.0
        elif self.state == DoorStates.Opening and self.timer >= Settings.door.Opening_time:
            self.action()
            self.state, self.timer = DoorStates.Fade_in, 0.0
        elif self.state == DoorStates.Fade_in and self.timer >= Settings.door.Fade_time:
            self.state = DoorStates.Idle

    def draw(self, screen: pygame.Surface):
        if self.state == DoorStates.Darken:
            t = min(self.timer / Settings.door.Fade_time, 1.0)
            Fade.draw_fade(screen, t)
            self.draw_door(screen, 0.0, int(255 * t))
        elif self.state == DoorStates.Opening:
            self.draw_door(screen, self.timer / Settings.door.Opening_time)
        elif self.state == DoorStates.Fade_in:
            Fade.draw_fade(screen, max(0.0, 1.0 - self.timer / Settings.door.Fade_time))

    def draw_door(self, screen: pygame.Surface, progress, alpha=255):
        progress = min(progress, 1.0)
        progress = progress * progress * (3 - 2 * progress)

        self.image.set_alpha(alpha)
        screen.set_clip(self.rect)
        offset = self.direction * progress * self.rect.width
        screen.blit(self.image, (self.rect.x + offset, self.rect.y))
        screen.set_clip(None)
        if alpha == 255:
            pygame.draw.rect(screen, (40, 20, 10), self.rect, 6)