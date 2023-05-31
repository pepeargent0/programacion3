from .heuristic import common_heuristic
from ..models.grid import Grid
from ..models.solution import Solution


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """
        Find the shortest path between two points in a grid using Greedy Best First Search algorithm.

        Args:
            grid (Grid): A grid containing the start and end positions.

        Returns:
            Solution: The solution containing the path and the explored nodes.
        """
        return common_heuristic(grid, "greedy")
