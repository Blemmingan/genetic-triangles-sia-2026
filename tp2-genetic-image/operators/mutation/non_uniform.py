from typing import Any

def mutate(individual: Any, **kwargs) -> Any:
    """
    Non-uniform mutation.
    Similar to uniform, but the extent of mutation or the probability changes 
    over generations (typically decreasing).
    
    :param individual: The Individual to mutate.
    :param kwargs: Should contain current 'generation' to scale the mutation.
    :return: The mutated Individual.
    """
    raise NotImplementedError("non_uniform mutation stub")
