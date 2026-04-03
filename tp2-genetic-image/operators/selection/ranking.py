from typing import List, Any

def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Ranking selection.
    Ranks the population by fitness, assigns pseudo-fitness values based on rank,
    and typically performs roulette wheel selection using these pseudo-fitness values.
    
    :param population: The current Population object.
    :param n_select: Number of individuals to select.
    :return: A list of selected individuals.
    """
    raise NotImplementedError("ranking selection stub")
