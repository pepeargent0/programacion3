from src.pathfinder.models.frontier import PriorityQueueFrontier
from src.pathfinder.models.node import Node


def init_heuristic(grid):
    start_node = Node("", grid.start, 0)
    start_node.f_cost = start_node.cost + int(grid.heuristic(start_node.state, grid.end))
    # Initialize the explored dictionary to be empty
    frontier = PriorityQueueFrontier()
    frontier.add(start_node)
    return frontier
