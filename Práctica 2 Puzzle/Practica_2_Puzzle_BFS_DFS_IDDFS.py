import numpy as np
from collections import deque
from copy import deepcopy
import pygame
import random

# Constantes para seleccionar el algoritmo de búsqueda
BUSQUEDA_AMPLITUD = 0
BUSQUEDA_PROFUNDIDAD = 1
IDDFS = 2
ALGORITMO = BUSQUEDA_PROFUNDIDAD # Cambia esta constante para elegir el algoritmo: BUSQUEDA_AMPLITUD, BUSQUEDA_PROFUNDIDAD o IDDFS

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
            yield nueva_matriz

# Realizar búsqueda en amplitud para encontrar la solución del 8-puzzle
def busqueda_amplitud(matriz):
    visitados = set()
    cola = deque([(matriz, 0, [])])

    while cola:
        matriz_actual, profundidad, camino = cola.popleft()
        cadena_actual = convertir_a_cadena(matriz_actual)

        if cadena_actual not in visitados:
            visitados.add(cadena_actual)

            if np.all(matriz_actual == matriz_objetivo):
                return profundidad, camino

            for siguiente_matriz in expandir(matriz_actual):
                nuevo_camino = camino.copy()
                nuevo_camino.append(siguiente_matriz)
                cola.append((siguiente_matriz, profundidad + 1, nuevo_camino))

    return -1, []

# Realizar búsqueda en profundidad iterativa para encontrar la solución del 8-puzzle
def iddfs(matriz):
    profundidad_max = 0
    while True:
        visitados = set()
        camino = []
        resultado, subcamino = dfs(matriz, 0, profundidad_max, visitados, camino)
        if resultado != -1:
            return resultado, subcamino
        profundidad_max += 1

# Realizar búsqueda en profundidad con límite de profundidad para encontrar la solución del 8-puzzle
def dfs(matriz, profundidad, profundidad_max, visitados, camino):
    cadena_actual = convertir_a_cadena(matriz)
    if cadena_actual in visitados:
        return -1, []

    visitados.add(cadena_actual)

    if np.all(matriz == matriz_objetivo):
        return profundidad, camino

    if profundidad == profundidad_max:
        return -1, []

    for siguiente_matriz in expandir(matriz):
        nuevo_camino = camino.copy()
        nuevo_camino.append(siguiente_matriz)
        resultado, subcamino = dfs(siguiente_matriz, profundidad + 1, profundidad_max, visitados, nuevo_camino)
        if resultado != -1:
            return resultado, subcamino

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

        if algoritmo == BUSQUEDA_AMPLITUD:
            num_movimientos, solucion = busqueda_amplitud(matriz_inicial)
        elif algoritmo == BUSQUEDA_PROFUNDIDAD:
            num_movimientos, solucion = iddfs(matriz_inicial)
        elif algoritmo == IDDFS:
            num_movimientos, solucion = iddfs(matriz_inicial)

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

