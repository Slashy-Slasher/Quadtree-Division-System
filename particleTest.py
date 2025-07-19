import random
import math
from itertools import combinations
from random import randint

from QuadTree import QuadTree
import pygame

from Render import Render
from pixel import pixel

backColor = (255, 255, 255)
resolution = (width, height) = (1000, 1000)   #This doesn't play with all systems well, but works as a test
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Barnes-Hut')
Rend = Render("test")
screen.fill(backColor)
dotSize = 3
SIZE = 80000
gravitational_constant = .1  # Gravitational Constant [Set to .01 by default]
render_quadtree = False
clock = pygame.time.Clock()
telemetry_enabled = True
zoom_level = .1
threshold_angle = 1000

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
    if len(grouped_pixelArray) < 1:
        grouped_pixelArray.append(pixelArray)
        return grouped_pixelArray
    return grouped_pixelArray


def findCenterOfMass(pixelArray):
    numeratorX = 0
    numeratorY = 0
    denominator = 0
    com = 0
    for x in pixelArray:
        numeratorX += x.getPosition()[0]*x.getMass()
        numeratorY += x.getPosition()[1]*x.getMass()
    for x in pixelArray:
        denominator += x.getMass()
    if(denominator != 0):
        com = (numeratorX/denominator, numeratorY/denominator)
    return com

def redrawQuadTree(pixelArray, size):
    tree = QuadTree(-size, -size, size, size, alignPoints(pixelArray), screen,0, render_quadtree, 1, pixelArray)  # Change Points to Align Points
    tree.out_of_bounds(tree.planets_in_sector)

    history = tree.subDivide(0)

    #Rendering pipeline
    #Rend.draw_history(screen, pixelArray, pygame.Vector2(0, 0))
    Rend.renderPlanets(screen, pixelArray, pygame.Vector2(0, 0), zoom_level)
    #Rend.renderQuadtree(screen, history, pygame.Vector2(0, 0), zoom_level)
    #pygame.display.flip()
    array = QuadTree.helperDFS3(tree, tree)    #Should contain all the relevant data from the struct

    return array, tree, history


#The threshold_angle is used to figure out the level of estimation needed
def gravitational_calculator(g, tree, leafList):
    #use s/d <

    #Create a linear path of planets to be iterated over (N)
    #For each planet in the list, start with the 4 children node of the root then compare s/d to threshold_angle
    #If the equation s/d < theta is true, the planet is far enough away to use the major approximation
    #elif the s/d > theta, break down that child_node into it's children and repeat the process till s/d < theta = True
    #AND if a leaf node is found, ensure that the leaf node doesn't contain the current planet.
    #Apply the
    # between the center of mass and the planet.

    sectors = []
    #print(len(leafList))
    for x in leafList:                  #This loops through every leaflist in the system
        for y in x.planets_in_sector:   #This loops through every planet in the systen
            sectors = tree.return_children()
            for z in sectors:
                if math.dist(z.COM, y.getPosition()) != 0:
                    if(z.width / math.dist(z.COM, y.getPosition())) > threshold_angle:
                        #print(z.width / math.dist(z.COM, y.getPosition()) > threshold_angle)
                        sectors.extend(z.return_children())
                    elif (z.width / math.dist(z.COM, y.getPosition())) < threshold_angle:
                        temp_pixel = pixel(z.mass, z.COM, (0, 0),0,(0,0,0), 5,True)
                        y.gravity(g, y, temp_pixel)
            y.applyForce()


#Testing more "efficient" method however results are varied
#Turns out they were varied because the program was still running n^2 notation, not because of any for loop combo, but
#Rather that the threshold value was always set to the minimum; degenerating the algorithm back to n^2
def gravitational_calculation_faster(g, nested_pixel_array):
    for cluster in nested_pixel_array:
        for i, planet1 in enumerate(cluster):
            for planet2 in cluster[i+1:]:
                planet1.gravity(g, planet1, planet2)
                planet2.gravity(g, planet2, planet1)

    cluster_coms = []
    for cluster in nested_pixel_array:
        com_mass = pixel.return_list_mass(cluster)
        com_pos = findCenterOfMass(cluster)
        cluster_coms.append(pixel(com_mass, com_pos, (0,0), 0, (0,0,0), 0,False))

    for i, cluster_x in enumerate(nested_pixel_array):
        for j, cluster_z in enumerate(nested_pixel_array):
            if i != j:
                com_z = cluster_coms[j]
                for planet in cluster_x:
                    planet.gravity(g, planet, com_z)

    for cluster in nested_pixel_array:
        for planet in cluster:
            planet.applyForce()
    return "Done"


def collision_tick(pixelArray, nested_pixel_array):
    to_remove = set()
    for sector in nested_pixel_array:
        for planet1, planet2 in combinations(sector, 2):
            if math.dist(planet1.getPosition(), planet2.getPosition()) < (planet1.radius + planet2.radius):
                if planet1.mass < planet2.mass:
                    to_remove.add(planet1)
                else:
                    to_remove.add(planet2)
    #Changed to more cleanly remove planets, will change to change vector + velocity after other issues are solved
    for planet in to_remove:
        if planet in pixelArray:
            pixelArray.remove(planet)
        for sector in nested_pixel_array:
            if planet in sector:
                sector.remove(planet)

    return pixelArray


def pixelFactory():
    temp_pixel = pixel(30, (resolution[0]/2+random.randint(-2000, 2000),
                        resolution[1]/2 + random.randint(-2000,2000)),
                       (0, 1), random.randint(-5,5), (random.randint(0, 255),
                        random.randint(0, 255),random.randint(0, 255)),5, False)
    return temp_pixel

def pixelFactory2(index, spacing, direction):
    return pixelArray[index].form_satellite(gravitational_constant, randint(int(pixelArray[index].radius)+50, spacing), direction)


def universe_tick(pixelArray, array, tree):   #Functions as the primary driver of the Barnes-Hut Simulation
    nested_pixel_array = pixelArrayGrouping(pixelArray, array) #Merges the information from the two lists together
    gravitational_calculator(gravitational_constant, tree, array)
    return nested_pixel_array

sun_mass = 10000000000
pixelArray = [
        pixel(sun_mass, (1,1), (1,0), 0, (255,255,0), 100, True),
        #pixel(sun_mass, (100, 0), (1, 0), 0, (255, 255, 0), 100, True),

    #pixel(200 * 10000, (0,0), (1, 0), 0, (255, 255, 0), 100, True),

    #pixel(sun_mass, (resolution[0] / 2 - 2500, resolution[1] / 2 - 2500), (1, 0), 0, (255, 255, 0), 100, True),
    #pixel(sun_mass, (resolution[0] / 2 + 2500, resolution[1] / 2 + 2500), (1, 0), 0, (255, 255, 0), 100, True),

    ]


#for _ in range(300):
#    x = random.randint(-500, 500)
#    y = random.randint(-500, 500)
#    dx = 0
#    dy = 0
#    mass = random.randint(10, 200)
#    diameter = random.randint(5, 20)
#    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
#    pixelArray.append(pixel(mass, (x, y), (dx, dy), 0, color, diameter, False))



#for x in range(100):
#    pixelArray.append(pixelFactory())

#for x in range(2000):   #Number of planets to be "Spawned"
#    pixelArray.append(pixelFactory2(0, 50, 1))

for x in range(2000):   #Number of planets to be "Spawned"
    pixelArray.append(pixelFactory2(0, 5000, -1))


for x in pixelArray:    #Initializes the force vectors
    x.vector_set(x.direction, x.force)

total_quadTree_time = 0
total_collision_time = 0
total_tick_time = 0
total_operations = 0
running = True
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or (keys[pygame.K_LCTRL] and keys[pygame.K_c]): #Pressing Ctrl + C kills task
            running = False
    clock.tick(60)
    screen.fill((0, 0, 0))  # <<< Clear the screen here

    if telemetry_enabled:
        print(f'Number of Pixel present: {(len(pixelArray))}')
        print("-----------------------------")
        start_ticks = pygame.time.get_ticks()
        array, tree, lineHistory = redrawQuadTree(pixelArray, SIZE)  #Draws out the quadtree and creates the game window, returns the leaf array
        SIZE = tree.rootSize
        end_ticks = pygame.time.get_ticks()
        quadtree_time = end_ticks - start_ticks
        total_quadTree_time += quadtree_time
        print(f"Quadtree time: {quadtree_time} milliseconds")
        start_ticks = pygame.time.get_ticks()
        nested_pixel_array = universe_tick(pixelArray,array, tree)  # Runs the model of the simulation based on the leaf array
        end_ticks = pygame.time.get_ticks()
        tick_time = end_ticks - start_ticks
        total_tick_time += tick_time
        print(f"Tick time: {tick_time} milliseconds")

        start_ticks = pygame.time.get_ticks()
        #collision_tick(pixelArray, nested_pixel_array)  # Currently disabled for visuals
        end_ticks = pygame.time.get_ticks()
        collision_tick_time = end_ticks - start_ticks
        total_collision_time += collision_tick_time
        print(f"Collision time: {collision_tick_time} milliseconds")
        print(f'Operational Time Cost {quadtree_time + tick_time + collision_tick_time} milliseconds')
        print("-----------------------------")
        total_operations += 1
    else:
        array, tree, lineHistory = redrawQuadTree(pixelArray, SIZE)  #Draws out the quadtree and creates the game window, returns the leaf array
        SIZE = tree.rootSize
        print(SIZE)
        nested_pixel_array = universe_tick(pixelArray,array, tree)  # Runs the model of the simulation based on the leaf array
        #collision_tick(pixelArray, nested_pixel_array)  # Currently disabled for visuals
        #Rend.scale_world(screen, .5)   #Use this for the minimap, will have to come back to it though

    pygame.display.flip()



if telemetry_enabled:
    print(f'Total QuadTree time: {total_quadTree_time} milliseconds')
    print(f'Total Tick time: {total_tick_time} milliseconds')
    print(f'Total Collision time: {total_collision_time} milliseconds')
    total_time = total_quadTree_time+total_tick_time+total_collision_time
    print(f'Total Operational time: {total_time} milliseconds')
    print(f'Total Operations: {total_operations} ticks')
    print("----------------------------------------------------")
    #print(f'Average TPS(Ticks per second): {total_tick_time/total_operations} milliseconds')
    print(f'Average FPS(Frames per second): {1000/(total_tick_time/total_operations)} FPS')
