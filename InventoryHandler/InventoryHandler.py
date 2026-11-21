"""Мост между инвентарём игрока и картинками предметов.

Заглушка до тех пор, пока человек 1 не принесёт assets.py: вместо текстур - None,
но сама логика уже рабочая, и HUD можно рисовать/проверять уже сейчас.

Состояние живёт на классе (как было задумано), поэтому обязателен reset() при
новом заходе - иначе собранные предметы останутся в экране победы и в следующей партии.
"""
import pygame

from Settings.Settings import settings


class InventoryHandler:
    assets: dict[str, pygame.Surface] = {}                     # kind -> Surface; придут из assets.py
    unlockedItems: dict[str, pygame.Surface | None] = {}       # предметы противогаза
    unlockedKeys: dict[str, pygame.Surface | None] = {}         # ключи от дверей

    @classmethod
    def initialize(cls, assets: dict[str, pygame.Surface]) -> None:
        cls.assets = assets
        cls.reset()

    @classmethod
    def reset(cls) -> None:
        cls.unlockedItems = dict.fromkeys(settings.items.Names)
        cls.unlockedKeys = dict.fromkeys(settings.keys.Names)

    @classmethod
    def update(cls, inventory, keys) -> None:
        """Инвентарь игрока -> то, что рисует HUD.

        Идём по своим словарям, а не по inventory: во-первых предмет и ключ лежат в
        одном списке и раньше писались в обе таблицы, во-вторых так слот очищается,
        когда предмет из инвентаря исчез.
        """
        inventory = set(inventory)
        keys = set(keys)
        for kind in cls.unlockedItems:
            cls.unlockedItems[kind] = cls.assets.get(kind) if kind in inventory else None
        for kind in cls.unlockedKeys:
            cls.unlockedKeys[kind] = cls.assets.get(kind) if kind in keys else None
