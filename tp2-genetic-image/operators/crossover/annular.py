import random
from copy import deepcopy
from typing import Any, Tuple


def crossover(parent1: Any, parent2: Any, **kwargs) -> Tuple[Any, Any]:
    """
    Cruce anular (annular crossover).

    Idea general
    ------------
    El cromosoma se considera circular.
    Se elige:
    - un punto de inicio
    - una longitud del segmento a intercambiar

    Luego se intercambia ese segmento entre ambos padres.
    Si el segmento sobrepasa el final del cromosoma, continúa desde
    el inicio (comportamiento circular).

    Parámetros esperados en kwargs
    ------------------------------
    crossover_rate : float
        Probabilidad global de aplicar crossover.
        Default: 1.0

    min_segment_length : int
        Longitud mínima del segmento intercambiado.
        Default: 1

    max_segment_length : int | None
        Longitud máxima del segmento intercambiado.
        Si es None, se usa chromosome_length - 1.

    Parámetros
    ----------
    parent1 : Any
        Primer padre.
    parent2 : Any
        Segundo padre.

    Retorna
    -------
    Tuple[Any, Any]
        Dos hijos resultantes del cruce anular.
    """

    crossover_rate = kwargs.get("crossover_rate", 1.0)
    min_segment_length = kwargs.get("min_segment_length", 1)
    max_segment_length = kwargs.get("max_segment_length", None)

    # -------------------------------------------------------------
    # 1) Copias base
    # -------------------------------------------------------------
    child1 = parent1.copy()
    child2 = parent2.copy()

    # -------------------------------------------------------------
    # 2) Validaciones
    # -------------------------------------------------------------
    if len(parent1.chromosome) != len(parent2.chromosome):
        raise ValueError("Los padres no tienen la misma cantidad de triángulos.")

    chromosome_length = len(parent1.chromosome)

    if chromosome_length < 2:
        return child1, child2

    # -------------------------------------------------------------
    # 3) Decidir si se realiza crossover
    # -------------------------------------------------------------
    if random.random() > crossover_rate:
        return child1, child2

    # -------------------------------------------------------------
    # 4) Ajustar rango de longitud del segmento
    # -------------------------------------------------------------
    if max_segment_length is None:
        max_segment_length = chromosome_length - 1

    min_segment_length = max(1, min(min_segment_length, chromosome_length - 1))
    max_segment_length = max(
        min_segment_length, min(max_segment_length, chromosome_length - 1)
    )

    segment_length = random.randint(min_segment_length, max_segment_length)

    # -------------------------------------------------------------
    # 5) Elegir inicio del segmento circular
    # -------------------------------------------------------------
    start_idx = random.randrange(chromosome_length)

    # Índices circulares a intercambiar
    segment_indices = [
        (start_idx + offset) % chromosome_length for offset in range(segment_length)
    ]

    # -------------------------------------------------------------
    # 6) Construir nuevos cromosomas
    # -------------------------------------------------------------
    new_chromosome_1 = deepcopy(parent1.chromosome)
    new_chromosome_2 = deepcopy(parent2.chromosome)

    for idx in segment_indices:
        new_chromosome_1[idx] = deepcopy(parent2.chromosome[idx])
        new_chromosome_2[idx] = deepcopy(parent1.chromosome[idx])

    child1.chromosome = new_chromosome_1
    child2.chromosome = new_chromosome_2

    # -------------------------------------------------------------
    # 7) Invalidar fitness
    # -------------------------------------------------------------
    child1.fitness = None
    child2.fitness = None

    return child1, child2
