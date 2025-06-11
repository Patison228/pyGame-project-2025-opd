import pygame
import random
from settings import *

class Bonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.type = random.choice(["health", "damage"])
        self.collected = False
        self.spawn_time = pygame.time.get_ticks()

        if self.type == "health":
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(GREEN)
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(RED)

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, (self.x, self.y))

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