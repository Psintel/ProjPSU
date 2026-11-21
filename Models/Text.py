from ParametrizedLine import ParametrizedLine

class Text:
    def __init__(self, lines: list[ParametrizedLine]):
        self.lines = []

        if len(lines) == 0:
            pass
        else:
            self.lines.append(lines)
