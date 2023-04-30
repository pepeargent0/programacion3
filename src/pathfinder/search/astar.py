from typing import Dict, Tuple
from ..models.frontier import PriorityQueueFrontier
from ..models.grid import Grid
from ..models.node import Node
from ..models.solution import Solution, NoSolution


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """
        Find path between two points in a grid using Depth First Search
            Args:
                grid (Grid): Grid of points

            Returns:
                Solution: Solution found
        """
        # Initialize start node with heuristic cost 0
        start_node = Node("", grid.start, 0)
        start_node.f_cost = start_node.cost + int(grid.heuristic(start_node.state, grid.end))
        # Initialize the explored dictionary to be empty
        explored: Dict[Tuple[int, int], bool] = {}
        frontier = PriorityQueueFrontier()
        frontier.add(start_node)
        while not frontier.is_empty():
            node = frontier.pop()
            if node.state == grid.end:
                return Solution(node, explored)
            if node.state in explored:
                continue
            explored[node.state] = True
            neighbours = grid.get_neighbours(node.state)
            for neighbor_state in neighbours:
                new_state = neighbours[neighbor_state]
                if neighbor_state not in explored:
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                    new_node.parent = node
                    new_node.action = neighbor_state
                    new_node.f_cost = node.cost + grid.get_cost(new_state) + grid.heuristic(new_state, grid.end)
                    frontier.add(new_node)
        return NoSolution(explored)
