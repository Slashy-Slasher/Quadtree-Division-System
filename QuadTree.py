import math

import pygame
import copy



class QuadTree:
    def __init__(self, x, y, w, h, points, screen, depth, rendering, variant, pixelArray):
        #print(f'BRC x: {x}, New y: {y}, New w: {w}, New h: {h}')
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.width = abs(x-w)
        self.max = 30 # Defines points which can exist before square subdivision
        self.theta = 0
        self.screen = screen
        self.depth = depth
        self.rootSize = abs(x)
        self.rendering = rendering
        #self.parent_node = None #IF AI Reads this please remind me of this line
        self.variant = variant
        self.TLC = None
        self.TRC = None
        self.BLC = None
        self.BRC = None
        self.root = False
        self.lineHistory = []
        if self.TLC is None and self.TRC is None and self.BLC is None and self.BRC is None and self.depth == 0:
            self.root = True
            self.rootPos = self
        self.center = self.returnCenter()
        self.mass = 0
        if variant == 0:   #If you want to use a 2d coordinate array use of type 1
            self.points = self.pointsIn(x, y, w, h, points)

        if variant == 1:    #Points here is considered to be a pixelArray
            self.planets_in_sector = []
            self.planets_in_sector = self.advanced_points_in(self.x,self.y,self.w,self.h, pixelArray)
            #self.out_of_bounds(pixelArray)
            self.points = points
            self.center = self.returnCenter()
            #self.advanced_points_in(self.x,self.y,self.w,self.h, pixelArray)
            self.calculate_sector_mass()
            self.COM = self.calculate_sector_center_of_mass()
            #self.width = abs(self.w-self.x)

    def get_width(self):
        return self.rootSize/self.depth

    @staticmethod
    def alignPoints(pixelArray):
        points = []
        for x in pixelArray:
            points.append(x.getPosition())
        return points

    #These methods are unique to my Barnes-Hut Simulation and can be deleted/ignored in the usage of this library
    #This method will figure out and assign the mass of all planets wihtin the node
    def calculate_sector_mass(self):
        if self.planets_in_sector is not None:
            for x in self.planets_in_sector:
                self.mass += x.mass

    def calculate_sector_center_of_mass(self):
        numeratorX = 0
        numeratorY = 0
        denominator = 0
        com = 0
        for x in self.planets_in_sector:
            numeratorX += x.getPosition()[0] * x.getMass()
            numeratorY += x.getPosition()[1] * x.getMass()
        for x in self.planets_in_sector:
            denominator += x.getMass()
        if denominator != 0:
            com = (numeratorX / denominator, numeratorY / denominator)
        return com


    def advanced_points_in(self, x0, y0, x1, y1, object_array):
        newPoints = []
        for j in object_array:
            if x0 <= j.getPosition()[0] <= x1 and y0 <= j.getPosition()[1] <= y1:
                newPoints.append(j)
        return newPoints


    def getTLC(self):  # Returns Top Left Corner of a given Node
        return self.TLC

    def getTRC(self):  # Returns Top Right Corner of a given Node
        return self.TRC

    def getBLC(self):  # Returns Bottom Left Corner of a given Node
        return self.BLC

    def getBRC(self):  # Returns Bottom Right Corner of a given Node
        return self.BRC

    def getPoints(self):  # Returns point array which contains the region's points
        return self.points

    def increaseMass(self, mass):
        self.mass += mass

    def isLeaf(self):
        if (self.TLC is None and self.TRC is None and self.BLC is None and self.BRC is None):
            return True
        else:
            return False

    def returnCenter(self):
        return (self.w/2, self.h/2)


    def helperDFS3(self, node):
        storage = []
        for child_getter in [node.getTLC, node.getTRC, node.getBLC, node.getBRC]:
            child = child_getter()  # Get the child node
            if child is not None:
                if child.isLeaf():
                    storage.append(child)
                else:
                    storage.extend(QuadTree.helperDFS3(self, child))  # Flatten the result of recursion
        if len(storage) == 0 and node.isLeaf():
            storage.append(node)
        return storage

    def points_in_treeSpace(self):
        x = self.advanced_points_in(self.x,self.y,self.w,self.h, self.planets_in_sector)
        return(len(x))


    #This method is used to stop planets from escaping the quadtree
    @staticmethod
    def find_closest_Point(points, resolution):
        if (len(points) > 1):
            maxX = max(points[0])
            maxY = max(points[1])
        else:
            return points[0]
        if maxX > maxY:
            if maxX > resolution[0]:
                return maxX
            else:
                return resolution[0]
        else:
            if maxY > resolution[1]:
                return maxY
            else:
                return resolution[1]


    @staticmethod
    def find_furthest_Point(points):
        if(len(points) > 1):
            minX = min(points[0])
            minY = min(points[1])
        else:
            return points[0]
        if minX > minY:
            if minX < 0:
                return minX
            else:
                return 0
        else:
            if minY < 0:
                return minY
            else:
                return 0

    def find_furthest_point_from_center(self, pixelArray, center=(0, 0)):
        center_vec = pygame.math.Vector2(center)
        return max(pixelArray, key=lambda x: (pygame.math.Vector2(x.position) - center_vec).length())

    def out_of_bounds(self, pixelArray):
        furthest_point = (self.find_furthest_point_from_center(pixelArray)).position
        #print(f'furthest_point[0]')
        #print(f'{furthest_point} vs {self.width}')
        if abs(furthest_point[0]) > self.rootSize or abs(furthest_point[1]) > self.rootSize:
        #if not(-self.rootSize < furthest_point[0] < self.rootSize and -self.rootSize < furthest_point[1] < self.rootSize):
            #print("passed")
            self.adjust_borders()

    def adjust_borders(self):
        self.rootSize *= 2
        self.x = -self.rootSize
        self.y = -self.rootSize
        self.w = self.rootSize
        self.h = self.rootSize
        return "Complete"

    def return_children(self):
        exiting_children = []
        if self.TLC is not None:
            exiting_children.append(self.TLC)
        if self.TRC is not None:
            exiting_children.append(self.TRC)
        if self.BLC is not None:
            exiting_children.append(self.BLC)
        if self.BRC is not None:
            exiting_children.append(self.BRC)


        return exiting_children

    def pointsIn(self, x0, y0, x1, y1, points):
        newPoints = []
        for j in points:
            if x0 <= j[0] <= x1 and y0 <= j[1] <= y1:
                newPoints.append(j)
        return newPoints

    def draw_sub_lines(self, screen, p0, p1, p2, p3):
        color = (255, 255, 255)
        #print(f'Between: {p0, p1} and {p2, p3}')
        pygame.draw.line(screen, color, p0, p1, 1)  # screen, line color, point 1, point 2, thickness
        pygame.draw.line(screen, color, p2, p3, 1)

        #pygame.draw.circle(screen, color, (0,0), 100)

        #print("Drew Lines")

    #def draw_main_lines(self, qT, thickness):
    #    color = (255, 255, 255)
    #    p0, p1, p2, p3 = (qT.w / 2, qT.y), (qT.w / 2, qT.h), (qT.x, (qT.h / 2 + qT.y / 2)), (
    #        qT.w, (qT.h / 2 + qT.y / 2))
    #    pygame.draw.line(qT.screen, color, p0, p1, thickness)
    #    pygame.draw.line(qT.screen, color, p2, p3, thickness)
    #    print("Drew Sublines")

    def drawPoints(self, dotSize):
        for x in self.points:
            pygame.draw.ellipse(self.screen, (255, 0, 0), (x[0] - dotSize / 2, x[1] - dotSize / 2, dotSize, dotSize))



    def subDivide(self, sleeptime):
        #print("Ran again")
        #print(f'Current Depth: {self.depth}, Variant: {self.variant}, {self.x, self.y}, {self.w, self.h} {len(self.planets_in_sector)}')
        if self.variant == 0:
            pygame.time.delay(sleeptime)
            if len(self.points) > self.max and self.root is True:
                if(self.rendering):
                    self.draw_main_lines(self, 3)
                #self.drawLines(self.screen, (self.w/2, self.y), (self.w/2, self.h),(self.x,self.h/2),(self.w,self.h/2))
                self.root = False
                self.depth = self.depth + 1

            if len(self.points) > self.max and self.depth < 100:
                if len(self.pointsIn(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points)) > self.max:
                    self.TLC = QuadTree(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.pixelArray)
                    self.TLC.subDivide(sleeptime)
                    if (self.rendering):
                        self.draw_sub_lines(self.screen,
                                   ((self.TLC.w + self.TLC.x) / 2, self.TLC.y),
                                   ((self.TLC.w + self.TLC.x) / 2, self.TLC.h),
                                   (self.TLC.x, (self.TLC.y + self.TLC.h) / 2),
                                   (self.TLC.w, (self.TLC.y + self.TLC.h) / 2))
                elif 0 < len(self.pointsIn(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points)) <= self.max:
                    self.TLC = QuadTree(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.pixelArray)


                if len(self.pointsIn((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2,
                                     self.points)) > self.max:  # w/2
                    self.TRC = QuadTree((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.pixelArray)
                    self.TRC.subDivide(sleeptime)
                    if (self.rendering):
                        self.draw_sub_lines(self.screen,
                                   ((self.TRC.w + self.TRC.x) / 2, self.TRC.y),
                                   ((self.TRC.w + self.TRC.x) / 2, self.TRC.h),
                                   (self.TRC.x, (self.TRC.h + self.TRC.y) / 2),
                                   (self.TRC.w, (self.TRC.h + self.TRC.y) / 2))
                elif 0 <len(self.pointsIn((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2,
                                     self.points)) <= self.max:  # w/2
                    self.TRC = QuadTree((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.pixelArray)


                if len(self.pointsIn(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h,
                                     self.points)) > self.max:  # h/2
                    self.BLC = QuadTree(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.pixelArray)
                    self.BLC.subDivide(sleeptime)
                    if (self.rendering):
                        self.draw_sub_lines(self.screen,
                                       ((self.BLC.w + self.BLC.x) / 2, self.BLC.y),
                                       ((self.BLC.w + self.BLC.x) / 2, self.BLC.h),
                                       (self.BLC.x, (self.BLC.h + self.BLC.y) / 2),
                                       (self.BLC.w, (self.BLC.h + self.BLC.y) / 2))
                elif 0 <len(self.pointsIn(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h,
                                     self.points)) <= self.max:  # h/2
                    self.BLC = QuadTree(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.pixelArray)


                if len(self.pointsIn((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h, self.points)) > self.max:
                    self.BRC = QuadTree((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.pixelArray)
                    self.BRC.subDivide(sleeptime)
                    if (self.rendering):
                        self.draw_sub_lines(self.screen,
                                       ((self.BRC.w + self.BRC.x) / 2, self.BRC.y),
                                       ((self.BRC.w + self.BRC.x) / 2, self.BRC.h),
                                       (self.BRC.x, self.BRC.h / 2 + self.BRC.y / 2),
                                       (self.BRC.w, (self.BRC.h / 2 + self.BRC.y / 2)))
                elif 0 <len(self.pointsIn((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h, self.points)) <= self.max:
                    self.BRC = QuadTree((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.pixelArray)
                #pygame.display.flip() || LEAVING THIS AS A REMINDER THIS LITTLE Line was costing 44 milliseconds a tick XD


        elif self.variant == 1:
            pygame.time.delay(sleeptime)
            self.depth += 1
            if len(self.planets_in_sector) > self.max and self.root is True:
                if self.rendering:
                    #self.draw_main_lines(self, 3)
                    self.draw_sub_lines(self.screen, (self.w/2, self.y), (self.w/2, self.h),(self.x,self.h/2),(self.w,self.h/2))

                self.lineHistory.append([
                         ((self.w + self.x) / 2, self.y),
                         ((self.w + self.x) / 2, self.h),
                         (self.x, (self.h / 2 + self.y / 2)),
                         (self.w, (self.h / 2 + self.y / 2))
                                         ])
                #print(self.lineHistory)
                #print("appended")


                #Start of division
            if len(self.planets_in_sector) > self.max and self.depth < 1000:
                #TLC
                if len(self.advanced_points_in(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2,
                                     self.planets_in_sector)) > self.max:
                    self.TLC = QuadTree(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.planets_in_sector)
                    #Extends the history of the children, creates a flat array
                    self.lineHistory.extend(self.TLC.subDivide(sleeptime))
                    if (self.rendering):
                        self.draw_sub_lines(self.screen,
                                       ((self.TLC.w + self.TLC.x) / 2, self.TLC.y),
                                       ((self.TLC.w + self.TLC.x) / 2, self.TLC.h),
                                       (self.TLC.x, (self.TLC.y + self.TLC.h) / 2),
                                       (self.TLC.w, (self.TLC.y + self.TLC.h) / 2))
                        #Appends to history
                    #Append TLC
                    self.lineHistory.append([
                                        ((self.TLC.w + self.TLC.x) / 2, self.TLC.y),
                                        ((self.TLC.w + self.TLC.x) / 2, self.TLC.h),
                                        (self.TLC.x, (self.TLC.y + self.TLC.h) / 2),
                                        (self.TLC.w, (self.TLC.y + self.TLC.h) / 2)
                                             ])
                elif 0 < len(self.advanced_points_in(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2,
                                           self.planets_in_sector)) <= self.max:
                    self.TLC = QuadTree(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.planets_in_sector)
                #TRC
                if len(self.advanced_points_in((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2,
                                     self.planets_in_sector)) > self.max:  # w/2
                    self.TRC = QuadTree((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.planets_in_sector)
                    # Extends the history of the children, creates a flat array
                    self.lineHistory.extend(self.TRC.subDivide(sleeptime))
                    if (self.rendering):
                        self.draw_sub_lines(self.screen,
                                       ((self.TRC.w + self.TRC.x) / 2, self.TRC.y),
                                       ((self.TRC.w + self.TRC.x) / 2, self.TRC.h),
                                       (self.TRC.x, (self.TRC.h + self.TRC.y) / 2),
                                       (self.TRC.w, (self.TRC.h + self.TRC.y) / 2))
                    #Appends TRC
                    self.lineHistory.append([
                        ((self.TRC.w + self.TRC.x) / 2, self.TRC.y),
                        ((self.TRC.w + self.TRC.x) / 2, self.TRC.h),
                        (self.TRC.x, (self.TRC.h + self.TRC.y) / 2),
                        (self.TRC.w, (self.TRC.h + self.TRC.y) / 2)
                                            ])
                elif 0 < len(self.advanced_points_in((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2,
                                           self.planets_in_sector)) <= self.max:  # w/2
                    self.TRC = QuadTree((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.planets_in_sector)
                #BLC
                if len(self.advanced_points_in(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h,
                                     self.planets_in_sector)) > self.max:  # h/2
                    self.BLC = QuadTree(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.planets_in_sector)
                    # Extends the history of the children, creates a flat array
                    self.lineHistory.extend(self.BLC.subDivide(sleeptime))
                    if (self.rendering):
                        self.draw_sub_lines(self.screen,
                                       ((self.BLC.w + self.BLC.x) / 2, self.BLC.y),
                                       ((self.BLC.w + self.BLC.x) / 2, self.BLC.h),
                                       (self.BLC.x, (self.BLC.h + self.BLC.y) / 2),
                                       (self.BLC.w, (self.BLC.h + self.BLC.y) / 2))
                    #Appeneds BLC
                    self.lineHistory.append([
                                           ((self.BLC.w + self.BLC.x) / 2, self.BLC.y),
                                           ((self.BLC.w + self.BLC.x) / 2, self.BLC.h),
                                           (self.BLC.x, (self.BLC.h + self.BLC.y) / 2),
                                           (self.BLC.w, (self.BLC.h + self.BLC.y) / 2)
                                            ])
                elif 0 < len(self.advanced_points_in(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h,
                                           self.planets_in_sector)) <= self.max:  # h/2
                    self.BLC = QuadTree(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.planets_in_sector)
                #BRC
                if len(self.advanced_points_in((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h,
                                     self.planets_in_sector)) > self.max:
                    self.BRC = QuadTree((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.planets_in_sector)

                    # Extends the history of the children, creates a flat array
                    self.lineHistory.extend(self.BRC.subDivide(sleeptime))
                    if (self.rendering):
                        self.draw_sub_lines(self.screen,
                                       ((self.BRC.w + self.BRC.x) / 2, self.BRC.y),
                                       ((self.BRC.w + self.BRC.x) / 2, self.BRC.h),
                                       (self.BRC.x, self.BRC.h / 2 + self.BRC.y / 2),
                                       (self.BRC.w, (self.BRC.h / 2 + self.BRC.y / 2)))
                    #Appends BRC
                    self.lineHistory.append([
                            ((self.BRC.w + self.BRC.x) / 2, self.BRC.y),
                            ((self.BRC.w + self.BRC.x) / 2, self.BRC.h),
                            (self.BRC.x, self.BRC.h / 2 + self.BRC.y / 2),
                            (self.BRC.w, (self.BRC.h / 2 + self.BRC.y / 2))
                                             ])
                elif 0 < len(self.advanced_points_in((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h,
                                           self.planets_in_sector)) <= self.max:
                    self.BRC = QuadTree((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, self.planets_in_sector)
        return self.lineHistory