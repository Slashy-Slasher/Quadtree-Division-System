import math
import random

import pygame


class pixel:
    def __init__(self, mass, position, direction, force):
        self.mass = mass  # Mass
        self.position = position  # (x,y) Tuple
        self.direction = pygame.Vector2(direction)  # (x,y) Vector2
        self.force = force  # float value
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def getPosition(self):
        return tuple(self.position)

    def getMass(self):
        return self.mass

    def vector_set(self, direction, force):
            self.direction = direction
            self.force = force


    def applyForce(self):
        self.position = self.force * pygame.Vector2(self.direction)

    def getDirection(self, p0, p1):
        p0, p1 = pygame.Vector2(p0[0], p0[1]), pygame.Vector2(p1[0], p1[1])
        distance = p0.distance_to(p1)
        p2 = pygame.Vector2(p1[0] - p0[0], p1[1] - p0[0])
        if(math.dist(p0, p1) == 0):
            return pygame.Vector2(0, 0)
        return p0.normalize()

    #def getDirection(self, p1): #Overloaded method which finds the direction relative to the referenced planet
    #    p0, p1 = pygame.Vector2(self.position[0], self.position[1]), pygame.Vector2(p1[0], p1[1])
    #    distance = p0.distance_to(p1)
    #    p2 = pygame.Vector2(p1[0] - p0[0], p1[1] - p0[0])
    #    print(p2.normalize())
    #    return p0

    def return_list_mass(pixel_array):
        temp_mass = 0
        for x in pixel_array:
            temp_mass += x.getMass()
        return temp_mass

    def gravity(self, g, obj0, obj1):
        self.direction = self.getDirection(obj0.position, obj1.position)
        print(f'obj0 position: {obj0.position}, obj1 position: {obj1.position}')
        self.force += (g * obj0.mass * obj1.mass) / (math.dist(obj0.position, obj1.position) ** 2)

        return (g * obj0.mass * obj1.mass) / (math.dist(obj0.position, obj1.position) ** 2)
