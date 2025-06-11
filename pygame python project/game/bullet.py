import pygame
from settings import *
from utils import load_image

class Bullet:
    def __init__(self, x, y, dx, dy, owner):
        self.width = 15
        self.height = 10 
        
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.dx = dx * BULLET_SPEED
        self.dy = dy * BULLET_SPEED
        self.owner = owner
        self.damage = 10
        self.sprite = None
        self.is_diagonal = abs(dy) > 0  
        self.load_sprite()
        
    def load_sprite(self):
        try:
            base_path = "pygame python project/image/"
            
            if (self.owner == "player_1"):
                sprite_name = "bullet_yellow.png"
            else:
                sprite_name = "bullet_red.png"

            self.sprite = load_image(base_path + sprite_name)
            
            if self.sprite:
                self.sprite = pygame.transform.scale(self.sprite, (self.rect.width, self.rect.height))
        except Exception as e:
            print(f"Download bullet sprite error: {e}")
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
            color = YELLOW if owner == "player_1" else RED
            pygame.draw.rect(surface, color, self.rect)
            
    def is_out_of_screen(self):
        return (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT)