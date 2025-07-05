import math

from pyanaconda.modules.network.utils import get_default_route_iface

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

def pixelArrayGrouping(pixelArray, leafList): #This method takes the 2d Coordinates from the quad tree and groups the pixel array
    position_hash = {pixel.getPosition(): pixel for pixel in pixelArray}
    grouped_pixelArray = []
    for leaf in leafList:
        points = set(leaf.getPoints())  # Faster lookup
        group = []
        for point in points:
            pixel = position_hash.get(point)
            if pixel:
                group.append(pixel)
        grouped_pixelArray.append(group)  # Add group for this leaf
    return grouped_pixelArray


def findCenterOfMass(pixelArray):
    numeratorX = 0
    numeratorY = 0
    denominator = 0
    for x in pixelArray:
        numeratorX += x.getPosition()[0]*x.getMass()
        numeratorY += x.getPosition()[1]*x.getMass()
    for x in pixelArray:
        denominator += x.getMass()
    com = (numeratorX/denominator, numeratorY/denominator)
    return com

def redrawQuadTree(pixelArray):
    tree = QuadTree(0, 0, resolution[0], resolution[1], alignPoints(pixelArray), screen, 0)  #Change Points to Align Points
    tree.drawPoints(5)
    tree.subDivide(0)
    array = QuadTree.helperDFS3(tree)    #Should contain all the relevant data from the struct
    print(f'Type: {type(array)}: Length {len(array)}')

    for x in array:
        print(f'Coords: {(x.getPoints())}')
    print()

    return array


def gravitational_calculation2(g, nested_pixel_array):

    for x in nested_pixel_array:     #x represents every grouping of planets
        for z in nested_pixel_array: #z also represents every grouping of planets
            print()
            if(x == z):
                for y in x:
                    for h in x:     #y represents every planet in a grouping
                        if(y != h):
                            y.gravity(g, y, h)
                    y.applyForce()

            #    for y in x:


            print(y)
        print()


    return False


def gravitational_calculation(g, nested_pixel_array):
    #Calculate the force of Gravity for everything within the leaf
    #Estimates the rest of the universal force using far off leafs
    temp_force = 0
    temp_direction = (0,0)

    for x in nested_pixel_array:
        for z in x:
            for i in x:
                if(z is not i):
                    z.direction += z.getDirection(i.position)
                    z.force += (g * i.getMass() * z.getMass())/math.dist(i.getPosition(), z.getPosition())

                for y in nested_pixel_array:
                    if(x is not y):
                        z.direction += z.getDirection(findCenterOfMass(y))
                        z.force += (g * pixel.return_list_mass(x) * pixel.return_list_mass(y))/math.dist(findCenterOfMass(x), findCenterOfMass(y))
            z.applyForce()
    return False

def universe_tick(pixelArray, array):   #Functions as the primary driver of the Barnes-Hut Simulation
    nested_pixel_array = pixelArrayGrouping(pixelArray, array) #Merges the information from the two lists together
    COM = 0                                                    #Center of Mas+s
    gravitational_constant = 1                                 #Gravitational Constant [Set to 1 by default]
    gravitational_calculation2(gravitational_constant, nested_pixel_array)

    #print(array)

    return True


pixelArray = [pixel(100, (0, 40), (0, 0), 0), pixel(1000, (60.323, 59), (0, 0), 0), pixel(100, (0, 5), (0, 0), 0), pixel(100, (0, 100), (0, 0), 0),pixel(100, (0, 450), (0, 0), 0)]
points = [(30, 30), (30, 40), (30, 50), (40, 50), (60, 50),(65, 50), (70, 50),(63, 30), (63, 30), (190, 180), (200, 180), (180, 180), (160, 180)]

redrawQuadTree(pixelArray)

pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or (keys[pygame.K_LCTRL] and keys[pygame.K_c]): #Pressing Ctrl + C kills task
            running = False

        screen.fill((0, 0, 0))  # <<< Clear the screen here
        print(f'Number of Pixel present: {(len(pixelArray))}')
        array = redrawQuadTree(pixelArray)  #Draws out the quadtree and creates the game window, returns leaf array
        universe_tick(pixelArray, array)             #Runs the model of the simulation based on the leaf array
        pygame.time.delay(1000)


        pygame.display.flip()