import pygame
import random

class Render:
    def __init__(self, name):
        CURRENT_OFFSET_X = 0
        CURRENT_OFFSET_Y = 0


    #def renderPlanets(self, screen, pixelArray, radius, CURRENT_OFFSET, zoom):
    #    for x in pixelArray:
    #        pygame.draw.circle(screen, x.color, pygame.Vector2(x.getPosition())+pygame.Vector2(CURRENT_OFFSET[0], CURRENT_OFFSET[1]), x.radius)

    def renderPlanets(self, screen, pixelArray, CURRENT_OFFSET, zoom):
        center = pygame.Vector2(screen.get_width() // 2, screen.get_height() // 2)
        for x in pixelArray:
            world_pos = pygame.Vector2(x.getPosition())
            screen_pos = (world_pos + pygame.Vector2(CURRENT_OFFSET)) * zoom + center
            scaled_radius = max(1, int(x.radius * zoom))
            pygame.draw.circle(screen, x.color, screen_pos, scaled_radius)

    def renderQuadtree(self, screen, lineHistory, CURRENT_OFFSET, zoom):
        center = pygame.Vector2(screen.get_width() // 2, screen.get_height() // 2)
        for line in lineHistory:
            if len(line) == 2:
                start = pygame.Vector2(line[0])
                end = pygame.Vector2(line[1])
                screen_start = (start + pygame.Vector2(CURRENT_OFFSET)) * zoom + center
                screen_end = (end + pygame.Vector2(CURRENT_OFFSET)) * zoom + center
                pygame.draw.line(screen, (0, 0, 0), screen_start, screen_end, 1)

    #def draw_history(self, screen, pixelArray, CURRENT_OFFSET, zoom):
    #    for x in pixelArray:
    #        position_history = list(x.getPositionHistory())
    #        position_history.reverse()
    #        if (len(x.getPositionHistory()) > 2):
    #            for i in range(1, len(position_history)):
    #                pygame.draw.line(screen, (255, 255, 255), position_history[i], position_history[2], 1)

    def scale_world(self, screen, zoom):
        scaled_world = pygame.transform.smoothscale(
            screen,
            (int(screen.get_width() * zoom), int(screen.get_height() * zoom))
        )
        screen.fill((0, 0, 0))
        # Center the scaled world in the screen
        world_rect = scaled_world.get_rect(center=screen.get_rect().center)

        return screen.blit(scaled_world, world_rect)
