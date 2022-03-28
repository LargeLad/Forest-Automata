import random
import pygame

WIDTH = 1000
HEIGHT = 600
FPS = 30
CELLSIZE = 6

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Automata")


class ground:
    def __init__(self):
        self.color = (100 + random.randint(-10,10), 60+ random.randint(-10,10), 20+ random.randint(-10,10))


class seed:
    def __init__(self):
        self.color = (120, 80, 40)
        self.age = 0


class tree:
    def __init__(self):
        self.color = (0, 120, 10)
        self.age = 0
        self.energy = 0

    def update_color(self):
        self.color = (0, 120 - self.age*5, 10)


class fire:
    def __init__(self):
        self.color = (200, 30, 0)
        self.age = 0

    def update_color(self):
        if self.age <= 25:
            self.color = (150 + self.age*4, 30, 10)

        else:
            self.color = (350 - self.age * 4, 30, 10)

def draw_cells(cells):
    for i in range(len(cells)):
        for j in range(len(cells[0])):
                x = i * CELLSIZE
                y = j * CELLSIZE
                pygame.draw.rect(WIN, cells[i][j].color, (x, y, CELLSIZE, CELLSIZE))

def update_ground(new_cells, i, j):
    if random.randint(0, 10000) == 4:
        new_cells[i][j] = seed()

    return new_cells

def update_seed(new_cells, i, j):
    if new_cells[i][j].age < 20:
        new_cells[i][j].age += 1
    else:
        new_cells[i][j] = tree()

    return new_cells

def update_tree(new_cells, i, j):
    new_cells[i][j].update_color()

    if new_cells[i][j].age < 9:
        new_cells[i][j].age += 0.5

    else:
        if new_cells[i][j].energy < -1:
            new_cells[i][j] = ground()

        elif new_cells[i][j].energy < 10:
            count = 1

            for k in range(-1, 2):
                for l in range(-1, 2):
                    try:
                        if type(new_cells[i + k][j + l]) is tree:
                            count += 1
                    except IndexError:
                        pass

            new_cells[i][j].energy += 8 - count

        else:
            new_cells[i][j].energy = 0
            dir = random.choice([[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]])

            try:
                if type(new_cells[i + dir[0]][j + dir[1]]) is ground:
                    new_cells[i + dir[0]][j + dir[1]] = seed()

            except IndexError:
                pass

    return new_cells

def update_fire(new_cells, i, j):
    if new_cells[i][j].age == 50:
        new_cells[i][j] = ground()

    else:
        if new_cells[i][j].age < 30:
            if random.randint(0,2) == 2:
                dir = random.choice([[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]])
                try:
                    if type(new_cells[i + dir[0]][j + dir[1]]) is tree:
                        new_cells[i + dir[0]][j + dir[1]] = fire()

                except IndexError:
                    pass

        new_cells[i][j].update_color()
        new_cells[i][j].age += 1

    return new_cells

def update(cells):

    new_cells = [row[:] for row in cells]

    for i in range(len(new_cells)):
        for j in range(len(new_cells[0])):
            if type(new_cells[i][j]) is ground:
                new_cells = update_ground(new_cells, i, j)

            elif type(new_cells[i][j]) is seed:
                new_cells = update_seed(new_cells, i, j)

            elif type(new_cells[i][j]) is tree:
                new_cells = update_tree(new_cells, i, j)

            elif type(new_cells[i][j]) is fire:
                new_cells = update_fire(new_cells, i, j)


    draw_cells(new_cells)

    return new_cells


def main():
    run = True
    clock = pygame.time.Clock()

    cells = [[ground() for j in range(0, (HEIGHT // CELLSIZE))] for i in range(0, WIDTH // CELLSIZE)]

    while run:
        clock.tick(FPS)
        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cells[x // CELLSIZE][y // CELLSIZE] = seed()

                if event.button == 3:
                    cells[x // CELLSIZE][y // CELLSIZE] = fire()

        cells = update(cells)
        pygame.display.update()

if __name__ == '__main__':
    main()
