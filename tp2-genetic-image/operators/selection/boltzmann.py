from typing import List, Any

def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Boltzmann selection: selects individuals with probabilities scaled
    by a temperature parameter, which decays over generations.
    
    :param population: The current Population object.
    :param n_select: Number of individuals to select.
    :param kwargs: Should contain 'temperature' or generation index.
    :return: A list of selected individuals.
    """
    raise NotImplementedError("boltzmann selection stub")
