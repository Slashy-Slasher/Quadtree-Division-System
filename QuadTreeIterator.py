from QuadTree import QuadTree
import pygame



width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
points = [(30, 30), (30, 40), (30, 50), (40, 50), (60, 50),(65, 50), (70, 50),(63, 30), (63, 30), (190, 180), (200, 180), (180, 180), (160, 180)]
tree = QuadTree(0, 0, width, height, points, screen, 0)  #Change Points to Align Points
tree.subDivide(0)

previous_node = None
currentNode = tree
current_level = 0

def preview(currentNode, current_level):
    print(f'Current level: {current_level}')
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
        currentNode = descend(tree, currentNode, int(input("1-4")))
        current_level += 1
    else:
        currentNode = ascend()
        current_level -= 1
    preview(currentNode, current_level)

def descend(tree, currentNode, branch):
    previous_node = currentNode
    if(branch == 1):
        currentNode = currentNode.TLC
    if(branch == 2):
        currentNode = currentNode.TRC
    if(branch == 3):
        currentNode = currentNode.BLC
    if(branch == 4):
        currentNode = currentNode.BRC
    return currentNode

def ascend():
    currentNode = previous_node
    return currentNode

#print(type(currentNode))
#print(currentNode.getPoints())
preview(currentNode, current_level)