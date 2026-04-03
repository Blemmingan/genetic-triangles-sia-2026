from typing import List, Any

def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Universal selection: similar to roulette, but uses evenly spaced pointers 
    to sample the population, reducing stochastic noise.
    
    :param population: The current Population object.
    :param n_select: Number of individuals to select.
    :return: A list of selected individuals.
    """
    raise NotImplementedError("universal selection stub")
