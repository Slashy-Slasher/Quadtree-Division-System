import math
import random

import pygame


class pixel:
    def __init__(self, mass, position, direction, force, color, diameter, isLocked):
        self.mass = mass  # Mass
        self.position = position  # (x,y) Tuple
        self.direction = pygame.Vector2(direction)  # (x,y) Vector2
        self.force = force  # float value
        self.color = color
        self.radius = diameter/2
        self.gForce = pygame.Vector2(0,0)
        self.lockedState = isLocked
        self.position_history = []
        self.velocity_history = []

    def getPosition(self):
        return tuple(self.position)

    def getlockedState(self):
        return self.lockedState

    def getMass(self):
        return self.mass

    def vector_set(self, direction, force):
            self.direction = direction
            self.force = force
            self.gForce = self.direction * self.force

    def applyForce(self):
        #self.position = self.force * pygame.Vector2(self.direction)
        if not self.getlockedState():
            self.position += self.gForce
            self.position_history.append(self.position)
            self.velocity_history.append(self.gForce)

        #self.gForce = pygame.Vector2(0,0)

    def getDirection(self, p0, p1):
        p0_vec = pygame.Vector2(p0[0], p0[1])
        p1_vec = pygame.Vector2(p1[0], p1[1])
        direction = p1_vec - p0_vec

        if direction.length() == 0:
            return pygame.Vector2(0, 0)  # No direction if points are the same

        return direction.normalize()

    @staticmethod
    def return_list_mass(pixel_array):
        temp_mass = 0
        for x in pixel_array:
            temp_mass += x.getMass()
        return temp_mass

    def gravity(self, g, obj0, obj1):
        self.direction = self.getDirection(obj0.position, obj1.position)    #Normalized Direction
        if(obj0.position != obj1.position):
            self.force = (g * obj0.mass * obj1.mass) / (math.dist(obj0.position, obj1.position) ** 2) #Force
        self.gForce += (self.direction * self.force)  #Vector Created


