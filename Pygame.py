
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

