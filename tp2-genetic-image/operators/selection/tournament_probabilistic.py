import random
from typing import List, Any


def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Selección por torneo probabilístico.

    Idea general
    ------------
    En cada selección:
    1. se eligen 2 individuos al azar
    2. con probabilidad 'threshold' se elige el más apto
    3. con probabilidad (1 - threshold) se elige el menos apto

    Esto introduce más diversidad que el torneo determinístico,
    porque el mejor no gana siempre.

    Parámetros esperados en kwargs
    ------------------------------
    tournament_threshold : float
        Probabilidad de elegir al mejor individuo del torneo.
        Debe estar en [0.5, 1.0].
        Default: 0.75
    """

    threshold = kwargs.get("tournament_threshold", 0.75)

    if n_select <= 0:
        raise ValueError("n_select debe ser mayor que 0.")

    if not (0.5 <= threshold <= 1.0):
        raise ValueError("tournament_threshold debe estar entre 0.5 y 1.0.")

    if not population.individuals:
        raise ValueError("La población está vacía.")

    for individual in population.individuals:
        if individual.fitness is None:
            raise ValueError(
                "Hay individuos sin fitness. Primero debés evaluar la población."
            )

    if len(population.individuals) == 1:
        return [population.individuals[0].copy() for _ in range(n_select)]

    selected: List[Any] = []

    for _ in range(n_select):
        a, b = random.sample(population.individuals, 2)

        best = a if a.fitness >= b.fitness else b
        worst = b if best is a else a

        if random.random() < threshold:
            selected.append(best.copy())
        else:
            selected.append(worst.copy())

    return selected