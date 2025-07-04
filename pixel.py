import math
import random

import pygame


class pixel:
    def __init__(self, mass, position, direction, force):
        self.mass = mass  # Mass
        self.position = position  # (x,y) Tuple
        self.direction = direction  # (x,y) Vector2
        self.force = force  # float value
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def getPosition(self):
        return self.position

    def getMass(self):
        return self.mass

    def applyForce(self):
        self.position += self.force * self.direction

    def getDirection(self, p0, p1):
        p0, p1 = pygame.Vector2(p0[0], p0[1]), pygame.Vector2(p1[0], p1[1])
        distance = p0.distance_to(p1)
        p2 = pygame.Vector2(p1[0] - p0[0], p1[1] - p0[0])
        print(p2.normalize())
        return p0

    def gravity(self, g, obj0, obj1):
        self.direction = self.getDirection(obj0.position, obj1.position)
        return (g * obj0.mass * obj1.mass) / (math.dist(obj0.position, obj1.position) ** 2)
