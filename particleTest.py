import random
import math
from itertools import combinations
from random import randint

from QuadTree import QuadTree
import pygame

from Render import Render
from pixel import pixel

backColor = (255, 255, 255)
resolution = (width, height) = (2000, 2000)   #This doesn't play with all systems well, but works as a test
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Barnes-Hut')
Rend = Render("test")
screen.fill(backColor)
dotSize = 3
SIZE = 2000
gravitational_constant = .01  # Gravitational Constant [Set to .01 by default]
render_quadtree = False

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
    tree = QuadTree(-size, -size, size, size, alignPoints(pixelArray), screen,0, render_quadtree)  # Change Points to Align Points
    tree.out_of_bounds(pixelArray)

    #Rendering pipeline
    Rend.renderPlanets(screen, pixelArray, 3, pygame.Vector2(0, 0))
    Rend.draw_history(screen, pixelArray, pygame.Vector2(0, 0))
    #Calling the tree to recursively divide
    tree.subDivide(0)
    array = QuadTree.helperDFS3(tree, tree)    #Should contain all the relevant data from the struct
    return array, tree.rootSize


#Testing more "efficient" method however results are varied
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
    temp_pixel = pixel(30, (resolution[0]/2+random.randint(-2000, 2000), resolution[1]/2 + random.randint(-2000,2000)), (0, 1), random.randint(-5,5), (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),5, False)
    return temp_pixel

def pixelFactory2(index):
    return pixelArray[index].form_satellite(gravitational_constant, randint(int(pixelArray[index].radius)+50, 1000))


def universe_tick(pixelArray, array):   #Functions as the primary driver of the Barnes-Hut Simulation
    nested_pixel_array = pixelArrayGrouping(pixelArray, array) #Merges the information from the two lists together
    gravitational_calculation_faster(gravitational_constant, nested_pixel_array)
    return nested_pixel_array


pixelArray = [
        pixel(200*10000, (resolution[0]/2, resolution[1]/2-2), (0,0), 0, (255,255,0), 100, True),
        #pixel(30, (resolution[0]/2+100, resolution[1]/2), (0, 1), 0, (255,0,0),5, False),
        #pixel(30, (resolution[0]/2+500, resolution[1]/2), (0, 1), 2, (255,0,0),5, False),
    ]

#pixelArray.append(pixelArray[0].form_satellite(gravitational_constant, 300))
#pixelArray.append(pixelArray[0].form_satellite(gravitational_constant, randint(pixelArray[0].radius+50, 1000)))
#pixelArray.append(pixelArray[0].form_satellite(gravitational_constant, 300))

#for x in range(1000):
#    pixelArray.append(pixelFactory())

#for x in range(2000):   #Number of planets to be "Spawned"
#    pixelArray.append(pixelFactory2())
pixelArray.append(pixelFactory2(0))
pixelArray.append(pixelFactory2(1))


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

    screen.fill((0, 0, 0))  # <<< Clear the screen here
    print(f'Number of Pixel present: {(len(pixelArray))}')

    print("-----------------------------")
    start_ticks = pygame.time.get_ticks()
    array, rootSize = redrawQuadTree(pixelArray, SIZE)  #Draws out the quadtree and creates the game window, returns the leaf array
    SIZE = rootSize
    end_ticks = pygame.time.get_ticks()
    quadtree_time = end_ticks - start_ticks
    total_quadTree_time += quadtree_time
    print(f"Quadtree time: {quadtree_time} milliseconds")


    start_ticks = pygame.time.get_ticks()
    nested_pixel_array = universe_tick(pixelArray, array)             #Runs the model of the simulation based on the leaf array
    end_ticks = pygame.time.get_ticks()
    tick_time = end_ticks - start_ticks
    total_tick_time += tick_time
    print(f"Tick time: {tick_time} milliseconds")

    start_ticks = pygame.time.get_ticks()
    #collision_tick(pixelArray, nested_pixel_array)     #Currently disabled for visuals
    end_ticks = pygame.time.get_ticks()
    collision_tick_time = end_ticks - start_ticks
    total_collision_time += collision_tick_time
    print(f"Collision time: {collision_tick_time} milliseconds")
    print(f'Operational Time Cost {quadtree_time+tick_time+collision_tick_time} milliseconds')
    print("-----------------------------")
    total_operations += 1
    pygame.display.flip()


print(f'Total QuadTree time: {total_quadTree_time} milliseconds')
print(f'Total Tick time: {total_tick_time} milliseconds')
print(f'Total Collision time: {total_collision_time} milliseconds')
total_time = total_quadTree_time+total_tick_time+total_collision_time
print(f'Total Operational time: {total_time} milliseconds')
print(f'Total Operations time: {total_operations} ticks')
print("----------------------------------------------------")
print(f'Average TPS(Ticks per second): {total_tick_time/total_operations} milliseconds')
print(f'Average FPS(Frames per second): {1000/(total_tick_time/total_operations)} FPS')