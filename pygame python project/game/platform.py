import pygame
from utils import *
from settings import PLATFORM_COLOR
from player import Player

class Platform:
    def __init__(self, x, y, width, height, color=PLATFORM_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.sprite = None
        self.load_sprite()

    def load_sprite(self):
        try:
            self.sprite = load_image("C:/Users/Denis/Desktop/pyGame-project-2025-opd-main/pygame python project/image/platform_1.png")
            if self.sprite:
                self.sprite = pygame.transform.scale(self.sprite, (self.rect.width, self.rect.height))
        except Exception as e:
            print(f"Error loading platform sprite: {e}")
            self.sprite = None

    def draw(self, surface):
        if self.sprite:
            surface.blit(self.sprite, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
