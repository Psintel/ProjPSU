from dataclasses import dataclass, asdict
import pygame
import json

@dataclass
class ScreenSettings:
    Width = 1920
    Height = 1080
    FPS = 60

@dataclass
class HudSettings:
    Hud_height = 120
    Game_height = ScreenSettings.Height - Hud_height
    Half_of_game_height = Game_height // 2

@dataclass
class SkipKeys:
    Skip_keys = (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN)

@dataclass
class ViewDistance:
    Distance = 6

@dataclass
class Raycasting:
    Walls_height = 1000

@dataclass
class Settings:
    screen: ScreenSettings
    hud: HudSettings
    skip_keys: SkipKeys
    view: ViewDistance
    raycasting: Raycasting

settings = Settings(ScreenSettings(), HudSettings(), SkipKeys(), ViewDistance(), Raycasting())

with open("settings.json", "w", encoding="utf-8") as file:
    json.dump(asdict(settings, file, indent=2))