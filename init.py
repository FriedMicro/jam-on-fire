import pygame
from pygame.locals import *
import os

pygame.init()
pygame.font.init()

size = width, height = 320, 240
screen = pygame.display.set_mode(size)

#Loosely based off: https://github.com/jpritcha3-14/shooting-game/blob/master/shooting_game.py
def render_image(name, x, y):
    filepath = os.path.join('/images', name)
    try:
        image = pygame.image.load(filepath)
    except:
        print('Cannot load', name)
    image = image.convert()
