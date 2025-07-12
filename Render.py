import pygame
import random

CURRENT_OFFSET_X = 0
CURRENT_OFFSET_Y = 0

def renderPlanets(screen, pixelArray, radius, CURRENT_OFFSET):
    for x in pixelArray:
        pygame.draw.circle(screen, x.color, pygame.Vector2(x.getPosition())+pygame.Vector2(CURRENT_OFFSET[0], CURRENT_OFFSET[1]), x.radius)