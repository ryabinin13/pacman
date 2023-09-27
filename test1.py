# Импортируем необходимые библиотеки
import pygame
import random
import math

# Инициализируем Pygame
pygame.init()

# Устанавливаем размер окна
screen_width = 800
screen_height = 600

# Создаем окно
screen = pygame.display.set_mode((screen_width, screen_height))

# Задаем цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


# Создаем класс для Пакмана
class Pacman:
    def __init__(self, x, y):
        # Задаем начальные координаты и скорость
        self.x = x
        self.y = y
        self.speed = 0.1
        # Задаем начальное направление
        self.direction = "right"
        # Задаем радиус Пакмана
        self.radius = 20

    def move(self):
        # Перемещаем Пакмана в соответствии с его направлением
        if self.direction == "right" and self.x < screen_width - self.speed:
            self.x += self.speed
        elif self.direction == "left" and self.x > self.speed:
            self.x -= self.speed
        elif self.direction == "up" and self.y > self.speed:
            self.y -= self.speed
        elif self.direction == "down" and self.y < screen_height - self.speed:
            self.y += self.speed

    def draw(self):
        # Рисуем Пакмана на экране
        pygame.draw.circle(screen, yellow, (self.x, self.y), self.radius)

    # Создаем класс для точек


class Dot:
    def __init__(self, x, y):
        # Задаем координаты точки и ее радиус
        self.x = x
        self.y = y
        self.radius = 5

    def draw(self):
        # Рисуем точку на экране
        pygame.draw.circle(screen, white, (self.x, self.y), self.radius)

    # Создаем список точек


dots = []
for i in range(50):
    # Генерируем случайные координаты для каждой точки
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    dot = Dot(x, y)
    dots.append(dot)

# Создаем Пакмана и расставляем его на экране
pacman = Pacman(screen_width / 2, screen_height / 2)

# Устанавливаем флаг окончания игры
game_over = False

# Запускаем игровой цикл
while not game_over:
    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Если пользователь закрыл окно, то завершаем игру
            game_over = True
        elif event.type == pygame.KEYDOWN:
            # Если пользователь нажал клавишу, то меняем направление Пакмана
            if event.key == pygame.K_RIGHT:
                pacman.direction = "right"
            elif event.key == pygame.K_LEFT:
                pacman.direction = "left"
            elif event.key == pygame.K_UP:
                pacman.direction = "up"
            elif event.key == pygame.K_DOWN:
                pacman.direction = "down"

                # Очищаем экран
    screen.fill(black)

    # Рисуем точки
    for dot in dots:
        dot.draw()
        # Проверяем, столкнулся ли Пакман с точкой
        if math.sqrt((dot.x - pacman.x)*2 + (dot.y - pacman.y)*2) < (pacman.radius + dot.radius):
            # Если да, то удаляем точку из списка
            dots.remove(dot)

            # Перемещаем Пакмана и рисуем его на экране
    pacman.move()
    pacman.draw()

    # Обновляем экран
    pygame.display.update()

# Выходим из Pygame
pygame.quit()