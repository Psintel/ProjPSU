from Intro.IntroPlayer import ClipHandler
from Models.Display import Display
from UI.TextWriter import TextWriter
from Colors.Color import Color
import pygame

def play_intro():
    display = Display(1920, 1080)
    screen = pygame.display.set_mode((display.width, display.height))

    TextWriter.draw_text(screen, "Загрузка...", display, 28, Color.White, True, True)

    ClipHandler.initialize(path)
    ClipHandler.play_intro_clip(screen)



