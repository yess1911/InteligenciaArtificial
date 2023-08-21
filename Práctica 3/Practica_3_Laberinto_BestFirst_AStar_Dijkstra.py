import pygame
import random
from collections import deque
import sys
import heapq

WIDTH, HEIGHT = 500, 500
ROWS, COLS = 15, 15
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 255, 200)


BEST_FIRST_SEARCH = 3
A_STAR_SEARCH = 4
DIJKSTRA_SEARCH = 5 
ALGORITMO = BEST_FIRST_SEARCH


class Node:
    def __init__(self, x, y, parent=None, g_cost=float('inf')):
        self.x = x
        self.y = y
        self.parent = parent
        self.g_cost = g_cost

    def __lt__(self, other):
        return self.g_cost < other.g_cost

    
def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def search(grid, window):
    start = Node(0, 0)
    end = Node(ROWS - 1, COLS - 1)

    if ALGORITMO == BEST_FIRST_SEARCH:
        return best_first_search(grid, window, start, end)
    elif ALGORITMO == A_STAR_SEARCH:
        return a_star_search(grid, window, start, end)
    elif ALGORITMO == DIJKSTRA_SEARCH:  # Agregar esta línea
        return dijkstra_search(grid, window, start, end)  # Agregar esta línea
    else:
        print("Algoritmo no válido")
        return None

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
        if grid[x][y] == WHITE or grid[x][y] == RED:
            return True
    return False



def heuristic(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def best_first_search(grid, window, start, end):
    open_set = [(heuristic(start, end), start)]
    heapq.heapify(open_set)
    closed_set = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while open_set:
        _, current_node = heapq.heappop(open_set)
        closed_set.add((current_node.x, current_node.y))

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
                    new_node.cost = heuristic(new_node, end)

                    if (new_x, new_y) not in closed_set:
                        heapq.heappush(open_set, (new_node.cost, new_node))

    return None

def best_first_search(grid, window, start, end):
    open_set = [(heuristic(start, end), start)]
    heapq.heapify(open_set)
    closed_set = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while open_set:
        _, current_node = heapq.heappop(open_set)
        closed_set.add((current_node.x, current_node.y))

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

                    if (new_x, new_y) not in closed_set:
                        heapq.heappush(open_set, (heuristic(new_node, end), new_node))

    return None

def a_star_search(grid, window, start, end):
    start.g_cost = 0
    start.h_cost = heuristic(start, end)
    start.f_cost = start.h_cost
    open_set = [(start.f_cost, start)]
    heapq.heapify(open_set)
    closed_set = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while open_set:
        _, current_node = heapq.heappop(open_set)
        closed_set.add((current_node.x, current_node.y))

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

                    if (new_x, new_y) not in closed_set:
                        tentative_g_cost = current_node.g_cost + 1
                        if tentative_g_cost < new_node.g_cost:
                            new_node.parent = current_node
                            new_node.g_cost = tentative_g_cost
                            new_node.h_cost = heuristic(new_node, end)
                            new_node.f_cost = new_node.g_cost + new_node.h_cost
                            heapq.heappush(open_set, (new_node.f_cost, new_node))

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


def dijkstra_search(grid, window, start, end):
    start.g_cost = 0
    open_set = [(start.g_cost, start)]
    heapq.heapify(open_set)
    closed_set = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while open_set:
        _, current_node = heapq.heappop(open_set)
        closed_set.add((current_node.x, current_node.y))

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

                    if (new_x, new_y) not in closed_set:
                        tentative_g_cost = current_node.g_cost + 1
                        if tentative_g_cost < new_node.g_cost:
                            new_node.parent = current_node
                            new_node.g_cost = tentative_g_cost
                            heapq.heappush(open_set, (new_node.g_cost, new_node))

    return None

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