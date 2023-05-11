from src.pathfinder.models.frontier import PriorityQueueFrontier
from src.pathfinder.models.node import Node


def init_heuristic(grid):
    start_node = Node("", grid.start, 0)
    # Initialize the explored dictionary to be empty
    costo = start_node.cost + int(grid.heuristic(start_node.state, grid.end))
    frontier = PriorityQueueFrontier()
    frontier.add(start_node, costo)
    return frontier
