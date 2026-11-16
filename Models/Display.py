from Logging.Logger import Logger
from Errors import ScreenError

class Display:
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        try:
            value = int(width)
        except ValueError:
            Logger.error(f"Invalid value {width}")
            raise ValueError

        if value < 0 or value > 4096:
            Logger.error("Text resolution is invalid")
            raise ScreenError

        self.__width = value


    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height: int):
        try:
            value = int(height)
        except ValueError:
            Logger.error(f"Invalid value {height}")
            raise ValueError

        if value < 0 or value > 2160:
            Logger.error("Text resolution is invalid")
            raise ScreenError

        self.__height = value