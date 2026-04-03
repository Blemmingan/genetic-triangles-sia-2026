from typing import Dict, Any

class StoppingCriteria:
    """
    Evaluates whether the Genetic Algorithm should terminate based on configured criteria.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the stopping criteria manager.
        
        :param config: Dictionary containing limits such as 'max_generations',
                       'fitness_threshold', or 'convergence_generations'.
        """
        self.config = config
        raise NotImplementedError("StoppingCriteria init stub")

    def should_stop(self, generation: int, best_fitness: float, population: Any) -> bool:
        """
        Checks all configured stopping criteria.
        
        Criteria might include:
        - Max generations reached.
        - Absolute fitness threshold met.
        - Structural / Content convergence (no improvement for N generations).
        
        :param generation: Current generation index.
        :param best_fitness: Best fitness in the current population.
        :param population: The current Population object (for detailed checks).
        :return: True if the algorithm should stop, False otherwise.
        """
        raise NotImplementedError("should_stop stub")
