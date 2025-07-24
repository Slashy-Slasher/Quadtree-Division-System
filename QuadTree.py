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
        self.max = 10 # Defines points which can exist before square subdivision
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
            self.planets_in_sector = self.advanced_points_in(x,y,w,h, pixelArray)
            self.points = points
            self.calculate_sector_mass()
            self.COM = self.calculate_sector_center_of_mass()

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

        for planet in self.planets_in_sector:
            pos = planet.position
            mass = planet.mass
            if(mass == 0):
                print(mass)
            numeratorX += pos[0] * mass
            numeratorY += pos[1] * mass
            denominator += mass

        if denominator != 0:
            return (numeratorX / denominator, numeratorY / denominator)
        else:
            return (0, 0)

    @staticmethod
    def advanced_points_in(x0, y0, x1, y1, object_array):
        #newPoints = []
        #for j in object_array:
        #    position = j.position
        #    if x0 <= position[0] <= x1 and y0 <= position[1] <= y1:
        #        newPoints.append(j)
        #return newPoints
        return [j for j in object_array
                if x0 <= j.position[0] <= x1 and y0 <= j.position[1] <= y1]



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
        return (self.x + self.w) / 2, (self.y + self.h) / 2


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
        if len(points) > 1:
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
        if len(points) > 1:
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
        if abs(furthest_point[0]) > self.rootSize or abs(furthest_point[1]) > self.rootSize:
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
            if x0 <= j[0] < x1 and y0 < j[1] <= y1:
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
                tlc_points = self.pointsIn(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points)
                if len(tlc_points) > self.max:
                    self.TLC = QuadTree(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, tlc_points)
                    self.TLC.subDivide(sleeptime)
                    if (self.rendering):
                        self.draw_sub_lines(self.screen,
                                   ((self.TLC.w + self.TLC.x) / 2, self.TLC.y),
                                   ((self.TLC.w + self.TLC.x) / 2, self.TLC.h),
                                   (self.TLC.x, (self.TLC.y + self.TLC.h) / 2),
                                   (self.TLC.w, (self.TLC.y + self.TLC.h) / 2))
                elif 0 < len(tlc_points) <= self.max:
                    self.TLC = QuadTree(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points,
                                        self.screen, self.depth + 1, self.rendering, self.variant, tlc_points)


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

            screen = self.screen
            x = self.x
            y = self.y
            w = self.w
            h = self.h
            max = self.max

            if len(self.planets_in_sector) > self.max and self.root is True:
                if self.rendering:
                    #self.draw_main_lines(self, 3)
                    self.draw_sub_lines(screen, (w/2, y), (w/2, h),(x, h/2),(w,h/2))

                new_x = x
                new_y = y
                new_w = w
                new_h = h
                self.lineHistory.append([
                         ((new_w + new_x) / 2, new_y),
                         ((new_w + new_x) / 2, new_h),
                         (new_x, (new_h / 2 + new_y / 2)),
                         (new_w, (new_h / 2 + new_y / 2))
                                         ])

                #Start of division
            if len(self.planets_in_sector) > max and self.depth < 10:
                #TLC
                tlc_points = self.advanced_points_in(x, y, (x + w) / 2, (y + h) / 2, self.planets_in_sector)
                if len(tlc_points) > max:
                    self.TLC = QuadTree(x, y, (x + w) / 2, (y + h) / 2, self.points,
                                        screen, self.depth + 1, self.rendering, self.variant, tlc_points)
                    #Extends the history of the children, creates a flat array
                    self.lineHistory.extend(self.TLC.subDivide(sleeptime))
                    new_x = self.TLC.x
                    new_y = self.TLC.y
                    new_w = self.TLC.w
                    new_h = self.TLC.h
                    #Appends the current line history to the array
                    self.lineHistory.append([
                                        ((new_w + new_x) / 2, new_y),
                                        ((new_w + new_x) / 2, new_h),
                                        (new_x, (new_y + new_h) / 2),
                                        (new_w, (new_y + new_h) / 2)
                                             ])
                elif 0 < len(tlc_points) <= max:
                    self.TLC = QuadTree(x, y, (x + w) / 2, (y + h) / 2, self.points,
                                        screen, self.depth + 1, self.rendering, self.variant, tlc_points)


                #TRC
                trc_points = self.advanced_points_in((w + x) / 2, y, w, (y + h) / 2,
                                     self.planets_in_sector)
                if len(trc_points) > max:  # w/2
                    self.TRC = QuadTree((w + x) / 2, y, w, (y + h) / 2, self.points,
                                        screen, self.depth + 1, self.rendering, self.variant, trc_points)
                    # Extends the history of the children, creates a flat array
                    self.lineHistory.extend(self.TRC.subDivide(sleeptime))

                    new_x = self.TRC.x
                    new_y = self.TRC.y
                    new_w = self.TRC.w
                    new_h = self.TRC.h

                    self.lineHistory.append([
                        ((new_w + new_x) / 2, new_y),
                        ((new_w + new_x) / 2, new_h),
                        (new_x, (new_h + new_y) / 2),
                        (new_w, (new_h + new_y) / 2)
                                            ])
                elif 0 < len(trc_points) <= max:  # w/2
                    self.TRC = QuadTree((w + x) / 2, y, w, (y + h) / 2, self.points,
                                        screen, self.depth + 1, self.rendering, self.variant, trc_points)


                #BLC
                blc_points = self.advanced_points_in(x, (y + h) / 2, (x + w) / 2, h,
                                     self.planets_in_sector)
                if len(blc_points) > max:  # h/2
                    self.BLC = QuadTree(x, (y + h) / 2, (x + w) / 2, h, self.points,
                                        screen, self.depth + 1, self.rendering, self.variant, blc_points)
                    # Extends the history of the children, creates a flat array
                    self.lineHistory.extend(self.BLC.subDivide(sleeptime))
                    new_x = self.BLC.x
                    new_y = self.BLC.y
                    new_w = self.BLC.w
                    new_h = self.BLC.h

                    #Appeneds BLC
                    self.lineHistory.append([
                                           ((new_w + new_x) / 2, new_y),
                                           ((new_w + new_x) / 2, new_h),
                                           (new_x, (new_h + new_y) / 2),
                                           (new_w, (new_h + new_y) / 2)
                                            ])
                elif 0 < len(blc_points) <= max:  # h/2
                    self.BLC = QuadTree(x, (y + h) / 2, (x + w) / 2, h, self.points,
                                        screen, self.depth + 1, self.rendering, self.variant, blc_points)

                #BRC
                brc_points = self.advanced_points_in((w + x) / 2, (y + h) / 2, w, h,
                                     self.planets_in_sector)
                if len(brc_points) > max:
                    self.BRC = QuadTree((w + x) / 2, (y + h) / 2, w, h, self.points,
                                        screen, self.depth + 1, self.rendering, self.variant, brc_points)

                    # Extends the history of the children, creates a flat array
                    self.lineHistory.extend(self.BRC.subDivide(sleeptime))
                    new_x = self.BRC.x
                    new_y = self.BRC.y
                    new_w = self.BRC.w
                    new_h = self.BRC.h

                    self.lineHistory.append([
                            ((new_w + new_x) / 2, new_y),
                            ((new_w + new_x) / 2, new_h),
                            (new_x, new_h / 2 + new_y / 2),
                            (new_w, (new_h / 2 + new_y / 2))
                                             ])
                elif 0 < len(brc_points) <= max:
                    self.BRC = QuadTree((w + x) / 2, (y + h) / 2, w, h, self.points,
                                        screen, self.depth + 1, self.rendering, self.variant, brc_points)
        return self.lineHistory