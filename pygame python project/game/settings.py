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
BONUS_INTERVAL = 5000  # 1 минута в миллисекундах
DAMAGE_BOOST_DURATION = 10000  # 10 секунд

COLOR_OF_SKY = (135, 206, 235)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (150, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PLATFORM_COLOR = (100, 70, 40)

title_font = pygame.font.Font("C:/Users/Denis/Desktop/pygame python project/font/zettameter.ttf", 64)
button_font = pygame.font.SysFont('arial', 32)
health_font = pygame.font.SysFont('arial', 16)
bonus_font = pygame.font.SysFont('arial', 24)
SHOOT_COOLDOWN = 30

PLAYER_SPRITES = {
    "player_1": "C:/Users/Denis/Desktop/pygame python project/image/slime_sprite_green.png",
    "player_2": "C:/Users/Denis/Desktop/pygame python project/image/slime_sprite_orange.png"
}

PLAYER_ACCELERATION = 0.5  # Ускорение при движении
PLAYER_FRICTION = 0.8      # Трение при остановке
MIN_SPAWN_DISTANCE = 300
PLATFORM_MARGIN = 5

player1_wins = 0
player2_wins = 0
match_winner = None
waiting_for_next_match = False
match_start_time = 0