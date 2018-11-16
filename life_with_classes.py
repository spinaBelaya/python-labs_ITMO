import pygame
from pygame.locals import *
import random
from copy import deepcopy
from typing import Any


class Cell:

    def __init__(self, row: int, col: int, state=False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> Any:
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize=False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        if randomize:
            self.grid = [[Cell(i, j, random.randint(0, 1))
                          for j in range(ncols)] for i in range(nrows)]
        else:
            self.grid = [[Cell(i, j) for j in range(ncols)]
                         for i in range(nrows)]

    def update(self):
        new_grid = deepcopy(self.grid)
        for cell in self:
            neighbours = self.get_neighbours(cell)
            alive = sum(check.is_alive() for check in neighbours)
            if cell.is_alive():
                if alive in [2, 3]:
                    new_grid[cell.row][cell.col].state = 1
                else:
                    new_grid[cell.row][cell.col].state = 0
            else:
                if alive == 3:
                    new_grid[cell.row][cell.col].state = 1
        self.grid = new_grid
        return self

    def get_neighbours(self, cell: Cell) -> list:
        neighbours = []
        x, y = cell.col, cell.row
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if i in range(0, self.nrows) and j in range(0, self.ncols) and (i != y or j != x):
                    neighbours.append(self.grid[i][j])
        return neighbours

    @classmethod
    def from_file(cls, filename: str):
        fgrid = []
        with open(filename) as file:
            for nrow, line in enumerate(file):
                row = [Cell(nrow, ncol, int(state))
                       for ncol, state in enumerate(line) if state in "01"]
                fgrid.append(row)
        clist = cls(len(fgrid), len(fgrid[0]))
        clist.grid = fgrid
        return clist

    def __iter__(self):
        self.i, self.j = 0, 0
        return self

    def __next__(self) -> Cell:
        if self.i == self.nrows:
            raise StopIteration
        ngrid = self.grid[self.i][self.j]
        self.j += 1
        if self.j == self.ncols:
            self.j = 0
            self.i += 1
        return ngrid

    def __str__(self) -> str:
        str = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.grid[i][j].state is True:
                    str += '1'
                else:
                    str += '0'
            str += '\n'
        return str


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
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.music.load("gimn.ogg")
        pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        clist = CellList(self.cell_width, self.cell_height, True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(clist)
            clist = CellList.update(clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, clist) -> None:
        for cell in clist:

            color_cell = pygame.Color('blue')

            if cell.is_alive():
                color_cell = pygame.Color('yellow')

            rect = Rect(cell.row * self.cell_size+1, cell.col *
                        self.cell_size+1, self.cell_size-1, self.cell_size-1)
            pygame.draw.rect(self.screen, color_cell, rect)


if __name__ == '__main__':
    game = GameOfLife(400, 400, 20)
    game.run()
