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
from music_menager import MusicManager

pygame.init()
musicManager = MusicManager(main_menu_music, game_music)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime crushers")

# Загрузка изображений
menu_background = load_background("pygame python project/image/main_menu_bg.png")
sky_background = load_background("pygame python project/image/bg_sky.jpg")

def generate_platforms(map_type):
    platforms = []

    if map_type == "classic":
        # Классическая карта с полом и платформами
        platforms = [
            Platform(100, 180, 200, 20),
            Platform(500, 180, 200, 20),
            Platform(300, 300, 200, 20),
            Platform(100, 420, 200, 20),
            Platform(500, 420, 200, 20),
            Platform(0, HEIGHT - 50, WIDTH, 50)  # Пол
        ]
    elif map_type == "no_floor":
        # Карта без пола
        platforms = [
            Platform(100, 325, 200, 20),
            Platform(450, 200, 200, 20),
            Platform(300, 500, 200, 20),
            Platform(150, 420, 200, 20),
            Platform(500, 420, 200, 20)
        ]
    elif map_type == "pits":
        # Карта с пропастями
        platforms = [
            Platform(50, 180, 200, 20),
            Platform(550, 180, 200, 20),
            Platform(300, 300, 200, 20),
            Platform(50, 420, 200, 20),
            Platform(550, 420, 200, 20),
            Platform(0, HEIGHT - 50, 300, 50),  # Левая часть пола
            Platform(WIDTH//2+100, HEIGHT - 50, 300, 50)  # Правая часть пола
        ]

    return platforms

def game_loop(map_type):
    clock = pygame.time.Clock()
    musicManager.play_game()
    global player1_wins, player2_wins, winner

    # Инициализация глобальных переменных
    global game_paused, final_winner, round_end_time
    game_paused = False
    final_winner = None
    round_end_time = 0

    platforms = generate_platforms(map_type)

    spawn_platforms = random.sample([p for p in platforms if p.height < 50], 2)

    player1 = Player(
        spawn_platforms[0].x + spawn_platforms[0].width // 2 - 25,
        spawn_platforms[0].y - 50 - 5,
        50, "player_1"
    )
    player2 = Player(
        spawn_platforms[1].x + spawn_platforms[1].width // 2 - 25,
        spawn_platforms[1].y - 50 - 5,
        50, "player_2"
    )

    bonuses = []
    running = True
    show_countdown = True  # Флаг для показа обратного отсчета
    countdown_start = pygame.time.get_ticks()
    last_bonus_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()
        
        # Показываем обратный отсчет в начале раунда
        if show_countdown and map_type:
            elapsed = current_time - countdown_start
            if elapsed < 3000:  # 5 секунд отсчета
                countdown_value = 3 - elapsed // 1000
                screen.blit(sky_background, (0, 0))
                countdown_text = number_font.render(str(countdown_value), True, WHITE)
                screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
                pygame.display.flip()
                continue
            else:
                show_countdown = False
                countdown_start = current_time

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player2_wins = 0
                    player1_wins = 0
                    return "menu"

        if not game_paused and not show_countdown:
            # Управление игроками
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]: player1.move(-1, platforms)
            if keys[pygame.K_d]: player1.move(1, platforms)
            if keys[pygame.K_LEFT]: player2.move(-1, platforms)
            if keys[pygame.K_RIGHT]: player2.move(1, platforms)
            if keys[pygame.K_w]: player1.jump()
            if keys[pygame.K_UP]: player2.jump()
            if keys[pygame.K_f]: player1.shoot(player1.direction, 0)
            if keys[pygame.K_l]: player2.shoot(player2.direction, 0)
            if keys[pygame.K_g]: player1.shoot(player1.direction, 1)
            if keys[pygame.K_k]: player2.shoot(player2.direction, 1)

            # Обновление игрового состояния
            player1.apply_gravity(platforms, map_type)
            player2.apply_gravity(platforms, map_type)
            player1.update_protection()
            player2.update_protection()
            player1.update_bullets(player2)
            player2.update_bullets(player1)
            player1.update_cooldown()
            player2.update_cooldown()
            
            # Проверка падения
            if map_type in ["no_floor", "pits"]:
                if player1.rect.top > HEIGHT + 100:
                    player1.health = 0
                if player2.rect.top > HEIGHT + 100:
                    player2.health = 0

            # Проверка условий победы
            if player1.health <= 0 or player2.health <= 0:
                if player1.health <= 0 and player2.health <= 0:
                    pass  # Ничья
                elif player1.health <= 0:
                    player2_wins += 1
                    winner = "Player 2"
                else:
                    player1_wins += 1
                    winner = "Player 1"

                # Проверка на финальную победу
                if player1_wins >= 3 or player2_wins >= 3:
                    final_winner = winner

                game_paused = True
                round_end_time = current_time

        # Отрисовка
        screen.blit(sky_background, (0, 0))

        # Рисуем платформы
        for platform in platforms:
            platform.draw(screen)

        #добавление бонуса
        if current_time - last_bonus_time > BONUS_INTERVAL:
            platform = random.choice(platforms)
            x = random.randint(platform.x, platform.x + platform.width - 30)
            y = platform.y - 30
            bonuses.append(Bonus(x, y))
            last_bonus_time = current_time

        #проверка подбора бонуса
        for bonus in bonuses[:]:
            if bonus.check_collision(player1) or bonus.check_collision(player2):
                bonuses.remove(bonus)

        while abs(spawn_platforms[0].x - spawn_platforms[1].x) < MIN_SPAWN_DISTANCE:
            spawn_platforms = random.sample(platforms, 2)

        # Рисуем игроков, если игра не закончена
        if not final_winner and not show_countdown:
            player1.draw(screen)
            player2.draw(screen)

        # Рисуем бонусы
        for bonus in bonuses:
            bonus.draw(screen)

        # Отрисовка счета
        score_text = f"{player1_wins} - {player2_wins}"
        score_surface = number_font.render(score_text, True, YELLOW)
        screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 20))

        # Если игра на паузе между раундами
        if game_paused and not show_countdown:
            if final_winner:
                # Финальная победа
                winner_text = number_font.render(f"{final_winner} won the game!", True, RED)
                subtitle = number_font.render("Returning to main menu...", True, RED)

                screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 50))
                screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 + 20))
                player2_wins = 0
                player1_wins = 0
                pygame.display.flip()
                pygame.time.wait(3000)

                return "menu"
            else:
                # Победа в раунде
                elapsed = current_time - round_end_time

                if elapsed < 3000:  # 5 секунд паузы
                    countdown = 3 - elapsed // 1000
                    winner_text = number_font.render(f"{winner} won the round!", True, WHITE)
                    countdown_text = number_font.render(f"Next round in {countdown}", True, WHITE)

                    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 50))
                    screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 + 20))
                else:
                    # Перезапуск раунда
                    game_paused = False
                    show_countdown = True
                    bonuses.clear()
                    countdown_start = pygame.time.get_ticks()
                    platforms = generate_platforms(map_type)
                    spawn_platforms = random.sample([p for p in platforms if p.height < 50], 2)

                    player1 = Player(
                        spawn_platforms[0].x + spawn_platforms[0].width // 2 - 25,
                        spawn_platforms[0].y - 50 - 5,
                        50, "player_1"
                    )
                    player2 = Player(
                        spawn_platforms[1].x + spawn_platforms[1].width // 2 - 25,
                        spawn_platforms[1].y - 50 - 5,
                        50, "player_2"
                    )

        pygame.display.update()
        clock.tick(FPS)

    return "menu"

def select_map():
    clock = pygame.time.Clock()
    buttons = [
        Button(WIDTH // 2 - 150, 200, 300, 50, "Classic Map"),
        Button(WIDTH // 2 - 150, 270, 300, 50, "No Floor Map"),
        Button(WIDTH // 2 - 150, 340, 300, 50, "Pits Map"),
        Button(WIDTH // 2 - 150, 410, 300, 50, "Back")
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.rect.collidepoint(mouse_pos):
                        if i == 3:  # Кнопка Back
                            return "menu"
                        else:
                            return ["classic", "no_floor", "pits"][i]

        # Отрисовка
        screen.blit(menu_background, (0, 0))
        title_text = title_font.render("Select Map", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 90))

        for button in buttons:
            button.is_hovered = button.rect.collidepoint(mouse_pos)
            button.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

def start_game():
    map_choice = select_map()
    if map_choice == "menu":
        return main_menu()
    else:
        game_loop(map_choice)

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