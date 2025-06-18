import random

import pygame
from settings import *
from bullet import Bullet
from utils import load_image


class Player:
    def __init__(self, x, y, size, player_id):
        self.x = x
        self.y = y
        self.width = size
        self.height = size
        self.rect = pygame.Rect(x, y, size, size)
        self.velocity_y = 0
        self.jumping = False
        self.direction = 1  # 1 - вправо, -1 - влево
        self.player_id = player_id
        self.health = MAX_HEALTH
        self.bullets = []
        self.shoot_cooldown = 0
        self.damage_boost = False
        self.damage_boost_time = 0
        self.protection_boost = False
        self.protection_count = 0
        self.sprite = None
        self.shield_sprite = None
        self.icon_damage_boost_sprite = None
        self.load_sprites()
        self.on_ground = False
        self.has_gauntlet = False
        self.push_cooldown = 0
        self.push_effect_time = 0
        self.is_pushed = False
        self.push_direction = (0, 0)
        self.disable_controls = False
        self.push_circle_time = 0
        self.push_circle_pos = (0, 0)
        self.push_target = (0, 0)  # Целевая позиция толчка
        self.push_start = (0, 0)  # Стартовая позиция
        self.push_start_time = 0  # Время начала толчка
        self.disable_controls_timer = 0  # Таймер для отслеживания времени без управления
        self.actual_x = x  # Фактическая позиция спрайта для отрисовки
        self.actual_y = y  # Фактическая позиция спрайта для отрисовки

    def push_enemy(self, enemy):
        if self.has_gauntlet and self.push_cooldown <= 0:
            # Расчёт направления толчка
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Избегаем деления на 0

            if distance <= PUSH_DISTANCE:
                # Настройка параметров толчка
                self.push_cooldown = GAUNTLET_COOLDOWN
                self.has_gauntlet = False

                # Нормализованный вектор направления
                nx = dx / distance
                ny = dy / distance * 0.7  # Меньше по вертикали

                # Вычисляем конечную позицию
                enemy.push_target = (
                    enemy.rect.x + nx * PUSH_DISTANCE,
                    enemy.rect.y + ny * PUSH_DISTANCE
                )
                enemy.push_start = (enemy.rect.x, enemy.rect.y)
                enemy.push_start_time = pygame.time.get_ticks()
                enemy.disable_controls_timer = pygame.time.get_ticks()

                # Активируем состояния
                enemy.is_pushed = True
                enemy.disable_controls = True

                # Визуальные эффекты
                self.push_circle_time = pygame.time.get_ticks()
                self.push_circle_pos = self.rect.center

                enemy.actual_x = enemy.x
                enemy.actual_y = enemy.y

    def draw_push_circle(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.push_circle_time < PUSH_DURATION:
            # Calculate alpha (transparency) based on remaining time
            elapsed = current_time - self.push_circle_time
            alpha = 255 - int((elapsed / PUSH_DURATION) * 255)

            # Create a surface for the circle
            circle_surface = pygame.Surface((PUSH_DISTANCE * 2, PUSH_DISTANCE * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (255, 165, 0, alpha),
                               (PUSH_DISTANCE, PUSH_DISTANCE), PUSH_DISTANCE, 2)

            # Blit the circle surface
            screen.blit(circle_surface,
                        (self.push_circle_pos[0] - PUSH_DISTANCE,
                         self.push_circle_pos[1] - PUSH_DISTANCE))

    def update_push_effect(self):
        current_time = pygame.time.get_ticks()

        # Обновление позиции при толчке
        if self.is_pushed:
            progress = min(1.0, (current_time - self.push_start_time) / (PUSH_DURATION * 1000))

            # Плавное перемещение к целевой точке
            self.x = self.push_start[0] + (self.push_target[0] - self.push_start[0]) * progress
            self.y = self.push_start[1] + (self.push_target[1] - self.push_start[1]) * progress
            self.rect.x = self.x
            self.rect.y = self.y

            # Обновляем позицию спрайта
            self.actual_x = self.x
            self.actual_y = self.y

            if progress < 0.8:
                self.actual_x += random.randint(-3, 3)
                self.actual_y += random.randint(-3, 3)
            # Проверяем завершение толчка
            if progress >= 1.0:
                self.is_pushed = False
                # Гарантируем точное попадание в конечную позицию
                self.x = self.push_target[0]
                self.y = self.push_target[1]
                self.rect.x = self.x
                self.rect.y = self.y
                self.actual_x = self.x
                self.actual_y = self.y

        # Отдельно проверяем таймер блокировки управления
        if self.disable_controls:
            if current_time - self.disable_controls_timer > PUSH_DISABLE_DURATION:
                self.disable_controls = False

    def load_sprites(self):
        try:
            self.sprite = load_image(PLAYER_SPRITES[self.player_id])
            self.shield_sprite = load_image(
                "C:/Users/Denis/Desktop/pyGame-project-2025-opd-main/pygame python project/image/shield.png")
            self.icon_damage_boost_sprite = load_image(
                "C:/Users/Denis/Desktop/pyGame-project-2025-opd-main/pygame python project/image/icon_damage_boost.png")

            if self.shield_sprite:
                self.shield_sprite = pygame.transform.scale(self.shield_sprite,
                                                            (self.rect.width + 8, self.rect.height + 8))

            if self.sprite:
                # Масштабируем спрайт под размер персонажа
                self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

                # Создаем зеркальное отражение для движения влево
                self.flipped_sprite = pygame.transform.flip(self.sprite, True, False)
        except Exception as e:
            print(f"Error loading player sprite: {e}")
            self.sprite = None

    def move(self, dx, platforms):
        if dx != 0:
            self.direction = dx

        old_x = self.x
        self.x += dx * PLAYER_SPEED
        self.actual_x = self.x

        # Ограничение по горизонтали (чтобы не выходил за границы экрана)
        self.x = max(0, min(self.x, WIDTH - self.rect.width))  # Не левее 0 и не правее WIDTH
        self.actual_x = self.x
        self.rect.x = self.x

        # Проверка боковых коллизий с платформами (только в воздухе)
        if not self.on_ground:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # Движение вправо
                    if dx > 0 and old_x + self.rect.width <= platform.rect.left:
                        self.rect.right = platform.rect.left
                        self.x = self.rect.x
                        self.actual_x = self.x
                    # Движение влево
                    elif dx < 0 and old_x >= platform.rect.right:
                        self.rect.left = platform.rect.right
                        self.x = self.rect.x
                        self.actual_x = self.x

    def jump(self):
        if self.on_ground and not self.jumping:
            self.velocity_y = JUMP_FORCE
            self.jumping = True
            self.on_ground = False

    def apply_gravity(self, platforms, map_type):
        # Всегда применяем гравитацию
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        self.actual_y = self.y
        self.rect.y = self.y

        # Сбрасываем флаг нахождения на земле перед проверкой коллизий
        self.on_ground = False

        # Проверяем коллизии с платформами
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Если падаем вниз и нижняя часть игрока выше нижней части платформы
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + self.velocity_y + 5:
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.actual_y = self.y
                    self.velocity_y = 0
                    self.jumping = False
                    self.on_ground = True

    def shoot(self, dx, dy):
        if self.shoot_cooldown <= 0:
            damage = 15 if self.damage_boost else 10
            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, dx, dy, self.player_id)
            bullet.damage = damage
            self.bullets.append(bullet)
            self.shoot_cooldown = SHOOT_COOLDOWN

    def update_bullets(self, enemy):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.colliderect(enemy.rect):
                if enemy.protection_boost:
                    enemy.protection_count = enemy.protection_count - 1
                    self.bullets.remove(bullet)
                else:
                    enemy.health -= bullet.damage
                    self.bullets.remove(bullet)
            elif bullet.is_out_of_screen():
                self.bullets.remove(bullet)

    def update_cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.damage_boost and current_time - self.damage_boost_time > DAMAGE_BOOST_DURATION:
            self.damage_boost = False
            print(f"Player {self.player_id}'s damage boost ended!")

    def update_protection(self):
        if self.protection_count > 0:
            self.protection_boost = True
        else:
            self.protection_boost = False

    def draw_shield(self, surface):

        if self.shield_sprite:
            surface.blit(self.shield_sprite, (self.x - 4, self.y - 4))
        else:
            pygame.draw.rect(surface, BLUE, self.rect)

    def draw_boost_damage_icon(self, surface):
        icon_width = 8
        icon_height = 8
        icon_x = self.rect.x + self.rect.width + 5
        icon_y = self.rect.y - 15

        surface.blit(self.icon_damage_boost_sprite, (icon_x, icon_y))

    def draw_health_bar(self, surface):
        # Размеры и положение health bar
        bar_width = self.rect.width
        bar_height = 8
        bar_x = self.rect.x
        bar_y = self.rect.y - 15

        # Фон health bar (черный)
        pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height))

        # Текущее здоровье (зеленый/желтый/красный)
        health_ratio = self.health / MAX_HEALTH
        health_width = int(bar_width * health_ratio)

        health_color = GREEN if health_ratio > 0.5 else YELLOW if health_ratio > 0.2 else RED

        pygame.draw.rect(surface, health_color, (bar_x, bar_y, health_width, bar_height))

        # Текст с количеством HP
        health_text = health_font.render(f"{self.health}/{MAX_HEALTH}", True, WHITE)
        text_rect = health_text.get_rect(center=(self.rect.centerx, bar_y - 8))
        surface.blit(health_text, text_rect)

    def draw(self, screen):
        # #отрисовка барьера
        if self.protection_boost:
            self.draw_shield(screen)

        if self.has_gauntlet:
            gauntlet_icon = load_image(
                "C:/Users/Denis/Desktop/pyGame-project-2025-opd-main/pygame python project/image/gauntlet_icon.png")
            if gauntlet_icon:
                gauntlet_icon = pygame.transform.scale(gauntlet_icon, (20, 20))
                screen.blit(gauntlet_icon, (self.rect.x + self.rect.width + 5, self.rect.y + 5))
        # Рисуем спрайт или прямоугольник, если спрайт не загружен
        if self.sprite:
            current_sprite = self.sprite if self.direction > 0 else self.flipped_sprite
            screen.blit(current_sprite, (self.actual_x, self.actual_y))
        else:
            color = YELLOW if self.player_id == "player_1" else RED
            pygame.draw.rect(screen, color, (self.actual_x, self.actual_y, self.width, self.height))

        if self.disable_controls:
            current_time = pygame.time.get_ticks()
            remaining_time = max(0, PUSH_DISABLE_DURATION - (current_time - self.push_effect_time))
            timer_text = health_font.render(f"{remaining_time / 60:.1f}s", True, RED)
            screen.blit(timer_text, (self.rect.centerx - 15, self.rect.y - 30))

        if DEBUG_MODE and self.is_pushed:
            # Рисуем линию от стартовой до целевой позиции
            pygame.draw.line(screen, (255, 0, 0),
                             (self.push_start[0] + self.width // 2, self.push_start[1] + self.height // 2),
                             (self.push_target[0] + self.width // 2, self.push_target[1] + self.height // 2), 2)
        if self.disable_controls:
            # Отображаем оставшееся время без управления
            remaining = max(0, PUSH_DISABLE_DURATION - (pygame.time.get_ticks() - self.disable_controls_timer))
            timer_text = health_font.render(f"{remaining // 1000}.{(remaining % 1000) // 100}s", True, RED)
            screen.blit(timer_text, (self.rect.x, self.rect.y - 30))
        # отрисовка хпбара
        self.draw_health_bar(screen)

        # отрисовка иконки увеличения урона
        if (self.damage_boost):
            self.draw_boost_damage_icon(screen)

        # Отрисовка пуль
        for bullet in self.bullets:
            bullet.draw(screen, self.player_id)

        self.draw_push_circle(screen)