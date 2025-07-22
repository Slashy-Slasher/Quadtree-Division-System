import math
import random
from collections import deque

import pygame
from numba import njit


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
        self.slated_for_removal = False

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
        #print(f'Entered Method with: {self.force} force')
        if not self.getlockedState():
            #print(f'Applied force: {self.force}')
            self.position += self.gForce * dt
            #self.position_history.append(self.position)
            #self.velocity_history.append(self.gForce)
            #self.position_history = deque(maxlen=100)



        #self.gForce = pygame.Vector2(0,0)

    def getDirection(self, p0, p1):
        p0_vec = pygame.Vector2(p0[0], p0[1])
        p1_vec = pygame.Vector2(p1[0], p1[1])
        direction = p1_vec - p0_vec

        if direction.length() == 0:
            return pygame.Vector2(0, 0)  # No direction if points are the same

        return direction.normalize()

    def get_distance_and_direction(self, p0, p1):
        vec = pygame.Vector2(p1) - pygame.Vector2(p0)
        distance  = vec.length_squared()
        #print(f'Distance: {distance}')
        if(distance > 0):
            direction = vec/distance
        else:
            direction = pygame.Vector2(0, 0)

        #print(f'Distance: {distance}, Direction: {direction}')
        return distance, direction



    @staticmethod
    def return_list_mass(pixel_array):
        temp_mass = 0
        for x in pixel_array:
            temp_mass += x.getMass()
        return temp_mass

    def gravity(self, g, obj0, obj1):
        position0 = obj0.getPosition()
        position1 = obj1.getPosition()
        distance, direction = self.get_distance_and_direction(position0, position1)
        #print(distance)
        if distance != 0:
            force = (g * obj0.mass * obj1.mass) / (distance ** 2)  # Force
        else:
            force = 0
        self.gForce += (direction * force)



    @staticmethod
    @njit
    def gravity_with_COM_numba(g, m1, m2, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        dist_squared = dx * dx + dy * dy
        if dist_squared > 0.0:
            inv_dist = 1.0 / dist_squared ** 0.5
            fx = dx * inv_dist
            fy = dy * inv_dist
            force = (g * m1 * m2) / dist_squared
        else:
            fx=  0.0
            fy = 0.0
            force = 0.0
        return fx * force, fy * force


    #Methods designed to calculate force between two planets. Works, but isn't performant because of Python's object
    def gravity_with_COM(self, g, obj0, position1, mass):
        position0 = obj0.position
        (distance, direction) = self.get_distance_and_direction(position0, position1)
        force = (g * obj0.mass * mass) / distance  # Force
        self.gForce += (direction * force)


    def form_galaxy(self, grav_constant, h, direction):
        vec0 = pygame.Vector2(self.getPosition())
        vec1 = pygame.Vector2(self.getPosition()[0] + (self.radius + h + 30), self.getPosition()[1]+ random.randint(-1000,1000))
        direction_to_com = pygame.Vector2(vec0 - vec1).normalize()
        # new_position = direction_to_com*(self.radius+h+30)

        needed_velocity = math.sqrt((grav_constant * self.getMass()) / (self.radius + h))
        new_direction = pygame.Vector2(direction_to_com[1] * -1 * direction, direction_to_com[0] * direction)
        return pixel(30, vec1, new_direction, needed_velocity*2,
                     (0, random.randint(0, 150), random.randint(150, 255)), 15, False)


    def form_satellite(self, grav_constant, h, direction):   #forms a satellite around "self", r is desired distance
        needed_velocity = math.sqrt((grav_constant * self.getMass())/(self.radius+h+15))
        vec0 = pygame.Vector2(self.getPosition())
        vec1 = pygame.Vector2(self.getPosition()[0]+(self.radius+h+30), self.getPosition()[1])
        direction_to_com = pygame.Vector2(vec0 - vec1).normalize()
        #new_position = direction_to_com*(self.radius+h+30)
        new_direction = pygame.Vector2(direction_to_com[1]*-1*direction, direction_to_com[0]*direction)
        return pixel(30, vec1, new_direction, needed_velocity*20, (0, random.randint(0, 150), random.randint(150, 255)), 15, False)
