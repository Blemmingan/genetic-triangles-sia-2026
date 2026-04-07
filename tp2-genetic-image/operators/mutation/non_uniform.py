import random
from typing import Any


def _clip_01(value: float) -> float:
    """
    Recorta un valor al intervalo [0, 1].
    """
    return max(0.0, min(1.0, value))


def _non_uniform_delta(y: float, progress: float, b: float) -> float:
    """
    Calcula una perturbación no uniforme.

    Parámetros
    ----------
    y : float
        Distancia máxima posible hasta el borde correspondiente.
    progress : float
        Progreso normalizado en [0,1]:
        - 0.0 -> inicio del algoritmo
        - 1.0 -> final del algoritmo
    b : float
        Parámetro de forma. Cuanto mayor es b, más rápido se reduce
        la amplitud de la mutación con el tiempo.

    Retorna
    -------
    float
        Magnitud del desplazamiento.
    """
    r = random.random()
    return y * (1.0 - (r ** ((1.0 - progress) ** b)))


def mutate(individual: Any, **kwargs) -> Any:
    """
    Mutación no uniforme.

    Idea general
    ------------
    Modifica un solo gen escalar del individuo, pero la amplitud de la
    mutación depende de la generación actual:

    - al principio: cambios más grandes
    - al final: cambios más pequeños

    Esto ayuda a combinar:
    - exploración al inicio
    - refinamiento fino al final

    Parámetros esperados en kwargs
    ------------------------------
    mutation_rate : float
        Probabilidad de aplicar la mutación al individuo.
        Default: 0.1

    generation : int
        Generación actual.
        Default: 0

    max_generations : int
        Cantidad máxima de generaciones del algoritmo.
        Default: 100

    b : float
        Parámetro de forma de la mutación no uniforme.
        Default: 2.0

    Parámetros
    ----------
    individual : Any
        Individuo a mutar.

    Retorna
    -------
    Any
        Una copia mutada del individuo.
    """

    mutation_rate = kwargs.get("mutation_rate", 0.1)
    generation = kwargs.get("generation", 0)
    max_generations = kwargs.get("max_generations", 100)
    b = kwargs.get("b", 2.0)

    mutated = individual.copy()

    # -------------------------------------------------------------
    # 1) Casos borde
    # -------------------------------------------------------------
    if not mutated.chromosome:
        return mutated

    if max_generations <= 0:
        raise ValueError("max_generations debe ser mayor que 0.")

    if random.random() > mutation_rate:
        return mutated

    # -------------------------------------------------------------
    # 2) Elegir triángulo y gen escalar al azar
    # -------------------------------------------------------------
    triangle_idx = random.randrange(len(mutated.chromosome))
    triangle = mutated.chromosome[triangle_idx]

    if not triangle:
        return mutated

    gene_idx = random.randrange(len(triangle))
    old_value = triangle[gene_idx]

    # -------------------------------------------------------------
    # 3) Calcular progreso temporal del algoritmo
    # -------------------------------------------------------------
    progress = min(max(generation / max_generations, 0.0), 1.0)

    # -------------------------------------------------------------
    # 4) Elegir dirección y magnitud de mutación
    # -------------------------------------------------------------
    # Con 50% de probabilidad movemos el gen hacia 1.0
    # Con 50% de probabilidad lo movemos hacia 0.0
    if random.random() < 0.5:
        # mover hacia arriba
        y = 1.0 - old_value
        delta = _non_uniform_delta(y=y, progress=progress, b=b)
        new_value = old_value + delta
    else:
        # mover hacia abajo
        y = old_value - 0.0
        delta = _non_uniform_delta(y=y, progress=progress, b=b)
        new_value = old_value - delta

    mutated.chromosome[triangle_idx][gene_idx] = _clip_01(new_value)

    # -------------------------------------------------------------
    # 5) Invalidar fitness
    # -------------------------------------------------------------
    mutated.fitness = None

    return mutated
