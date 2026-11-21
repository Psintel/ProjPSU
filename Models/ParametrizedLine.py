from dataclasses import dataclass

from Colors.Color import Color


@dataclass
class ParametrizedLine:
    """Строка текста вместе со своими параметрами.

    Межстрочная высота вынесена в height, потому что расчёт блока и его рисование
    раньше считали `size * 1.5` по отдельности и могли разъехаться.
    """

    line: str
    text_size: int = 24
    color: Color = Color.White
    bold: bool = False

    @property
    def height(self) -> int:
        return int(self.text_size * 1.5)
