"""
Modulo principal.
Autor: Mauro Lucci.
Fecha: 2023.
Materia: Prog3 - TUIA
"""

import parse
import load
import search
import plot
import problem

# Algoritmos involucrados
HILL_CLIMBING = "hill"
HILL_CLIMBING_RANDOM_RESET = "hill_reset"
TABU_SEARCH = "tabu"
HILL_CLIMBING_RANDOM_RESET_ESTOCASTICO = "hill_reset_estocastico"
ALGO_NAMES = [HILL_CLIMBING, HILL_CLIMBING_RANDOM_RESET, HILL_CLIMBING_RANDOM_RESET_ESTOCASTICO, TABU_SEARCH]


def main() -> None:
    """Funcion principal."""
    # Parsear los argumentos de la linea de comandos
    args = parse.parse()

    # Leer la instancia
    graph, coords = load.read_tsp(args.filename)

    # Construir la instancia de TSP
    p = problem.TSP(graph)

    # Construir las instancias de los algoritmos
    algos = {
        HILL_CLIMBING: search.HillClimbing(),
        TABU_SEARCH: search.Tabu(tabu_list_size=20),
        HILL_CLIMBING_RANDOM_RESET: search.HillClimbingReset(
            max_restarts=2,
            max_iters=2,
            rest='no_estocastico'),
        HILL_CLIMBING_RANDOM_RESET_ESTOCASTICO: search.HillClimbingReset(max_restarts=2, max_iters=400)
    }
    # BUSQUEDA TABU PAREMATROS
    # search.Tabu(tabu_list_size=4, max_iters=2) ar24.tsp
    # search.Tabu(tabu_list_size=4, max_iters=2) att48.tsp
    # search.Tabu(tabu_list_size=4, max_iters=2) berlin52.tsp -3461 0.00 4 tabu
    # search.Tabu(tabu_list_size=4, max_iters=2) burma14.tsp -3461 0.00 4 tabu
    # search.Tabu(tabu_list_size=4, max_iters=2) pr76.tsp -3461 0.00 4 tabu
    # search.Tabu(tabu_list_size=4, max_iters=2) ulysses16.tsp -3461 0.00 4 tabu
    # Graficar los tours
    tours = {'init': (p.init, p.obj_val(p.init))}

    # Resolver el TSP con cada algoritmo
    for algo in algos.values():
        algo.solve(p)

    # Mostrar resultados por linea de comandos
    print("Valor:", "Tiempo:", "Iters:", "Algoritmo:", sep="\t\t")
    for name, algo in algos.items():
        print(algo.value, "%.2f" % algo.time, algo.niters, name, sep="\t\t")

    for name, algo in algos.items():
        tours[name] = (algo.tour, algo.value)
    plot.show(graph, coords, args.filename, tours)


if __name__ == "__main__":
    main()
