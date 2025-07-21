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

    def getVelocity(self):
        return self.gForce

    def getPositionHistory(self):
        return self.position_history

    def getVelocityHistory(self):
        return self.velocity_history

    def vector_set(self, direction, force):
            self.direction = direction
            self.force = force
            self.gForce = self.direction * self.force

    def applyForce(self, dt):
        #self.position = self.force * pygame.Vector2(self.direction)
        if not self.getlockedState():
            self.position += self.gForce * dt
            self.position_history.append(self.position)
            self.velocity_history.append(self.gForce)
            if len(self.position_history) > 100:
                del self.position_history[0]

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
            if(math.dist(obj0.position, obj1.position) > (obj0.radius + obj1.radius)): #While collision is disabled, remove later
                self.force = (g * obj0.mass * obj1.mass) / (math.dist(obj0.position, obj1.position) ** 2) #Force
        self.gForce += (self.direction * self.force)  #Vector Created

    def form_satellite(self, grav_constant, h, direction):   #forms a satellite around "self", r is desired distance
        needed_velocity = math.sqrt((grav_constant * self.getMass())/(self.radius+h+15))
        vec0 = pygame.Vector2(self.getPosition())
        #vec1 = pygame.Vector2(self.getPosition())+pygame.Vector2(random.randint(-r, r), random.randint(-r, r))
        vec1 = pygame.Vector2(self.getPosition()[0]+(self.radius+h+30), self.getPosition()[1])
        direction_to_com = pygame.Vector2(vec0 - vec1).normalize()
        new_position = direction_to_com*(self.radius+h+30)
        new_direction = pygame.Vector2(direction_to_com[1]*-1*direction, direction_to_com[0]*direction)

        return pixel(30, vec1, new_direction, needed_velocity*30, (0, random.randint(0, 150), random.randint(150, 255)), 15, False)
