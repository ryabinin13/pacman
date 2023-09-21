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
        self.direction = 'right'
    def draw(self):
        pygame.draw.circle(sc, (255,255,0), (self.x, self.y), self.size)
    def move(self):
        pygame.draw.circle(sc, (0, 0, 0), (self.x, self.y), self.size)
        if self.direction == 'up':
            # Проверяем, есть ли стена на пути движения вверх
            for wall in walls:
                if self.y - self.size >= wall[1]  and self.y - self.size <= wall[1] + 60 and self.x >= wall[0] and self.x <= wall[0] + 30:
                    return
            # Если стены нет, то изменяем координату y
            if self.y > 0:
                self.y -= SIZE_ONE_CELL
        elif self.direction == 'down':
            # Проверяем, есть ли стена на пути движения вниз
            for wall in walls:
                if self.y + self.size >= wall[1] - 30 and self.y + self.size <= wall[1] + 30 and self.x >= wall[0] and self.x <= wall[0] + 30:
                    return
            # Если стены нет, то изменяем координату y
            if self.y < SIZE - self.size:
                self.y += SIZE_ONE_CELL
        elif self.direction == 'right':
            # Проверяем, есть ли стена на пути движения вправо
            for wall in walls_unique:
                if self.x + self.size >= wall[0] - 30 and self.x + self.size <= wall[0] + 30 and self.y >= wall[1] and self.y <= wall[1] +30:
                    return
            # Если стены нет, то изменяем координату x
            if self.x < SIZE - self.size:
                self.x += SIZE_ONE_CELL
        elif self.direction == 'left':
            # Проверяем, есть ли стена на пути движения влево
            for wall in walls_unique:
                if self.x - self.size >= wall[0] and self.x - self.size <= wall[0] + 60 and self.y >= wall[1] and self.y <= wall[1] + 30:
                    return
            # Если стены нет, то изменяем координату x
            if self.x > 0:
                self.x -= SIZE_ONE_CELL


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
        if coord[0] > SIZE:
            continue
        pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
        walls.append(coord)
    for l in range(1, random_left):
        coord = [random_XY[0] -l * SIZE_ONE_CELL, random_XY[1]]
        if coord[0] < 0:
            continue
        pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
        walls.append(coord)
    for u in range(1, random_up):
        coord = [random_XY[0], random_XY[1] -u * SIZE_ONE_CELL]
        if coord[1] < 0:
            continue
        pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
        walls.append(coord)
    for d in range(1, random_down):
        coord = [random_XY[0], random_XY[1] +d * SIZE_ONE_CELL]
        if coord[1] > SIZE:
            continue
        pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
        walls.append(coord)

walls_unique = list(set(tuple(w) for w in walls))

i = 0
while i < COUNT_OF_AWARDS:
    random_XY = [random.randint(0, SIZE) for i in range(2)]
    pygame.draw.circle(sc, (50, 100, 150), (random_XY[0], random_XY[1]), SIZE_ONE_CELL / 4)

    i = i +1


for i in range(SIZE):
    if i % SIZE_ONE_CELL == 0:
        pygame.draw.line(sc, (255,0,255), (0,i),(SIZE,i), 1)
        pygame.draw.line(sc, (255, 0, 255), (i,0), (i,SIZE), 1)

print(len(walls_unique))

pacman.draw()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pacman.direction = "right"
                pacman.move()
            elif event.key == pygame.K_LEFT:
                pacman.direction = "left"
                pacman.move()
            elif event.key == pygame.K_UP:
                pacman.direction = "up"
                pacman.move()
            elif event.key == pygame.K_DOWN:
                pacman.direction = "down"
                pacman.move()
    pacman.draw()
    pygame.display.flip()
