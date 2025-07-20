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

    def set_Offset(self, offset):
        self.CURRENT_OFFSET_X = offset[0]
        self.CURRENT_OFFSET_Y = offset[1]
        self.CURRENT_OFFSET = offset

    def set_zoom(self, zoom):
        self.zoom = zoom

    def renderPlanets(self, screen, pixelArray):
        for x in pixelArray:
            world_pos = pygame.Vector2(x.getPosition())
            screen_pos = (world_pos + pygame.Vector2(self.CURRENT_OFFSET)) * self.zoom + self.center
            scaled_radius = max(1, int(x.radius * self.zoom))
            pygame.draw.circle(screen, x.color, screen_pos, scaled_radius)

    def renderQuadtree(self, screen, lineHistory, tree):
        self.encapsulate_quadtree(screen, tree)
        for line_set in lineHistory:
            for i in range(0, len(line_set), 2):
                start = pygame.Vector2(line_set[i])
                end = pygame.Vector2(line_set[i + 1])
                line_start = (start * self.zoom) + pygame.Vector2(self.CURRENT_OFFSET) + self.center
                line_end = (end * self.zoom) + pygame.Vector2(self.CURRENT_OFFSET) + self.center
                pygame.draw.line(screen, (255, 255, 255), line_start, line_end, 1)


    def encapsulate_quadtree(self, screen, tree):
        top_left = self.tuple_world_to_screen((tree.x, tree.y))
        top_right = self.tuple_world_to_screen((tree.w, tree.y))
        bottom_left = self.tuple_world_to_screen((tree.x, tree.h))
        bottom_right = self.tuple_world_to_screen((tree.w, tree.h))

        pygame.draw.line(screen, (255, 255, 255), top_left, top_right, 1)
        pygame.draw.line(screen, (255, 255, 255), top_right, bottom_right, 1)
        pygame.draw.line(screen, (255, 255, 255), bottom_right, bottom_left, 1)
        pygame.draw.line(screen, (255, 255, 255), bottom_left, top_left, 1)


        #line_start = (tree.x, tree.y * self.zoom) + pygame.Vector2(self.CURRENT_OFFSET) + self.center
        #line_end = (tree.w, tree.y * self.zoom) + pygame.Vector2(self.CURRENT_OFFSET) + self.center
        #pygame.draw.line(screen, (255, 255, 255), line_start, line_end, 1)


    def renderSquare(self, screen, node, targeted):
        if(targeted):
            color = pygame.Color(255, 0, 255)
        else:
            color = pygame.Color(0, 255, 0)
        pygame.draw.line(screen, color, self.tuple_world_to_screen((node.x, node.y)), self.tuple_world_to_screen((node.w, node.h)))
        pygame.draw.line(screen, color, self.tuple_world_to_screen((node.w, node.y)), self.tuple_world_to_screen((node.x, node.h)))

    def render_text(self, screen, position, text):
        my_font = pygame.font.SysFont("Gill Sans", 20)
        text_surface = my_font.render(text, True, pygame.Color("White"))
        screen.blit(text_surface, position)

    def highlight_planet(self, screen, planet):
        pygame.draw.circle(screen, planet.color, self.tuple_world_to_screen(planet.position), self.scale_radius(50))


    def scale_radius(self,radius):
        scaled_radius = max(1, int(radius * self.zoom))
        return scaled_radius


    def tuple_world_to_screen(self, grouped_tuple):
        return pygame.Vector2(pygame.Vector2(grouped_tuple) * self.zoom) + self.CURRENT_OFFSET + self.center

    def tuple_screen_to_world(self, grouped_tuple):
        return (pygame.Vector2(grouped_tuple) - self.center - self.CURRENT_OFFSET)/self.zoom

    def scale_world(self, screen, zoom):
        scaled_world = pygame.transform.smoothscale(
            screen,
            (int(screen.get_width() * zoom), int(screen.get_height() * zoom))
        )
        screen.fill((0, 0, 0))
        # Center the scaled world in the screen
        world_rect = scaled_world.get_rect(center=screen.get_rect().center)

        return screen.blit(scaled_world, world_rect)
