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
        frontier = QueueFrontier()
        frontier.add(node)
        explored[node.state] = True
        while not frontier.is_empty():
            node = frontier.remove()
            explored[node.state] = True
            if node.state == grid.end:
                return Solution(node, explored)
            neighbours = grid.get_neighbours(node.state)
            for neighbor_state in neighbours:
                node_state = neighbours[neighbor_state]
                if node_state not in explored and not frontier.contains_state(node_state):
                    new_node = Node("", node_state, node.cost + grid.get_cost(node_state))
                    new_node.parent = node
                    new_node.action = neighbor_state
                    frontier.add(new_node)
        return NoSolution(explored)
