from ..models.grid import Grid
from src.pathfinder.models.frontier import PriorityQueueFrontier
from src.pathfinder.models.node import Node
from src.pathfinder.models.solution import NoSolution, Solution
from typing import Dict, Tuple


def function_heuristic(state, goal):
    """Calculate the Euclidean distance heuristic between two points"""
    x1, y1 = state
    x2, y2 = goal
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def init_heuristic(grid: Grid, algorithm="A*"):
    start_node = Node("", grid.start, 0)
    if algorithm == "A*":
        cost = start_node.cost + int(function_heuristic(start_node.state, grid.end))
    else:
        cost = int(function_heuristic(start_node.state, grid.end))
    frontier = PriorityQueueFrontier()
    frontier.add(start_node, cost)
    return frontier


def common_heuristic(grid: Grid, algorithm="A*") -> Solution:
    explored: Dict[Tuple[int, int], bool] = {}
    if algorithm == "A*":
        frontier = init_heuristic(grid)
    else:
        frontier = init_heuristic(grid, algorithm="greedy")
    while not frontier.is_empty():
        node = frontier.pop()
        if node.state == grid.end:
            return Solution(node, explored)
        if node.state in explored:
            continue
        explored[node.state] = True
        neighbours = grid.get_neighbours(node.state)
        for neighbour_state in neighbours:
            new_state = neighbours[neighbour_state]
            if neighbour_state not in explored:
                new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                new_node.parent = node
                new_node.action = neighbour_state
                if algorithm == "A*":
                    priority = new_node.cost + int(function_heuristic(new_state, grid.end))
                else:
                    priority = int(function_heuristic(new_state, grid.end))
                frontier.add(new_node, priority)
    return NoSolution(explored)
