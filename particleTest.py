import math
import random
from time import sleep

from QuadTree import QuadTree
import pygame

from Render import renderPlanets
from pixel import pixel

backColor = (255, 255, 255)
resolution = (width, height) = (2000, 2000)   #This doesn't play with all systems well, but works as a test
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Barnes-Hut')
screen.fill(backColor)
dotSize = 3
SIZE = 2000

def alignPoints(pixelArray):
    points = []
    for x in pixelArray:
        points.append(x.getPosition())
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
    if(len(grouped_pixelArray) < 1):
        grouped_pixelArray.append(pixelArray)
        return grouped_pixelArray
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

def redrawQuadTree(pixelArray, size):
    #tree = QuadTree(-resolution[0], -resolution[1], resolution[0], resolution[1], alignPoints(pixelArray), screen, 0)  #Change Points to Align Points
    tree = QuadTree(-size, -size, size, size, alignPoints(pixelArray), screen,0)  # Change Points to Align Points
    tree.out_of_bounds(pixelArray)
    renderPlanets(screen, pixelArray, 3, pygame.Vector2(0, 0))
    tree.subDivide(0)
    array = QuadTree.helperDFS3(tree, tree)    #Should contain all the relevant data from the struct
    return array,tree.rootSize


#Testing more "efficient" method however results are varied
def gravitational_calculation_faster(g, nested_pixel_array):
    # Step 1: Compute intra-cluster (nearby planets) brute force gravity
    #print(nested_pixel_array)
    #print()
    for cluster in nested_pixel_array:
        for i, planet1 in enumerate(cluster):
            for planet2 in cluster[i+1:]:
                planet1.gravity(g, planet1, planet2)
                planet2.gravity(g, planet2, planet1)

    # Step 2: Compute inter-cluster gravity using center of mass approximations
    # Precompute COM for each cluster to avoid recomputation
    cluster_coms = []
    for cluster in nested_pixel_array:
        com_mass = pixel.return_list_mass(cluster)
        com_pos = findCenterOfMass(cluster)
        cluster_coms.append(pixel(com_mass, com_pos, (0,0), 0, (0,0,0), 0,False))

    # Apply gravity between clusters
    for i, cluster_x in enumerate(nested_pixel_array):
        for j, cluster_z in enumerate(nested_pixel_array):
            if i != j:
                com_z = cluster_coms[j]
                for planet in cluster_x:
                    planet.gravity(g, planet, com_z)

    # Step 3: Apply forces to all planets after all gravity calculations
    for cluster in nested_pixel_array:
        for planet in cluster:
            planet.applyForce()
    #print(f"PixelArray: {(nested_pixel_array)}")
    #print("Ticked Gravity")
    return "Done"
def collision_tick(nested_pixel_array):
    for sector in nested_pixel_array:
        for planet in sector:
            for planet2 in sector:
                if planet != planet2:
                    closest_planet = min(sector, key=lambda planet: math.dist(planet.getPosition(), planet2.getPosition()))
                    print(f'Current Planet:{planet.getPosition()} -- Closest Planet: {closest_planet.getPosition()}')
                    if(math.dist(planet.getPosition(), closest_planet.getPosition()) < planet.radius):
                        print("Collision Detected")
                        pygame.time.wait(1000)
    return False


#def pixelFactory():
#    #temp_pixel = pixel(30, resolution[0]/2 + random.randint(0, 1000), random.randint(0, 1440), (0,1), random.randint(0,4), False)
#    temp_pixel = pixel(30, (resolution[0]/2+random.randint(-1000, 1000), resolution[1]/2 + random.randint(-720,720)), (0, 1), random.randint(-4,4), (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),False)
#    return temp_pixel


def universe_tick(pixelArray, array):   #Functions as the primary driver of the Barnes-Hut Simulation
    nested_pixel_array = pixelArrayGrouping(pixelArray, array) #Merges the information from the two lists together
    COM = 0                                                    #Center of Mas+s
    #gravitational_constant = 6.67430e-11
    gravitational_constant = (6.67430e-11)*10000000                       #Gravitational Constant [Set to 1 by default]
    gravitational_calculation_faster(gravitational_constant, nested_pixel_array)
    collision_tick(nested_pixel_array)
    return True


pixelArray = [
        pixel(200*1000, (resolution[0]/2, resolution[1]/2), (0,0), 0, (255,0,0), 10, True),
        pixel(30, (resolution[0]/2+250, resolution[1]/2), (0, 1), 4, (255,0,0),5, False),
        pixel(30, (resolution[0]/2+500,      resolution[1]/2), (0, 1), 2, (255,0,0),5, False),

    ]


#pixelArray = [
#    pixel(200*1000, (resolution[0]/2, resolution[1]/2), (0.2, -0.1), 0, (255,0,0), 10, True),
#    pixel(30, (resolution[0]/2+250, resolution[1]/2), (0, 1), 5, (255,0,0),5, False),
#    pixel(30, (resolution[0]/2+500,      resolution[1]/2), (0, 1), 2, (255,0,0),5, False),
#    pixel(30, (resolution[0] / 2 + 750,  resolution[1]/2), (0, 1), 2, (255,0,0),5, False),
#    pixel(30, (resolution[0] / 2 + 1000, resolution[1]/2), (0, 1), 2, (255,0,0),5, False),
#    ]

#for x in range(500):
#    pixelArray.append(pixelFactory())
#    pixelArray.append(pixelFactory())

#pixelArray = [
#    pixel(1.9891* 10**30, (resolution[0]/2, resolution[1]/2), (0, 0), 0, (255,255,0), 150, True),
#    pixel(5.972 * 10**24, (resolution[0]/2+500000, resolution[1]/2), (0, 1), 10, (0,123,123),50, False),
#    pixel(7.34767309 * 10**22, (resolution[0]/2+552, resolution[1]/2), (0, 1), 1, (255,255,255), 27/2,False),
#    #pixel(30, (resolution[0] / 2 + 750, 738.2), (0, 1), 2, (255,0,0),False),
#    #pixel(30, (resolution[0] / 2 + 1000, 738.2), (0, 1), 2, (255,0,0),False),
#    ]


for x in pixelArray:    #Initializes the force vectors
    x.vector_set(x.direction, x.force)


#pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or (keys[pygame.K_LCTRL] and keys[pygame.K_c]): #Pressing Ctrl + C kills task
            running = False

    screen.fill((0, 0, 0))  # <<< Clear the screen here
    #print(f'Number of Pixel present: {(len(pixelArray))}')
    pygame.init()
    start_ticks = pygame.time.get_ticks()
    print()
    print(pixelArray[0].color)

    array, rootSize = redrawQuadTree(pixelArray, SIZE)  #Draws out the quadtree and creates the game window, returns leaf array
    SIZE = rootSize
    end_ticks = pygame.time.get_ticks()
    print(f"Quadtree time: {(end_ticks - start_ticks)} milliseconds")


    pygame.init()
    start_ticks = pygame.time.get_ticks()
    universe_tick(pixelArray, array)             #Runs the model of the simulation based on the leaf array
    end_ticks = pygame.time.get_ticks()
    print(f"Tick time: {(end_ticks - start_ticks)} milliseconds")
    print()
    print(pixelArray[0].color)
    #pygame.time.delay(1000)

    #pygame.init()
    #start_ticks = pygame.time.get_ticks()
    #collision_tick()
    #end_ticks = pygame.time.get_ticks()
    #print(f"Collision time: {(end_ticks - start_ticks)} milliseconds")

    pygame.display.flip()