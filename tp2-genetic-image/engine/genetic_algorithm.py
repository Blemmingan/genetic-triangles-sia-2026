import os
from typing import Any, Optional, Callable, List
from PIL import Image

from engine.population import Population
from fitness.image_fitness import compute_fitness
from metrics.tracker import MetricsTracker
from stopping.criteria import StoppingCriteria

from operators.selection.elite import select as elite_select
from operators.selection.roulette import select as roulette_select
from operators.selection.universal import select as universal_select
from operators.selection.boltzmann import select as boltzmann_select
from operators.selection.tournament_deterministic import (
    select as tournament_deterministic_select,
)
from operators.selection.tournament_probabilistic import (
    select as tournament_probabilistic_select,
)
from operators.selection.ranking import select as ranking_select

from operators.crossover.one_point import crossover as one_point_crossover
from operators.crossover.uniform import crossover as uniform_crossover

from operators.mutation.gen import mutate as gen_mutate
from operators.mutation.multigen import mutate as multigen_mutate

from replacement.exclusive import replace as exclusive_replace
from replacement.additive import replace as additive_replace

from operators.mutation.non_uniform import mutate as non_uniform_mutate

from operators.crossover.two_point import crossover as two_point_crossover

from operators.crossover.annular import crossover as annular_crossover


class GeneticAlgorithm:
    def __init__(
        self,
        target_image: Image.Image,
        population_size: int,
        num_triangles: int,
        generations: int,
        selection_method: str = "tournament_deterministic",
        tournament_k: int = 3,
        tournament_threshold: float = 0.75,
        boltzmann_temperature: float = 100.0,
        boltzmann_decay: float = 0.99,
        min_temperature: float = 1e-3,
        crossover_method: str = "one_point",
        crossover_rate: float = 0.8,
        uniform_swap_probability: float = 0.5,
        mutation_method: str = "gen",
        mutation_rate: float = 0.1,
        mutation_mode: str = "delta",
        sigma: float = 0.05,
        multigen_min_genes: int = 3,
        multigen_max_genes: int = 10,
        elite_fraction: float = 0.3,
        replacement_method: str = "exclusive",
        fitness_threshold: Optional[float] = None,
        no_improvement_generations: Optional[int] = None,
        improvement_epsilon: float = 1e-6,
        init_method: str = "guided",
        init_alpha_min: float = 0.2,
        init_alpha_max: float = 0.8,
        init_triangle_size_min: float = 0.05,
        init_triangle_size_max: float = 0.35,
        init_color_jitter: float = 0.05,
        non_uniform_b: float = 2.0,
        annular_min_segment_length: int = 1,
        annular_max_segment_length: Optional[int] = None,
    ):
        self.target_image = target_image
        self.annular_min_segment_length = annular_min_segment_length
        self.annular_max_segment_length = annular_max_segment_length
        self.non_uniform_b = non_uniform_b

        self.population_size = population_size
        self.num_triangles = num_triangles
        self.generations = generations

        self.selection_method = selection_method
        self.tournament_k = tournament_k
        self.tournament_threshold = tournament_threshold
        self.boltzmann_temperature = boltzmann_temperature
        self.boltzmann_decay = boltzmann_decay
        self.min_temperature = min_temperature

        self.crossover_method = crossover_method
        self.crossover_rate = crossover_rate
        self.uniform_swap_probability = uniform_swap_probability

        self.mutation_method = mutation_method
        self.mutation_rate = mutation_rate
        self.mutation_mode = mutation_mode
        self.sigma = sigma
        self.multigen_min_genes = multigen_min_genes
        self.multigen_max_genes = multigen_max_genes

        self.elite_fraction = elite_fraction
        self.replacement_method = replacement_method

        self.init_method = init_method
        self.init_alpha_min = init_alpha_min
        self.init_alpha_max = init_alpha_max
        self.init_triangle_size_min = init_triangle_size_min
        self.init_triangle_size_max = init_triangle_size_max
        self.init_color_jitter = init_color_jitter

        self.population = Population(
            size=self.population_size,
            num_triangles=self.num_triangles
        )

        self.best_individual: Optional[Any] = None
        self.tracker = MetricsTracker()

        self.stopper = StoppingCriteria(
            max_generations=self.generations,
            fitness_threshold=fitness_threshold,
            no_improvement_generations=no_improvement_generations,
            improvement_epsilon=improvement_epsilon,
        )

    def _update_global_best(self):
        current_best = self.population.get_best()

        if self.best_individual is None:
            self.best_individual = current_best.copy()
            return

        if current_best.fitness > self.best_individual.fitness:
            self.best_individual = current_best.copy()

    def _get_fitness_function(self) -> Callable[[Any], float]:
        return lambda individual: compute_fitness(individual, self.target_image)

    def _get_selection_function(self) -> Callable:
        if self.selection_method == "elite":
            return elite_select

        if self.selection_method == "roulette":
            return roulette_select

        if self.selection_method == "universal":
            return universal_select

        if self.selection_method == "boltzmann":
            return boltzmann_select

        if self.selection_method == "tournament_deterministic":
            return tournament_deterministic_select

        if self.selection_method == "tournament_probabilistic":
            return tournament_probabilistic_select

        if self.selection_method == "ranking":
            return ranking_select

        raise ValueError(
            f"selection_method desconocido: {self.selection_method}. "
            f"Usá 'elite', 'roulette', 'universal', 'boltzmann', "
            f"'tournament_deterministic', 'tournament_probabilistic' o 'ranking'."
        )

    def _get_crossover_function(self) -> Callable:
        if self.crossover_method == "one_point":
            return one_point_crossover

        if self.crossover_method == "two_point":
            return two_point_crossover

        if self.crossover_method == "uniform":
            return uniform_crossover

        if self.crossover_method == "annular":
            return annular_crossover

        raise ValueError(
            f"crossover_method desconocido: {self.crossover_method}. "
            f"Usá 'one_point', 'two_point', 'uniform' o 'annular'."
        )

    def _get_replacement_function(self) -> Callable:
        if self.replacement_method == "exclusive":
            return exclusive_replace

        if self.replacement_method == "additive":
            return additive_replace

        raise ValueError(
            f"replacement_method desconocido: {self.replacement_method}. "
            f"Usá 'exclusive' o 'additive'."
        )

    def _select_parents_for_mating(self) -> List[Any]:
        n_parents = max(2, int(self.population_size * self.elite_fraction))
        n_parents = min(n_parents, self.population_size)

        selection_fn = self._get_selection_function()

        if self.selection_method == "tournament_deterministic":
            return selection_fn(
                self.population,
                n_select=n_parents,
                tournament_k=self.tournament_k
            )

        if self.selection_method == "tournament_probabilistic":
            return selection_fn(
                self.population,
                n_select=n_parents,
                tournament_threshold=self.tournament_threshold
            )

        if self.selection_method == "boltzmann":
            current_generation = self.tracker.generations[-1] if self.tracker.generations else 0
            return selection_fn(
                self.population,
                n_select=n_parents,
                generation=current_generation,
                boltzmann_temperature=self.boltzmann_temperature,
                boltzmann_decay=self.boltzmann_decay,
                min_temperature=self.min_temperature,
            )

        return selection_fn(
            self.population,
            n_select=n_parents
        )

    def _apply_crossover(self, parent1: Any, parent2: Any):
        crossover_fn = self._get_crossover_function()

        if self.crossover_method in {"one_point", "two_point"}:
            return crossover_fn(
                parent1,
                parent2,
                crossover_rate=self.crossover_rate
            )

        if self.crossover_method == "uniform":
            return crossover_fn(
                parent1,
                parent2,
                crossover_rate=self.crossover_rate,
                swap_probability=self.uniform_swap_probability
            )

        if self.crossover_method == "annular":
            return crossover_fn(
                parent1,
                parent2,
                crossover_rate=self.crossover_rate,
                min_segment_length=self.annular_min_segment_length,
                max_segment_length=self.annular_max_segment_length,
            )

        raise ValueError(
            f"crossover_method desconocido: {self.crossover_method}"
        )

    def _mutate_child(self, child: Any) -> Any:
        if self.mutation_method == "gen":
            return gen_mutate(
                child,
                mutation_rate=self.mutation_rate,
                mutation_mode=self.mutation_mode,
                sigma=self.sigma
            )

        if self.mutation_method == "multigen":
            return multigen_mutate(
                child,
                mutation_rate=self.mutation_rate,
                mutation_mode=self.mutation_mode,
                sigma=self.sigma,
                min_genes=self.multigen_min_genes,
                max_genes=self.multigen_max_genes
            )

        if self.mutation_method == "non_uniform":
            current_generation = self.tracker.generations[-1] if self.tracker.generations else 0

            return non_uniform_mutate(
                child,
                mutation_rate=self.mutation_rate,
                generation=current_generation,
                max_generations=self.generations,
                b=self.non_uniform_b
        )

        raise ValueError(
            f"mutation_method desconocido: {self.mutation_method}. "
            f"Usá 'gen', 'multigen' o 'non_uniform'."
        )

    def _create_children(self, parents: List[Any], n_children: int) -> List[Any]:
        if len(parents) < 2:
            raise ValueError(
                "Se necesitan al menos 2 padres para generar descendencia."
            )

        children: List[Any] = []
        parent_idx = 0

        while len(children) < n_children:
            parent1 = parents[parent_idx % len(parents)]
            parent2 = parents[(parent_idx + 1) % len(parents)]

            child1, child2 = self._apply_crossover(parent1, parent2)

            child1 = self._mutate_child(child1)
            child2 = self._mutate_child(child2)

            children.append(child1)

            if len(children) < n_children:
                children.append(child2)

            parent_idx += 2

        return children

    def _create_next_generation(self) -> List[Any]:
        mating_parents = self._select_parents_for_mating()

        children = self._create_children(
            parents=mating_parents,
            n_children=self.population_size
        )

        replacement_fn = self._get_replacement_function()
        fitness_fn = self._get_fitness_function()

        next_generation = replacement_fn(
            parents=self.population.individuals,
            children=children,
            fitness_fn=fitness_fn,
            population_size=self.population_size
        )

        if len(next_generation) != self.population_size:
            raise ValueError(
                "La nueva generación no tiene el tamaño esperado."
            )

        return next_generation

    def initialize(self):
        self.stopper.reset()

        if self.init_method == "guided":
            self.population.initialize_guided(
                target_image=self.target_image,
                alpha_range=(self.init_alpha_min, self.init_alpha_max),
                triangle_size_range=(
                    self.init_triangle_size_min,
                    self.init_triangle_size_max,
                ),
                color_jitter=self.init_color_jitter,
            )
        elif self.init_method == "random":
            self.population.initialize_random()
        else:
            raise ValueError(
                f"init_method desconocido: {self.init_method}. "
                f"Usá 'random' o 'guided'."
            )

        self.population.evaluate_all(self.target_image)

        self._update_global_best()
        self.tracker.record(generation=0, population=self.population)

    def run(self) -> Any:
        self.initialize()

        if self.stopper.should_stop(generation=0, population=self.population):
            print(f"\nEjecución detenida: {self.stopper.get_stop_reason()}")
            return self.best_individual

        for generation in range(1, self.generations + 1):
            new_individuals = self._create_next_generation()

            self.population.set_individuals(new_individuals)
            self.population.evaluate_all(self.target_image)

            self._update_global_best()
            self.tracker.record(generation=generation, population=self.population)

            best = self.population.get_best()
            avg = self.population.get_average_fitness()

            print(
                f"Generación {generation:04d} | "
                f"Best: {best.fitness:.6f} | "
                f"Avg: {avg:.6f} | "
                f"Selection: {self.selection_method} | "
                f"Crossover: {self.crossover_method} | "
                f"Mutation: {self.mutation_method} | "
                f"Replacement: {self.replacement_method} | "
                f"Init: {self.init_method}"
            )

            if self.stopper.should_stop(generation=generation, population=self.population):
                print(f"\nEjecución detenida: {self.stopper.get_stop_reason()}")
                break

        return self.best_individual

    def save_metrics(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)

        json_path = os.path.join(output_dir, "metrics.json")
        plot_path = os.path.join(output_dir, "fitness_plot.png")

        self.tracker.save_json(json_path)
        self.tracker.plot(plot_path)

        print("\nMétricas guardadas:")
        print(f"- JSON : {json_path}")
        print(f"- Plot : {plot_path}")