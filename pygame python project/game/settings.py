import pygame

pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
JUMP_FORCE = -12
PLAYER_SPEED = 5
FLOOR_HEIGHT = 50
BULLET_SPEED = 10
MAX_HEALTH = 100

COLOR_OF_SKY = (135, 206, 235)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (150, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PLATFORM_COLOR = (100, 70, 40)  # Коричневый цвет для платформ

title_font = pygame.font.Font("pygame python project/font/zettameter.ttf", 64)
button_font = pygame.font.SysFont('arial', 32)
health_font = pygame.font.SysFont('arial', 16)