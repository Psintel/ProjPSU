from Models.ParametrizedLine import ParametrizedLine


class Text:
    """Блок строк для показа на отдельном экране (титул, сообщение перед интро)."""

    def __init__(self, lines: list[ParametrizedLine] | None = None) -> None:
        self.lines: list[ParametrizedLine] = list(lines or [])

    def add(self, line: ParametrizedLine) -> None:
        self.lines.append(line)

    @property
    def height(self) -> int:
        return sum(line.height for line in self.lines)
