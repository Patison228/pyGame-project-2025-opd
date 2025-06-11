import pygame
import os
import sys
import math
from settings import *
from player import Player
from platform import Platform
from utils import *
from button import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime crushers")
    
menu_background = load_background("pygame python project/image/main_menu_bg.png")  
sky_background = load_background("pygame python project/image/bg_sky.jpg")

def game_loop():
    clock = pygame.time.Clock()
    player1 = Player(WIDTH // 2 - 200, HEIGHT // 2, 50, "player_1")
    player2 = Player(WIDTH // 2 + 100, HEIGHT // 2, 50, "player_2")
    
    # Создаем платформы
    platforms = [
        Platform(100, 430, 200, 20),
        Platform(500, 430, 200, 20),
        Platform(300, 300, 200, 20),
        Platform(100, 200, 200, 20),
        Platform(500, 200, 200, 20)
    ]
    
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
        player1.apply_gravity(platforms)
        player2.apply_gravity(platforms)
        
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
        screen.blit(sky_background, (0,0))
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - FLOOR_HEIGHT, WIDTH, FLOOR_HEIGHT))
        
        # Рисуем платформы
        for platform in platforms:
            platform.draw(screen)
        
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