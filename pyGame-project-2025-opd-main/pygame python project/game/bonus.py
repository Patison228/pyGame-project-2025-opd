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
        self.type = random.choice(["health", "damage", "protection", "gauntlet"])
        self.collected = False
        self.spawn_time = pygame.time.get_ticks()

        # Загрузка спрайтов
        if self.type == "health":
            self.image = load_image("C:/Users/Denis/Desktop/pyGame-project-2025-opd-main/pygame python project/image/health_bonus.png")
        elif self.type == "damage":
            self.image = load_image("C:/Users/Denis/Desktop/pyGame-project-2025-opd-main/pygame python project/image/damage_bonus.png")
        elif self.type == "protection":
            self.image = load_image("C:/Users/Denis/Desktop/pyGame-project-2025-opd-main/pygame python project/image/protection_bonus.png")
        elif self.type == "gauntlet":
            self.image = load_image("C:/Users/Denis/Desktop/pyGame-project-2025-opd-main/pygame python project/image/gauntlet.png")

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
            elif self.type == "damage":
                player.damage_boost = True
                player.damage_boost_time = pygame.time.get_ticks()
                print(f"Player {player.player_id} got damage boost!")
            elif self.type == "protection":
                player.protection_count = 3
                print(f"Player {player.player_id} got protection boost!")
            elif self.type == "gauntlet":
                player.has_gauntlet = True
                print(f"Player {player.player_id} collected gauntlet!")
            return True
        return False

    def draw(self, screen):
        global color
        if not self.collected and self.image is not None:
            screen.blit(self.image, (self.x, self.y))
        elif not self.collected:  
            # Рисуем простой прямоугольник
            if self.type == "health":
                color = GREEN
            elif self.type == "damage":
                color = RED
            elif self.type == "protection":
                color = BLUE
            elif self.type == "gauntlet":
                color = BLACK
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))