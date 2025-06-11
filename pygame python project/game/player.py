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
        self.sprite = None
        self.load_sprites()
        self.on_ground = False
    def load_sprites(self):
        try:
            self.sprite = load_image(PLAYER_SPRITES[self.player_id])
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
        self.rect.x = self.x

        # Проверка боковых коллизий с платформами
        if not self.on_ground:  # Проверяем только если в воздухе
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # Движение вправо
                    if dx > 0 and old_x + self.width <= platform.rect.left:
                        self.rect.right = platform.rect.left
                        self.x = self.rect.x
                    # Движение влево
                    elif dx < 0 and old_x >= platform.rect.right:
                        self.rect.left = platform.rect.right
                        self.x = self.rect.x

    def jump(self):
        if self.on_ground and not self.jumping:
            self.velocity_y = JUMP_FORCE
            self.jumping = True
            self.on_ground = False

    def apply_gravity(self, platforms):
        # Применяем гравитацию
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        self.rect.y = self.y

        # Сбрасываем флаг нахождения на земле
        self.on_ground = False

        # Проверяем коллизии с платформами
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Если падаем вниз и нижняя часть игрока выше нижней части платформы
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + self.velocity_y + 5:
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.velocity_y = 0
                    self.jumping = False
                    self.on_ground = True
                # Если движемся вверх и ударяемся головой
                elif self.velocity_y < 0 and self.rect.top >= platform.rect.bottom + self.velocity_y - 5:
                    self.rect.top = platform.rect.bottom
                    self.y = self.rect.y
                    self.velocity_y = 0

        # Проверка столкновения с полом
        if self.rect.bottom > HEIGHT - FLOOR_HEIGHT:
            self.rect.bottom = HEIGHT - FLOOR_HEIGHT
            self.y = self.rect.y
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

    def draw(self, screen):
        # Рисуем спрайт или прямоугольник, если спрайт не загружен
        if self.sprite:
            # Выбираем направленный спрайт
            current_sprite = self.sprite if self.direction > 0 else self.flipped_sprite
            screen.blit(current_sprite, (self.x, self.y))
        else:
            color = YELLOW if self.player_id == "player_1" else RED
            pygame.draw.rect(screen, color, self.rect)

        # Отрисовка здоровья
        health_text = health_font.render(f"HP: {self.health}", True, WHITE)
        screen.blit(health_text, (self.x, self.y - 20))

        # Отрисовка пуль
        for bullet in self.bullets:
            bullet.draw(screen, self.player_id)