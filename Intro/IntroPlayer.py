"""Видеопролог со звуком.

Порт intro.play_intro_video. Два правила, без которых пролог ломает запуск:
  * moviepy импортируется лениво и только внутри load_clip - без него игра обязана
    стартовать (интро просто пропускается), а импорт на уровне модуля вешал всё;
  * anything, что не даёт посмотреть видео, не должно мешать игре: ловим ошибку,
    пишем в лог, возвращаем True.

Звук: дорожка вытаскивается во временный wav и играется через pygame.mixer - картинка
при этом выбирается по wall-clock, чтобы звук и видео не расходились.
"""
import os
import tempfile
import time

import pygame

from Colors.Color import Color
from Logging.Logger import Logger
from Models.Display import Display
from Settings.Settings import settings
from UI.TextWriter import TextWriter


class ClipHandler:
    path: str = settings.clip.Path

    @staticmethod
    def initialize(path: str | None = None) -> None:
        """Путь по умолчанию берётся из конфига, чтобы модуль можно было переиспользовать
        в тесте/между партиями, не зная settings.
        """
        ClipHandler.path = path or settings.clip.Path

    @staticmethod
    def load_clip():
        """Открывает видео через moviepy (подходит и 1.x, и 2.x)."""
        try:
            from moviepy import VideoFileClip            # moviepy 2.x
        except ImportError:
            from moviepy.editor import VideoFileClip     # moviepy 1.x
        return VideoFileClip(ClipHandler.path)

    @staticmethod
    def load_audio_from_clip(clip) -> str | None:
        """Извлекает дорожку во временный файл; возвращает путь или None, если звука нет."""
        if clip.audio is None:
            return None

        handle = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        handle.close()
        audio_file = handle.name
        clip.audio.write_audiofile(audio_file, logger=None)
        pygame.mixer.music.load(audio_file)
        return audio_file

    @staticmethod
    def play_intro_clip(screen: pygame.Surface, display: Display) -> bool:
        """True - идём дальше (досмотрели/пропустили/видео недоступно), False - окно закрыли."""
        if not os.path.exists(ClipHandler.path):
            Logger.info(f"Intro was skipped: file {ClipHandler.path} was not found")
            return True

        try:
            clip = ClipHandler.load_clip()
        except ImportError:
            Logger.error("Intro was skipped: install moviepy with  pip install moviepy")
            return True
        except Exception as exc:
            Logger.error(f"Intro was skipped: can't open {ClipHandler.path}: {exc}")
            return True

        clock = pygame.time.Clock()
        audio_file = None
        keep_running = True

        try:
            screen.fill((0, 0, 0))
            TextWriter.draw_text(
                screen, "Загрузка...",
                (display.width // 2, display.height // 2), 28, Color.White, center=True,
            )
            pygame.display.flip()

            audio_file = ClipHandler.load_audio_from_clip(clip)

            video_width, video_height = clip.size
            k = min(display.width / video_width, display.height / video_height)
            size = (int(video_width * k), int(video_height * k))
            position = ((display.width - size[0]) // 2, (display.height - size[1]) // 2)

            screen.fill((0, 0, 0))
            if audio_file:
                pygame.mixer.music.play()
            start = time.perf_counter()

            playing = True
            while playing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        keep_running = playing = False
                    elif event.type == pygame.KEYDOWN and event.key in settings.skip_keys.Skip_keys:
                        playing = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        playing = False

                t = time.perf_counter() - start
                if t >= clip.duration:
                    break

                frame = clip.get_frame(t)
                image = pygame.image.frombuffer(frame.tobytes(), (video_width, video_height), "RGB")
                screen.fill((0, 0, 0))
                screen.blit(pygame.transform.scale(image, size), position)
                TextWriter.draw_text(
                    screen, "Пропустить: пробел",
                    (display.width - 170, display.height - 30), 16, Color.Fading,
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
