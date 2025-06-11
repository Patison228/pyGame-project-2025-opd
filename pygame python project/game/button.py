import pygame
from settings import *
from utils import load_image

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