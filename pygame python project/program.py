import pygame
import sys
import os
import math

pygame.init()

# Константы игры
FPS = 60
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
JUMP_FORCE = -12
PLAYER_SPEED = 5
FLOOR_HEIGHT = 50
BULLET_SPEED = 10
MAX_HEALTH = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime crushers")

# Загрузка изображений
def load_image(path):
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except:
        print(f"Не удалось загрузить изображение: {path}")
        return None

def load_background(path):
    image = pygame.image.load(path).convert()
    return pygame.transform.scale(image, (WIDTH, HEIGHT))
    
menu_background = load_background("pygame python project/image/main_menu_bg.png")  
sky_background = load_background("pygame python project/image/bg_sky.jpg")

# Цвета
COLOR_OF_SKY = (135, 206, 235)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (150, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Шрифты
title_font = pygame.font.Font("pygame python project/font/zettameter.ttf", 64)
button_font = pygame.font.SysFont('arial', 32)
health_font = pygame.font.SysFont('arial', 16)

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

class Bullet:
    def __init__(self, x, y, dx, dy, owner):
        # Размеры пули (можно настроить под ваши спрайты)
        self.width = 15
        self.height = 10 
        
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.dx = dx * BULLET_SPEED
        self.dy = dy * BULLET_SPEED
        self.owner = owner
        self.damage = 10
        self.sprite = None
        self.is_diagonal = abs(dy) > 0  # Определяем тип выстрела
        self.load_sprite()
        
    def load_sprite(self):
        try:
            base_path = "pygame python project/image/"
            
            # Используем один спрайт для всех типов выстрелов
            if (self.owner == "player_1"):
                sprite_name = "bullet_yellow.png"
            else:
                sprite_name = "bullet_red.png"

            self.sprite = load_image(base_path + sprite_name)
            
            if self.sprite:
                self.sprite = pygame.transform.scale(self.sprite, (self.rect.width, self.rect.height))
        except Exception as e:
            print(f"Ошибка загрузки спрайта пули: {e}")
            self.sprite = None

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
    def draw(self, surface, owner):
        if self.sprite:
            # Определяем направление движения
            direction = -1 if self.dx < 0 else 1
            
            # Для диагональных пуль добавляем вращение
            if self.is_diagonal:
                angle = 45 * direction * (-1 if self.dy > 0 else 1)
                rotated_sprite = pygame.transform.rotate(self.sprite, angle)
                
                # Корректируем позицию после вращения
                rotated_rect = rotated_sprite.get_rect(center=self.rect.center)
                surface.blit(rotated_sprite, rotated_rect)
            else:
                # Для прямых пуль просто отражаем по горизонтали если нужно
                flipped_sprite = pygame.transform.flip(self.sprite, self.dx < 0, False)
                surface.blit(flipped_sprite, self.rect)
        else:
            # Фолбэк: рисуем цветные прямоугольники если спрайты не загрузились
            color = YELLOW if owner == "player_1" else RED
            pygame.draw.rect(surface, color, self.rect)
            
    def is_out_of_screen(self):
        return (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT)

class Player:
    def __init__(self, x, y, size=50, character_type="player_1"):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = PLAYER_SPEED
        self.color = RED if character_type == "player_1" else BLUE
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
        self.cooldown = 0
        self.max_cooldown = 40  # Задержка между выстрелами
        self.health = MAX_HEALTH
        self.max_health = MAX_HEALTH
        self.bullets = []
        
    def load_sprites(self):
        try:
            if self.character_type == "player_1":
                idle_img = load_image("pygame python project/image/slime_sprite_green.png")
                jump_img = load_image("pygame python project/image/slime_sprite_green.png")
            elif self.character_type == "player_2":
                idle_img = load_image("pygame python project/image/slime_sprite_orange.png")
                jump_img = load_image("pygame python project/image/slime_sprite_orange.png")
            
            if idle_img and jump_img:
                self.sprites['idle'] = pygame.transform.scale(idle_img, (self.rect.width, self.rect.height))
                self.sprites['jump'] = pygame.transform.scale(jump_img, (self.rect.width, self.rect.height))
                self.current_sprite = self.sprites['idle']
        except:
            print(f"Не удалось загрузить спрайты для {self.character_type}")
            self.current_sprite = None
    
    def move(self, dx, dy=0):
        if dx != 0:
            self.direction = 1 if dx > 0 else -1
        self.rect.x += dx * self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        
    def apply_gravity(self, floor_y):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        if self.jumping:
            self.current_sprite = self.sprites.get('jump', None)
        else:
            self.current_sprite = self.sprites.get('idle', None)
        
        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.velocity_y = 0
            self.jumping = False
            
    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_FORCE
            self.jumping = True
            self.current_sprite = self.sprites.get('jump', None)
            
    def shoot(self, dx, dy):
        if self.cooldown <= 0:
            # Определяем стартовую позицию пули
            start_x = self.rect.centerx + (20 * self.direction)
            start_y = self.rect.centery
            
            # Нормализуем вектор направления
            length = max(1, math.sqrt(dx*dx + dy*dy))
            ndx = dx / length
            ndy = dy / length
            
            self.bullets.append(Bullet(start_x, start_y, ndx, ndy, self.character_type))
            self.cooldown = self.max_cooldown
            
    def update_bullets(self, other_player):
        # Обновляем пули
        for bullet in self.bullets[:]:
            bullet.update()
            
            # Проверяем столкновение с другим игроком
            if bullet.rect.colliderect(other_player.rect) and bullet.owner != other_player:
                other_player.take_damage(bullet.damage)
                self.bullets.remove(bullet)
            # Удаляем пули за пределами экрана
            elif bullet.is_out_of_screen():
                self.bullets.remove(bullet)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
    def update_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            
    def draw_health_bar(self, surface):
        # Размеры и положение health bar
        bar_width = self.rect.width
        bar_height = 8
        bar_x = self.rect.x
        bar_y = self.rect.y - 15
        
        # Фон health bar (черный)
        pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height))
        
        # Текущее здоровье (зеленый/красный)
        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        
        health_color = GREEN if health_ratio > 0.5 else YELLOW if health_ratio > 0.2 else RED
        
        pygame.draw.rect(surface, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Текст с количеством HP
        health_text = health_font.render(f"{self.health}/{self.max_health}", True, WHITE)
        text_rect = health_text.get_rect(center=(self.rect.centerx, bar_y - 8))
        surface.blit(health_text, text_rect)
            
    def draw(self, surface):
        if self.current_sprite:
            flipped_sprite = pygame.transform.flip(self.current_sprite, self.direction < 0, False)
            surface.blit(flipped_sprite, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        
        # Рисуем health bar
        self.draw_health_bar(surface)
        
        # Рисуем все пули
        for bullet in self.bullets:
            bullet.draw(surface, self.character_type)

def game_loop():
    clock = pygame.time.Clock()
    player1 = Player(WIDTH // 2 - 100, HEIGHT // 2, 50, "player_1")
    player2 = Player(WIDTH // 2 + 100, HEIGHT // 2, 50, "player_2")
    
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
                    return
                if event.key == pygame.K_SPACE:
                    player1.jump()
                if event.key == pygame.K_UP:
                    player2.jump()
                # Выстрел для игрока 1
                if event.key == pygame.K_f:
                    dx = 1 if player1.direction > 0 else -1
                    player1.shoot(dx, 0)
                if event.key == pygame.K_g:
                    dx = 1 if player1.direction > 0 else -1
                    player1.shoot(dx, 1)  # Диагональный выстрел вниз
                # Выстрел для игрока 2
                if event.key == pygame.K_l:
                    dx = 1 if player2.direction > 0 else -1
                    player2.shoot(dx, 0)
                if event.key == pygame.K_k:
                    dx = 1 if player2.direction > 0 else -1
                    player2.shoot(dx, 1)  # Диагональный выстрел вниз
        
        # Управление
        keys = pygame.key.get_pressed()
        
        # Игрок 1 (WASD + Space)
        dx1 = keys[pygame.K_d] - keys[pygame.K_a]
        player1.move(dx1)
        
        # Игрок 2 (Стрелки)
        dx2 = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        player2.move(dx2)
        
        # Физика
        player1.apply_gravity(floor_y)
        player2.apply_gravity(floor_y)
        
        # Обновление пуль и проверка столкновений
        player1.update_bullets(player2)
        player2.update_bullets(player1)
        
        # Обновление кулдауна
        player1.update_cooldown()
        player2.update_cooldown()
        
        # Проверка здоровья
        if (player1.health <= 0):  
            print("Игра окончена! Победил Красный!")
            return
        elif (player2.health <= 0):
            print("Игра окончена! Победил Желтый!")
            return
        
        # Отрисовка
        screen.blit(sky_background, (0, 0))
        pygame.draw.rect(screen, GREEN, (0, floor_y, WIDTH, FLOOR_HEIGHT))
        
        player1.draw(screen)
        player2.draw(screen)
        
        pygame.display.update()
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            for button in buttons:
                result = button.handle_event(event)
                if result is not None:
                    return result
        
        for button in buttons:
            button.check_hover(mouse_pos)
        
        screen.blit(menu_background, (0, 0))
        
        title_text = title_font.render("Slime crushers", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, 150))
        screen.blit(title_text, title_rect)
        
        for button in buttons:
            button.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()