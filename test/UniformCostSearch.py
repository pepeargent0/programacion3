from src.pathfinder.models.grid import Grid
from src.pathfinder.models.solution import Solution, NoSolution
from src.pathfinder.search.ucs import UniformCostSearch

# Caso 1 - Un camino directo entre el inicio y el final
grid1 = Grid([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
], (0, 0), (2, 2))
solution1 = UniformCostSearch.search(grid1)
assert isinstance(solution1, Solution)
assert solution1.path == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]

# Caso 2 - El inicio y el final son la misma posición
grid2 = Grid([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
], (1, 1), (1, 1))
solution2 = UniformCostSearch.search(grid2)
assert isinstance(solution2, Solution)
assert solution2.path == [(1, 1)]

# Caso 3 - No hay camino entre el inicio y el final
grid3 = Grid([
    [0, 0, 0],
    [0, 1, 1],
    [0, 0, 0]
], (0, 0), (2, 2))
solution3 = UniformCostSearch.search(grid3)
assert isinstance(solution3, NoSolution)

# Caso 4 - El camino más corto pasa por una casilla con mayor costo
grid4 = Grid([
    [0, 0, 0, 0],
    [0, 1, 2, 0],
    [0, 3, 1, 0],
    [0, 0, 0, 0]
], (0, 0), (3, 3))
solution4 = UniformCostSearch.search(grid4)
assert isinstance(solution4, Solution)
assert solution4.path == [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]
assert solution4.cost == 7
