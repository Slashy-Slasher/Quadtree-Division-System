from QuadTree import QuadTree
import pygame

from pixel import pixel

backColor = (255, 255, 255)
resolution = (width, height) = (2560, 1440)   #This doesn't play with all systems well, but works as a test
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
    #print(pixelArray)
    #print(points)
    return points


def redrawQuadTree(pixelArray):
    tree = QuadTree(0, 0, resolution[0], resolution[1], alignPoints(pixelArray), screen, 0)  #Change Points to Align Points
    tree.drawPoints(5)
    tree.subDivide(0)
    array = QuadTree.helperDFS3(tree)    #Should contain all the relevant data from the struct
    #print(f'Type: {type(array)}: Length {len(array)}')
    print(f'Type: {type(array)}: Length {len(array)}')
    print(array[0])
    print(array[0].getPoints())
    print(array[0].returnCenter())
    print()
    pygame.draw.circle(screen, (0,0,255), array[0].returnCenter(), 5)
    return array


def universalGravity(pixelArray, array):   #Functions as the primary driver of the Barnes-Hut Simulation
    #Finds the number of planets in each leaf node
    #Finds the total mass of each leaf node
    #Finds the center of mass(Depends on the coordinates of the leaf node)
    #Calculates and then Applies the force to each planet represented by the center of mass



    print(array)

    return True



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
#redrawQuadTree(pixelArray)


redrawQuadTree(pixelArray)

pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or (keys[pygame.K_LCTRL] and keys[pygame.K_c]): #Pressing Ctrl + C kills task
            running = False

        #redrawQuadTree(pixelArray)

        #print(len(quadTree[0][0]))


        #universalGravity(pixelArray, points)

        pygame.display.flip()
