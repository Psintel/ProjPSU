"""Точка входа.   Запуск:  python main.py

Порядок: пролог (сообщения -> видео -> название) -> игра.
Окно создаёт play_intro(); если игрок закрыл его на прологе, игру не запускаем.
"""
import pygame

from GameManager.game import Game
from GameManager.GameManager import play_intro


def main() -> None:
    if not play_intro():
        pygame.quit()
        return

    screen = pygame.display.get_surface()
    Game(screen).run()


if __name__ == "__main__":
    main()