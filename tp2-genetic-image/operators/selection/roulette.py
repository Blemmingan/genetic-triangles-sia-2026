from typing import List, Any

def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Roulette wheel selection: selects individuals with probability proportional to their fitness.
    
    :param population: The current Population object.
    :param n_select: Number of individuals to select.
    :return: A list of selected individuals.
    """
    raise NotImplementedError("roulette selection stub")
