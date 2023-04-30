from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        explored = {}
        frontier = PriorityQueueFrontier()
        frontier.add(node)
        while True:
            if frontier.is_empty():
                return NoSolution(explored)
            node = frontier.pop()
            explored[node.state] = True

            if node.state == grid.end:
                return Solution(node, explored)

            if node.state not in explored or node.cost < explored[node.state]:
                explored[node.state] = node.cost
                neighbours = grid.get_neighbours(node.state)
                for neighbour_state in neighbours:
                    new_state = neighbours[neighbour_state]
                    new_cost = node.cost + grid.get_cost(new_state)
                    new_node = Node(neighbour_state, new_state, new_cost, node)
                    frontier.add(new_node)
                    print(neighbour_state)
                    print(node.cost, grid.get_cost(new_state))

        return NoSolution(explored)
