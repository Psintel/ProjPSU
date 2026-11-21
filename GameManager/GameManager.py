"""Пролог: чёрное окно -> сообщения -> видео -> название игры.

Единственный владелец цикла событий на время пролога: у ScreenWriter и ClipHandler
своих pygame.init()/set_mode быть не должно, они рисуют на экран, который создали здесь.
Сама игра (Game) ещё не подключена - это часть человека 2; когда появится main.py,
он должен вызвать play_intro() и по False не запускать игру.

Проверить без игры:  python -m GameManager.GameManager
"""
import pygame

from Intro.IntroPlayer import ClipHandler
from Models.Display import Display
from Settings.Settings import settings
from UI.ScreenWriter import ScreenWriter


def play_intro() -> bool:
    """False - игрок закрыл окно во время пролога, дальше идти не надо."""
    pygame.init()
    display = Display(settings.screen.Width, settings.screen.Height)
    screen = pygame.display.set_mode((display.width, display.height))
    pygame.display.set_caption("Сбеги из ПГНИУ")

    writer = ScreenWriter(screen)
    return (
        writer.show_messages()
        and ClipHandler.play_intro_clip(screen, display)
        and writer.show_title_screen()
    )


if __name__ == "__main__":
    play_intro()
    pygame.quit()
