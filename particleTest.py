import math

from QuadTree import QuadTree
import pygame

from pixel import pixel

backColor = (255, 255, 255)
resolution = (width, height) = (2560, 1440)   #This doesn't play with all systems well, but works as a test
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Barnes-Hut')
screen.fill(backColor)
dotSize = 3


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
    minPoint = QuadTree.find_furthest_Point(alignPoints(pixelArray))
    maxPoint = QuadTree.find_closest_Point(alignPoints(pixelArray), resolution)
    print(f'minPoint: {minPoint}, maxPoint: {maxPoint}')
    #tree = QuadTree(minPoint, minPoint, resolution[0], resolution[1], alignPoints(pixelArray), screen, 0)  #Change Points to Align Points
    tree = QuadTree(minPoint, minPoint, maxPoint, maxPoint, alignPoints(pixelArray), screen, 0)  # Change Points to Align Points
    tree.drawPoints(10)
    tree.subDivide(0)
    array = QuadTree.helperDFS3(tree, tree)    #Should contain all the relevant data from the struct
    #print(f'Type: {type(array)}: Length {len(array)}')

    #for x in array:
    #    print(f'Coords: {(x.getPoints())}')
    #print()

    return array


#Testing more "efficient" method however results are varied
def gravitational_calculation_faster(g, nested_pixel_array):
    # Step 1: Compute intra-cluster (nearby planets) brute force gravity
    print(nested_pixel_array)
    print()
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
        cluster_coms.append(pixel(com_mass, com_pos, (0,0), 0, False))

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

    #print("Ticked Gravity")
    return "Done"

def gravitational_calculation2(g, nested_pixel_array):
    for x in nested_pixel_array:     #x represents every grouping of planets
        for z in nested_pixel_array: #z also represents every grouping of planets
            for y in x:
                if(x == z):             #For nearby planets, we brute-force the calculation
                    for h in x:     #y represents every planet in a grouping
                        if(y != h):
                            y.gravity(g, y, h)
                if(x != z):             #For far off planets, we estimate based on COM and go from there
                    for y in x:
                        tempPixel = pixel(pixel.return_list_mass(z), findCenterOfMass(z)
                                          , (0, 0), 0, False)  #Creates a temporary planet obj to utilize easy gravity
                        y.gravity(g, y, tempPixel)  #Applies force on y
                y.applyForce()
            #print("Ticked Gravity")

    #for x in nested_pixel_array:    #Runs through at the end and applies the calculated for to all items in the pixelArray
    #    for y in x:
    #        y.applyForce()      #Applies for to each planet
    return "Done"

def gravitational_calculation(g, nested_pixel_array):
    #Calculate the force of Gravity for everything within the leaf
    #Estimates the rest of the universal force using far off leafs
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
    gravitational_constant = 6.67430e-11                       #Gravitational Constant [Set to 1 by default]
    gravitational_calculation2(gravitational_constant, nested_pixel_array)

    #print(array)

    return True

pixelArray = [
    pixel(121.4*100, (1275.3, 738.2), (0.2, -0.1), 0, True),
    pixel(162.8, (1290.5, 712.4), (-0.3, 0.1), 0, False),
    pixel(89.6, (1263.1, 734.9), (0.1, -0.4),  0, False ),
    pixel(101.2, (1293.7, 705.6), (-0.1, 0.2), 0, False),
    #pixel(195.3, (1279.0, 720.0), (0.0, 0.0), 0, False),
    pixel(72.5, (1301.8, 719.2), (-0.2, -0.3), 0, False)
    ]


'''
pixelArray = [
    pixel(121.4, (1275.3, 738.2), (0.2, -0.1), 0),
    pixel(162.8, (1290.5, 712.4), (-0.3, 0.1), 0),
    pixel(89.6, (1263.1, 734.9), (0.1, -0.4), 0),
    pixel(101.2, (1293.7, 705.6), (-0.1, 0.2), 0),
    pixel(195.3, (1279.0, 720.0), (0.0, 0.0), 0),
    pixel(72.5, (1301.8, 719.2), (-0.2, -0.3), 0),
    pixel(155.7, (1256.2, 741.7), (0.3, -0.2), 0),
    pixel(181.0, (1269.3, 700.4), (-0.4, 0.3), 0),
    pixel(94.3, (1298.1, 739.9), (0.1, 0.1), 0),
    pixel(137.9, (1283.5, 709.8), (-0.2, 0.4), 0),
    pixel(120.6, (1266.8, 715.5), (0.0, -0.1), 0),
    pixel(144.2, (1302.7, 725.6), (-0.3, 0.0), 0),
    pixel(110.8, (1287.6, 729.1), (0.1, 0.2), 0),
    pixel(133.4, (1270.9, 707.7), (-0.1, -0.1), 0),
    pixel(175000.5, (1281.1, 745.3), (0.2, 0.0), 0),
    pixel(69.9, (1304.2, 710.6), (-0.2, 0.1), 0),
    pixel(158.3, (1259.7, 726.4), (0.1, -0.2), 0),
    pixel(104.7, (1278.8, 698.2), (0.0, 0.3), 0),
    pixel(198.1, (1294.0, 733.3), (-0.4, -0.1), 0),
    pixel(88.0, (1273.6, 719.9), (0.0, 0.0), 0),
    pixel(112.5, (1299.9, 716.2), (-0.3, 0.2), 0),
    pixel(166.6, (1284.7, 701.1), (0.2, -0.3), 0),
    pixel(97.3, (1255.4, 707.8), (0.4, 0.1), 0),
    pixel(183.7, (1276.1, 735.5), (-0.1, 0.0), 0),
    pixel(141.9, (1305.6, 742.1), (-0.2, -0.2), 0),
    pixel(100.2, (1287.3, 711.4), (0.1, 0.3), 0),
    pixel(134.0, (1261.8, 714.0), (0.0, -0.1), 0),
    pixel(191.5, (1291.6, 727.2), (-0.3, 0.0), 0),
    pixel(118.9, (1279.9, 722.1), (0.0, 0.0), 0),
    pixel(102.4, (1282.2, 717.6), (0.1, -0.1), 0)
]
'''
points = [(30, 30), (30, 40), (30, 50), (40, 50), (60, 50),(65, 50), (70, 50),(63, 30), (63, 30), (190, 180), (200, 180), (180, 180), (160, 180)]


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
    array = redrawQuadTree(pixelArray)  #Draws out the quadtree and creates the game window, returns leaf array
    end_ticks = pygame.time.get_ticks()
    print(f"Quadtree time: {(end_ticks - start_ticks)} milliseconds")


    pygame.init()
    start_ticks = pygame.time.get_ticks()
    universe_tick(pixelArray, array)             #Runs the model of the simulation based on the leaf array
    end_ticks = pygame.time.get_ticks()
    print(f"Tick time: {(end_ticks - start_ticks)} milliseconds")


    pygame.display.flip()