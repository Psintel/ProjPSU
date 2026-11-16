from typing import Any
from Text.TextWriter import TextWriter
import pygame
import os
from moviepy import VideoFileClip
from Logging.Logger import Logger
import tempfile
from Models.Display import Display
import time
from Settings.SkipKeys import Skip_keys
from Colors.Color import Color

class ClipHandler:
    path: str = ""

    @staticmethod
    def initialize(path: str):
        ClipHandler.path = path

    @staticmethod
    def load_clip() -> VideoFileClip:
        try:
            from moviepy import VideoFileClip
            return VideoFileClip(ClipHandler.path)
        except Exception as e:
            Logger.error("Can't import intro video file")

    @staticmethod
    def play_intro_clip(screen: pygame.Surface, display: Display) -> Any | None:
        if not os.path.exists(ClipHandler.path):
            Logger.info(f"Intro was skipped: file {ClipHandler.path} was not found")
            return None

        clip = ClipHandler.load_clip()

        if clip is None:
            return None

        audio_file = ClipHandler.load_audio_from_clip(clip)

        video_width, video_height = clip.size
        k = min(display.width / video_width, display.height / video_height)
        size = (int(video_width * k), int(video_height * k))
        position = ((display.width - size[0]) // 2, (display.height - size[1]) // 2)

        clock = pygame.time.Clock()
        keep_running = True
        screen.fill((0, 0, 0))
        if audio_file:
            pygame.mixer.music.play()
        start = time.perf_counter()

        try:
            playing = True
            while playing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        keep_running = playing = False
                    elif event.type == pygame.KEYDOWN and event.key in Skip_keys:
                        playing = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        playing = False

                t = time.perf_counter() - start  # кадр выбираем по времени - так звук и картинка не расходятся
                if t >= clip.duration:
                    break

                frame = clip.get_frame(t)  # массив (высота, ширина, RGB)
                image = pygame.image.frombuffer(frame.tobytes(), (video_width, video_height), "RGB")
                screen.blit(pygame.transform.scale(image, size), position)
                TextWriter.draw_text(
                    screen,
                    "Пропустить: пробел",
                    (display.width - 170, display.height - 30),
                    16,
                    Color.Fading,
                )
                pygame.display.flip()
                clock.tick(clip.fps or 30)

        finally:
            pygame.mixer.music.stop()
            if hasattr(pygame.mixer.music, "unload"):
                pygame.mixer.music.unload()
            clip.close()
            if audio_file and os.path.exists(audio_file):
                try:
                    os.remove(audio_file)
                except OSError:
                    pass
        return keep_running

    @staticmethod
    def load_audio_from_clip(clip):
        audio_file = None
        if clip.auido is not None:
            audio_file = os.path.join(tempfile.gettempdir(), "game_intro_audio.wav")
            clip.auido.write_audiofile(audio_file, logger=None)
            pygame.mixer.music.load(audio_file)

        return audio_file