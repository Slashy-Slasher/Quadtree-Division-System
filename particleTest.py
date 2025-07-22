import random
import math
from itertools import combinations
from random import randint
from concurrent.futures import ThreadPoolExecutor

from jaxlib.xla_client import profiler
from sympy import false


from QuadTree import QuadTree
import pygame

from Render import Render
from pixel import pixel

from pyinstrument import Profiler
import pyinstrument

backColor = (255, 255, 255)
resolution = (width, height) = (1000, 1000)   #This doesn't play with all systems well, but works as a test
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Barnes-Hut')
screen.fill(backColor)
dotSize = 3
SIZE = 8000
gravitational_constant = 1 # Gravitational Constant [Set to .01 by default]
render_quadtree = False
clock = pygame.time.Clock()
telemetry_enabled = False

zoom_level = .02
threshold_angle = 10
threshold_angle_collision = .01
debug = False
center = pygame.Vector2(screen.get_width() // 2, screen.get_height() // 2)
current_offset = (0,0)


Rend = Render(center, current_offset, zoom_level)


def alignPoints(pixelArray):
    points = []
    for x in pixelArray:
        points.append(x.getPosition())
    return points


#def pixelArrayGrouping(pixelArray, leafList): #This method takes the 2d Coordinates from the quad tree and groups the pixel array
#    position_hash = {pixel.getPosition(): pixel for pixel in pixelArray}
#    grouped_pixelArray = []
#    for leaf in leafList:
#        points = set(leaf.getPoints())  # Faster lookup
#        group = []
#        for point in points:
#            pixel = position_hash.get(point)
#            if pixel:
#                group.append(pixel)
#        grouped_pixelArray.append(group)  # Add group for this leaf
#    if len(grouped_pixelArray) < 1:
#        grouped_pixelArray.append(pixelArray)
#        return grouped_pixelArray
#    return grouped_pixelArray


@pyinstrument.profile()
def universe_tick(pixelArray, leafList, tree, history, delta_time):   #Functions as the primary driver of the Barnes-Hut Simulation
    #Pre-check to see if some planets are out of bounds
    tree.out_of_bounds(pixelArray)
    #Calculates the force for every object in the quadtree
    gravitational_calculator(gravitational_constant, tree, leafList)
    #Applies forces calculated in the gravitational_calculator
    for x in pixelArray:
        x.applyForce(delta_time)

@pyinstrument.profile()
def redrawQuadTree(pixelArray, size):
    tree = QuadTree(-size, -size, size, size, alignPoints(pixelArray), screen,0, false, 1, pixelArray)  # Change Points to Align Points
    tree.out_of_bounds(tree.planets_in_sector)

    history = tree.subDivide(0)

    #Rendering pipeline
    #Rend.draw_history(screen, pixelArray, pygame.Vector2(0, 0))

    Rend.renderPlanets(screen, pixelArray)
    if(render_quadtree):
        Rend.renderQuadtree(screen, history, tree)
    #pygame.display.flip()
    array = QuadTree.helperDFS3(tree, tree)    #Should contain all the relevant data from the struct
    return array, tree, history

def gravitational_calculator_multithread(g, tree, leaf, pixelArray, debug, delta_time, history, screen, zoom_level):
    for planet in leaf.planets_in_sector:
        sectors = tree.return_children()
        if debug:
            Rend.highlight_planet(screen, planet)  # REMOVE or use thread-safe queue
        for current_node in sectors:
            if debug:
                pygame.draw.circle(screen, (0, 0, 255), Rend.tuple_world_to_screen(current_node.COM), 5)
                pygame.display.flip()
            distance = math.dist(current_node.COM, planet.getPosition())
            if distance != 0 and math.dist(current_node.COM, leaf.COM) != 0:
                if debug:
                    Rend.renderSquare(screen, current_node, False)  # REMOVE
                    pygame.display.flip()
                if (current_node.width / distance) > threshold_angle:
                    sectors.extend(current_node.return_children())
                else:
                    temp_pixel = pixel(current_node.mass, current_node.COM, (0, 0), 0, (0, 0, 0), 5, True)
                    planet.gravity(g, planet, temp_pixel)
            else:
                if debug:
                    Rend.renderSquare(screen, current_node, True)
                    pygame.display.flip()
                for temp_planet in current_node.planets_in_sector:
                    for comparison_planet in current_node.planets_in_sector:
                        if temp_planet != comparison_planet:
                            temp_planet.gravity(g, temp_planet, comparison_planet)
        if debug:
            screen.fill(pygame.Color(0, 0, 0))
            Rend.renderQuadtree(screen, history, tree)
            Rend.renderPlanets(screen, pixelArray)



#The threshold_angle is used to figure out the level of estimation needed
def gravitational_calculator(g, tree, leafList):

    planet_list = []
    planet_to_leaf = {}
    for leaf in leafList:                       #Reverse dictionary lookup, converts the planet to the current Leaf
        for planet in leaf.planets_in_sector:   #Reverse dictionary lookup, converts the planet to the current Leaf
            planet_to_leaf[planet] = leaf       #Reverse dictionary lookup, converts the planet to the current Leaf
            planet_list.append(planet)

    for planet in planet_list:                   #Avoids needing to double loop
        #Can functionally ignore above
        sectors = tree.return_children()    #4 root children
        p1_position = planet.getPosition()
        for current_node in sectors:
            distance = math.dist(current_node.COM, p1_position) #Finds the distance between x planet and y COM
            current_nodes_COM = current_node.COM
            # Far-Off Sectors
            # Easy Computations
            if current_node != planet_to_leaf[planet]:
                if(current_node.width / distance) < threshold_angle:    #Need to implement better solution which will compute better
                    planet.gForce += pygame.Vector2(planet.gravity_with_COM_numba(g, planet.mass, current_node.mass, p1_position[0], p1_position[1], current_nodes_COM[0],current_nodes_COM[1]))
                else:
                    sectors.extend(current_node.return_children())
                    #planet.gravity_with_COM_numba(g, planet, current_nodes_COM, current_node.mass)

            # Intra-Sector Calculation
            #Hard Computations
            else:
                for a,b in combinations(current_node.planets_in_sector, 2):
                    a_position = a.getPosition()
                    b_position = b.getPosition()
                    a.gForce += pygame.Vector2(planet.gravity_with_COM_numba(g, a.mass, b.mass, a_position[0], a_position[1], b_position[0], b_position[1]))
                    b.gForce += pygame.Vector2(planet.gravity_with_COM_numba(g, a.mass, b.mass, a_position[0], a_position[1], b_position[0], b_position[1]))
                    #a.gravity(g, a, b)
                    #b.gravity(g, a, b)




##Testing more "efficient" method however results are varied
##Turns out they were varied because the program was still running n^2 notation, not because of any for loop combo, but
##Rather that the threshold value was always set to the minimum; degenerating the algorithm back to n^2
#def gravitational_calculation_faster(g, nested_pixel_array):
#    for cluster in nested_pixel_array:
#        for i, planet1 in enumerate(cluster):
#            for planet2 in cluster[i+1:]:
#                planet1.gravity(g, planet1, planet2)
#                planet2.gravity(g, planet2, planet1)
#
#    cluster_coms = []
#    for cluster in nested_pixel_array:
#        com_mass = pixel.return_list_mass(cluster)
#        com_pos = findCenterOfMass(cluster)
#        cluster_coms.append(pixel(com_mass, com_pos, (0,0), 0, (0,0,0), 0,False))
#
#    for i, cluster_x in enumerate(nested_pixel_array):
#        for j, cluster_z in enumerate(nested_pixel_array):
#            if i != j:
#                com_z = cluster_coms[j]
#                for planet in cluster_x:
#                    planet.gravity(g, planet, com_z)
#
#    for cluster in nested_pixel_array:
#        for planet in cluster:
#            planet.applyForce()
#    return "Done"

@pyinstrument.profile()
def collision_with_quadtree(tree, leafList, pixelArray):
    planet_list = []
    planet_to_leaf = {}
    planet_to_properPlanet = {}
    for leaf in leafList:  # Reverse dictionary lookup, converts the planet to the current Leaf
        for planet in leaf.planets_in_sector:  # Reverse dictionary lookup, converts the planet to the current Leaf
            planet_to_leaf[planet] = leaf  # Reverse dictionary lookup, converts the planet to the current Leaf
            planet_list.append(planet)

    for planet in pixelArray:  # Reverse dictionary lookup, converts the planet to the current Leaf
        planet_to_properPlanet[planet] = planet  # Reverse dictionary lookup, converts the planet to the current Leaf
        #planet_list.append(planet)

    for planet in planet_list:  # Avoids needing to double loop
        # Can functionally ignore above
        sectors = tree.return_children()  # 4 root children
        p1_position = planet.getPosition()
        p1_radius = planet.radius
        check_list = []
        check_list.extend(planet_to_leaf[planet].planets_in_sector)
        for current_node in sectors:
            distance = math.dist(current_node.COM, p1_position)  # Finds the distance between x planet and y COM
            if current_node != planet_to_leaf[planet]:
                if (current_node.width / distance) < threshold_angle_collision:
                   check_list.extend(current_node.planets_in_sector)
                else:
                    sectors.extend(current_node.return_children())
        for comparison_planet in check_list:
            if(comparison_planet != planet):
                if math.dist(p1_position, comparison_planet.getPosition()) < (p1_radius + comparison_planet.radius):
                    if(planet.mass > comparison_planet.mass):
                        if comparison_planet in pixelArray:
                            planet.mass += comparison_planet.mass
                            planet.gForce += comparison_planet.gForce
                            pixelArray.remove(comparison_planet)
                            planet_list.remove(comparison_planet)


                    #planet.gForce += comparison_planet.gForce/2


    #for planet in check_list:
    #    for a, b in combinations(check_list, 2):





    #for leaf in leafList:
    #    for a, b in combinations(leaf.planets_in_sector, 2):
    #        a_planet = a
    #        b_planet = b
    #        a_position = pygame.Vector2(a_planet.getPosition())
    #        b_position = pygame.Vector2(b_planet.getPosition())
    #        if(math.dist(a_position, b_position) < (a_planet.radius + b_planet.radius)):
    #            return True


#def collision_tick(pixelArray, nested_pixel_array):
#    to_remove = set()
#    for sector in nested_pixel_array:
#        for planet1, planet2 in combinations(sector, 2):
#            if math.dist(planet1.getPosition(), planet2.getPosition()) < (planet1.radius + planet2.radius):
#                if planet1.mass < planet2.mass:
#                    to_remove.add(planet1)
#                else:
#                    to_remove.add(planet2)
#    #Changed to more cleanly remove planets, will change to change vector + velocity after other issues are solved
#    for planet in to_remove:
#        if planet in pixelArray:
#            pixelArray.remove(planet)
#        for sector in nested_pixel_array:
#            if planet in sector:
#                sector.remove(planet)
#
#    return pixelArray


def pixelFactory():
    temp_pixel = pixel(30, (resolution[0]/2+random.randint(-2000, 2000),
                        resolution[1]/2 + random.randint(-2000,2000)),
                       (0, 1), random.randint(-5,5), (random.randint(0, 255),
                        random.randint(0, 255),random.randint(0, 255)),5, False)
    return temp_pixel

def pixelFactory2(index, spacing, direction):
    return pixelArray[index].form_galaxy(gravitational_constant, randint(int(pixelArray[index].radius), spacing), direction)



sun_mass = 100000
pixelArray = [
        pixel(sun_mass, (50,50), (1,0), 0, (255,255,0), 100, True),
        #pixel(sun_mass, (100, 0), (1, 0), 0, (255, 255, 0), 100, True),

    #pixel(200 * 10000, (0,0), (1, 0), 0, (255, 255, 0), 100, True),

    #pixel(sun_mass, (resolution[0] / 2 - 2500, resolution[1] / 2 - 2500), (1, 0), 0, (255, 255, 0), 100, True),
    #pixel(sun_mass, (resolution[0] / 2 + 2500, resolution[1] / 2 + 2500), (1, 0), 0, (255, 255, 0), 100, True),

    ]


#for _ in range(2000):
#    x = random.randint(-500000, 500000)
#    y = random.randint(-500000, 500000)
#    dx = 0
#    dy = -1
#    mass = random.randint(10, 200)
#    diameter = random.randint(5, 20)
#    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
#    pixelArray.append(pixel(mass, (x, y), (dx, dy), 6, color, diameter, False))



#for x in range(100):
#    pixelArray.append(pixelFactory())

#for x in range(2000):   #Number of planets to be "Spawned"
#    pixelArray.append(pixelFactory2(0, 8000, 1))

for x in range(1000):   #Number of planets to be "Spawned"
    pixelArray.append(pixelFactory2(0, 50000, -1))


for x in pixelArray:    #Initializes the force vectors
    x.vector_set(x.direction, x.force)

total_quadTree_time = 0
total_collision_time = 0
total_tick_time = 0
total_operations = 0
zoom_step = .01
last_mouse_pos = 0
dragging = False

running = True
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or (keys[pygame.K_LCTRL] and keys[pygame.K_c]): #Pressing Ctrl + C kills task
            running = False
        old_zoom = zoom_level
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                zoom_level -= zoom_step
                zoom_level = max(0.0001, zoom_level)
            elif event.key == pygame.K_DOWN:
                zoom_level += zoom_step
                zoom_level = max(0.0001, zoom_level)
            elif event.key == pygame.K_LEFT:
                zoom_step -= 0.001
                zoom_step = max(0.001, zoom_step)
            elif event.key == pygame.K_RIGHT:
                zoom_step += 0.001
                zoom_step = max(0.001, zoom_step)
            elif event.key == pygame.K_SPACE:
                render_quadtree = not render_quadtree
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                zoom_level -= zoom_step  # Scroll up = zoom in
                zoom_level = max(0.0001, zoom_level)
            elif event.y < 0:
                zoom_level += zoom_step  # Scroll down = zoom out
                zoom_level = max(0.0001, zoom_level)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                dragging = True
                #print("M Down")
                last_mouse_pos = (pygame.Vector2(pygame.mouse.get_pos()))
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                #print("M Up")

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                movement = ((mouse_pos) - (last_mouse_pos))
                current_offset += movement
                Rend.set_Offset(current_offset)
                last_mouse_pos = mouse_pos


    Rend.set_zoom(zoom_level)
    delta_time = clock.tick(60)/1000
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
        nested_pixel_array = universe_tick(pixelArray,array, tree, lineHistory, delta_time)  # Runs the model of the simulation based on the leaf array
        SIZE = tree.rootSize
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
        leafList, tree, lineHistory = redrawQuadTree(pixelArray, SIZE)  #Draws out the quadtree and creates the game window, returns the leaf array
        SIZE = tree.rootSize
        #collision_with_quadtree(tree, leafList, pixelArray) #Run collision first to prevent=
        universe_tick(pixelArray,leafList, tree, lineHistory, delta_time)  # Runs the model of the simulation based on the leaf array
        SIZE = tree.rootSize
        #collision_tick(pixelArray, nested_pixel_array)  # Currently disabled for visuals
        #Rend.scale_world(screen, .5)   #Use this for the minimap, will have to come back to it though

    text_arr = [
    f'Total Planets: {len(pixelArray)}',
    f'Max: {tree.max}',
    f'Theta: {threshold_angle}',
    f'FPS: {clock.get_fps():.2f}',
    f'RootSize: {tree.rootSize}'

    ]
    Rend.render_UI(screen, (0,0), text_arr, True)
    text_arr = [f'Furthest_Point: {tree.find_furthest_point_from_center(pixelArray).position}',
    f'Zoom_Level: {zoom_level}',
    f'Zoom_Step:  {zoom_step}']
    Rend.render_UI(screen, (0, 0), text_arr, False)

    pygame.display.flip()



if telemetry_enabled:
    print(f'Total QuadTree time: {total_quadTree_time} milliseconds')
    print(f'Total Tick time: {total_tick_time} milliseconds')
    print(f'Total Collision time: {total_collision_time} milliseconds')
    total_time = total_quadTree_time+total_tick_time+total_collision_time
    print(f'Total Operational time: {total_time} milliseconds')
    print(f'Total Operations: {total_operations} ticks')
    print("----------------------------------------------------")
    print(f'Ratio between total Quadtree and Universe Ticks: {(total_tick_time/total_quadTree_time)}x more universe ticks')
    print(f'Average FPS(Frames per second): {1000/(total_tick_time/total_operations)} FPS')
