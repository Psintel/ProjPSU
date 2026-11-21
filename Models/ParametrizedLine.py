from dataclasses import dataclass
from typing import Any
from Colors.Color import Color

@dataclass
class ParametrizedLine:
    line: str
    text_size: int
    color: Color
    bold: Any