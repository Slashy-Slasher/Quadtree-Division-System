import pygame


def renderPlanets(screen, pixelArray, radius):
    for x in pixelArray:
        pygame.draw.circle(screen, (255,0,0),x.getPosition(), radius)