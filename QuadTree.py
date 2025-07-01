import pygame


class QuadTree:
    def __init__(self, x, y, w, h, points, screen, depth):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.points = self.pointsIn(x, y, w, h, points)
        self.max = 3  # Defines points which can exist before square subdivision
        self.screen = screen
        self.depth = depth
        self.TLC = None
        self.TRC = None

        self.BLC = None
        self.BRC = None
        self.root = False
        if self.TLC is None and self.TRC is None and self.BLC is None and self.BRC is None and self.depth == 0:
            self.root = True

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

    def isLeaf(self):
        if (self.TLC is None and self.TRC is None and self.BLC is None and self.BRC is None):
            return True
        else:
            return False

    def helperDFS(self, node):  # Uses Depth First Search to return all leaf nodes of the quadtree
        storage = []
        if node.getTLC() is not None:
            if node.TLC.isLeaf():
                storage.append(node.getTLC())
            else:
                storage.append(self.helperDFS(node.TLC))

        if node.TRC is not None:
            if node.TRC.isLeaf():
                storage.append(node.getTRC())
            else:
                storage.append(self.helperDFS(node.TRC))

        if node.BLC is not None:
            if node.BLC.isLeaf():
                storage.append(node.getBLC())
            else:
                storage.append(self.helperDFS(node.BLC))

        if node.BRC is not None:
            if node.BRC.isLeaf():
                storage.append(node.getBRC())
            else:
                storage.append(self.helperDFS(node.BRC))
        return storage

    def pointsIn(self, x0, y0, x1, y1, points):  # Returns a list of the points within an area
        newPoints = []
        for j in points:
            if x0 <= j[0] <= x1 and y0 <= j[1] <= y1:
                newPoints.append(j)
        return newPoints

    def drawLines(self, screen, p0, p1, p2, p3):
        black = (0, 0, 0)
        pygame.draw.line(screen, black, p0, p1, 1)  # screen, line color, point 1, point 2, thickness
        pygame.draw.line(screen, black, p2, p3, 1)

    def drawLines2(self, qT, thickness):
        black = (0, 0, 0)
        p0, p1, p2, p3 = (qT.w / 2, qT.y), (qT.w / 2, qT.h), (qT.x, (qT.h / 2 + qT.y / 2)), (
            qT.w, (qT.h / 2 + qT.y / 2))
        pygame.draw.line(qT.screen, black, p0, p1, thickness)
        pygame.draw.line(qT.screen, black, p2, p3, thickness)

    def drawPoints(self, dotSize):
        for x in self.points:
            pygame.draw.ellipse(self.screen, (255, 0, 0), (x[0] - dotSize / 2, x[1] - dotSize / 2, dotSize, dotSize))

    def subDivide(self, sleeptime):
        pygame.time.delay(sleeptime)
        if len(self.points) > self.max and self.root is True:
            self.drawLines2(self, 3)
            # self.drawLines(self.screen, (self.w/2, self.y), (self.w/2, self.h),(self.x,self.h/2),(self.w,self.h/2))
            self.root = False
            self.depth = self.depth + 1

        if len(self.points) > self.max and self.depth < 10000000:
            if len(self.pointsIn(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points)) > self.max:
                self.TLC = QuadTree(self.x, self.y, (self.x + self.w) / 2, (self.y + self.h) / 2, self.points,
                                    self.screen, self.depth + 1)
                self.TLC.subDivide(sleeptime)
                self.drawLines(self.screen,
                               ((self.TLC.w + self.TLC.x) / 2, self.TLC.y),
                               ((self.TLC.w + self.TLC.x) / 2, self.TLC.h),
                               (self.TLC.x, (self.TLC.y + self.TLC.h) / 2),
                               (self.TLC.w, (self.TLC.y + self.TLC.h) / 2))

            if len(self.pointsIn((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2,
                                 self.points)) > self.max:  # w/2
                self.TRC = QuadTree((self.w + self.x) / 2, self.y, self.w, (self.y + self.h) / 2, self.points,
                                    self.screen, self.depth + 1)
                self.TRC.subDivide(sleeptime)
                self.drawLines(self.screen,
                               ((self.TRC.w + self.TRC.x) / 2, self.TRC.y),
                               ((self.TRC.w + self.TRC.x) / 2, self.TRC.h),
                               (self.TRC.x, (self.TRC.h + self.TRC.y) / 2),
                               (self.TRC.w, (self.TRC.h + self.TRC.y) / 2))

            if len(self.pointsIn(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h,
                                 self.points)) > self.max:  # h/2
                self.BLC = QuadTree(self.x, (self.y + self.h) / 2, (self.x + self.w) / 2, self.h, self.points,
                                    self.screen, self.depth + 1)
                self.BLC.subDivide(sleeptime)
                self.drawLines(self.screen,
                               ((self.BLC.w + self.BLC.x) / 2, self.BLC.y),
                               ((self.BLC.w + self.BLC.x) / 2, self.BLC.h),
                               (self.BLC.x, (self.BLC.h + self.BLC.y) / 2),
                               (self.BLC.w, (self.BLC.h + self.BLC.y) / 2))

            if len(self.pointsIn((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h, self.points)) > self.max:
                self.BRC = QuadTree((self.w + self.x) / 2, (self.y + self.h) / 2, self.w, self.h, self.points,
                                    self.screen, self.depth + 1)
                self.BRC.subDivide(sleeptime)
                self.drawLines(self.screen,
                               ((self.BRC.w + self.BRC.x) / 2, self.BRC.y),
                               ((self.BRC.w + self.BRC.x) / 2, self.BRC.h),
                               (self.BRC.x, self.BRC.h / 2 + self.BRC.y / 2),
                               (self.BRC.w, (self.BRC.h / 2 + self.BRC.y / 2)))
            pygame.display.flip()
        else:
            print("Depth Reached")
