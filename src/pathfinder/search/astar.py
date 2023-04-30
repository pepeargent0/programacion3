from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        # Initialize the explored dictionary to be empty
        explored = {}
        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost + grid.heuristic(node.state, grid.end))
        while not frontier.is_empty():
            node = frontier.pop()
            explored[node.state] = True
            if node.state == grid.end:
                return Solution(node, explored)
            neighbours = grid.get_neighbours(node.state)
            for neighbor_state in neighbours:
                new_state = neighbours[neighbor_state]

                #print(frontier.frontier)
                if neighbor_state not in explored and not frontier.contains_state(new_state):
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                    new_node.parent = node
                    new_node.action = neighbor_state
                    frontier.add(new_node, new_node.cost + grid.heuristic(new_state, grid.end))
        return NoSolution(explored)
