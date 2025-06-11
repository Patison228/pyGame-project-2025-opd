import pygame
from utils import load_image
from settings import PLATFORM_COLOR


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
            self.sprite = load_image("C:/Users/Denis/Desktop/pygame python project/images/platform.png")
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

    def check_collision(self, player):
        if player.rect.colliderect(self.rect):
            if (player.velocity_y > 0 and player.rect.bottom <= self.rect.top + player.velocity_y + 1):
                player.rect.bottom = self.rect.top
                player.velocity_y = 0
                player.jumping = False
                return True
        return False