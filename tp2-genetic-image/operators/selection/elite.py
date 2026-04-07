from typing import Any, List


def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Selección elite.
    Esta estrategia selecciona directamente a los individuos con mayor fitness.
    """

    #  Validar que la cantidad solicitada tenga sentido
    if n_select <= 0:
        raise ValueError("n_select debe ser mayor que 0.")

    # Verificar que la población no esté vacía
    if not population.individuals:
        raise ValueError("La población está vacía.")

    # Verificar que todos los individuos tengan fitness calculada
    for individual in population.individuals:
        if individual.fitness is None:
            raise ValueError(
                "Hay individuos sin fitness. Primero debés evaluar la población."
            )

    #  Ordenar individuos de mayor a menor fitness
    sorted_individuals = sorted(
        population.individuals, key=lambda ind: ind.fitness, reverse=True
    )

    # Seleccionar los mejores individuos

    selected = []

    while len(selected) < n_select:
        for individual in sorted_individuals:
            if len(selected) >= n_select:
                break

            # Agregamos una copia para evitar efectos colaterales.
            selected.append(individual.copy())

    return selected
