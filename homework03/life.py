import pygame
from pygame.locals import *
import random
import copy
from typing import List


class GameOfLife:

    def __init__(self, width=400, height=400, cell_size=20, speed=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(
                'black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(
                'black'), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        self.clist = self.cell_list()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.clist)
            self.update_cell_list(self.clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True) -> List[list]:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1. 
        В противном случае клетка считается мертвой, то 
        есть ее значение равно 0.
        Если параметр randomize = True, то создается список, где
        каждая клетка может быть равновероятно живой или мертвой.
        """
        self.clist = []
        self.clist = [[0] * self.cell_width for i in range(self.cell_height)]
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    self.clist[i][j] = random.randint(0, 1)
        return self.clist

    def draw_cell_list(self, clist) -> None:
        """Отображение списка клеток 'rects' с закрашиванием их в 
        соответствующе цвета
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.clist[i][j] == 1:
                    color = pygame.Color('yellow')
                else:
                    color = pygame.Color('blue')
                pygame.draw.rect(self.screen, color, (j * self.cell_width + 1, i *
                                                      self.cell_height + 1, self.cell_size - 1, self.cell_size - 1))

    def get_neighbours(self, cell: tuple) -> list:
        """
        Вернуть список соседних клеток для клетки cell.

        Соседними считаются клетки по горизонтали,
        вертикали и диагоналям, то есть во всех
        направлениях.
        """
        neighbours = []
        x, y = cell
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i in range(0, self.cell_height) and j in range(0, self.cell_width) and (i != x or j != y):
                    neighbours.append(self.clist[i][j])
        return neighbours

    def update_cell_list(self, cell_list: List[list]) -> List[list]:
        """
        Обновление состояния клеток
        """
        new_clist = copy.deepcopy(self.clist)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if sum(self.get_neighbours((i, j))) == 2:
                    if new_clist[i][j] == 1:
                        new_clist[i][j] = 1
                    else:
                        new_clist[i][j] = 0
                elif sum(self.get_neighbours((i, j))) == 3:
                    new_clist[i][j] = 1
                else:
                    new_clist[i][j] = 0
        self.clist = new_clist
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(400, 400, 20)
    game.run()
