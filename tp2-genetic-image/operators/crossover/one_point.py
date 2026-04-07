import random
from copy import deepcopy
from typing import Any, Tuple


def crossover(parent1: Any, parent2: Any, **kwargs) -> Tuple[Any, Any]:
    """
    Cruce de un punto (one-point crossover).

    Idea general
    ------------
    Cada individuo está compuesto por una lista de triángulos.
    Entonces el cromosoma tiene esta forma conceptual:

        [triángulo_1, triángulo_2, ..., triángulo_n]

    El cruce de un punto consiste en:
    1. elegir un punto de corte
    2. tomar el prefijo de un padre
    3. combinarlo con el sufijo del otro padre

    Resultado:
    - hijo 1 = inicio de parent1 + final de parent2
    - hijo 2 = inicio de parent2 + final de parent1

    Parámetros esperados en kwargs
    ------------------------------
    crossover_rate : float
        Probabilidad de realizar realmente el cruce.
        Si no se cruza, los hijos serán copias de los padres.
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

    Nota importante
    ---------------
    En este problema hacemos el cruce a nivel de TRIÁNGULOS,
    no a nivel de parámetros internos del triángulo.
    Eso mantiene una estructura genética más coherente.
    """

    # Leer probabilidad de cruce
    crossover_rate = kwargs.get("crossover_rate", 1.0)

    # Crear copias base de los padres

    child1 = parent1.copy()
    child2 = parent2.copy()

    # Validaciones básicas

    if len(parent1.chromosome) != len(parent2.chromosome):
        raise ValueError("Los padres no tienen la misma cantidad de triángulos.")

    chromosome_length = len(parent1.chromosome)

    # Si no hay triángulos o hay uno solo, no tiene sentido cortar.
    # En ese caso devolvemos copias tal cual.
    if chromosome_length <= 1:
        return child1, child2

    # Decidir si se realiza el cruce o no
    if random.random() > crossover_rate:
        return child1, child2

    # Elegir punto de corte
    # Elegimos un índice entre 1 y chromosome_length - 1.

    cut_point = random.randint(1, chromosome_length - 1)

    # Construir los cromosomas hijos
    # Usamos deepcopy para evitar compartir referencias internas
    # a los triángulos entre hijos y padres.
    child1.chromosome = deepcopy(parent1.chromosome[:cut_point]) + deepcopy(
        parent2.chromosome[cut_point:]
    )

    child2.chromosome = deepcopy(parent2.chromosome[:cut_point]) + deepcopy(
        parent1.chromosome[cut_point:]
    )

    # Invalidar fitness
    # Como los cromosomas cambiaron, las fitness anteriores ya no valen.
    child1.fitness = None
    child2.fitness = None

    return child1, child2
