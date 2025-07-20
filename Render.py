import pygame
import random

class Render:
    def __init__(self, name, center, offset, zoom_level):
        self.CURRENT_OFFSET_X = offset[0]
        self.CURRENT_OFFSET_Y = offset[1]
        self.CURRENT_OFFSET = pygame.Vector2(self.CURRENT_OFFSET_X, self.CURRENT_OFFSET_Y)
        self.center = pygame.Vector2(center)
        self.zoom = zoom_level


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
        #print(f'Line History Length: {len(lineHistory)}')
        #print(f'Line History: {lineHistory}')
        for line_set in lineHistory:
            for i in range(0, len(line_set), 2):
                start = pygame.Vector2(line_set[i])
                end = pygame.Vector2(line_set[i + 1])
                line_start = (start * zoom) + pygame.Vector2(CURRENT_OFFSET) + center
                line_end = (end * zoom) + pygame.Vector2(CURRENT_OFFSET) + center
                pygame.draw.line(screen, (255, 255, 255), line_start, line_end, 1)

    def renderSquare(self, screen, node, targeted):
        if(targeted):
            color = pygame.Color(255, 0, 255)
        else:
            color = pygame.Color(0, 255, 0)
        pygame.draw.line(screen, color, self.tuple_world_to_screen((node.x, node.y)), self.tuple_world_to_screen((node.w, node.h)))
        pygame.draw.line(screen, color, self.tuple_world_to_screen((node.x, node.h)), self.tuple_world_to_screen((node.w, node.y)))


    def highlight_planet(self, screen, planet):
        pygame.draw.circle(screen, planet.color, self.tuple_world_to_screen(planet.position), self.scale_radius(50))


    def scale_radius(self,radius):
        scaled_radius = max(1, int(radius * self.zoom))
        return scaled_radius


    def tuple_world_to_screen(self, grouped_tuple):
        return pygame.Vector2(pygame.Vector2(grouped_tuple) * self.zoom) + self.CURRENT_OFFSET + self.center

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
