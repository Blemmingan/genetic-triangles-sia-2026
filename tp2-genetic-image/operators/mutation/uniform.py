import random
from copy import deepcopy
from typing import Any, Tuple


def crossover(parent1: Any, parent2: Any, **kwargs) -> Tuple[Any, Any]:
    """
    Cruce uniforme (uniform crossover).

    Idea general
    ------------
    En lugar de elegir un único punto de corte, decidimos para cada
    posición del cromosoma (en este caso, cada triángulo) de qué padre
    hereda cada hijo.

    En este problema trabajamos a nivel de triángulos:
        cromosoma = [triángulo_1, triángulo_2, ..., triángulo_n]

    Entonces, para cada índice i:
    - con cierta probabilidad, el hijo 1 toma el triángulo i del padre 1
      y el hijo 2 toma el triángulo i del padre 2
    - en caso contrario, se intercambian

    Parámetros esperados en kwargs
    ------------------------------
    crossover_rate : float
        Probabilidad global de realizar el cruce.
        Si no se cruza, los hijos son copias de los padres.
        Default: 1.0

    swap_probability : float
        Probabilidad de intercambiar en una posición dada.
        Por default usamos 0.5, que es el caso más clásico.

    Parámetros
    ----------
    parent1 : Any
        Primer padre.
    parent2 : Any
        Segundo padre.

    Retorna
    -------
    Tuple[Any, Any]
        Dos hijos resultantes del cruce uniforme.

    Nota importante
    ---------------
    Hacemos el cruce a nivel de TRIÁNGULOS, no a nivel de valores
    internos del triángulo. Esto mantiene una estructura más coherente.
    """

    crossover_rate = kwargs.get("crossover_rate", 1.0)
    swap_probability = kwargs.get("swap_probability", 0.5)

    # -------------------------------------------------------------
    # 1) Crear copias base de los padres
    # -------------------------------------------------------------
    child1 = parent1.copy()
    child2 = parent2.copy()

    # -------------------------------------------------------------
    # 2) Validaciones básicas
    # -------------------------------------------------------------
    if len(parent1.chromosome) != len(parent2.chromosome):
        raise ValueError(
            "Los padres no tienen la misma cantidad de triángulos."
        )

    chromosome_length = len(parent1.chromosome)

    if chromosome_length == 0:
        return child1, child2

    # -------------------------------------------------------------
    # 3) Decidir si se realiza el cruce o no
    # -------------------------------------------------------------
    if random.random() > crossover_rate:
        return child1, child2

    # -------------------------------------------------------------
    # 4) Construir nuevos cromosomas hijo
    # -------------------------------------------------------------
    new_chromosome_1 = []
    new_chromosome_2 = []

    for i in range(chromosome_length):
        gene1 = parent1.chromosome[i]
        gene2 = parent2.chromosome[i]

        # Con probabilidad swap_probability intercambiamos el origen
        if random.random() < swap_probability:
            new_chromosome_1.append(deepcopy(gene2))
            new_chromosome_2.append(deepcopy(gene1))
        else:
            new_chromosome_1.append(deepcopy(gene1))
            new_chromosome_2.append(deepcopy(gene2))

    child1.chromosome = new_chromosome_1
    child2.chromosome = new_chromosome_2

    # -------------------------------------------------------------
    # 5) Invalidar fitness
    # -------------------------------------------------------------
    child1.fitness = None
    child2.fitness = None

    return child1, child2