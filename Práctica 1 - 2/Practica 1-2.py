from enum import Enum
from random import random, randint
import os
import time
from time import sleep

class TipoDeCelda(Enum):
    Limpia = "⬜"
    Sucia = "⬛"
    Ocupada = "🔬"

class Entorno:
    def __init__(self, ancho: int, proporcion_sucia: float = .5) -> None:
        self.espacio = []
        for i in range(ancho):
            if random() > proporcion_sucia:
                self.espacio.append(TipoDeCelda.Limpia)
            else:
                self.espacio.append(TipoDeCelda.Sucia)
        self.espacioAux = self.espacio.copy()#espacioAux tendrá el espacio sin la aspiradora, es necesario para mostrar la aspiradora y que no intervenga en las condiciones

    def __str__(self):
        cadena = ""
        for celda in self.espacio:
            cadena += celda.value
        return cadena

    def esta_dentro(self, x: int) -> bool:
        if x >= 0 and x < len(self.espacio):
            return True
        else:
            return False

    def esta_sucia(self, x: int) -> bool:
        return self.espacioAux[x] == TipoDeCelda.Sucia

    def limpiar(self, x: int) -> None:
        if self.esta_dentro(x):
            self.espacioAux[x] = TipoDeCelda.Limpia

    def esta_todo_limpio(self) -> bool:
        return TipoDeCelda.Sucia not in self.espacioAux


class Aspiradora:
    class Direccion(Enum):
        Izquierda = -1
        Derecha = 1

    def __init__(self, ent: Entorno, x: int):
        self.entorno = ent
        self.entorno.espacio[x] = TipoDeCelda.Ocupada
        self.x = x
        self.puntaje = 0
        self.direccion = Aspiradora.Direccion.Izquierda

    def actuar(self):
        if self.entorno.esta_sucia(self.x):
            self.entorno.limpiar(self.x)
            self.puntaje += 1
        else:
            self.mover()

    def mover(self):
        self.entorno.espacio[self.x] = TipoDeCelda.Limpia
        self.x += self.direccion.value
        if not self.entorno.esta_dentro(self.x):
            if self.direccion == Aspiradora.Direccion.Derecha:
                self.direccion = Aspiradora.Direccion.Izquierda
            else:
                self.direccion = Aspiradora.Direccion.Derecha
            self.x += self.direccion.value * 2

        self.entorno.espacio[self.x] = TipoDeCelda.Ocupada

def limpiar_pantalla():
    os.system('cls')


tamanio  = 6
limpiar_pantalla()
entorno = Entorno(tamanio)
Aspiradora = Aspiradora(entorno, 0)
print(entorno)
print(f'Puntuación = {Aspiradora.puntaje}')
sleep(0.7)

while not Aspiradora.entorno.esta_todo_limpio():
    Aspiradora.actuar()
    limpiar_pantalla()
    print(entorno)
    print(f'Puntuación = {Aspiradora.puntaje}')
    sleep(1)