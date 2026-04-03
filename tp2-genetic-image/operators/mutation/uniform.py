from typing import Any

def mutate(individual: Any, **kwargs) -> Any:
    """
    Uniform mutation.
    Iterates over all genes and with a certain probability p_m, mutates each gene.
    
    :param individual: The Individual to mutate.
    :param kwargs: Should contain mutation probability 'p_m'.
    :return: The mutated Individual.
    """
    raise NotImplementedError("uniform mutation stub")
