import math
import random
from typing import List, Any


def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Selección de Boltzmann.

    Idea general
    ------------
    En vez de usar la fitness real directamente, se construye una
    pseudo-fitness transformada con una función exponencial:

        pseudo_i = exp(fitness_i / T)

    donde T es la temperatura actual.

    Efecto:
    - T alta  -> las diferencias entre individuos se suavizan
    - T baja  -> las diferencias se acentúan

    Luego se aplica una ruleta sobre esas pseudo-fitness.

    Parámetros esperados en kwargs
    ------------------------------
    generation : int
        Generación actual.

    boltzmann_temperature : float
        Temperatura inicial.

    boltzmann_decay : float
        Factor de decaimiento multiplicativo por generación.

    min_temperature : float
        Piso mínimo para evitar divisiones por cero o exponentes
        demasiado extremos.

    Nota
    ----
    Esta implementación usa:
        T(g) = max(T0 * decay^g, min_temperature)
    """

    generation = kwargs.get("generation", 0)
    initial_temperature = kwargs.get("boltzmann_temperature", 100.0)
    decay = kwargs.get("boltzmann_decay", 0.99)
    min_temperature = kwargs.get("min_temperature", 1e-3)

    # -------------------------------------------------------------
    # 1) Validaciones básicas
    # -------------------------------------------------------------
    if n_select <= 0:
        raise ValueError("n_select debe ser mayor que 0.")

    if initial_temperature <= 0:
        raise ValueError("boltzmann_temperature debe ser mayor que 0.")

    if decay <= 0:
        raise ValueError("boltzmann_decay debe ser mayor que 0.")

    if min_temperature <= 0:
        raise ValueError("min_temperature debe ser mayor que 0.")

    if not population.individuals:
        raise ValueError("La población está vacía.")

    for individual in population.individuals:
        if individual.fitness is None:
            raise ValueError(
                "Hay individuos sin fitness. "
                "Primero debés evaluar la población."
            )

    # -------------------------------------------------------------
    # 2) Calcular temperatura actual
    # -------------------------------------------------------------
    temperature = max(initial_temperature * (decay ** generation), min_temperature)

    # -------------------------------------------------------------
    # 3) Construir pseudo-fitness Boltzmann
    # -------------------------------------------------------------
    # Para mejorar estabilidad numérica, centramos por el máximo fitness.
    # Así evitamos exponentes demasiado grandes:
    #
    # exp((f_i - max_f) / T)
    #
    # Esto no cambia las probabilidades relativas finales de la ruleta.
    fitness_values = [ind.fitness for ind in population.individuals]
    max_fitness = max(fitness_values)

    pseudo_fitness = [
        math.exp((ind.fitness - max_fitness) / temperature)
        for ind in population.individuals
    ]

    total_pseudo = sum(pseudo_fitness)

    # -------------------------------------------------------------
    # 4) Caso especial: suma cero
    # -------------------------------------------------------------
    if total_pseudo == 0:
        return [random.choice(population.individuals).copy() for _ in range(n_select)]

    # -------------------------------------------------------------
    # 5) Probabilidades acumuladas
    # -------------------------------------------------------------
    cumulative_probs = []
    cumulative = 0.0

    for value in pseudo_fitness:
        cumulative += value / total_pseudo
        cumulative_probs.append(cumulative)

    cumulative_probs[-1] = 1.0

    # -------------------------------------------------------------
    # 6) Selección por ruleta sobre pseudo-fitness
    # -------------------------------------------------------------
    selected: List[Any] = []

    for _ in range(n_select):
        r = random.random()

        for idx, threshold in enumerate(cumulative_probs):
            if r <= threshold:
                selected.append(population.individuals[idx].copy())
                break

    return selected