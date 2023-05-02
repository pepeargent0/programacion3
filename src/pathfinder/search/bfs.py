from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
import time


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        # Initialize the explored dictionary to be empty
        explored = {}
        frontier = QueueFrontier()
        frontier.add(node)
        start_time = time.time()
        timeout = 5  # Timeout in seconds
        while not frontier.is_empty():
            # Check if the elapsed time exceeds the timeout
            if time.time() - start_time > timeout:
                return NoSolution(explored)
            node = frontier.remove()
            explored[node.state] = True
            if node.state == grid.end:
                return Solution(node, explored)
            neighbors = grid.get_neighbours(node.state)
            for neighbor_state in neighbors:
                new_state = neighbors[neighbor_state]
                if neighbor_state not in explored and not frontier.contains_state(new_state):
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                    new_node.parent = node
                    new_node.action = neighbor_state
                    frontier.add(new_node)
        return NoSolution(explored)
