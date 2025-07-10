import pygame
import random

def renderPlanets(screen, pixelArray, radius):
    for x in pixelArray:
        pygame.draw.circle(screen, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),x.getPosition(), radius)