from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        # Initialize the explored dictionary to be empty
        explored = {}
        frontier = StackFrontier()
        frontier.add(node)
        while not frontier.is_empty():
            node = frontier.remove()
            explored[node.state] = True
            if node.state == grid.end:
                return Solution(node, explored)
            neighbours = grid.get_neighbours(node.state)
            for neighbor_state in neighbours:
                new_state = neighbours[neighbor_state]
                if new_state not in explored:
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                    new_node.parent = node
                    new_node.action = neighbor_state
                    frontier.add(new_node)
        return NoSolution(explored)
