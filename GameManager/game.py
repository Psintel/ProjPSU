import math
import pygame

from InventoryHandler.InventoryHandler import InventoryHandler
from Player.Player import Player
from Settings.Settings import settings
from UI.Backgrounds import create_background, create_vignette, get_shade
from UI.Door import Door, Side
from UI.GameElementDrawer import GameElementDrawer
from UI.ScreenWriter import ScreenWriter
from map import GameMap


class Game:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.won = False

        InventoryHandler.initialize({})

        self.game_map = GameMap()
        spawn_x, spawn_y, spawn_angle = self.game_map.load_level(0)
        self.player = Player(x=spawn_x, y=spawn_y, angle=spawn_angle)
        self.screen_writer = ScreenWriter(screen)
        self.drawer = GameElementDrawer(screen, self.clock)

        door_surf = pygame.Surface(settings.door.Animation_size).convert()
        door_surf.fill((90, 50, 25))
        self.door = Door(door_surf)

        self.background = create_background()
        self.vignette = create_vignette()

        self.fov = math.pi / 3
        self.num_rays = 320
        self.ray_width = settings.screen.Width // self.num_rays
        self.z_buffer: list[float] = [settings.view.Distance] * self.num_rays

        self.unlocked_doors: set[tuple[int, int, int]] = set()
        self.status_message = self.game_map.level_name
        self.status_timer = 4.0
        self.door_hint = ""

    def _set_status(self, text: str, duration: float = 3.5) -> None:
        self.status_message = text
        self.status_timer = duration

    def _get_door_in_front(self) -> tuple[int, int, int] | None:
        cos_a = math.cos(self.player.angle)
        sin_a = math.sin(self.player.angle)

        for i in range(1, 18):
            dist = i * 0.1
            tx = int(self.player.x + cos_a * dist)
            ty = int(self.player.y + sin_a * dist)
            tile = self.game_map.get_tile(tx, ty)
            if tile in (2, 3, 4, 5):
                return tx, ty, tile
            if tile == 1:
                break
        return None

    def _update_door_prompt(self) -> None:
        door_info = self._get_door_in_front()
        if not door_info:
            self.door_hint = ""
            return

        tx, ty, tile = door_info
        is_unlocked = (self.game_map.level_index, tx, ty) in self.unlocked_doors

        if tile == 2:
            if is_unlocked or "key_red" in self.player.keys:
                self.door_hint = "Нажмите [E], чтобы пройти через красную дверь"
            else:
                self.door_hint = "Закрыто: нужен Красный ключ"
        elif tile == 3:
            if is_unlocked or "key_blue" in self.player.keys:
                self.door_hint = "Нажмите [E], чтобы пройти через синюю дверь"
            else:
                self.door_hint = "Закрыто: нужен Синий ключ"
        elif tile == 4:
            if self.player.has_mask:
                self.door_hint = "Нажмите [E], чтобы сбежать из ПГНИУ!"
            else:
                self.door_hint = "Выход закрыт: нужен противогаз (уголь, марля, бутылка)"
        elif tile == 5:
            self.door_hint = "Нажмите [E], чтобы перейти на следующий этаж"

    def _pass_through_door(self, tx: int, ty: int) -> None:
        """Переносит игрока на противоположную сторону двери (tx, ty), оставляя её на карте."""
        self.unlocked_doors.add((self.game_map.level_index, tx, ty))

        dx = (tx + 0.5) - self.player.x
        dy = (ty + 0.5) - self.player.y

        if abs(dx) >= abs(dy):
            step = 1.0 if dx > 0 else -1.0
            new_x, new_y = tx + 0.5 + step, ty + 0.5
        else:
            step = 1.0 if dy > 0 else -1.0
            new_x, new_y = tx + 0.5, ty + 0.5 + step

        if not self.game_map.is_blocked(new_x, new_y):
            self.player.x = new_x
            self.player.y = new_y

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_e and not self.won and not self.door.active:
                    self._interact()

    def _interact(self) -> None:
        door_info = self._get_door_in_front()
        if not door_info:
            return

        tx, ty, tile = door_info
        is_unlocked = (self.game_map.level_index, tx, ty) in self.unlocked_doors

        if tile == 2:
            if is_unlocked or "key_red" in self.player.keys:
                self.door.start(lambda x=tx, y=ty: self._pass_through_door(x, y), Side.Dir_left)
            else:
                self._set_status("Нужен Красный ключ!")
        elif tile == 3:
            if is_unlocked or "key_blue" in self.player.keys:
                self.door.start(lambda x=tx, y=ty: self._pass_through_door(x, y), Side.Dir_right)
            else:
                self._set_status("Нужен Синий ключ!")
        elif tile == 4:
            if self.player.has_mask:
                self.door.start(self._win_game, Side.Dir_left)
            else:
                self._set_status("Без противогаза наружу нельзя!")
        elif tile == 5:
            if self.game_map.has_next_level():
                self.door.start(self._go_to_next_level, Side.Dir_right)
            else:
                self._set_status("Дальше прохода нет")

    def _go_to_next_level(self) -> None:
        next_idx = self.game_map.level_index + 1
        spawn_x, spawn_y, spawn_angle = self.game_map.load_level(next_idx)
        self.player.x = spawn_x
        self.player.y = spawn_y
        self.player.angle = spawn_angle
        self._set_status(self.game_map.level_name, 4.0)

    def _win_game(self) -> None:
        self.won = True

    def _check_item_pickups(self) -> None:
        for item in self.game_map.world_items:
            if item["collected"]:
                continue
            dist = math.hypot(self.player.x - item["x"], self.player.y - item["y"])
            if dist < 0.6:
                item["collected"] = True
                if item["type"] == "key":
                    self.player.keys.add(item["id"])
                    name = settings.keys.Names[item["id"]][0]
                    self._set_status(f"Подобран: {name}")
                else:
                    self.player.inventory.add(item["id"])
                    name = settings.items.Names[item["id"]]
                    self._set_status(f"Подобран компонент: {name}")
                    if {"coal", "gauze", "bottle"}.issubset(self.player.inventory):
                        self.player.has_mask = True
                        self._set_status("Противогаз собран! Ищи зелёный выход!", 5.0)

    def update(self, dt: float) -> None:
        self.door.update(dt)

        if self.status_timer > 0:
            self.status_timer -= dt
            if self.status_timer <= 0:
                self.status_message = ""

        if self.won or self.door.active:
            self.door_hint = ""
            return

        self.player.update(dt, self.game_map)
        self._check_item_pickups()
        self._update_door_prompt()
        InventoryHandler.update(self.player.inventory, self.player.keys)

    def _cast_rays(self) -> None:
        start_angle = self.player.angle - self.fov / 2
        delta_angle = self.fov / self.num_rays
        max_depth = settings.view.Distance
        half_h = settings.screen.Half_of_game_height

        wall_colors = {
            1: (130, 135, 145),
            2: (200, 60, 60),
            3: (60, 110, 220),
            4: (70, 200, 90),
            5: (225, 185, 55),
        }

        for ray in range(self.num_rays):
            angle = start_angle + ray * delta_angle
            sin_a = math.sin(angle)
            cos_a = math.cos(angle)

            depth = 0.0
            hit_tile = 0
            while depth < max_depth:
                depth += 0.03
                target_x = int(self.player.x + cos_a * depth)
                target_y = int(self.player.y + sin_a * depth)
                tile = self.game_map.get_tile(target_x, target_y)
                if tile != 0:
                    hit_tile = tile
                    break

            if hit_tile != 0:
                corrected_depth = depth * math.cos(self.player.angle - angle)
                self.z_buffer[ray] = corrected_depth

                wall_h = min(
                    settings.screen.Game_height,
                    int(settings.raycasting.Walls_height / (corrected_depth + 0.0001)),
                )
                shade = get_shade(corrected_depth)
                base_color = wall_colors.get(hit_tile, (120, 120, 120))
                shaded_color = tuple(int(c * shade) for c in base_color)

                rect = pygame.Rect(
                    ray * self.ray_width,
                    half_h - wall_h // 2,
                    self.ray_width + 1,
                    wall_h,
                )
                pygame.draw.rect(self.screen, shaded_color, rect)
            else:
                self.z_buffer[ray] = max_depth

    def _draw_items_3d(self) -> None:
        item_colors = {
            "key_red": (255, 70, 70),
            "key_blue": (70, 140, 255),
            "coal": (60, 60, 65),
            "gauze": (240, 240, 245),
            "bottle": (90, 210, 220),
        }

        visible_items = []
        for item in self.game_map.world_items:
            if item["collected"]:
                continue
            dx = item["x"] - self.player.x
            dy = item["y"] - self.player.y
            dist = math.hypot(dx, dy)
            if 0.2 < dist < settings.view.Distance:
                visible_items.append((dist, dx, dy, item))

        visible_items.sort(key=lambda entry: entry[0], reverse=True)

        half_w = settings.screen.Width // 2
        half_h = settings.screen.Half_of_game_height

        for dist, dx, dy, item in visible_items:
            theta = math.atan2(dy, dx)
            gamma = theta - self.player.angle
            while gamma > math.pi:
                gamma -= 2 * math.pi
            while gamma < -math.pi:
                gamma += 2 * math.pi

            if abs(gamma) > self.fov / 2 + 0.2:
                continue

            screen_x = int(half_w + (gamma / (self.fov / 2)) * half_w)
            ray_idx = int(screen_x // self.ray_width)

            if 0 <= ray_idx < self.num_rays and dist >= self.z_buffer[ray_idx]:
                continue

            proj_height = int(settings.raycasting.Walls_height / dist)
            radius = max(6, proj_height // 8)
            screen_y = half_h + proj_height // 3

            shade = get_shade(dist)
            base_color = item_colors.get(item["id"], (255, 220, 60))
            color = tuple(int(c * shade) for c in base_color)

            pygame.draw.circle(self.screen, color, (screen_x, screen_y), radius)
            pygame.draw.circle(self.screen, (255, 255, 255), (screen_x, screen_y), radius, 1)

    def _draw_minimap(self) -> None:
        tile_px = 14
        margin = 20
        map_w = self.game_map.width * tile_px
        offset_x = settings.screen.Width - map_w - margin
        offset_y = margin

        bg = pygame.Surface((map_w + 8, self.game_map.height * tile_px + 8), pygame.SRCALPHA)
        bg.fill((10, 10, 15, 180))
        self.screen.blit(bg, (offset_x - 4, offset_y - 4))

        tile_colors = {
            0: (45, 48, 55),
            1: (130, 135, 145),
            2: (220, 60, 60),
            3: (60, 120, 240),
            4: (70, 210, 90),
            5: (225, 185, 55),
        }

        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                tile = self.game_map.get_tile(x, y)
                rect = pygame.Rect(offset_x + x * tile_px, offset_y + y * tile_px, tile_px - 1, tile_px - 1)
                pygame.draw.rect(self.screen, tile_colors.get(tile, (80, 80, 80)), rect)

        for item in self.game_map.world_items:
            if not item["collected"]:
                ix = int(offset_x + item["x"] * tile_px)
                iy = int(offset_y + item["y"] * tile_px)
                pygame.draw.circle(self.screen, (255, 220, 70), (ix, iy), 3)

        px = int(offset_x + self.player.x * tile_px)
        py = int(offset_y + self.player.y * tile_px)
        pygame.draw.circle(self.screen, (255, 255, 255), (px, py), 4)
        look_x = int(px + math.cos(self.player.angle) * 10)
        look_y = int(py + math.sin(self.player.angle) * 10)
        pygame.draw.line(self.screen, (255, 255, 100), (px, py), (look_x, look_y), 2)

    def draw(self) -> None:
        if self.door.blackout:
            self.screen.fill((0, 0, 0))
        else:
            self.drawer.draw_hud(self.player, self.status_message, self.door_hint)
            self.screen.blit(self.background, (0, 0))
            self._cast_rays()
            self._draw_items_3d()
            self.screen.blit(self.vignette, (0, 0))

            self.drawer.draw_crosshair()
            self.drawer.draw_fps()
            self._draw_minimap()

        self.door.draw(self.screen)
        if self.won:
            self.screen_writer.draw_win_screen()

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(settings.screen.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()