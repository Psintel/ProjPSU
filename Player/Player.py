"""Состояние игрока, которое читает интерфейс.

Движение/поворот/коллизии - часть человека 1, и он же решит, в каком модуле жить
Player'у. Здесь только те поля, без которых не запустится HUD: инвентарь, ключи,
наличие противогаза. Как только человек 1 перенесёт своего Player'а сюда, эти три поля
остаться должны как есть - на них завязан InventoryHandler.
"""


import math
import pygame


class Player:
    def __init__(self, x: float = 1.5, y: float = 1.5, angle: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.inventory: set[str] = set()   # 'coal', 'gauze', 'bottle'
        self.keys: set[str] = set()        # 'key_red', 'key_blue'
        self.has_mask: bool = False

        self.speed: float = 3.0       # клеток в секунду
        self.rot_speed: float = 2.2   # радиан в секунду
        self.radius: float = 0.2      # радиус хитбокса

    def update(self, dt: float, game_map) -> None:
        """Движение (WASD / стрелки) и поворот (стрелки / Q) с учетом коллизий."""
        keys = pygame.key.get_pressed()

        # Поворот влево / вправо (клавиша E освобождена для открытия дверей)
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.angle -= self.rot_speed * dt
        if keys[pygame.K_RIGHT]:
            self.angle += self.rot_speed * dt

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        dx, dy = 0.0, 0.0
        move_step = self.speed * dt

        # Вперед / Назад
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx += cos_a * move_step
            dy += sin_a * move_step
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx -= cos_a * move_step
            dy -= sin_a * move_step

        # Шаг боком (стрейф)
        if keys[pygame.K_a]:
            dx += sin_a * move_step
            dy -= cos_a * move_step
        if keys[pygame.K_d]:
            dx -= sin_a * move_step
            dy += cos_a * move_step

        self._move_with_collisions(dx, dy, game_map)

    def _move_with_collisions(self, dx: float, dy: float, game_map) -> None:
        """Раздельная проверка коллизий по X и Y для скольжения вдоль стен."""
        margin_x = self.radius if dx > 0 else -self.radius
        if not game_map.is_blocked(self.x + dx + margin_x, self.y):
            self.x += dx

        margin_y = self.radius if dy > 0 else -self.radius
        if not game_map.is_blocked(self.x, self.y + dy + margin_y):
            self.y += dy

    def reset(self) -> None:
        """Состояние на новый заход, иначе инвентарь течёт между партиями."""
        self.inventory.clear()
        self.keys.clear()
        self.has_mask = False