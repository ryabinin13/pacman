import pygame
import random
import itertools
import numpy as np
import math
pygame.init()

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.direction = 'k'
    def draw(self):
        pygame.draw.circle(sc, (255,255,0), (self.x, self.y), self.size)
    def move(self):
        if self.direction == 'up':
            self.y-= SIZE_ONE_CELL
        elif self.direction == 'down':
            self.y+=SIZE_ONE_CELL
        elif self.direction == 'right':
            self.x+=SIZE_ONE_CELL
        elif self.direction == 'left':
            self.x-=SIZE_ONE_CELL
    def clear(self):
        pygame.draw.circle(sc, (0, 0, 0), (self.x, self.y), self.size)

pacman = Pacman(315,315)

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
    def draw(self):
        pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))

SIZE = 600
FPS = 60
SIZE_ONE_CELL = 30
COUNT_OF_WALL =5
COUNT_OF_AWARDS = 10

sc = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('pacman')
clock = pygame.time.Clock()

for i in range(SIZE):
    if i % SIZE_ONE_CELL == 0:
        pygame.draw.line(sc, (255,0,255), (0,i),(SIZE,i), 1)
        pygame.draw.line(sc, (255, 0, 255), (i,0), (i,SIZE), 1)

walls = []
for j in range(0, COUNT_OF_WALL):
    random_XY = [random.randint(0, SIZE) for i in range(2)]
    random_XY = [random_XY[i] - random_XY[i] % SIZE_ONE_CELL for i in range(2)]

    walls.append(random_XY)

    pygame.draw.rect(sc, (200,200,200), (random_XY[0], random_XY[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
    random_right, random_left, random_up, random_down = [random.randint(0,10) for _ in range(4)]

    for r in range(1, random_right):
        coord = [random_XY[0] + r * SIZE_ONE_CELL, random_XY[1]]
        if coord[0] > SIZE-100:
            continue
        pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
        walls.append(coord)
    for l in range(1, random_left):
        coord = [random_XY[0] -l * SIZE_ONE_CELL, random_XY[1]]
        if coord[0] < 0+100:
            continue
        pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
        walls.append(coord)
    for u in range(1, random_up):
        coord = [random_XY[0], random_XY[1] -u * SIZE_ONE_CELL]
        if coord[1] < 0+100:
            continue
        pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
        walls.append(coord)
    for d in range(1, random_down):
        coord = [random_XY[0], random_XY[1] +d * SIZE_ONE_CELL]
        if coord[1] > SIZE-100:
            continue
        pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
        walls.append(coord)

walls_unique = list(set(tuple(w) for w in walls))

for awards in range(COUNT_OF_AWARDS):
    cross = False
    random_XY = [random.randint(0, SIZE) for i in range(2)]
    random_XY = [random_XY[i] - random_XY[i] % SIZE_ONE_CELL for i in range(2)]
    for wall in walls:
        if random_XY == wall:
            cross = True
            break
    if cross == False:
        random_XY = [random_XY[i] + SIZE_ONE_CELL/2 for i in range(2)]
        pygame.draw.circle(sc, (50, 100, 150), (random_XY[0], random_XY[1]), SIZE_ONE_CELL / 4)

for i in range(SIZE):
    if i % SIZE_ONE_CELL == 0:
        pygame.draw.line(sc, (255,0,255), (0,i),(SIZE,i), 1)
        pygame.draw.line(sc, (255, 0, 255), (i,0), (i,SIZE), 1)

print(len(walls_unique))

pacman.draw()

pygame.display.flip()
while True:
     for event in pygame.event.get():
         if event.type == pygame.QUIT:
             exit()
         elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_RIGHT:
                 pacman.direction = 'right'
     pacman.move()
     pacman.draw()