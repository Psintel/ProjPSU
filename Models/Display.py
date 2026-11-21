from Errors.ScreenError import ScreenError
from Logging.Logger import Logger


class Display:
    """Размер окна. Валидация одна на ширину и высоту и работает в том числе при
    создании: `__init__` идёт через сеттеры, а не пишет в приватные поля напрямую.

    Назначение - только габарит экрана. Координаты текста сюда не кладём: для этого
    есть обычный кортеж (x, y) у TextWriter.draw_text.
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        self.__width = self.__validate(width, "Width", 4096)

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        self.__height = self.__validate(height, "Height", 2160)

    @staticmethod
    def __validate(value, name: str, maximum: int) -> int:
        try:
            number = int(value)
        except (TypeError, ValueError) as exc:
            Logger.error(f"Display.{name}: not a number: {value!r}")
            raise ValueError(f"Display.{name} must be an integer, got {value!r}") from exc

        if not 1 <= number <= maximum:
            Logger.error(f"Display.{name}: out of range 1..{maximum}: {number}")
            raise ScreenError(f"Display.{name}: out of range 1..{maximum}: {number}")

        return number
