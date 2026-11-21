from enum import Enum


class Color(Enum):
    """Палитра интерфейса.

    Значение - кортеж RGB. pygame принимает напрямую любой итерируемый объект из
    трёх чисел, поэтому переисчисляем __iter__/__len__/__getitem__: вызывающий код
    пишет screen.fill(Color.White) и не помнит, что это Enum, а не кортеж.
    Без этого любой Color.X в render()/draw.line() давал TypeError.
    """

    White = (255, 255, 255)
    Yellow = (240, 220, 50)
    Green = (50, 220, 50)
    Gray = (100, 100, 100)
    Ceiling_color = (45, 45, 55)
    Floor_color = (65, 55, 45)
    Fading = (120, 120, 120)
    Blue = (150, 220, 255)
    Red = (200, 40, 40)

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self.value

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, index):
        return self.value[index]
