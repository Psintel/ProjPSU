class ScreenError(Exception):
    """Недопустимый размер окна."""

    def __init__(self, message: str = "UI resolution is invalid") -> None:
        self.message = message
        super().__init__(self.message)
