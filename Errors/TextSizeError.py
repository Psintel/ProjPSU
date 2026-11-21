class TextSizeError(Exception):
    """Недопустимый кегль текста."""

    def __init__(self, message: str = "Text size must be a positive integer") -> None:
        self.message = message
        super().__init__(self.message)
