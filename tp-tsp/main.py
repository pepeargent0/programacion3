"""Modulo principal.

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
ALGO_NAMES = [HILL_CLIMBING, HILL_CLIMBING_RANDOM_RESET, HILL_CLIMBING_RANDOM_RESET_ESTOCASTICO , TABU_SEARCH]


def main() -> None:
    """Funcion principal."""
    # Parsear los argumentos de la linea de comandos
    args = parse.parse()

    # Leer la instancia
    G, coords = load.read_tsp(args.filename)

    # Construir la instancia de TSP
    p = problem.TSP(G)

    # Construir las instancias de los algoritmos
    algos = {
        HILL_CLIMBING: search.HillClimbing(),
        TABU_SEARCH: search.Tabu(tabu_list_size=50, max_iters=50),
        HILL_CLIMBING_RANDOM_RESET: search.HillClimbingReset(max_restarts=1, max_iters=33333),
        HILL_CLIMBING_RANDOM_RESET_ESTOCASTICO: search.HillClimbingResetEstocastico(max_restarts=1, max_iters=38883)
    }
    # Graficar los tours
    tours = {}
    tours['init'] = (p.init, p.obj_val(p.init))  # estado inicial

    # Resolver el TSP con cada algoritmo
    for algo in algos.values():
        algo.solve(p)

    # Mostrar resultados por linea de comandos
    print("Valor:", "Tiempo:", "Iters:", "Algoritmo:", sep="\t\t")
    for name, algo in algos.items():
        print(algo.value, "%.2f" % algo.time, algo.niters, name, sep="\t\t")

    
    for name, algo in algos.items():
        tours[name] = (algo.tour, algo.value)
    plot.show(G, coords, args.filename, tours)


if __name__ == "__main__":
    main()
