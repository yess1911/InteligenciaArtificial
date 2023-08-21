import numpy as np
import heapq
from collections import deque
from copy import deepcopy
import pygame
import random

# Constantes para seleccionar el algoritmo de búsqueda
BEST_FIRST = 1
ASTAR = 2
DIJKSTRA = 3
ALGORITMO = BEST_FIRST
# Inicializar Pygame, crear una ventana de 300x300 y establecer el título
pygame.init()
pantalla = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Resolviendo problema 8-puzzle")
fuente = pygame.font.Font(None, 36)
reloj = pygame.time.Clock()

# Definir colores como constantes para usar en el dibujo
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Convertir la matriz en una cadena única para facilitar la comparación
def convertir_a_cadena(matriz):
    return ''.join(str(e) for fila in matriz for e in fila)

# Generar todas las matrices posibles a partir de la matriz actual moviendo una ficha adyacente a la posición vacía
def expandir(matriz):
    # Encontrar la posición de la ficha vacía (0) en la matriz
    vacio_x, vacio_y = np.where(matriz == 0)
    vacio_x, vacio_y = int(vacio_x), int(vacio_y)

    # Definir los posibles movimientos de la ficha vacía: arriba, abajo, izquierda, derecha
    movimientos = [
        (-1, 0),  # Arriba
        (1, 0),   # Abajo
        (0, -1),  # Izquierda
        (0, 1)    # Derecha
    ]

    # Iterar sobre los posibles movimientos
    for dx, dy in movimientos:
        # Calcular la nueva posición de la ficha vacía después de moverla
        nuevo_x, nuevo_y = vacio_x + dx, vacio_y + dy

        # Comprobar si la nueva posición está dentro de los límites de la matriz (3x3)
        if 0 <= nuevo_x < 3 and 0 <= nuevo_y < 3:
            # Crear una copia de la matriz actual para no modificar la matriz original
            nueva_matriz = deepcopy(matriz)
             # Intercambiar la posición de la ficha vacía con la posición adyacente en la dirección del movimiento
            nueva_matriz[vacio_x, vacio_y] = nueva_matriz[nuevo_x, nuevo_y]
            nueva_matriz[nuevo_x, nuevo_y] = 0
            # Devolver la nueva matriz generada después de mover la ficha vacía
            yield tuple(map(tuple, nueva_matriz))

def distancia_manhattan_posicion(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])




def distancia_manhattan(matriz):
    matriz = np.array(matriz)
    distancia = 0
    for i in range(3):
        for j in range(3):
            valor = matriz[i][j]
            if valor != 0:
                fila_objetivo = (valor - 1) // 3
                columna_objetivo = (valor - 1) % 3
                distancia += distancia_manhattan_posicion((i, j), (fila_objetivo, columna_objetivo))
    return int(distancia)

def dijkstra(matriz):
    visitados = set()
    inicio = (0, tuple(map(tuple, matriz)), [])
    cola_prioridad = [inicio]

    while cola_prioridad:
        profundidad, matriz_actual, camino = heapq.heappop(cola_prioridad)
        matriz_actual = np.array(matriz_actual)

        cadena_actual = convertir_a_cadena(matriz_actual)

        if cadena_actual in visitados:
            continue
        visitados.add(cadena_actual)

        if np.array_equal(matriz_actual, matriz_objetivo):
            return profundidad, camino

        for siguiente_matriz in expandir(matriz_actual):
            if convertir_a_cadena(siguiente_matriz) not in visitados:
                nuevo_camino = camino.copy()
                nuevo_camino.append(siguiente_matriz)
                siguiente_matriz_tuple = tuple(map(tuple, siguiente_matriz))
                heapq.heappush(cola_prioridad, (profundidad + 1, siguiente_matriz_tuple, nuevo_camino))

    return -1, []

# Realizar búsqueda "Primero el mejor" para encontrar la solución del 8-puzzle
def best_first(matriz):
    visitados = set()
    inicio = (distancia_manhattan(matriz), 0, tuple(map(tuple, matriz)), [])
    cola_prioridad = [inicio]

    while cola_prioridad:
        heuristica, profundidad, matriz_actual, camino = heapq.heappop(cola_prioridad)
        matriz_actual = np.array(matriz_actual)

        cadena_actual = convertir_a_cadena(matriz_actual)

        if cadena_actual in visitados:
            continue
        visitados.add(cadena_actual)

        if np.array_equal(matriz_actual, matriz_objetivo):
            return profundidad, camino

        for siguiente_matriz in expandir(matriz_actual):
            if convertir_a_cadena(siguiente_matriz) not in visitados:
                nuevo_camino = camino.copy()
                nuevo_camino.append(siguiente_matriz)
                siguiente_matriz_tuple = tuple(map(tuple, siguiente_matriz))
                heapq.heappush(cola_prioridad, (distancia_manhattan(siguiente_matriz_tuple) + profundidad + 1, profundidad + 1, siguiente_matriz_tuple, nuevo_camino))


    return -1, []
def a_star(matriz):
    visitados = set()
    inicio = (distancia_manhattan(matriz), 0, tuple(map(tuple, matriz)), [])
    cola_prioridad = [inicio]

    while cola_prioridad:
        heuristica, profundidad, matriz_actual, camino = heapq.heappop(cola_prioridad)
        matriz_actual = np.array(matriz_actual)

        cadena_actual = convertir_a_cadena(matriz_actual)

        if cadena_actual in visitados:
            continue
        visitados.add(cadena_actual)

        if np.array_equal(matriz_actual, matriz_objetivo):
            return profundidad, camino

        for siguiente_matriz in expandir(matriz_actual):
            if convertir_a_cadena(siguiente_matriz) not in visitados:
                nuevo_camino = camino.copy()
                nuevo_camino.append(siguiente_matriz)
                siguiente_matriz_tuple = tuple(map(tuple, siguiente_matriz))
                heapq.heappush(cola_prioridad, (distancia_manhattan(siguiente_matriz_tuple) + profundidad + 1, profundidad + 1, siguiente_matriz_tuple, nuevo_camino))

    return -1, []




# Dibujar la matriz en la pantalla utilizando Pygame
def dibujar_matriz(matriz):
    pantalla.fill(BLANCO)

    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if valor != 0:
                rect = pygame.Rect(j * 100 , i * 100, 100, 100)
                pygame.draw.rect(pantalla, NEGRO, rect, 3)
                texto = fuente.render(str(valor), True, NEGRO)
                rect_texto = texto.get_rect(center=rect.center)
                pantalla.blit(texto, rect_texto)

    pygame.display.flip()

# Mostrar un mensaje en la pantalla mientras se procesa la solución
def mostrar_mensaje_procesando():
    pantalla.fill(BLANCO)
    texto = fuente.render("Procesando solución...", True, NEGRO)
    rect_texto = texto.get_rect(center=(150, 150))
    pantalla.blit(texto, rect_texto)
    pygame.display.flip()

# Animar la solución del 8-puzzle paso a paso
def animar_solucion(solucion):
    for matriz in solucion:
        dibujar_matriz(matriz)
        pygame.display.update()
        reloj.tick(5)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

# Generar una matriz inicial aleatoria para el 8-puzzle
def generar_matriz_inicial():
    numeros = list(range(9))
    random.shuffle(numeros)
    return np.array(numeros).reshape(3, 3)

# Definir la matriz objetivo del 8-puzzle
matriz_objetivo = np.array([
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
])

# Resolver el 8-puzzle utilizando el algoritmo seleccionado
def resolver_puzzle(algoritmo):
    while True:
        matriz_inicial = generar_matriz_inicial()
        print("Matriz inicial:")
        print(matriz_inicial)

        mostrar_mensaje_procesando()
        if algoritmo == BEST_FIRST:
            num_movimientos, solucion = best_first(matriz_inicial)
        elif algoritmo == ASTAR:
            num_movimientos, solucion = a_star(matriz_inicial)
        elif algoritmo == DIJKSTRA:
            num_movimientos, solucion = dijkstra(matriz_inicial)
        if num_movimientos != -1:
            break

    print("Número de movimientos:", num_movimientos)
    return matriz_inicial, solucion


# Obtener la matriz inicial y la solución del 8-puzzle
matriz_inicial, solucion = resolver_puzzle(ALGORITMO)
solucion.insert(0, matriz_inicial)
animar_solucion(solucion)

# Bucle principal para mantener la ventana abierta y mostrar la solución final
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    dibujar_matriz(solucion[-1])
    pygame.display.update()
    reloj.tick(500)

pygame.quit()