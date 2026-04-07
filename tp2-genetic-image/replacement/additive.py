from typing import Any, List


def replace(
    parents: List[Any], children: List[Any], fitness_fn: Any, **kwargs
) -> List[Any]:
    """
    En supervivencia aditiva, la nueva generación NO se forma solamente
    con los hijos, sino con un pool combinado:

        pool = padres + hijos

    Luego, de ese pool total, se eligen los mejores individuos hasta
    completar el tamaño deseado de la nueva población.

    Permite que:
    - un padre muy bueno pueda seguir sobreviviendo
    - un hijo bueno también pueda entrar
    - exista una competencia directa entre generaciones

    Parámetros
    ----------
    parents : List[Any]
        Lista de individuos padres.

    children : List[Any]
        Lista de individuos hijos.

    fitness_fn : Any
        Función para calcular la fitness si algún individuo no la tiene.
        Se espera algo del estilo:
            fitness_fn(individual) -> float

    kwargs : dict
        Parámetros adicionales.

        Esperamos:
        - population_size : int
            tamaño deseado de la nueva generación

    Retorna
    -------
    List[Any]
        Lista de individuos que forman la nueva generación.

    Decisión de diseño
    ------------------
    Esta implementación usa una estrategia determinística:
    - evaluar fitness si falta
    - ordenar todo el pool de mayor a menor fitness
    - quedarse con los mejores 'population_size'

    Esto es simple, robusto y muy fácil de justificar.
    """

    #  Leer tamaño objetivo de la población siguiente
    population_size = kwargs.get("population_size", len(parents))

    if population_size <= 0:
        raise ValueError("population_size debe ser mayor que 0.")

    # Validar que exista al menos algún individuo en el pool

    if not parents and not children:
        raise ValueError("No hay padres ni hijos para construir la nueva generación.")

    # Armar el pool combinado
    # En supervivencia aditiva, ambos grupos compiten juntos.
    pooled_individuals = list(parents) + list(children)

    # Evaluar fitness si hace falta
    # Algunos padres pueden ya venir evaluados.
    # Algunos hijos también.
    # Si alguno no tiene fitness, la calculamos acá.
    for individual in pooled_individuals:
        if individual.fitness is None:
            individual.fitness = fitness_fn(individual)

    # Ordenar todo el pool por fitness descendente
    sorted_pool = sorted(pooled_individuals, key=lambda ind: ind.fitness, reverse=True)

    # Tomar los mejores 'population_size'
    # Si el pool total es menor que population_size, lanzamos error
    # porque no hay suficientes individuos para llenar la población.
    if len(sorted_pool) < population_size:
        raise ValueError(
            f"Supervivencia aditiva: se necesitan al menos "
            f"{population_size} individuos en el pool combinado, "
            f"pero solo hay {len(sorted_pool)}."
        )

    # Devolvemos copias para evitar aliasing accidental.
    next_generation = [
        individual.copy() for individual in sorted_pool[:population_size]
    ]

    return next_generation
