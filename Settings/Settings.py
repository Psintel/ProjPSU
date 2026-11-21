from dataclasses import dataclass, asdict
import pygame
import json

@dataclass
class ScreenSettings:
    Width = 1920
    Height = 1080
    FPS = 60
    Hud_height = 120
    Game_height = Height - Hud_height
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
class Items:
    Names = {
        'coal': 'Уголь',
        'gauze': 'Марля',
        'bottle': 'Бутылка'}

@dataclass
class Keys:
    Names = {
        'key_red': ('Красный ключ', (255, 90, 90)),
        'key_blue': ('Синий ключ', (90, 140, 255)),
    }

@dataclass
class Title:
    Fade_time = 1.2
    Pre_intro_messages = [
        ["Идея игры вдохновлена", "предхеллоуинским видео от студентов ПГНИУ"],
    ]
    Message_hold_time = 4.0
    Text = "СБЕГИ ИЗ ПГНИУ"
    Lines = ["Тебе понадобится самодельный противогаз,", "чтобы выйти наружу."]
    Hold_time = 5.0

@dataclass
class Door:
    Animation_size = (420, 520)
    Opening_time = 0.8
    Fade_time = 0.4

@dataclass
class Settings:
    screen: ScreenSettings
    skip_keys: SkipKeys
    view: ViewDistance
    raycasting: Raycasting
    items: Items
    keys: Keys
    title: Title
    door: Door

settings = Settings(ScreenSettings(), SkipKeys(), ViewDistance(), Raycasting(), Items(), Keys(), Title(), Door())

with open("settings.json", "w", encoding="utf-8") as file:
    json.dump(asdict(settings, file, indent=2))