import pygame
import random

class Render:
    def __init__(self, name):
        CURRENT_OFFSET_X = 0
        CURRENT_OFFSET_Y = 0


    def renderPlanets(self, screen, pixelArray, radius, CURRENT_OFFSET):
        for x in pixelArray:
            pygame.draw.circle(screen, x.color, pygame.Vector2(x.getPosition())+pygame.Vector2(CURRENT_OFFSET[0], CURRENT_OFFSET[1]), x.radius)

    def draw_history(self, screen, pixelArray, CURRENT_OFFSET):
        for x in pixelArray:
            position_history = list(x.getPositionHistory())
            position_history.reverse()
            if (len(x.getPositionHistory()) > 2):
                for i in range(1, len(position_history)):
                    pygame.draw.line(screen, (255, 255, 255), position_history[i], position_history[2], 1)
