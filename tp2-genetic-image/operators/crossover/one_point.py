from typing import Tuple, Any

def crossover(parent1: Any, parent2: Any, **kwargs) -> Tuple[Any, Any]:
    """
    One-point crossover: picks a random point and swaps the tails of the parents
    to create two offspring.
    
    :param parent1: The first parent Individual.
    :param parent2: The second parent Individual.
    :return: A tuple of two offspring Individuals.
    """
    raise NotImplementedError("one_point crossover stub")
