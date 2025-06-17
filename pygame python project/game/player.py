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

    def load_sprites(self):
        try:
            self.sprite = load_image(PLAYER_SPRITES[self.player_id])
            self.shield_sprite = load_image("pygame python project/image/shield.png")
            self.icon_damage_boost_sprite = load_image("pygame python project/image/icon_damage_boost.png")

            if self.shield_sprite:
                self.shield_sprite = pygame.transform.scale(self.shield_sprite, (self.rect.width + 8, self.rect.height + 8))

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
        
        # Ограничение по горизонтали (чтобы не выходил за границы экрана)
        self.x = max(0, min(self.x, WIDTH - self.rect.width))  # Не левее 0 и не правее WIDTH
        self.rect.x = self.x

        # Проверка боковых коллизий с платформами (только в воздухе)
        if not self.on_ground:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # Движение вправо
                    if dx > 0 and old_x + self.rect.width <= platform.rect.left:
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

    def apply_gravity(self, platforms, map_type):
        # Всегда применяем гравитацию
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
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

        # Рисуем спрайт или прямоугольник, если спрайт не загружен
        if self.sprite:
            # Выбираем направленный спрайт
            current_sprite = self.sprite if self.direction > 0 else self.flipped_sprite
            screen.blit(current_sprite, (self.x, self.y))
        else:
            color = YELLOW if self.player_id == "player_1" else RED
            pygame.draw.rect(screen, color, self.rect)

        #отрисовка хпбара
        self.draw_health_bar(screen)
        
        #отрисовка иконки увеличения урона
        if (self.damage_boost):
            self.draw_boost_damage_icon(screen)

        # Отрисовка пуль
        for bullet in self.bullets:
            bullet.draw(screen, self.player_id)