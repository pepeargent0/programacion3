"""
from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        print(grid.start, grid.end)

        # Initialize the explored dictionary to be empty
        explored = {}
        frontier = PriorityQueueFrontier()
        frontier.add(node, grid.heuristic(node.state, grid.end))

        while True:
            if frontier.is_empty():
                return NoSolution(explored)
            node = frontier.pop()
            print(node, node.cost)
            explored[node.state] = True
            if node.state == grid.end:
                return Solution(node, explored)
            neighbours = grid.get_neighbours(node.state)
            for neighbor_state in neighbours:
                if neighbor_state not in explored:

                    new_node = Node("", neighbor_state, node.cost + grid.get_cost(neighbor_state))
                    new_node.parent = node
                    new_node.action = neighbor_state
                    frontier.add(new_node, grid.heuristic(neighbor_state, grid.end))
                    print('frontier', frontier)
                    print('node', new_node)
        return NoSolution(explored)
"""
from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
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
        node = Node("", grid.start, 0)
        node.f_cost = node.cost + grid.heuristic(node.state, grid.end)
        # Initialize the explored dictionary to be empty
        explored = {}
        frontier = PriorityQueueFrontier()
        # frontier.add(node, grid.heuristic(node.state, grid.end))
        frontier.add(node)
        print(frontier)
        while True:
            if frontier.is_empty():
                return NoSolution(explored)
            node = frontier.pop()
            explored[node.state] = True
            if node.state == grid.end:
                return Solution(node, explored)
            neighbours = grid.get_neighbours(node.state)
            for neighbor_state in neighbours:
                if neighbor_state not in explored:
                    new_state = neighbours[neighbor_state]
                    new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                    new_node.parent = node
                    new_node.action = neighbor_state
                    new_node.f_cost = node.cost + grid.get_cost(new_state) + grid.heuristic(new_state, grid.end)
                    frontier.add(new_node)

        return NoSolution(explored)
