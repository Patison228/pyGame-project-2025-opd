import pygame
import math
from settings import *
from utils import load_image
from bullet import Bullet

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
            print(f"Сouldn't upload image for this character {self.character_type}")
            self.current_sprite = None
    
    def move(self, dx, dy=0):
        if dx != 0:
            self.direction = 1 if dx > 0 else -1
        self.rect.x += dx * self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        
    def apply_gravity(self, platforms):
        # Сохраняем предыдущую позицию по Y
        prev_y = self.rect.y
        
        # Применяем гравитацию
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Проверяем столкновения с платформами
        on_platform = False
        for platform in platforms:
            if platform.check_collision(self):
                on_platform = True
                break
        
        # Если не на платформе, проверяем пол
        if not on_platform:
            if self.rect.bottom >= HEIGHT - FLOOR_HEIGHT:
                self.rect.bottom = HEIGHT - FLOOR_HEIGHT
                self.velocity_y = 0
                self.jumping = False
        
        # Обновляем состояние прыжка
        if self.velocity_y != 0:
            self.jumping = True
        else:
            self.jumping = False
            
        # Обновляем спрайт
        if self.jumping:
            self.current_sprite = self.sprites.get('jump', None)
        else:
            self.current_sprite = self.sprites.get('idle', None)
            
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