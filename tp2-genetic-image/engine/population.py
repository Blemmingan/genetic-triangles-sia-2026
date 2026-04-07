from typing import List

from PIL import Image

from engine.individual import Individual
from fitness.image_fitness import compute_fitness


class Population:
    """
    Representa una población de individuos.
    """

    def __init__(self, size: int, num_triangles: int):
        self.size = size
        self.num_triangles = num_triangles
        self.individuals: List[Individual] = []

    def initialize_random(self):
        """
        Inicializa la población de forma completamente aleatoria.
        """
        self.individuals = []

        for _ in range(self.size):
            individual = Individual(num_triangles=self.num_triangles)
            individual.random_init()
            self.individuals.append(individual)

    def initialize_guided(
        self,
        target_image: Image.Image,
        alpha_range=(0.2, 0.8),
        triangle_size_range=(0.05, 0.35),
        color_jitter=0.05,
    ):
        """
        Inicializa la población usando información de la imagen objetivo.
        """
        self.individuals = []

        for _ in range(self.size):
            individual = Individual(num_triangles=self.num_triangles)
            individual.guided_init(
                target_image=target_image,
                alpha_range=alpha_range,
                triangle_size_range=triangle_size_range,
                color_jitter=color_jitter,
            )
            self.individuals.append(individual)

    def evaluate_all(self, target_image: Image.Image):
        """
        Evalúa la fitness de todos los individuos.
        """
        for individual in self.individuals:
            individual.fitness = compute_fitness(individual, target_image)

    def get_best(self) -> Individual:
        if not self.individuals:
            raise ValueError("La población está vacía.")

        for individual in self.individuals:
            if individual.fitness is None:
                raise ValueError(
                    "Hay individuos sin fitness. Primero debés llamar a evaluate_all()."
                )

        return max(self.individuals, key=lambda ind: ind.fitness)

    def get_worst(self) -> Individual:
        if not self.individuals:
            raise ValueError("La población está vacía.")

        for individual in self.individuals:
            if individual.fitness is None:
                raise ValueError(
                    "Hay individuos sin fitness. Primero debés llamar a evaluate_all()."
                )

        return min(self.individuals, key=lambda ind: ind.fitness)

    def get_average_fitness(self) -> float:
        if not self.individuals:
            raise ValueError("La población está vacía.")

        for individual in self.individuals:
            if individual.fitness is None:
                raise ValueError(
                    "Hay individuos sin fitness. Primero debés llamar a evaluate_all()."
                )

        total = sum(individual.fitness for individual in self.individuals)
        return total / len(self.individuals)

    def get_fitness_values(self):
        if not self.individuals:
            raise ValueError("La población está vacía.")

        for individual in self.individuals:
            if individual.fitness is None:
                raise ValueError(
                    "Hay individuos sin fitness. Primero debés llamar a evaluate_all()."
                )

        return [individual.fitness for individual in self.individuals]

    def set_individuals(self, individuals: List[Individual]):
        if len(individuals) != self.size:
            raise ValueError(
                f"La cantidad de individuos recibida ({len(individuals)}) "
                f"no coincide con el tamaño de la población ({self.size})."
            )

        self.individuals = individuals

    def copy(self) -> "Population":
        new_population = Population(size=self.size, num_triangles=self.num_triangles)
        new_population.individuals = [
            individual.copy() for individual in self.individuals
        ]
        return new_population

    def __len__(self):
        return len(self.individuals)

    def __repr__(self):
        return (
            f"Population(size={self.size}, "
            f"num_triangles={self.num_triangles}, "
            f"loaded_individuals={len(self.individuals)})"
        )
