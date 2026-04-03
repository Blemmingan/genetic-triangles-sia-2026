import random
from typing import List, Tuple

class Individual:
    """
    Represents a single candidate solution (a set of semi-transparent triangles).
    """

    def __init__(self):
        """
        Initializes an empty individual.
        'chromosome' is a list of N triangles, where each triangle is:
        [x1, y1, x2, y2, x3, y3, r, g, b, a] (all floats normalized 0-1).
        """
        self.chromosome: List[List[float]] = []
        self.fitness: float = None

    def random_init(self, n_triangles: int, image_size: Tuple[int, int]):
        """
        Initializes the chromosome with random triangles.
        
        :param n_triangles: Number of triangles.
        :param image_size: Tuple of (width, height) used if scaling is needed, 
                           though parameters are generally 0-1.
        """
        raise NotImplementedError("random_init stub")

    def copy(self) -> 'Individual':
        """
        Creates and returns a deep copy of this individual.
        """
        raise NotImplementedError("copy stub")

    def __repr__(self) -> str:
        return f"<Individual (fitness={self.fitness}, triangles={len(self.chromosome)})>"
