import random
from Render import Render

from QuadTree import QuadTree
import pygame

from pixel import pixel

resolution = width, height = 1000, 1000
SIZE = 1000
screen = pygame.display.set_mode((width, height))
points = [(30, 30), (30, 40), (30, 50), (40, 50), (60, 50),(65, 50), (70, 50),(63, 30), (63, 30), (190, 180), (200, 180), (180, 180), (160, 180)]

sun_mass = 1000000
pixelArray = [
    pixel(sun_mass, (resolution[0] / 2, resolution[1] / 2), (1, 0), 0, (255, 255, 0), 100, True),
    #pixel(sun_mass, (resolution[0] / 2 + 3500, resolution[1] / 2 - 3500), (-1, 0), 0, (255, 255, 0), 100, True),
]

# Add 30 random test planets
for _ in range(30):
    x = resolution[0] / 2 + random.randint(-500, 500)
    y = resolution[1] / 2 + random.randint(-500, 500)
    dx = random.uniform(-1, 1)
    dy = random.uniform(-1, 1)
    mass = random.randint(10, 200)
    diameter = random.randint(5, 20)
    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    locked = False
    pixelArray.append(pixel(mass, (x, y), (dx, dy), 0, color, diameter, locked))

print(len(pixelArray))
tree = QuadTree(-SIZE, -SIZE, SIZE, SIZE, QuadTree.alignPoints(pixelArray), screen, 0, True, 1, pixelArray)  #Change Points to Align Points
tree.subDivide(0)

screen.fill((0, 0, 0))  # <<< Clear the screen here
rend = Render("Name")
rend.renderPlanets(screen, pixelArray, 0, 1)
pygame.display.flip()
previous_node = None
currentNode = tree
current_level = 0

def preview(currentNode, current_level):
    print(f'Current level: {current_level}')
    print(currentNode.mass)
    if(currentNode.TLC is not None):
        print(currentNode.TLC.getPoints())
    else:
        print("No TLC")

    if(currentNode.TRC is not None):
        print(currentNode.TRC.getPoints())
    else:
        print("No TRC")

    if (currentNode.BLC is not None):
        print(currentNode.BLC.getPoints())
    else:
        print("No BLC")

    if (currentNode.BRC is not None):
        print(currentNode.BRC.getPoints())
    else:
        print("No BRC")
    print()
    if(int(input("1-2")) == 1):
        currentNode = descend(currentNode, int(input("1-4")))
        current_level += 1
    else:
        currentNode = ascend(currentNode)
        current_level -= 1
    preview(currentNode, current_level)

def descend(currentNode, branch):
    if(branch == 1):
        currentNode = currentNode.TLC
    if(branch == 2):
        currentNode = currentNode.TRC
    if(branch == 3):
        currentNode = currentNode.BLC
    if(branch == 4):
        currentNode = currentNode.BRC
    return currentNode

def ascend(currentNode):
    if(currentNode.parent_node is not None):
        currentNode = currentNode.parent_node
    return currentNode

#print(type(currentNode))
#print(currentNode.getPoints())
preview(currentNode, current_level)