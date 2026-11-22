LEVELS = (
    # Уровень 0 (Этаж 2: поиск Красного ключа, Угля и переход на 1-й этаж через дверь '5')
    {
        "name": "Этаж 2: Лабораторный корпус",
        "spawn": (1.5, 1.5, 0.0),
        "grid": (
            "111111111111111111111111111",
            "100000000010000001000000001",
            "100000000010000003000000001",
            "100000000010000001000000001",
            "100000000020000001000000001",
            "100000000010000001111111111",
            "100000000010000005000000001",
            "100000000010000001111111111",
            "111111111110000000001000001",
            "100000000020000000001000001",
            "100000000010000000001000001",
            "111111121110000001111113111",
            "100000000010000000000000001",
            "100000000010000000000000001",
            "111111111111111111111111111",
        ),
        "items": (
            {"x": 3.5, "y": 3.5, "id": "key_red", "type": "key", "collected": False},
            {"x": 8.5, "y": 1.5, "id": "coal", "type": "item", "collected": False},
        ),
    },
    # Уровень 1 (Этаж 1: поиск Синего ключа, Марли, Бутылки и выход '4' на улицу)
    {
        "name": "Этаж 1: Главный холл и медпункт",
        "spawn": (1.5, 2.5, 0.0),
        "grid": (
            "11111111111111",
            "10000100000001",
            "10000300011001",
            "10000100011004",
            "10000100000001",
            "11111111111111",
        ),
        "items": (
            {"x": 3.5, "y": 1.5, "id": "key_blue", "type": "key", "collected": False},
            {"x": 8.5, "y": 1.5, "id": "gauze", "type": "item", "collected": False},
            {"x": 11.5, "y": 4.5, "id": "bottle", "type": "item", "collected": False},
        ),
    },
)


class GameMap:
    def __init__(self) -> None:
        # 0 - пол
        # 1 - стена
        # 2 - красная дверь (нужен key_red)
        # 3 - синяя дверь (нужен key_blue)
        # 4 - финальный выход на улицу (нужен противогаз)
        # 5 - лестница / дверь перехода на следующий уровень
        self.level_index: int = 0
        self.level_name: str = ""
        self.grid: list[list[int]] = []
        self.world_items: list[dict] = []
        self.height: int = 0
        self.width: int = 0
        self.load_level(0)

    def load_level(self, index: int) -> tuple[float, float, float]:
        """Загружает уровень по индексу и возвращает (x, y, angle) спавна игрока."""
        self.level_index = index
        data = LEVELS[index]
        self.level_name = data["name"]
        self.grid = [list(map(int, row)) for row in data["grid"]]
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.world_items = [dict(item) for item in data["items"]]
        return data["spawn"]

    def has_next_level(self) -> bool:
        return self.level_index + 1 < len(LEVELS)

    def get_tile(self, x: int, y: int) -> int:
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x]
        return 1

    def is_blocked(self, x: float, y: float) -> bool:
        return self.get_tile(int(x), int(y)) != 0

    def open_door(self, x: int, y: int) -> None:
        if 0 <= y < self.height and 0 <= x < self.width:
            self.grid[y][x] = 0