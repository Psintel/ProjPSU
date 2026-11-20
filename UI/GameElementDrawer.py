import pygame
from Settings.Settings import settings
from Colors.Color import Color
from TextWriter import TextWriter
from Models.Display import Display
from Settings.Settings import Settings
from InventoryHandler.InventoryHandler import InventoryHandler
from Player.Player import Player

class GameElementDrawer:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock

    def draw_crosshair(self) -> None:
        chord_x, chord_y = settings.screen.Width // 2, settings.hud.Half_of_game_height
        pygame.draw.line(self.screen, Color.White, (chord_x - 8, chord_x), (chord_x + 8, chord_y), 1)
        pygame.draw.line(self.screen, Color.White, (chord_x, chord_y - 8), (chord_x, chord_y + 8), 1)

    def draw_fps(self) -> None:
        TextWriter.draw_text(self.screen, f"FPS: {int(self.clock.get_fps())}", Display(10, 8), 18, Color.Yellow, True, False)

    def __draw_slot(self, rect, image=None, label="") -> None:
        if image:
            self.screen.blit(pygame.transform.scale(image, rect.size), rect)
            pygame.draw.rect(self.screen, Color.White, rect, 2)
        else:
            pygame.draw.rect(self.screen, (30, 30, 30), rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)
            if label:
                text = TextWriter.get_font(14, False).render(label, True, (100, 100, 100))
                self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.bottom - 18))

    def draw_item(self) -> None:
        size = 50
        for i, (kind, name) in enumerate(Settings.items):
            rect = pygame.Rect(20 + i * (size + 12), Settings.screen.Game_height + 10, size, size)
            self.__draw_slot(rect, InventoryHandler.unlockedItems, name)

    def draw_key(self) -> None:
        key_size = 36
        for i, kind in enumerate(Settings.keys.Names):
            rect = pygame.Rect(20 + i * (key_size + 12), Settings.screen.Game_height + 72, key_size, key_size)
            self.__draw_slot(rect, InventoryHandler.unlockedKeys)

    def draw_hud(self, player: Player, notification: str, hint: str) -> None:
        pygame.draw.rect(self.screen, (60, 60, 60), (0, Settings.screen.Game_height, Settings.screen.Width, Settings.screen.Hud_height))
        pygame.draw.line(self.screen, (150, 150, 150), (0, Settings.screen.Game_height), (Settings.screen.Width, Settings.screen.Game_height), 3)
        pygame.draw.line(self.screen, (30, 30, 30), (300, Settings.screen.Game_height), (300, Settings.screen.Hud_height), 2)

        TextWriter.draw_text(self.screen, "Ключи", Display(20 + len(settings.keys.Names) * (36 + 12) + 4, Settings.screen.Width + 80), 16, Color.Fading, False, False)

        self.__draw_target(player, notification, hint)

    def __draw_target(self, player: Player, notification: str, hint: str) -> None:
        chord_x = 300 + (Settings.screen.Width - 300) // 2
        if player.has_mask:
            goal, color = "Цель: Выйти из здания (E)", Color.Green
        else:
            goal, color = f"Цель: Собрать предметы ({len(player.inventory)}/{len(Settings.items.Names)})", Color.Yellow

        TextWriter.draw_text(self.screen, goal, Display(chord_x, Settings.screen.Game_height + 20), 22, color, True, True)

        if notification:
            TextWriter.draw_text(self.screen, notification, Display(chord_x, Settings.screen.Hud_height + 55), 24, True, True)
        if hint:
            TextWriter.draw_text(self.screen, hint, Display(chord_x, Settings.screen.Game_height + 85), 20, Color.Blue, True, True)