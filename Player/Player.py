"""Состояние игрока, которое читает интерфейс.

Движение/поворот/коллизии - часть человека 1, и он же решит, в каком модуле жить
Player'у. Здесь только те поля, без которых не запустится HUD: инвентарь, ключи,
наличие противогаза. Как только человек 1 перенесёт своего Player'а сюда, эти три поля
остаться должны как есть - на них завязан InventoryHandler.
"""

class Player:
    def __init__(self, x: float = 0.0, y: float = 0.0, angle: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.inventory: set[str] = set()   # 'coal', 'gauze', 'bottle'
        self.keys: set[str] = set()        # 'key_red', 'key_blue'
        self.has_mask: bool = False

    # TODO(человек 1): update/rotate/move и коллизии - поверх этих полей.

    def reset(self) -> None:
        """Состояние на новый заход, иначе инвентарь течёт между партиями."""
        self.inventory.clear()
        self.keys.clear()
        self.has_mask = False