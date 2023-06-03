"""
Este modulo define la clase LocalSearch.

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

from typing import Optional, List, Set

from problem import OptProblem, State
from node import Node
from random import choice, sample
from time import time
import logging

logger = logging.getLogger(__name__)


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
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]
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
                actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """
    Clase que representa un algoritmo de ascenso de colinas con reinicios aleatorios.
    En cada iteración se mueve al estado sucesor con mejor valor objetivo.
    Se realiza un reinicio aleatorio cuando se alcanza un óptimo local.
    """

    def __init__(self, max_restarts: int = 3, max_iters: int = 10, rest: bool = False):
        """
        Construye una instancia de la clase HillClimbingReset.
        max_restarts: int máximo número de reinicios (por defecto, 3)
        max_iters: int numero maximo de interaciones (por defecto 10)
        type_reset: bool True para versión estocástica (por defecto False)
        """
        super().__init__()
        self.max_restarts = max_restarts
        self.max_iters = max_iters
        self.type_reset = rest

    def solve(self, problem: OptProblem):
        """
        Resuelve un problema de optimización con ascenso de colinas y reinicios aleatorios.
        Argumentos:
        ==========
        problem: OptProblem un problema de optimización
        """
        try:
            # Inicio del reloj
            start = time()
            best_tour = None
            best_value = float('-inf')
            restarts = 0
            self.niters = 0  # Reiniciar el contador de iteraciones

            while restarts < self.max_restarts:
                # Crear el nodo inicial mediante un reinicio aleatorio
                if restarts != 0:
                    problem.random_reset()
                no_improvement_count = 0
                actual = Node(problem.init, problem.obj_val(problem.init))

                while self.max_iters > no_improvement_count:
                    # Determinar las acciones que se pueden aplicar y las diferencias en valor objetivo que resultan
                    diff = problem.val_diff(actual.state)
                    # Elegir una acción aleatoria de las que generan incremento positivo en el valor objetivo

                    if self.type_reset:
                        positive_diff_acts = [act for act, val in diff.items() if val == max(diff.values())]
                    else:
                        positive_diff_acts = [act for act, val in diff.items() if val > 0]

                    if positive_diff_acts:
                        act = choice(positive_diff_acts)
                        # Moverse a un nodo con el estado sucesor
                        actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                        # Guardar la mejor solución encontrada en este reinicio
                        if actual.value > best_value:
                            best_tour = actual.state
                            best_value = actual.value
                            no_improvement_count = 0  # Reiniciar el contador de iteraciones sin mejora
                        else:
                            no_improvement_count += 1
                        self.niters += 1
                    else:
                        break
                # Incrementar el contador de reinicios
                restarts += 1
            # Asignar la mejor solución encontrada a las variables de la instancia
            self.tour = best_tour
            self.value = best_value
            # Finalizar el reloj
            end = time()
            self.time = end - start
        except Exception as e:
            logger.error(f"Se produjo un error en el método solve: ERROR={e}", exc_info=True)
            self.tour = None
            self.value = None
            self.time = None


class Tabu(LocalSearch):
    """Algoritmo de búsqueda tabú."""

    def __init__(self, tabu_list_size=0, max_iters=None):
        """
        Construye una instancia de la clase Tabu.
        tabu_list_size: int tamaño de la lista tabú (por defecto, None)
        max_iters: int número máximo de iteraciones (por defecto, None)
        """
        super().__init__()
        self.tabu_list_size = tabu_list_size
        self.max_iters = max_iters

    @staticmethod
    def get_neighbors(
            state: List,
            problem: OptProblem,
            tabu_list: Optional[Set[tuple]] = None
    ) -> List[Node]:
        """
        Obtiene los vecinos permitidos por las restricciones de la lista tabú.
        state: estado actual
        problem: OptProblem un problema de optimización
        tabu_list: set lista tabú que contiene los movimientos prohibidos
        Return
        list: lista de vecinos permitidos junto con sus valores objetivo
        """
        neighbors = []
        try:
            for action in problem.actions(state):
                # Se verifica si el movimiento es permitido por las restricciones de la lista tabú
                if tuple(action) not in tabu_list:
                    # Se obtiene el estado vecino aplicando la acción al estado actual
                    neighbor_state = problem.result(state, action)
                    # Se calcula el valor objetivo del estado vecino
                    neighbor_value = problem.obj_val(neighbor_state)
                    # Se agrega el vecino (estado y valor objetivo) a la lista de vecinos permitidos
                    neighbors.append(Node(neighbor_state, neighbor_value))
        except Exception as e:
            logger.error(f"Se produjo un error al obtener los vecinos permitidos error={e}", exc_info=True)
            return []
        # Se devuelve la lista de vecinos permitidos junto con sus valores objetivo
        return neighbors

    def remove_elements_random(self, tabu_list: Set[tuple]) -> Set[tuple]:
        """
        Elimina elementos aleatorios en la lista Tabú.
        tabu_list: Set[tuple] - Lista Tabú que contiene los elementos a eliminar.
        Return
        Set[tuple]: Lista Tabú modificada después de eliminar elementos aleatorios.
        """
        try:
            if len(tabu_list) > self.tabu_list_size:
                tabu_list = set(sample(tabu_list, self.tabu_list_size))
            return tabu_list
        except Exception as e:
            logger.error(f"Se produjo un error al eliminar elementos de la lista Tabú: {e}", exc_info=True)
            return set()

    def solve(self, problem: OptProblem):
        """
        Resuelve un problema de optimización con Búsqueda Tabú.
        Argumentos:
        ==========
        problem: OptProblem - Un problema de optimización.
        """
        try:
            # Inicio del reloj
            start = time()
            # tabu_list = []
            tabu_list = set()
            if self.tabu_list_size == 0:
                self.tabu_list_size = int(len(problem.init) * 0.20)
            if self.max_iters is None:
                self.max_iters = len(problem.init)
            iter_count = 0
            actual = Node(problem.init, problem.obj_val(problem.init))
            while iter_count < self.max_iters:
                # Obtener los vecinos permitidos por las restricciones de la lista tabú
                neighbors = self.get_neighbors(actual.state, problem, tabu_list)
                # Elegir el vecino con el mejor valor objetivo
                best_neighbor = max(neighbors, key=lambda x: x.value)
                # Retornar si estamos en un óptimo local
                if best_neighbor.value <= actual.value:
                    self.tour = actual.state
                    self.value = actual.value
                    end = time()
                    self.time = end - start
                    return
                else:
                    # Moverse al vecino seleccionado
                    actual = best_neighbor
                    # Agregar el movimiento a la lista Tabú
                    tabu_list.add(tuple(best_neighbor.state))
                    if len(tabu_list) > self.tabu_list_size:
                        # Eliminar elementos aleatorios en la lista Tabú
                        tabu_list = self.remove_elements_random(tabu_list)
                    iter_count += 1
                    self.niters += 1
            # Asignar la mejor solución encontrada a las variables de la instancia
            self.tour = actual.state
            self.value = actual.value
            # Finalizar el reloj
            end = time()
            self.time = end - start
        except Exception as e:
            logger.error(f"Se produjo un error en el método solve: {e}", exc_info=True)
            self.tour = None
            self.value = None
            self.time = None
