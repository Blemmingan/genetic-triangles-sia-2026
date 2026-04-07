from typing import Any, List


def replace(
    parents: List[Any], children: List[Any], fitness_fn: Any, **kwargs
) -> List[Any]:
    """
    En supervivencia exclusiva, la nueva generación se construye
    únicamente a partir de los HIJOS.
    - los padres NO compiten por sobrevivir
    - la población siguiente sale solo de la descendencia

    1. tomar la lista de hijos
    2. evaluar su fitness si todavía no la tienen
    3. ordenar a los hijos por fitness de mayor a menor
    4. devolver los mejores 'population_size'

    Parámetros
    ----------
    parents : List[Any]
        Lista de padres.
        En esta estrategia se recibe por compatibilidad de interfaz,
        pero no se usa para decidir la nueva generación.

    children : List[Any]
        Lista de descendientes generados por crossover / mutación.

    fitness_fn : Any
        Función para evaluar la fitness de un individuo.
        Se espera algo del estilo:
            fitness_fn(individual) -> float

        Importante:
        si ya evaluaste los hijos antes de llamar a replace(),
        no hace falta recalcular nada porque se reutiliza child.fitness.

    kwargs : dict
        Parámetros adicionales.
        Esperamos:
        - population_size : int
            tamaño deseado de la nueva generación

    Retorna
    -------
    List[Any]
        Lista de individuos que forman la nueva generación.

    """

    # -------------------------------------------------------------
    # 1) Leer tamaño objetivo de la nueva población
    # -------------------------------------------------------------
    population_size = kwargs.get("population_size", len(parents))

    if population_size <= 0:
        raise ValueError("population_size debe ser mayor que 0.")

    # Validar que haya hijos

    if not children:
        raise ValueError(
            "La lista de hijos está vacía. "
            "La supervivencia exclusiva necesita descendencia."
        )

    # 3) Verificar que haya suficientes hijos para reemplazar
    #    completamente a la población anterior
    if len(children) < population_size:
        raise ValueError(
            f"Supervivencia exclusiva: se necesitan al menos "
            f"{population_size} hijos, pero solo llegaron {len(children)}."
        )

    # Evaluar fitness de los hijos si hace falta
    # Si un hijo todavía no tiene fitness calculada, la evaluamos acá.
    for child in children:
        if child.fitness is None:
            child.fitness = fitness_fn(child)

    #  Ordenar hijos por fitness descendente
    sorted_children = sorted(children, key=lambda ind: ind.fitness, reverse=True)

    # Devolvemos copias para evitar aliasing accidental con la lista
    # original de hijos.
    next_generation = [child.copy() for child in sorted_children[:population_size]]

    return next_generation
