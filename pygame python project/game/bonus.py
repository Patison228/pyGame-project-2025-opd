import pygame
import random
from settings import *
from utils import load_image

class Bonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.image = None
        self.type = random.choice(["health", "damage"])
        self.collected = False
        self.spawn_time = pygame.time.get_ticks()

        # Загрузка спрайтов
        if self.type == "health":
            self.image = load_image("pygame python project/image/health_bonus.png")
        else:
            self.image = load_image("pygame python project/image/damage_bonus.png")
        

    def check_collision(self, player):
        if self.collected:
            return False

        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        bonus_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if player_rect.colliderect(bonus_rect):
            self.collected = True
            if self.type == "health":
                player.health = min(player.health + 10, 100)
                print(f"Player {player.player_id} collected health!")
            else:
                player.damage_boost = True
                player.damage_boost_time = pygame.time.get_ticks()
                print(f"Player {player.player_id} got damage boost!")
            return True
        return False

    def draw(self, screen):
        if not self.collected and self.image is not None:
            screen.blit(self.image, (self.x, self.y))
        elif not self.collected:  # Если image всё равно None
            # Рисуем простой прямоугольник
            color = (0, 255, 0) if self.type == "health" else (255, 0, 0)
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))