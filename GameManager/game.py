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
        self.player = Player(x=1.5, y=1.5, angle=0.0)
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

        self.status_message = "Найди красный ключ и собери противогаз"
        self.status_timer = 4.0
        self.door_hint = ""

    def _set_status(self, text: str, duration: float = 3.5) -> None:
        self.status_message = text
        self.status_timer = duration

    def _get_door_in_front(self) -> tuple[int, int, int] | None:
        cos_a = math.cos(self.player.angle)
        sin_a = math.sin(self.player.angle)

        for dist in (0.4, 0.7, 1.0, 1.3):
            tx = int(self.player.x + cos_a * dist)
            ty = int(self.player.y + sin_a * dist)
            tile = self.game_map.get_tile(tx, ty)
            if tile in (2, 3, 4):
                return tx, ty, tile
            if tile == 1:
                break
        return None

    def _update_door_prompt(self) -> None:
        door_info = self._get_door_in_front()
        if not door_info:
            self.door_hint = ""
            return

        _, _, tile = door_info
        if tile == 2:
            if "key_red" in self.player.keys:
                self.door_hint = "Нажмите [E], чтобы открыть красную дверь"
            else:
                self.door_hint = "Закрыто: нужен Красный ключ"
        elif tile == 3:
            if "key_blue" in self.player.keys:
                self.door_hint = "Нажмите [E], чтобы открыть синюю дверь"
            else:
                self.door_hint = "Закрыто: нужен Синий ключ"
        elif tile == 4:
            if self.player.has_mask:
                self.door_hint = "Нажмите [E], чтобы сбежать из ПГНИУ!"
            else:
                self.door_hint = "Выход закрыт: нужен противогаз (уголь, марля, бутылка)"

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
        if tile == 2:
            if "key_red" in self.player.keys:
                self.door.start(lambda x=tx, y=ty: self.game_map.open_door(x, y), Side.Dir_left)
                self._set_status("Красная дверь открыта!")
            else:
                self._set_status("Нужен Красный ключ!")
        elif tile == 3:
            if "key_blue" in self.player.keys:
                self.door.start(lambda x=tx, y=ty: self.game_map.open_door(x, y), Side.Dir_right)
                self._set_status("Синяя дверь открыта!")
            else:
                self._set_status("Нужен Синий ключ!")
        elif tile == 4:
            if self.player.has_mask:
                self.door.start(self._win_game, Side.Dir_left)
            else:
                self._set_status("Без противогаза наружу нельзя!")

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
                    name = settings.keys.Names[item["id"]]
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

    def draw(self) -> None:
        if self.door.blackout:
            self.screen.fill((0, 0, 0))
        else:
            self.drawer.draw_hud(self.player, self.status_message, self.door_hint)
            self.screen.blit(self.background, (0, 0))
            self._cast_rays()
            self.screen.blit(self.vignette, (0, 0))

            self.drawer.draw_crosshair()
            self.drawer.draw_fps()

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
