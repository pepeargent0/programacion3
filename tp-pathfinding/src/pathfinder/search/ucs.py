from ..models.frontier import PriorityQueueFrontier
from typing import Dict, Tuple
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """
        Find path between two points in a grid using Depth First Search
            Args:
                grid (Grid): Grid of points

            Returns:
                Solution: Solution found
        """
        # Initialize a node with the initial position
        start_node = Node("", grid.start, 0)
        explored: Dict[Tuple[int, int], bool] = {}
        frontier = PriorityQueueFrontier()
        frontier.add(start_node, start_node.cost)
        while not frontier.is_empty():
            node = frontier.pop()
            if node.state in explored:
                continue
            explored[node.state] = True
            if node.state == grid.end:
                return Solution(node, explored)
            neighbours = grid.get_neighbours(node.state)
            for neighbor_state in neighbours:
                new_state = neighbours[neighbor_state]
                if neighbours[neighbor_state] not in explored:
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                    new_node.parent = node
                    new_node.action = neighbor_state
                    frontier.add(new_node, node.cost + grid.get_cost(new_state) )
        return NoSolution(explored)
