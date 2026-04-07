import random
from typing import Any, List


def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Selección por ranking.

    Idea general
    ------------
    En lugar de usar directamente la fitness real, primero ordenamos
    los individuos por fitness y luego les asignamos una pseudo-fitness
    basada en su posición (ranking).

    Después aplicamos una ruleta sobre esas pseudo-fitness.

    Ventaja
    -------
    Reduce el problema de que un individuo con fitness muy superior
    domine demasiado pronto toda la selección.
    """

    if n_select <= 0:
        raise ValueError("n_select debe ser mayor que 0.")

    if not population.individuals:
        raise ValueError("La población está vacía.")

    for individual in population.individuals:
        if individual.fitness is None:
            raise ValueError(
                "Hay individuos sin fitness. Primero debés evaluar la población."
            )

    # -------------------------------------------------------------
    # 1) Ordenar de mejor a peor
    # -------------------------------------------------------------
    sorted_individuals = sorted(
        population.individuals, key=lambda ind: ind.fitness, reverse=True
    )

    n = len(sorted_individuals)

    # -------------------------------------------------------------
    # 2) Asignar pseudo-fitness por ranking
    # -------------------------------------------------------------
    # Mejor individuo -> peso n
    # Segundo         -> peso n-1
    # ...
    # Peor            -> peso 1
    ranking_weights = [n - i for i in range(n)]
    total_weight = sum(ranking_weights)

    # -------------------------------------------------------------
    # 3) Construir probabilidades acumuladas
    # -------------------------------------------------------------
    cumulative_probs = []
    cumulative = 0.0

    for weight in ranking_weights:
        cumulative += weight / total_weight
        cumulative_probs.append(cumulative)

    cumulative_probs[-1] = 1.0

    # -------------------------------------------------------------
    # 4) Seleccionar por ruleta sobre el ranking
    # -------------------------------------------------------------
    selected: List[Any] = []

    for _ in range(n_select):
        r = random.random()

        for idx, threshold in enumerate(cumulative_probs):
            if r <= threshold:
                selected.append(sorted_individuals[idx].copy())
                break

    return selected
