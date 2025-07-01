import random
import pygame
from QuadTree import QuadTree
import sys

def generatePointPositions(points, x, resolution):
    for y in range(x):
        points.append((random.randint(0, resolution[0]), random.randint(0, resolution[1])))
    return points


def drawSeperations(p0, p1, p2, p3):
    pygame.draw.line(screen, (0, 0, 0), p0, p1, 1)
    pygame.draw.line(screen, (0, 0, 0), p2, p3, 1)



args = sys.argv
backColor = (255, 255, 255)
resolution = (width, height) = (500, 300)
dotNumber = 1000
sleeptime = 10
print(args)
if len(args) > 1:
    resolution = (width, height) = (int(args[1]), int(args[2]))
    dotNumber = int(args[3])
    sleeptime = int(args[4])

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('QuadTree Visual Implementation')
screen.fill(backColor)
dotSize = 5

#points = generatePointPositions([], dotNumber, resolution)
points = [(30, 30), (30, 40), (30, 50), (40, 50), (60, 50),(65, 50), (70, 50),(63, 30), (63, 30), (190, 180), (200, 180), (180, 180), (160, 180)]

testTree = QuadTree(0, 0, resolution[0], resolution[1], points, screen, 0)



#points = generatePointPositions([], dotNumber, resolution)
#points = [(50, 160), (120, 170), (130, 180), (120, 180), (120, 190), (120, 200)]
#points = [(151, 160), (220, 170), (230, 180), (220, 180), (220, 190), (220, 200)]  #Bottom Right

#points = [(250, 10), (260, 15), (270, 20), (255, 25)]       #Top Right

#saltedPoints = generatePointPositions(points, 30)
#points = [(30, 30), (30, 40), (30, 50), (200, 50), (250, 50), (270, 50), (300, 50)]

#newPoints = testTree.pointsIn(0, 0, 100, 200, points)
#print(f'{points}\n{newPoints}')


#for x in testTree.cullLeaf(testTree.getLeaf()):
#    print(x.getPoints())
# print("TLC Points: ")
# print(testTree.getTLC().getPoints())
#
# print("TRC Points: ")
# print(testTree.getTRC().getPoints())
'''''
if testTree.TLC is not None:
    TLCPoints = testTree.getTLC().getPoints()
if testTree.TRC is not None:
    TRCPoints = testTree.getTRC().getPoints()
if testTree.BLC is not None:
    BLCPoints = testTree.getBLC().getPoints()
if testTree.BRC is not None:
    BRCPoints = testTree.getBRC().getPoints()
    '''''
#if testTree.TLC is not None:
#    experimental = testTree.depthfirst().getPoints()

# newPoints = QuadTree.pointsIn(test, 0, 0, 100, 200, points)  # (x0,y0,x1,y1)

'''''
for x in points:
    pygame.draw.ellipse(screen, (255, 0, 0), (x[0] - dotSize/2, x[1]-dotSize/2, dotSize, dotSize))
'''''


#for x in TLCPoints:
#    pygame.draw.ellipse(screen, (0, 0, 255), (x[0], x[1], dotSize, dotSize))
#for x in TRCPoints:
#    pygame.draw.ellipse(screen, (0, 255, 00), (x[0], x[1], dotSize, dotSize))
#for x in BLCPoints:
#    pygame.draw.ellipse(screen, (255, 0, 255), (x[0], x[1], dotSize, dotSize))
#for x in BRCPoints:
#    pygame.draw.ellipse(screen, (0, 122, 122), (x[0], x[1], dotSize, dotSize))
#
#for x in experimental:
#    pygame.draw.ellipse(screen, (255, 0, 0), (x[0], x[1], dotSize, dotSize))

# drawSeperations((resolution[0]/2,0),(resolution[0]/2,resolution[1]), (0, resolution[1]/2), (resolution[0], resolution[1]/2))

testTree.drawPoints(5)
pygame.display.flip()
testTree.subDivide(sleeptime)



pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
