import pygame
import sys
import os

pygame.init()

# Константы игры
FPS = 60
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
JUMP_FORCE = -12
PLAYER_SPEED = 5
FLOOR_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime crushers")

# Загрузка и растягивание фонового изображения
def load_background(path):
    image = pygame.image.load(path).convert()
    return pygame.transform.scale(image, (WIDTH, HEIGHT))
    
background = load_background("pygame python project/image/main_menu_bg.png")  

# Цвета
COLOR_OF_SKY = (135, 206, 235)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (150, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Цвет пола

# Шрифты
title_font = pygame.font.Font("pygame python project/font/zettameter.ttf", 64)
button_font = pygame.font.SysFont('arial', 32)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        
    def draw(self, surface):
        color = HOVER_COLOR if self.is_hovered else WHITE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surf = button_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                return self.action()
        return None

class Player:
    def __init__(self, x, y, size=50, character_type = "player_1"):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = PLAYER_SPEED
        self.color = RED
        self.velocity_y = 0
        self.jumping = False
        self.direction = 1  # 1 - вправо, -1 - влево
        self.character_type = character_type
        self.sprites = {
            'idle': None,
            'jump': None
        }
        self.current_sprite = None
        self.load_sprites()
        
    def load_sprites(self):
        try:
            if self.character_type == "player_1":
                idle_img = pygame.image.load("pygame python project/image/slime_sprite_green.png").convert_alpha()
                jump_img = pygame.image.load("pygame python project/image/slime_sprite_green.png").convert_alpha()
            elif self.character_type == "player_2":
                idle_img = pygame.image.load("pygame python project/image/slime_sprite_orange.png").convert_alpha()
                jump_img = pygame.image.load("pygame python project/image/slime_sprite_orange.png").convert_alpha()
            else:
                # Если тип персонажа не распознан, используем стандартный квадрат
                return
            
            self.sprites['idle'] = pygame.transform.scale(idle_img, (self.rect.width, self.rect.height))
            self.sprites['jump'] = pygame.transform.scale(jump_img, (self.rect.width, self.rect.height))
            self.current_sprite = self.sprites['idle']
        except:
            print(f"Не удалось загрузить спрайты для {self.character_type}. Будет использован стандартный квадрат.")
            self.current_sprite = None
    
    def move(self, dx):
        if dx != 0:
            self.direction = 1 if dx > 0 else -1
        self.rect.x += dx * self.speed
        # Ограничение движения по горизонтали
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        
    def apply_gravity(self, floor_y):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Обновляем спрайт в зависимости от состояния
        if self.jumping:
            self.current_sprite = self.sprites.get('jump', None)
        else:
            self.current_sprite = self.sprites.get('idle', None)
        
        # Проверка столкновения с полом
        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.velocity_y = 0
            self.jumping = False
            
    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_FORCE
            self.jumping = True
            self.current_sprite = self.sprites.get('jump', None)
            
    def draw(self, surface):
        if self.current_sprite:
            # Отражаем спрайт, если направление изменилось
            flipped_sprite = pygame.transform.flip(self.current_sprite, self.direction < 0, False)
            surface.blit(flipped_sprite, self.rect)
        else:
            # Рисуем квадрат, если спрайты не загружены
            pygame.draw.rect(surface, self.color, self.rect)

def game_loop():
    clock = pygame.time.Clock()
    player1 = Player(WIDTH // 2 - 100, HEIGHT // 2, 50, "player_1")
    player2 = Player(WIDTH // 2 + 100, HEIGHT // 2, 50, "player_2")
    
    # Параметры пола
    floor_y = HEIGHT - FLOOR_HEIGHT
    
    running = True
    
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Возврат в меню
                if event.key == pygame.K_SPACE:
                    player1.jump()
                if event.key == pygame.K_UP:
                    player2.jump()
        
        # Управление
        keys = pygame.key.get_pressed()
        
        # Управление для первого игрока (WASD + Space)
        dx1 = 0
        if keys[pygame.K_a]:
            dx1 -= 1
        if keys[pygame.K_d]:
            dx1 += 1
        player1.move(dx1)
        
        # Управление для второго игрока (Стрелки)
        dx2 = 0
        if keys[pygame.K_LEFT]:
            dx2 -= 1
        if keys[pygame.K_RIGHT]:
            dx2 += 1
        player2.move(dx2)
        
        player1.apply_gravity(floor_y)
        player2.apply_gravity(floor_y)
        
        # Отрисовка
        screen.fill(COLOR_OF_SKY)
        
        # Рисуем пол
        pygame.draw.rect(screen, GREEN, (0, floor_y, WIDTH, FLOOR_HEIGHT))
        
        player1.draw(screen)
        player2.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Функции действий кнопок
def start_game():
    print("Play!")
    game_loop()

def quit_game():
    pygame.quit()
    sys.exit()

# Создание кнопок
buttons = [
    Button(WIDTH//2 - 100, 250, 200, 50, "Start game", start_game),
    Button(WIDTH//2 - 100, 320, 200, 50, "Quit", quit_game)
]

# Основной цикл меню
def main_menu():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            for button in buttons:
                result = button.handle_event(event)
                if result is not None:
                    return result
        
        # Обновление состояния кнопок
        for button in buttons:
            button.check_hover(mouse_pos)
        
        # Отрисовка - сначала фон
        screen.blit(background, (0, 0))
        
        # Заголовок
        title_text = title_font.render("Slime crushers", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, 150))
        screen.blit(title_text, title_rect)
        
        # Кнопки
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

# Запуск меню
if __name__ == "__main__":
    main_menu()