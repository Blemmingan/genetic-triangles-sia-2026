import random
from typing import Any, List


def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Selección por torneo determinístico.

    Idea general
    ------------
    En cada selección:
    1. se eligen k individuos al azar de la población
    2. de esos k individuos, se toma el mejor
    3. se repite hasta obtener n_select individuos

    Esto introduce una presión de selección importante, pero sin ser tan
    rígida como elite pura, porque el "torneo" se arma al azar.

    Parámetros esperados en kwargs
    ------------------------------
    tournament_k : int
        Cantidad de individuos que participan en cada torneo.
        Default: 3

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
    """

    tournament_k = kwargs.get("tournament_k", 3)

    # -------------------------------------------------------------
    # 1) Validaciones básicas
    # -------------------------------------------------------------
    if n_select <= 0:
        raise ValueError("n_select debe ser mayor que 0.")

    if tournament_k <= 0:
        raise ValueError("tournament_k debe ser mayor que 0.")

    if not population.individuals:
        raise ValueError("La población está vacía.")

    for individual in population.individuals:
        if individual.fitness is None:
            raise ValueError(
                "Hay individuos sin fitness. Primero debés evaluar la población."
            )

    # -------------------------------------------------------------
    # 2) Ajustar k para no exceder el tamaño de la población
    # -------------------------------------------------------------
    tournament_k = min(tournament_k, len(population.individuals))

    # -------------------------------------------------------------
    # 3) Realizar torneos
    # -------------------------------------------------------------
    selected = []

    for _ in range(n_select):
        # Elegimos k participantes al azar
        contenders = random.sample(population.individuals, tournament_k)

        # Tomamos el mejor del torneo
        winner = max(contenders, key=lambda ind: ind.fitness)

        # Devolvemos copia para evitar aliasing
        selected.append(winner.copy())

    return selected
