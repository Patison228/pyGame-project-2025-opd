import pygame
from settings import WIDTH, HEIGHT

def load_image(path):
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except:
        print(f"Download image error: {path}")
        return None

def load_background(path):
    image = pygame.image.load(path).convert()
    return pygame.transform.scale(image, (WIDTH, HEIGHT))