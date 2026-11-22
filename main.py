import pygame
from GameManager.GameManager import play_intro
from GameManager.game import Game


def main() -> None:
    if not play_intro():
        pygame.quit()
        return

    screen = pygame.display.get_surface()
    game = Game(screen)
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
