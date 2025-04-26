'''
import pygame
pygame.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
size = (300, 300)
screen = pygame.display.set_mode(size)

#Параметры квадрата
square_size=int(input("Введите размер вашего квадратика (желательно не огромное значение): "))
square_x,square_y = 0,0
square_color = red
dragging = False
offset_x,offset_y = 0,0

while True:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN: #Кнопка опущена
            if event.button == 1: #Левая кнопка мыши
                mouse_x,mouse_y= pygame.mouse.get_pos() #Получаю координаты где нажал
                #Проверяем не попадает ли курсор за квадрат
                if (square_x <= mouse_x <=square_x + square_size and
                square_y <= square_y <=square_y + square_size):
                    dragging = True
                    offset_x = square_x - mouse_x
                    offset_y = square_y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP: #Отжал
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION: #Движение мыши
            if dragging:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                #Обновляем координаты с учётом смещения
                square_x = mouse_x + offset_x
                square_y = mouse_y + offset_y
                #Ограничиваем пермещение в пределах экрана
                square_x = max(0,min(square_x,size[0]-square_size))
                square_y = max(0,min(square_y,size[1]-square_size))
    pygame.draw.rect(screen,square_color, (square_x,square_y, square_size,square_size))
    pygame.display.update()
'''
from itertools import filterfalse

import pygame
import time
import random
PLAYER_VEL = 1
WIDTH,HEIGHT = 1000,800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Dodge")
BG = pygame.transform.scale(pygame.image.load("photos/images.jpg"), (WIDTH,HEIGHT))

def draw(player):
    WIN.blit(BG, (0,0))
    pygame.draw.rect(WIN, (255,255,0), player )
    pygame.display.update()
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.x -= PLAYER_VEL
        if keys[pygame.K_d]:
            player.x += PLAYER_VEL
        if keys[pygame.K_w]:
            player.y -= PLAYER_VEL
        if keys[pygame.K_s]:
            player.y += PLAYER_VEL
        if keys[pygame.K_ESCAPE]:
            run = False
            break

        draw(player)
    pygame.quit()

if __name__ == "__main__":
    main()

