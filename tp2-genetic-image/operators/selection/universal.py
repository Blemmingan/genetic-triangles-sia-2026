import random
from typing import List, Any


def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Selección universal (Stochastic Universal Sampling).

    Idea general
    ------------
    Es parecida a la ruleta, pero en vez de tirar n_select números
    aleatorios independientes, se tira un único punto inicial y luego
    se generan punteros regularmente espaciados.

    Eso reduce la varianza de la selección y hace el muestreo más estable.

    Ejemplo conceptual
    ------------------
    Si queremos seleccionar K individuos, usamos punteros:
        r, r + 1/K, r + 2/K, ..., r + (K-1)/K

    donde r se elige al azar en [0, 1/K).

    Parámetros
    ----------
    population : Any
        Objeto Population ya evaluado.

    n_select : int
        Cantidad de individuos a seleccionar.

    Retorna
    -------
    List[Any]
        Lista de individuos seleccionados (copias).

    Nota
    ----
    Esta implementación asume fitness no negativas.
    """

    # -------------------------------------------------------------
    # 1) Validaciones básicas
    # -------------------------------------------------------------
    if n_select <= 0:
        raise ValueError("n_select debe ser mayor que 0.")

    if not population.individuals:
        raise ValueError("La población está vacía.")

    for individual in population.individuals:
        if individual.fitness is None:
            raise ValueError(
                "Hay individuos sin fitness. "
                "Primero debés evaluar la población."
            )
        if individual.fitness < 0:
            raise ValueError(
                "La selección universal requiere fitness no negativas."
            )

    # -------------------------------------------------------------
    # 2) Suma total de fitness
    # -------------------------------------------------------------
    total_fitness = sum(ind.fitness for ind in population.individuals)

    # -------------------------------------------------------------
    # 3) Caso especial: total_fitness == 0
    # -------------------------------------------------------------
    # Si nadie tiene ventaja, seleccionamos uniformemente al azar.
    if total_fitness == 0:
        return [random.choice(population.individuals).copy() for _ in range(n_select)]

    # -------------------------------------------------------------
    # 4) Probabilidades acumuladas
    # -------------------------------------------------------------
    cumulative_probs = []
    cumulative = 0.0

    for individual in population.individuals:
        relative_prob = individual.fitness / total_fitness
        cumulative += relative_prob
        cumulative_probs.append(cumulative)

    cumulative_probs[-1] = 1.0

    # -------------------------------------------------------------
    # 5) Generar los punteros universales
    # -------------------------------------------------------------
    step = 1.0 / n_select
    start = random.uniform(0.0, step)

    pointers = [start + i * step for i in range(n_select)]

    # -------------------------------------------------------------
    # 6) Seleccionar individuos usando los punteros
    # -------------------------------------------------------------
    selected: List[Any] = []
    idx = 0

    for pointer in pointers:
        while idx < len(cumulative_probs) - 1 and pointer > cumulative_probs[idx]:
            idx += 1

        selected.append(population.individuals[idx].copy())

    return selected