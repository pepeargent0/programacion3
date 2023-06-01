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

    def __init__(self, max_restarts=3):
        """
        Construye una instancia de la clase HillClimbingReset.
        Argumentos:
        ==========
        max_restarts: int máximo número de reinicios (por defecto, 3)
        """
        super().__init__()
        self.max_restarts = max_restarts

    def solve(self, problem: OptProblem):
        """
        Resuelve un problema de optimización con ascenso de colinas y reinicios aleatorios.
        Argumentos:
        ==========
        problem: OptProblem un problema de optimización
        """
        # Inicio del reloj
        start = time()
        # Configurar el número máximo de iteraciones por reinicio
        max_iters = len(problem.init)
        best_tour = None
        best_value = float('-inf')
        restarts = 0
        while restarts < self.max_restarts:
            # Crear el nodo inicial mediante un reinicio aleatorio
            if restarts != 0:
                problem.random_reset()
            actual = Node(problem.init, problem.obj_val(problem.init))
            no_improvement_count = 0
            while no_improvement_count < max_iters:
                # Determinar las acciones que se pueden aplicar y las diferencias en valor objetivo que resultan
                diff = problem.val_diff(actual.state)
                # Elegir una acción aleatoria de las que generan incremento positivo en el valor objetivo
                positive_diff_acts = [act for act, val in diff.items() if val > 0]
                if positive_diff_acts:
                    act = choice(positive_diff_acts)
                else:
                    break
                # Moverse a un nodo con el estado sucesor
                actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                self.niters += 1
                # Verificar si se ha encontrado una solución mejor
                if actual.value > best_value:
                    best_tour = actual.state
                    best_value = actual.value
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1
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
    def __init__(self, tabu_list_size=None, max_iters=None):
        """Construye una instancia de la clase Tabu.
        Argumentos:
        ==========
        tabu_list_size: int tamaño de la lista tabú (por defecto, None)
        max_iters: int número máximo de iteraciones (por defecto, None)
        """
        super().__init__()
        self.tabu_list_size = tabu_list_size
        self.max_iters = max_iters

    @staticmethod
    def get_neighbors(state, problem, tabu_list):
        """
        Obtiene los vecinos permitidos por las restricciones de la lista tabú.
        Argumentos:
        ==========
        state: any estado actual
        problem: OptProblem un problema de optimización
        tabu_list: list lista tabú que contiene los movimientos prohibidos
        Retorna:
        =======
        list: lista de vecinos permitidos junto con sus valores objetivo
        """
        neighbors = []
        for action in problem.actions(state):
            # Se verifica si el movimiento es permitido por las restricciones de la lista tabú
            if action not in tabu_list:
                neighbor_state = problem.result(state, action)
                neighbor_value = problem.obj_val(neighbor_state)
                neighbors.append((neighbor_state, neighbor_value))
        return neighbors

    def solve(self, problem):
        """
        Resuelve un problema de optimización con Búsqueda Tabú.
        Argumentos:
        ==========
        problem: OptProblem un problema de optimización
        """
        # Inicio del reloj
        start = time()
        tabu_list = []
        if self.tabu_list_size is None:
            self.tabu_list_size = int(len(problem.init) * 0.2)
        if self.max_iters is None:
            self.max_iters = len(problem.init)
        iter_count = 0
        actual = Node(problem.init, problem.obj_val(problem.init))
        while iter_count < self.max_iters:
            # Obtener los vecinos permitidos por las restricciones de la lista tabú
            neighbors = self.get_neighbors(actual.state, problem, tabu_list)
            # Elegir el vecino con el mejor valor objetivo
            best_neighbor = max(neighbors, key=lambda x: x[1])
            # Retornar si estamos en un óptimo local
            if best_neighbor[1] <= actual.value:
                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end - start
                return
            else:
                # Moverse al vecino seleccionado
                actual = Node(best_neighbor[0], best_neighbor[1])
                # Agregar el movimiento a la lista Tabú
                tabu_list.append(best_neighbor[0])
                if len(tabu_list) > self.tabu_list_size:
                    tabu_list.pop(0)
                iter_count += 1
                self.niters += 1
        # Asignar la mejor solución encontrada a las variables de la instancia
        self.tour = actual.state
        self.value = actual.value
        # Finalizar el reloj
        end = time()
        self.time = end - start
