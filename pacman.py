import time
import pygame
import random
import math
pygame.init()

score = 0 #счетчик очков
game_over_font = pygame.font.SysFont("Arial", 60)

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.direction = 'right'
        self.visibility = 75

    def draw(self):
        pygame.draw.circle(sc, (255,255,0), (self.x + SIZE_ONE_CELL/2, self.y + SIZE_ONE_CELL/2), self.size)
    def move(self):
        pygame.draw.circle(sc, (0, 0, 0), (self.x + SIZE_ONE_CELL/2, self.y + SIZE_ONE_CELL/2), self.size)
        if self.direction == 'up':
            for wall in walls:
                if self.y - SIZE_ONE_CELL == wall[1] and self.x == wall[0]:
                    return
            if self.y == 0:
                return
            self.y -= SIZE_ONE_CELL
        elif self.direction == 'down':
            for wall in walls:
                if self.y + SIZE_ONE_CELL == wall[1] and self.x == wall[0]:
                    return
            if self.y == SIZE - SIZE_ONE_CELL:
                return
            self.y += SIZE_ONE_CELL
        elif self.direction == 'right':
            for wall in walls:
                if self.y == wall[1] and self.x + SIZE_ONE_CELL == wall[0]:
                    return
            if self.x ==SIZE-SIZE_ONE_CELL:
                return
            self.x += SIZE_ONE_CELL
        elif self.direction == 'left':
            for wall in walls:
                if self.y == wall[1] and self.x - SIZE_ONE_CELL == wall[0]:
                    return
            if self.x == 0:
                return
            self.x -= SIZE_ONE_CELL

#считываю из файла координаты стен
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

COUNT_OF_CELL = 11
SIZE_ONE_CELL = 50
SIZE = COUNT_OF_CELL * SIZE_ONE_CELL
COUNT_OF_WALL =8
COUNT_OF_AWARDS = 50

pacman = Pacman(SIZE/2 - SIZE_ONE_CELL/2, SIZE/2 - SIZE_ONE_CELL/2)

sc = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('pacman')

#добавляем стены
random_number_of_maps = random.randint(1,100)
walls_ = read_list_from_line('maps.txt', random_number_of_maps)
walls = []
#for w in walls_:
#   walls.append(list(w))

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
    for aw in awards:
        if random_XY[1] == aw[1] and random_XY[0] == aw[0]:
            cross = True
    if random_XY[0] == pacman.x and random_XY[1] == pacman.y:
        cross = True
    if cross == False:
        awards.append([random_XY[0], random_XY[1]])
        a += 1

def score_count():
    global score
    for a in awards:
        if(int(a[0]) == pacman.x and int(a[1]) == pacman.y):
            awards.remove(a)
            score += 1
    score_text = score_font.render("Счёт: {}".format(score), True, (255, 255, 255))  # для отображения
    sc.blit(score_text, (2, 2))

pacman.draw()
def create_map():
    #строю стены
    for w in walls:
        pygame.draw.rect(sc, (200, 200, 200), (w[0], w[1], SIZE_ONE_CELL, SIZE_ONE_CELL))
    #строю награды
    for award in awards:
        pygame.draw.circle(sc, (50, 100, 150), (award[0] + SIZE_ONE_CELL / 2, award[1] + SIZE_ONE_CELL / 2), SIZE_ONE_CELL / 4)
    #строю клетки
    for i in range(SIZE):
        if i % SIZE_ONE_CELL == 0:
            pygame.draw.line(sc, (255, 0, 255), (0, i), (SIZE, i), 1)
            pygame.draw.line(sc, (255, 0, 255), (i, 0), (i, SIZE), 1)

fog_of_war = pygame.Surface((SIZE, SIZE))
fog_of_war.fill((0, 0, 0))
def visibility():
    pygame.draw.rect(fog_of_war, (60, 60, 60), (pacman.x + 25-pacman.visibility, pacman.y + 25-pacman.visibility,pacman.visibility*2, pacman.visibility*2), 0)
    fog_of_war.set_colorkey((60, 60, 60))
    sc.blit(fog_of_war, (0, 0))
    pygame.display.flip()

map = [[i, j, 0] for i in range(SIZE) for j in range(SIZE) if (i % SIZE_ONE_CELL == 0) and (j % SIZE_ONE_CELL == 0)]

def clear_fog(m):
    if walls.count([m[0], m[1]]):
        m[2] = 2
    elif awards.count([m[0], m[1]]):
        m[2] = 3
    else:
        m[2] = 1
for m in map:
    if [m[0], m[1]] in [[200, 200], [250, 200], [300, 200], [200, 250], [250, 250], [300, 250], [200, 300], [250, 300], [300, 300]]:
        clear_fog(m)

for i in range(SIZE // SIZE_ONE_CELL):
    for j in range(0, len(map), SIZE // SIZE_ONE_CELL):
        print(map[i+j][2], end=" ")
    print()
print()
def alghoritm_move():
    three = []
    for m in map:
        if m[2] == 3:
            move = []
            move_x = int((m[0] - pacman.x)/SIZE_ONE_CELL)
            move_y = int((m[1] - pacman.y)/SIZE_ONE_CELL)
            if move_x < 0:
                for x in range(abs(move_x)):
                    move.append('l')
            if move_x > 0:
                for x in range(abs(move_x)):
                    move.append('r')
            if move_y < 0:
                for x in range(abs(move_y)):
                    move.append('u')
            if move_y > 0:
                for x in range(abs(move_y)):
                    move.append('d')
            move.append(m)
            three.append(move)
    best_way = []
    if three:
        best_way = min(three, key=len)
        best_way[-1][2] = 1
        best_way.pop()
    else:
        random_way = random.randint(1, 4)
        if random_way == 1:
            best_way.append('r')
        if random_way == 2:
            best_way.append('l')
        if random_way == 3:
            best_way.append('u')
        if random_way == 4:
            best_way.append('d')
    currentXY = [pacman.x, pacman.y]
    for bv in best_way:
        if bv == 'l':
            for m in map:
                if [m[0], m[1]] in [[currentXY[0] * SIZE_ONE_CELL, currentXY[1]], [currentXY[0] - 2 * SIZE_ONE_CELL, currentXY[1] - SIZE_ONE_CELL], [currentXY[0] - 2 * SIZE_ONE_CELL, currentXY[1] + SIZE_ONE_CELL]]:
                    clear_fog(m)
            currentXY[0] = currentXY[0] - SIZE_ONE_CELL
        elif bv == 'r':
            for m in map:
                if [m[0], m[1]] in [[currentXY[0] + 2 * SIZE_ONE_CELL, currentXY[1]], [currentXY[0] + 2 * SIZE_ONE_CELL, currentXY[1] - SIZE_ONE_CELL], [currentXY[0] + 2 * SIZE_ONE_CELL, currentXY[1] + SIZE_ONE_CELL]]:
                    clear_fog(m)
            currentXY[0] = currentXY[0] + SIZE_ONE_CELL
        elif bv == 'u':
            for m in map:
                if [m[0], m[1]] in [[currentXY[0], currentXY[1] - 2 * SIZE_ONE_CELL], [currentXY[0] - SIZE_ONE_CELL, currentXY[1] - 2 * SIZE_ONE_CELL], [currentXY[0] + SIZE_ONE_CELL, currentXY[1] - 2* SIZE_ONE_CELL]]:
                    clear_fog(m)
            currentXY[1] = currentXY[1] - SIZE_ONE_CELL
        elif bv == 'd':
            for m in map:
                if [m[0], m[1]] in [[currentXY[0], currentXY[1] + 2 * SIZE_ONE_CELL], [currentXY[0] - SIZE_ONE_CELL, currentXY[1] + 2 * SIZE_ONE_CELL], [currentXY[0] + SIZE_ONE_CELL, currentXY[1] + 2 * SIZE_ONE_CELL]]:
                    clear_fog(m)
            currentXY[1] = currentXY[1] + SIZE_ONE_CELL
    for i in range(SIZE // SIZE_ONE_CELL):
        for j in range(0, len(map), SIZE // SIZE_ONE_CELL):
            print(map[i+j][2], end=" ")
        print()
    print()
    return best_way

create_map()
visibility()
pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if score == COUNT_OF_AWARDS:
            time.sleep(1)
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pacman.direction = "right"
                pacman.move()
                create_map()
                visibility()
            elif event.key == pygame.K_LEFT:
                pacman.direction = "left"
                pacman.move()
                create_map()
                visibility()
            elif event.key == pygame.K_UP:
                pacman.direction = "up"
                pacman.move()
                create_map()
                visibility()
            elif event.key == pygame.K_DOWN:
                pacman.direction = "down"
                pacman.move()
                create_map()
                visibility()
            elif event.key == pygame.K_SPACE:
                for i in range(200):
                    move = alghoritm_move()
                    for m in move:
                        directions = {'r' : "right", 'l' :"left", 'u':"up", 'd':"down"}
                        pacman.direction = directions[m]
                        pacman.move()
                        create_map()
                        visibility()
                        score_count()
                        pacman.draw()
                        pygame.display.flip()
                        pygame.time.delay(200)
    pygame.draw.rect(sc, (0, 0, 0), (2, 2, 90, 25))
    score_count()
    pacman.draw()
    pygame.display.flip()
