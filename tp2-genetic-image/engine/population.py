from typing import List, Any
from .individual import Individual

class Population:
    """
    Manages a collection of Individual candidate solutions.
    """

    def __init__(self, size: int, n_triangles: int, image_size: tuple):
        """
        Initializes a population of the given size with random individuals.
        
        :param size: Number of individuals in the population.
        :param n_triangles: Number of triangles per individual.
        :param image_size: The target image size (width, height).
        """
        self.individuals: List[Individual] = []
        raise NotImplementedError("Population init stub")

    def evaluate_all(self, fitness_fn: Any, renderer: Any, target_pixels: Any):
        """
        Evaluates the fitness of all individuals in the population.
        
        :param fitness_fn: Function to compute fitness.
        :param renderer: Renderer used to draw the individual into pixels.
        :param target_pixels: The true image pixels to compare against.
        """
        raise NotImplementedError("evaluate_all stub")
