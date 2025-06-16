from QuadTree import QuadTree
import pygame

from pixel import pixel

backColor = (255, 255, 255)
resolution = (width, height) = (500, 300)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Barnes-Hut')
screen.fill(backColor)
dotSize = 5


def updatePixels():

    print()


def alignPoints(pixelArray):
    points = []
    for x in pixelArray:
        points.append(x.getPosition())
    print(pixelArray)
    print(points)
    return points


def redrawQuadTree(pixelArray):
    tree = QuadTree(0, 0, resolution[0], resolution[1], alignPoints(pixelArray), screen, 0)  #Change Points to Align Points
    tree.drawPoints(5)
    tree.subDivide(0)
    array = tree.helperDFS(tree)
    return array


pixelArray = [pixel(100, (0, 40), (0, 0), 1), pixel(100, (60, 59), (0, 0), 1), pixel(100, (0, 5), (0, 0), 1), pixel(100, (0, 100), (0, 0), 1),pixel(100, (0, 450), (0, 0), 1)]
#p0 = pixel(10,(100, 100),0,0)
#p1 = pixel(10,(0,0), 0,0)
#pixel.gravity(p0, 1, p0, p1)
points = [(30, 30), (30, 40), (30, 50), (40, 50), (60, 50),(65, 50), (70, 50),(63, 30), (63, 30), (190, 180), (200, 180), (180, 180), (160, 180)]

#tree = QuadTree(0, 0, resolution[0], resolution[1], points, screen, 0)
#tree.drawPoints(5)

#tree.subDivide(0)
#array = tree.helperDFS(tree)
#print(array)
#for x in array:
#    for y in x:
#        print(y)


pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        redrawQuadTree(pixelArray)