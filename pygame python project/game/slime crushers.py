import pygame
import os
import sys
import random
from settings import *
from player import Player
from platform import Platform
from utils import *
from button import Button
from bonus import Bonus

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime crushers")

menu_background = load_background("C:/Users/Denis/Desktop/pygame python project/image/main_menu_bg.png")
sky_background = load_background("C:/Users/Denis/Desktop/pygame python project/image/bg_sky.jpg")


def game_loop():
    clock = pygame.time.Clock()

    global player1_wins, player2_wins, match_winner, waiting_for_next_match, match_start_time


    # Создаем платформы
    platforms = [
        Platform(100, 180, 200, 20),
        Platform(500, 180, 200, 20),
        Platform(300, 300, 200, 20),
        Platform(100, 420, 200, 20),
        Platform(500, 420, 200, 20)
    ]

    # Выбираем случайные платформы для спавна игроков
    spawn_platforms = random.sample(platforms, 2)

    # Создаем игроков на платформах
    player1 = Player(
        spawn_platforms[0].x + spawn_platforms[0].width // 2 - 25,
        spawn_platforms[0].y - 50 - 5,  # -5 чтобы гарантированно стоял на платформе
        50, "player_1"
    )
    player2 = Player(
        spawn_platforms[1].x + spawn_platforms[1].width // 2 - 25,
        spawn_platforms[1].y - 50 - 5,
        50, "player_2"
    )

    # Другие переменные игры
    bonuses = []
    last_bonus_time = 0
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        if waiting_for_next_match:
            if current_time - match_start_time >= 5000:
                if player1_wins >= 3 or player2_wins >= 3:
                    player1_wins = 0
                    player2_wins = 0
                    match_winner = None
                    waiting_for_next_match = False
                    return  # Возврат в меню
                else:
                    match_winner = None
                    waiting_for_next_match = False
                    return game_loop()  # Новая игра

            # Отрисовка результатов матча
            screen.blit(sky_background, (0, 0))


            # Победитель матча
            winner_text = f"Player {match_winner[-1]} wins!"
            winner_surface = button_font.render(winner_text, True, WHITE)

            if player1_wins >= 3 or player2_wins >= 3:
                final_text = f"Player {match_winner[-1]} wins the tournament!"
                final_surface = button_font.render(final_text, True, WHITE)
                screen.blit(final_surface, (WIDTH // 2 - final_surface.get_width() // 2, HEIGHT // 2 - 50))
                screen.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2))

                timer_text = f"Returning to main menu in {5 - (current_time - match_start_time) // 1000} seconds"
                timer_surface = button_font.render(timer_text, True, WHITE)
                screen.blit(timer_surface, (WIDTH // 2 - timer_surface.get_width() // 2, HEIGHT // 2 + 25))

            else:
                screen.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2 - 25))
                # Таймер
                timer_text = f"Next match in {5 - (current_time - match_start_time) // 1000} seconds"
                timer_surface = button_font.render(timer_text, True, WHITE)
                screen.blit(timer_surface, (WIDTH // 2 - timer_surface.get_width() // 2, HEIGHT // 2 + 25))

            pygame.display.update()
            clock.tick(FPS)
            continue

        if current_time - last_bonus_time > BONUS_INTERVAL:
            platform = random.choice(platforms)
            x = random.randint(platform.x, platform.x + platform.width - 30)
            y = platform.y - 30
            bonuses.append(Bonus(x, y))
            last_bonus_time = current_time

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
                if event.key == pygame.K_f:
                    dx = 1 if player1.direction > 0 else -1
                    player1.shoot(dx, 0)
                if event.key == pygame.K_g:
                    dx = 1 if player1.direction > 0 else -1
                    player1.shoot(dx, 1)
                if event.key == pygame.K_l:
                    dx = 1 if player2.direction > 0 else -1
                    player2.shoot(dx, 0)
                if event.key == pygame.K_k:
                    dx = 1 if player2.direction > 0 else -1
                    player2.shoot(dx, 1)

        keys = pygame.key.get_pressed()
        player1.move(keys[pygame.K_d] - keys[pygame.K_a], platforms)
        player2.move(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], platforms)

        player1.apply_gravity(platforms)
        player2.apply_gravity(platforms)

        player1.update_bullets(player2)
        player2.update_bullets(player1)

        player1.update_cooldown()
        player2.update_cooldown()

        # Проверка столкновений с бонусами
        for bonus in bonuses[:]:
            if bonus.check_collision(player1) or bonus.check_collision(player2):
                bonuses.remove(bonus)

        while abs(spawn_platforms[0].x - spawn_platforms[1].x) < MIN_SPAWN_DISTANCE:
            spawn_platforms = random.sample(platforms, 2)

        if player1.health <= 0 or player2.health <= 0:
            if player1.health <= 0:
                player2_wins += 1
                match_winner = "player_2"
            else:
                player1_wins += 1
                match_winner = "player_1"

            waiting_for_next_match = True
            match_start_time = pygame.time.get_ticks()

        screen.blit(sky_background, (0, 0))
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - FLOOR_HEIGHT, WIDTH, FLOOR_HEIGHT))

        for platform in platforms:
            platform.draw(screen)

        for bonus in bonuses:
            bonus.draw(screen)

        player1.draw(screen)
        player2.draw(screen)

        # Отрисовка счета
        score_text = f"{player1_wins} - {player2_wins}"
        score_surface = button_font.render(score_text, True, WHITE)
        screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 20))

        pygame.display.update()
        clock.tick(FPS)

def start_game():
    print("Play!")
    game_loop()

def quit_game():
    pygame.quit()
    sys.exit()

def main_menu():
    clock = pygame.time.Clock()
    buttons = [
        Button(WIDTH // 2 - 100, 250, 200, 50, "Start game", start_game),
        Button(WIDTH // 2 - 100, 320, 200, 50, "Quit", quit_game)
    ]

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
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))

        for button in buttons:
            button.draw(screen)


        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()