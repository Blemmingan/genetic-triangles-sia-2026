from typing import List, Any

def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Deterministic Tournament selection.
    Randomly picks groups of 'k' individuals and selects the best from each group.
    
    :param population: The current Population object.
    :param n_select: Number of individuals to select.
    :param kwargs: Expected to contain 'tournament_k' (group size).
    :return: A list of selected individuals.
    """
    raise NotImplementedError("deterministic tournament selection stub")
