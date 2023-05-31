from .heuristic import common_heuristic
from ..models.grid import Grid
from ..models.solution import Solution


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """
        Find path between two points in a grid using Depth First Search
            Args:
                grid (Grid): Grid of points

            Returns:
                Solution: Solution found
        """
        return common_heuristic(grid, "A*")
