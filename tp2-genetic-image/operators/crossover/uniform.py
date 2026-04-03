from typing import Tuple, Any

def crossover(parent1: Any, parent2: Any, **kwargs) -> Tuple[Any, Any]:
    """
    Uniform crossover: for each gene, offspring receives it uniformly at random
    from either parent 1 or parent 2.
    
    :param parent1: The first parent Individual.
    :param parent2: The second parent Individual.
    :return: A tuple of two offspring Individuals.
    """
    raise NotImplementedError("uniform crossover stub")
