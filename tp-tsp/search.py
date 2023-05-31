"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""

from __future__ import annotations
from problem import OptProblem
from node import Node
from random import choice, shuffle
from time import time


def random_reset(initial_state):
    """Genera un estado inicial aleatorio para cada reinicio."""
    # Implementa aquí la generación de un nuevo estado inicial aleatorio basado en el estado inicial original
    # Puedes utilizar métodos o algoritmos adecuados según las características del problema
    # Retorna el nuevo estado inicial generado

    # Ejemplo: Generación aleatoria de un nuevo estado inicial permutando el estado inicial original
    new_initial_state = initial_state[:]  # Copia del estado inicial original

    # Permutar aleatoriamente el nuevo estado inicial
    shuffle(new_initial_state)

    return new_initial_state


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local
            if diff[act] <= 0:

                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end - start
                return

            # Sino, moverse a un nodo con el estado sucesor
            else:

                actual = Node(problem.result(actual.state, act),
                              actual.value + diff[act])
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Clase que representa un algoritmo de ascenso de colinas con reinicios aleatorios.

    En cada iteración se mueve al estado sucesor con mejor valor objetivo.
    Se realiza un reinicio aleatorio cuando se alcanza un óptimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con ascenso de colinas y reinicios aleatorios.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        """
        # Inicio del reloj
        start = time()
        max_restarts = 1
        max_iters = 100
        best_tour = None
        best_value = float('-inf')

        restarts = 0
        while restarts < max_restarts:
            # Crear el nodo inicial mediante un reinicio aleatorio
            actual = Node(random_reset(problem.init), problem.obj_val(problem.init))

            while True:
                # Determinar las acciones que se pueden aplicar
                # y las diferencias en valor objetivo que resultan
                diff = problem.val_diff(actual.state)

                # Buscar las acciones que generan el mayor incremento de valor objetivo
                max_acts = [act for act, val in diff.items() if val == max(diff.values())]

                # Elegir una acción aleatoria
                act = choice(max_acts)

                # Retornar si estamos en un óptimo local o se alcanzó el número máximo de iteraciones
                if diff[act] <= 0 or self.niters >= max_iters:
                    break

                # Moverse a un nodo con el estado sucesor
                actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                self.niters += 1

            # Guardar la mejor solución encontrada en este reinicio
            if actual.value > best_value:
                best_tour = actual.state
                best_value = actual.value

            # Incrementar el contador de reinicios
            restarts += 1

        # Asignar la mejor solución encontrada a las variables de la instancia
        self.tour = best_tour
        self.value = best_value

        # Finalizar el reloj
        end = time()
        self.time = end - start


class Tabu(LocalSearch):
    """Algoritmo de búsqueda tabú."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con Búsqueda Tabú.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        """
        # Inicio del reloj
        start = time()

        lista_tabu = set()  # Utilizamos un conjunto para la lista tabú

        actual = Node(problem.init, problem.obj_val(problem.init))
        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el mayor incremento de valor objetivo y no estén en la lista Tabú
            max_acts = [act for act, val in diff.items() if (val == max(diff.values())) and (val not in lista_tabu)]

            if max_acts:
                act = choice(max_acts)
            else:
                break

            # Retornar si estamos en un óptimo local
            if diff[act] <= 0:
                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end - start
                return
            else:
                # Agregar movimiento a la lista Tabú
                lista_tabu.add(act)

                actual = Node(problem.result(actual.state, act),
                              actual.value + diff[act])
                self.niters += 1
