import math
import time
import pygame
import random
pygame.init()

score = 0 #счетчик очков
game_over_font = pygame.font.SysFont("Arial", 60)

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.direction = 'right'
    def draw(self):
        pygame.draw.circle(sc, (255,255,0), (self.x, self.y), self.size)
    def move(self):
        pygame.draw.circle(sc, (0, 0, 0), (self.x, self.y), self.size)
        if self.direction == 'up':
            # Проверяем, есть ли стена на пути движения вверх
            for wall in walls:
                if self.y - self.size >= wall[1]  and self.y - self.size <= wall[1] + SIZE_ONE_CELL*2 and self.x >= wall[0] and self.x <= wall[0] + SIZE_ONE_CELL:
                    return
            if self.y <= SIZE_ONE_CELL:
                return
            # Если стены нет, то изменяем координату y
            if self.y > 0:
                self.y -= SIZE_ONE_CELL
        elif self.direction == 'down':
            # Проверяем, есть ли стена на пути движения вниз
            for wall in walls:
                if self.y + self.size >= wall[1] - SIZE_ONE_CELL and self.y + self.size <= wall[1] + SIZE_ONE_CELL and self.x >= wall[0] and self.x <= wall[0] + SIZE_ONE_CELL:
                    return
            if self.y >=SIZE-SIZE_ONE_CELL:
                return
            # Если стены нет, то изменяем координату y
            if self.y < SIZE - self.size:
                self.y += SIZE_ONE_CELL
        elif self.direction == 'right':
            # Проверяем, есть ли стена на пути движения вправо
            for wall in walls:
                if self.x + self.size >= wall[0] - SIZE_ONE_CELL and self.x + self.size <= wall[0] + SIZE_ONE_CELL and self.y >= wall[1] and self.y <= wall[1] +SIZE_ONE_CELL:
                    return
            if self.x >=SIZE-SIZE_ONE_CELL:
                return
            # Если стены нет, то изменяем координату x
            if self.x < SIZE - self.size:
                self.x += SIZE_ONE_CELL
        elif self.direction == 'left':
            # Проверяем, есть ли стена на пути движения влево
            for wall in walls:
                if self.x - self.size >= wall[0] and self.x - self.size <= wall[0] + SIZE_ONE_CELL*2 and self.y >= wall[1] and self.y <= wall[1] + SIZE_ONE_CELL:
                    return
            if self.x <=SIZE_ONE_CELL:
                return
            # Если стены нет, то изменяем координату x
            if self.x > 0:
                self.x -= SIZE_ONE_CELL

def add_data_to_file(data, filename):
    try:
        with open(filename, 'a') as file:
            for d in data:
                file.write(str(d) + ' ')
            file.write('\n')
    except:
        print("Ошибка")

def read_list_from_line(filename, line_number, separator=' '):
    result = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            line = lines[line_number-1].strip()
            list_data = line.split(separator)
            formatted_list = [x for x in list_data]
            for item in formatted_list:
                item = item.replace('[', '').replace(']', '')
                result.append(item)
                res = [int(item.replace(',', '')) for item in result]
                r = list(zip(res[::2], res[1::2]))
            return r

    except:
        print("Ошибка")

def check_block(walls, random_XY):
    for w1 in walls:
        if (random_XY[0] - SIZE_ONE_CELL == w1[0]) and (random_XY[1] == w1[1]):
            for w2 in walls:
                if (random_XY[0] - SIZE_ONE_CELL == w2[0]) and (random_XY[1] - SIZE_ONE_CELL == w2[1]):
                    for w3 in walls:
                        if (random_XY[0] == w3[0]) and (random_XY[1] - SIZE_ONE_CELL == w3[1]):
                            return True
            for w4 in walls:
                if (random_XY[0] - SIZE_ONE_CELL == w4[0]) and (random_XY[1] + SIZE_ONE_CELL == w4[1]):
                    for w5 in walls:
                        if (random_XY[0] == w5[0]) and (random_XY[1] + SIZE_ONE_CELL == w5[1]):
                            return True
    for w6 in walls:
        if (random_XY[0] + SIZE_ONE_CELL == w6[0]) and (random_XY[1] == w6[1]):
            for w7 in walls:
                if (random_XY[0] + SIZE_ONE_CELL == w7[0]) and (random_XY[1] - SIZE_ONE_CELL == w7[1]):
                    for w8 in walls:
                        if (random_XY[0] == w8[0]) and (random_XY[1] - SIZE_ONE_CELL == w8[1]):
                            return True
            for w9 in walls:
                if (random_XY[0] + SIZE_ONE_CELL == w9[0]) and (random_XY[1] + SIZE_ONE_CELL == w9[1]):
                    for w10 in walls:
                        if (random_XY[0] == w10[0]) and (random_XY[1] + SIZE_ONE_CELL == w10[1]):
                            return True
    return False


FPS = 60
COUNT_OF_CELL = 11
SIZE_ONE_CELL = 50
SIZE = COUNT_OF_CELL * SIZE_ONE_CELL
COUNT_OF_WALL =8
COUNT_OF_AWARDS = 10

pacman = Pacman(SIZE/2, SIZE/2)
sc = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('pacman')
clock = pygame.time.Clock()

walls = []
#строим стены

for j in range(0, COUNT_OF_WALL):
    random_XY = [random.randint(0, SIZE) for i in range(2)]
    random_XY = [random_XY[i] - random_XY[i] % SIZE_ONE_CELL for i in range(2)]


    if check_block(walls, random_XY) == False:
        walls.append(random_XY)
        pygame.draw.rect(sc, (200,200,200), (random_XY[0], random_XY[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
        random_right, random_left, random_up, random_down = [random.randint(0,4) for _ in range(4)]


    for r in range(1, random_right):
        coord = [random_XY[0] + r * SIZE_ONE_CELL, random_XY[1]]
        if coord[0] > SIZE-SIZE_ONE_CELL:
            continue
        elif check_block(walls, coord) == False:
            pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
            walls.append(coord)

    for l in range(1, random_left):
        coord = [random_XY[0] -l * SIZE_ONE_CELL, random_XY[1]]
        if coord[0] < 0+SIZE_ONE_CELL:
            continue
        elif check_block(walls, coord) == False:
            pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
            walls.append(coord)
    for u in range(1, random_up):
        coord = [random_XY[0], random_XY[1] -u * SIZE_ONE_CELL]
        if coord[1] < 0+SIZE_ONE_CELL:
            continue
        elif check_block(walls, coord) == False:
            pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
            walls.append(coord)
    for d in range(1, random_down):
        coord = [random_XY[0], random_XY[1] +d * SIZE_ONE_CELL]
        if coord[1] > SIZE-SIZE_ONE_CELL:
            continue
        elif check_block(walls, coord) == False:
            pygame.draw.rect(sc, (200, 200, 200), (coord[0], coord[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
            walls.append(coord)



#walls_ = read_list_from_line('maps.txt', 8)
#walls = []
#for w in walls_:
#    walls.append(list(w))
walls_unique = list(set(tuple(w) for w in walls))
print(len(walls_unique))

for w in walls:
    pygame.draw.rect(sc, (200,200,200), (w[0], w[1], SIZE_ONE_CELL, SIZE_ONE_CELL))

#строим награды
awards = []
score_font = pygame.font.SysFont("Arial", 24)
a = 0
while( a != COUNT_OF_AWARDS ):
    cross = False
    random_XY = [random.randint(0, SIZE) for i in range(2)]
    random_XY = [int(random_XY[i] - random_XY[i] % SIZE_ONE_CELL) for i in range(2)]
    for wall in walls:
        if random_XY == wall:
            cross = True
    if a != 0:
        if awards[a-1] == random_XY:
           cross = True
    if cross == False:
        random_XY = [int(random_XY[i] + SIZE_ONE_CELL/2) for i in range(2)]
        pygame.draw.circle(sc, (50, 100, 150), (random_XY[0], random_XY[1]), SIZE_ONE_CELL / 4)
        awards.append((random_XY[0], random_XY[1]))
        a += 1
#строим клетки
for i in range(SIZE):
    if i % SIZE_ONE_CELL == 0:
        pygame.draw.line(sc, (255,0,255), (0,i),(SIZE,i), 1)
        pygame.draw.line(sc, (255, 0, 255), (i,0), (i,SIZE), 1)

def score_count():
    global score
    for a in awards:
        if(int(a[0]) == pacman.x and int(a[1]) == pacman.y):
            awards.remove(a)
            score += 1
    score_text = score_font.render("Счёт: {}".format(score), True, (255, 255, 255))  # для отображения
    sc.blit(score_text, (2, 2))

pacman.draw()

pygame.display.flip()
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
            elif event.key == pygame.K_s:
                add_data_to_file(walls, 'maps.txt')
    pygame.draw.rect(sc, (0, 0, 0), (2, 2, 90, 25))
    score_count()
    pacman.draw()
    pygame.display.flip()