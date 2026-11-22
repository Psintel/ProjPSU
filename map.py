class GameMap:
    def __init__(self) -> None:
        raw_map = (
            "111111111111111111111111111",
            "100000000010000001000000001",
            "100000000010000003000000001",
            "100000000010000001000000001",
            "100000000020000001000000001",
            "100000000010000001111111111",
            "100000000010000003000000001",
            "100000000010000001111111111"
            "111111111110000000001000001",
            "100000000020000000001000001",
            "100000000010000000001000001",
            "111111121110000001111113111",
            "100000000010000000000000001",
            "100000000010000000000000001",
            "111111111111111111111111111",
        )
        self.grid = [list(map(int, row)) for row in raw_map]
        self.height = len(self.grid)
        self.width = len(self.grid)

        self.world_items = [
            {"x": 3.5, "y": 3.5, "id": "key_red", "type": "key", "collected": False},
            {"x": 12.5, "y": 1.5, "id": "coal", "type": "item", "collected": False},
            {"x": 11.5, "y": 3.5, "id": "key_blue", "type": "key", "collected": False},
            {"x": 2.5, "y": 9.5, "id": "gauze", "type": "item", "collected": False},
            {"x": 12.5, "y": 6.5, "id": "bottle", "type": "item", "collected": False},
        ]

    def get_tile(self, x: int, y: int) -> int:
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x]
        return 1

    def is_blocked(self, x: float, y: float) -> bool:
        return self.get_tile(int(x), int(y)) != 0

    def open_door(self, x: int, y: int) -> None:
        if 0 <= y < self.height and 0 <= x < self.width:
            self.grid[y][x] = 0
