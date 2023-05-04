from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

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
        explored[node.state] = True
        frontier = QueueFrontier()
        frontier.add(node)
        while not frontier.is_empty():
            node = frontier.remove()
            neighbors = grid.get_neighbours(node.state)
            for action in neighbors:
                new_state = neighbors[action]
                if new_state not in explored:
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                    new_node.parent = node
                    new_node.action = action
                    if new_state == grid.end:
                        return Solution(node, explored)
                    explored[new_state] = True
                    frontier.add(new_node)
        return NoSolution(explored)
