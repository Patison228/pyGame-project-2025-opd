import pygame

class MusicManager:
    def __init__(self, menu_music: pygame.mixer.Sound, game_music: pygame.mixer.Sound):
        self.menu_music = menu_music
        self.game_music = game_music
        self.current_music = None
        self.volume = 0.5  
    
    def play_menu(self, loops = -1):
        self._stop_current()
        self.current_music = self.menu_music
        self._play(self.menu_music, loops)
    
    def play_game(self, loops = -1):
        self._stop_current()
        self.current_music = self.game_music
        self._play(self.game_music, loops)
    
    def stop(self):
        self._stop_current()
        self.current_music = None
    
    def set_volume(self, volume: float):
        self.volume = volume

        if self.current_music:
            self.current_music.set_volume(volume)
    
    def _play(self, sound: pygame.mixer.Sound, loops: int):
        sound.set_volume(self.volume)
        sound.play(loops=loops)
    
    def _stop_current(self):
        if self.current_music:
            self.current_music.stop()