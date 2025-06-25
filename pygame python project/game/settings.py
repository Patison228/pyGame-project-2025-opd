import pygame

pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
JUMP_FORCE = -12
PLAYER_SPEED = 5
FLOOR_HEIGHT = 50
BULLET_SPEED = 13
MAX_HEALTH = 100
BONUS_INTERVAL = 15000
DAMAGE_BOOST_DURATION = 10000  # 10 секунд
SHOOT_COOLDOWN = 30

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

shoot_sound = pygame.mixer.Sound("pygame python project/sounds/shoot_sound.mp3")
jump_sound = pygame.mixer.Sound("pygame python project/sounds/jump_sound.wav")
health_bonus_sound = pygame.mixer.Sound("pygame python project/sounds/health_bonus_collect.mp3")
damage_bonus_sound = pygame.mixer.Sound("pygame python project/sounds/shield_bonus_collect.mp3")
shield_bonus_sound = pygame.mixer.Sound("pygame python project/sounds/shield_bonus_collect.mp3")

main_menu_music = [
    pygame.mixer.Sound("pygame python project/sounds/main_menu_music.mp3"),
    pygame.mixer.Sound("pygame python project/sounds/videoplayback.mp3")
]

game_music = [
    pygame.mixer.Sound("pygame python project/sounds/game_music.mp3"),
    pygame.mixer.Sound("pygame python project/sounds/Supporting_Me.mp3")
]

shoot_sound.set_volume(0.45)
jump_sound.set_volume(0.5)

button_font = pygame.font.SysFont('arial', 32)
health_font = pygame.font.SysFont('arial', 16)
bonus_font = pygame.font.SysFont('arial', 24)
title_font = pygame.font.Font("pygame python project/font/zettameter.ttf", 80)
number_font = pygame.font.Font("pygame python project/font/RubikSprayPaint-Regular.ttf", 40)

PLAYER_SPRITES = {
    "player_1": "pygame python project/image/slime_sprite_green.png",
    "player_2": "pygame python project/image/slime_sprite_orange.png"
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

last_bonus_time = 0
running = True
game_paused = False
winner = None
final_winner = None
round_end_time = 0