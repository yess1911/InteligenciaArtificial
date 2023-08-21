import pygame
import random
from collections import deque
import sys


WIDTH, HEIGHT = 500, 500
ROWS, COLS = 15, 15
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 255, 200)

BUSQUEDA_AMPLITUD = 0
BUSQUEDA_PROFUNDIDAD = 1
IDDFS = 2
ALGORITMO = IDDFS

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

def create_grid():
    grid = [[WHITE] * COLS for _ in range(ROWS)]

    num_obstaculos = random.randint(5, 15)
    for _ in range(num_obstaculos):
        size = random.randint(2, 4)
        x = random.randint(0, ROWS - size - 1)
        y = random.randint(0, COLS - size - 1)

        for i in range(x, x + size):
            for j in range(y, y + size):
                grid[i][j] = BLACK

    grid[0][0] = GREEN
    grid[ROWS - 1][COLS - 1] = RED
    return grid

def draw_grid(window, grid):
    for i in range(ROWS):
        for j in range(COLS):
            pygame.draw.rect(window, grid[i][j], (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(window, BLACK, (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
def valid_move(x, y, grid):
    if x >= 0 and x < ROWS and y >= 0 and y < COLS:
        if grid[x][y] == WHITE or grid[x][y] == RED or (ALGORITMO == IDDFS and (grid[x][y] == YELLOW or grid[x][y] == GREEN)):
            return True
    return False



def search(grid, window):
    start = Node(0, 0)
    end = Node(ROWS - 1, COLS - 1)

    if ALGORITMO == BUSQUEDA_AMPLITUD:
        return bfs(grid, window, start, end)
    elif ALGORITMO == BUSQUEDA_PROFUNDIDAD:
        return dfs(grid, window, start, end)
    elif ALGORITMO == IDDFS:
        return iddfs(grid, window, start, end)
    else:
        print("Algoritmo no válido")
        return None

def bfs(grid, window, start, end):
    queue = deque([start])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        current_node = queue.popleft()

        for dx, dy in directions:
            new_x, new_y = current_node.x + dx, current_node.y + dy
            if valid_move(new_x, new_y, grid):
                new_node = Node(new_x, new_y, current_node)
                queue.append(new_node)

                if grid[new_x][new_y] == RED:
                    return new_node

                if grid[new_x][new_y] == WHITE:  # Add this line
                    grid[new_x][new_y] = YELLOW  # Indent this line
                    draw_grid(window, grid)
                    pygame.display.update()
                    check_pygame_events()
                    pygame.time.delay(50)
    return None

def dfs(grid, window, start, end):
    stack = [start]
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while stack:
        current_node = stack.pop()

        if grid[current_node.x][current_node.y] == RED:
            return current_node

        if grid[current_node.x][current_node.y] != YELLOW:
            grid[current_node.x][current_node.y] = YELLOW
            draw_grid(window, grid)
            pygame.display.update()
            check_pygame_events()
            pygame.time.delay(50)

            for dx, dy in directions:
                new_x, new_y = current_node.x + dx, current_node.y + dy
                if valid_move(new_x, new_y, grid):
                    new_node = Node(new_x, new_y, current_node)
                    stack.append(new_node)

    return None

def iddfs(grid, window, start, end):
    def dls(grid, window, current_node, end, depth):
        if depth == 0 and grid[current_node.x][current_node.y] == RED:
            return current_node

        if depth > 0:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                new_x, new_y = current_node.x + dx, current_node.y + dy
                if valid_move(new_x, new_y, grid):
                    prev_color = grid[new_x][new_y]
                    grid[new_x][new_y] = YELLOW
                    draw_grid(window, grid)
                    pygame.display.update()
                    check_pygame_events()
                    pygame.time.delay(50)

                    result = dls(grid, window, Node(new_x, new_y, current_node), end, depth - 1)
                    
                    if result is None:
                        grid[new_x][new_y] = prev_color
                        draw_grid(window, grid)
                        pygame.display.update()
                        pygame.time.delay(50)
                    else:
                        return result

        return None

    depth = 0
    max_depth = ROWS * COLS
    while depth < max_depth:
        result = dls(grid, window, start, end, depth)
        if result is not None:
            return result
        depth += 1

    print("No se encontró un camino")
    return None

def reconstruct_path(end_node, grid):
    current_node = end_node.parent
    while current_node.parent is not None:
        if grid[current_node.x][current_node.y] != GREEN and grid[current_node.x][current_node.y] != RED:
            grid[current_node.x][current_node.y] = BLUE
        current_node = current_node.parent

def check_pygame_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visualización del algoritmo")
    grid = create_grid()
    end_node = search(grid, window)
    if end_node is not None:
        reconstruct_path(end_node, grid)
    running = True

    while running:
        window.fill(WHITE)
        draw_grid(window, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

    pygame.quit()


main()