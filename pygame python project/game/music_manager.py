import pygame
import random


class MusicManager:
    def __init__(self, menu_music_list, game_music_list):
        self.menu_music_list = menu_music_list
        self.game_music_list = game_music_list
        self.current_music = None
        self.volume = 0.4
        self.current_menu_index = random.randint(0, len(menu_music_list) - 1)
        self.current_game_index = random.randint(0, len(game_music_list) - 1)
        self._menu_initialized = False
        self._game_initialized = False

    def play_menu(self, loops=-1):
        self._stop_current()
        if not self._menu_initialized:
            self.current_menu_index = random.randint(0, len(self.menu_music_list) - 1)
            self._menu_initialized = True
        self.current_music = self.menu_music_list[self.current_menu_index]
        self._play(self.current_music, loops)
        return self.current_menu_index  # Возвращаем текущий индекс

    def play_game(self, loops=-1):
        self._stop_current()
        if not self._game_initialized:
            self.current_game_index = random.randint(0, len(self.game_music_list) - 1)
            self._game_initialized = True
        self.current_music = self.game_music_list[self.current_game_index]
        self._play(self.current_music, loops)
        return self.current_game_index  # Возвращаем текущий индекс

    def stop(self):
        self._stop_current()
        self.current_music = None

    def set_volume(self, volume: float):
        self.volume = volume
        if self.current_music:
            self.current_music.set_volume(volume)

    def next_menu_track(self):
        self.current_menu_index = (self.current_menu_index + 1) % len(self.menu_music_list)
        if self.current_music in self.menu_music_list:
            self.play_menu()

    def next_game_track(self):
        self.current_game_index = (self.current_game_index + 1) % len(self.game_music_list)
        if self.current_music in self.game_music_list:
            self.play_game()

    def _play(self, sound: pygame.mixer.Sound, loops: int):
        sound.set_volume(self.volume)
        sound.play(loops=loops)
    def _stop_current(self):
        if self.current_music:
            self.current_music.stop()

    def get_current_track_info(self):
        if self.current_music in self.menu_music_list:
            return "menu", self.current_menu_index
        elif self.current_music in self.game_music_list:
            return "game", self.current_game_index
        return None, None