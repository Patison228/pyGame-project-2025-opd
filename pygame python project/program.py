import pygame
import sys

pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime crushers")

# Загрузка и растягивание фонового изображения
def load_background(path):
    image = pygame.image.load(path).convert()
    return pygame.transform.scale(image, (WIDTH, HEIGHT))
    
background = load_background("pygame python project/image/main_menu_bg.png")  

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (150, 150, 255)

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

# Функции действий кнопок
def start_game():
    print("Play!")

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