"""HUD: панель внизу экрана (предметы, ключи, цель, уведомление, подсказка), прицел и FPS.

Картинки слотов берутся из InventoryHandler, текст цели - из player. Правильнее было бы
передать готовый HudState (строки + список (surface, label)), тогда UI не знал бы ни про
инвентарь, ни про правила крафта противогаза; пока оставили подпись как в игре, и player
здесь - единственный домен, о котором UI что-то знает.

Все координаты меряются от Game_height (низ 3D-вида = верх HUD), а не от Height/Hud_height.
"""
import pygame

from Colors.Color import Color
from InventoryHandler.InventoryHandler import InventoryHandler
from Player.Player import Player
from Settings.Settings import settings
from UI.TextWriter import TextWriter

ITEM_SLOT = 50
KEY_SLOT = 36
SLOT_GAP = 12
LEFT_COLUMN = 300          # вертикальная линия, отделяющая слоты от текста цели


class GameElementDrawer:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
        self.screen = screen
        self.clock = clock

    def draw_crosshair(self) -> None:
        chord_x, chord_y = settings.screen.Width // 2, settings.screen.Half_of_game_height
        pygame.draw.line(self.screen, Color.White, (chord_x - 8, chord_y), (chord_x + 8, chord_y), 1)
        pygame.draw.line(self.screen, Color.White, (chord_x, chord_y - 8), (chord_x, chord_y + 8), 1)

    def draw_fps(self) -> None:
        TextWriter.draw_text(
            self.screen, f"FPS: {int(self.clock.get_fps())}", (10, 8), 18, Color.Yellow, True
        )

    def draw_hud(self, player: Player, notification: str = "", hint: str = "") -> None:
        hud_y = settings.screen.Game_height
        pygame.draw.rect(
            self.screen, (60, 60, 60), (0, hud_y, settings.screen.Width, settings.screen.Hud_height)
        )
        pygame.draw.line(self.screen, (150, 150, 150), (0, hud_y), (settings.screen.Width, hud_y), 3)
        pygame.draw.line(self.screen, (30, 30, 30), (LEFT_COLUMN, hud_y), (LEFT_COLUMN, settings.screen.Height), 2)

        self.__draw_items(hud_y)
        self.__draw_keys(hud_y)
        self.__draw_texts(player, hud_y, notification, hint)

    def __draw_items(self, hud_y: int) -> None:
        for i, (kind, name) in enumerate(settings.items.Names.items()):
            rect = pygame.Rect(20 + i * (ITEM_SLOT + SLOT_GAP), hud_y + 10, ITEM_SLOT, ITEM_SLOT)
            self.__draw_slot(rect, InventoryHandler.unlockedItems.get(kind), name)

    def __draw_keys(self, hud_y: int) -> None:
        for i, kind in enumerate(settings.keys.Names):
            rect = pygame.Rect(20 + i * (KEY_SLOT + SLOT_GAP), hud_y + 72, KEY_SLOT, KEY_SLOT)
            self.__draw_slot(rect, InventoryHandler.unlockedKeys.get(kind))
        TextWriter.draw_text(
            self.screen,
            "Ключи",
            (20 + len(settings.keys.Names) * (KEY_SLOT + SLOT_GAP) + 4, hud_y + 80),
            16,
            Color.Fading,
        )

    def __draw_texts(self, player: Player, hud_y: int, notification: str, hint: str) -> None:
        chord_x = LEFT_COLUMN + (settings.screen.Width - LEFT_COLUMN) // 2
        if player.has_mask:
            goal, color = "Цель: Выйти из здания (E)", Color.Green
        else:
            goal = f"Цель: Собрать предметы ({len(player.inventory)}/{len(settings.items.Names)})"
            color = Color.Yellow
        TextWriter.draw_text(self.screen, goal, (chord_x, hud_y + 20), 22, color, True, True)

        if notification:
            TextWriter.draw_text(self.screen, notification, (chord_x, hud_y + 55), 24, bold=True, center=True)
        if hint:
            TextWriter.draw_text(self.screen, hint, (chord_x, hud_y + 85), 20, Color.Blue, True, True)

    def __draw_slot(self, rect: pygame.Rect, image=None, label: str = "") -> None:
        if image:
            self.screen.blit(pygame.transform.scale(image, rect.size), rect)
            pygame.draw.rect(self.screen, Color.White, rect, 2)
        else:
            pygame.draw.rect(self.screen, (30, 30, 30), rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)
            if label:
                text = TextWriter.get_font(14).render(label, True, (100, 100, 100))
                self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.bottom - 18))
