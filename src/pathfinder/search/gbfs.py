from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from typing import Dict, Tuple


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """
        Find the shortest path between two points in a grid using Greedy Best First Search algorithm.

        Args:
            grid (Grid): A grid containing the start and end positions.

        Returns:
            Solution: The solution containing the path and the explored nodes.
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        node.f_cost = node.cost + int(grid.heuristic(node.state, grid.end))
        # Initialize the explored set to be empty
        explored: Dict[Tuple[int, int], bool] = {}
        # Initialize the frontier with the starting node
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        while not frontier.is_empty():
            node = frontier.pop()
            if node.state == grid.end:
                return Solution(node, explored)
            if node.state in explored:
                continue
            explored[node.state] = True
            neighbours = grid.get_neighbours(node.state)
            for neighbour_state in neighbours:
                new_state = neighbours[neighbour_state]
                if neighbour_state not in explored:
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                    new_node.parent = node
                    new_node.action = neighbour_state
                    new_node.f_cost = new_node.cost + grid.heuristic(new_state, grid.end)
                    frontier.add(new_node)
        return NoSolution(explored)
