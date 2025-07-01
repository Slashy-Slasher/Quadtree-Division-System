from QuadTree import QuadTree
import pygame

from Particle import Particle

backColor = (255, 255, 255)
resolution = (width, height) = (500, 300)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Barnes-Hut')
screen.fill(backColor)
dotSize = 5


def updateParticles():

    print()


def alignPoints(ParticleArray):
    points = []
    for x in ParticleArray:
        points.append(x.getPosition())
    print(ParticleArray)
    print(points)
    return points


def redrawQuadTree(ParticleArray):
    tree = QuadTree(0, 0, resolution[0], resolution[1], alignPoints(ParticleArray), screen, 0)  #Change Points to Align Points
    tree.drawPoints(5)
    tree.subDivide(0)
    array = tree.helperDFS(tree)
    return array


def universalGravity(g, ParticleArray):



    return



#Test batch of the Particle array
ParticleArray = [Particle(100, (0, 40), (0, 0), 1), Particle(100, (60, 59), (0, 0), 1), Particle(100, (0, 5), (0, 0), 1), Particle(100, (0, 100), (0, 0), 1),Particle(100, (0, 450), (0, 0), 1)]
#points = [(30, 30), (30, 40), (30, 50), (40, 50), (60, 50),(65, 50), (70, 50),(63, 30), (63, 30), (190, 180), (200, 180), (180, 180), (160, 180)]






pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        redrawQuadTree(ParticleArray)