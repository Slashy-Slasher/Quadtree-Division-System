import pygame
import random

def renderPlanets(screen, pixelArray, radius):
    for x in pixelArray:
        pygame.draw.circle(screen, x.color, x.getPosition(), radius * (x.mass ** (1/5)))