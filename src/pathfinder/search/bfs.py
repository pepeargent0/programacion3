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
        while True:
            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)
            # Remove a node from the frontier
            node = frontier.remove()
            # Add the node to the explored dictionary
            explored[node.state] = True
            # Return if the node contains a goal state
            if node.state == grid.end:
                return Solution(node, explored)
            # BFS
            neighbours = grid.get_neighbours(node.state)
            for neighbor_state in neighbours:
                new_state = neighbours[neighbor_state]
                if neighbor_state not in explored and not frontier.contains_state(new_state):
                    print(new_state)
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                    new_node.parent = node
                    new_node.action = neighbor_state
                    # Add the new node to the frontier
                    frontier.add(new_node)

        return NoSolution(explored)