import random
from copy import deepcopy
from typing import Any, Tuple


def crossover(parent1: Any, parent2: Any, **kwargs) -> Tuple[Any, Any]:
    """
    Cruce de dos puntos (two-point crossover).

    Idea general
    ------------
    Dado un cromosoma representado como una lista de triángulos:

        [T0, T1, T2, T3, T4, T5, ...]

    se eligen dos puntos de corte:
        cut1 < cut2

    y se intercambia el segmento central entre ambos padres.

    Resultado:
    - hijo 1 = inicio de parent1 + medio de parent2 + final de parent1
    - hijo 2 = inicio de parent2 + medio de parent1 + final de parent2

    Parámetros esperados en kwargs
    ------------------------------
    crossover_rate : float
        Probabilidad global de aplicar el cruce.
        Si no se aplica, los hijos son copias de los padres.
        Default: 1.0

    Parámetros
    ----------
    parent1 : Any
        Primer padre.
    parent2 : Any
        Segundo padre.

    Retorna
    -------
    Tuple[Any, Any]
        Dos hijos resultantes del cruce.
    """

    crossover_rate = kwargs.get("crossover_rate", 1.0)

    # -------------------------------------------------------------
    # 1) Crear copias base de los padres
    # -------------------------------------------------------------
    child1 = parent1.copy()
    child2 = parent2.copy()

    # -------------------------------------------------------------
    # 2) Validaciones
    # -------------------------------------------------------------
    if len(parent1.chromosome) != len(parent2.chromosome):
        raise ValueError("Los padres no tienen la misma cantidad de triángulos.")

    chromosome_length = len(parent1.chromosome)

    # Para hacer two-point crossover necesitamos al menos 3 posiciones
    # para que existan dos puntos internos distintos.
    if chromosome_length < 3:
        return child1, child2

    # -------------------------------------------------------------
    # 3) Decidir si se hace crossover
    # -------------------------------------------------------------
    if random.random() > crossover_rate:
        return child1, child2

    # -------------------------------------------------------------
    # 4) Elegir dos puntos de corte distintos
    # -------------------------------------------------------------
    cut1, cut2 = sorted(random.sample(range(1, chromosome_length), 2))

    # -------------------------------------------------------------
    # 5) Construir cromosomas hijos
    # -------------------------------------------------------------
    child1.chromosome = (
        deepcopy(parent1.chromosome[:cut1])
        + deepcopy(parent2.chromosome[cut1:cut2])
        + deepcopy(parent1.chromosome[cut2:])
    )

    child2.chromosome = (
        deepcopy(parent2.chromosome[:cut1])
        + deepcopy(parent1.chromosome[cut1:cut2])
        + deepcopy(parent2.chromosome[cut2:])
    )

    # -------------------------------------------------------------
    # 6) Invalidar fitness
    # -------------------------------------------------------------
    child1.fitness = None
    child2.fitness = None

    return child1, child2
