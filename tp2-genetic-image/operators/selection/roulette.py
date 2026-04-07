import random
from typing import List, Any


def select(population: Any, n_select: int, **kwargs) -> List[Any]:
    """
    Selección por ruleta.
    Cada individuo ocupa una "porción" de una ruleta proporcional
    a su fitness.Entonces cuanto mayor es la fitness de un individuo,
    mayor es su probabilidad de ser seleccionado pero los demás individuos
    también pueden salir elegidos

    """

    # Validaciones básicas
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
                "La selección por ruleta requiere fitness no negativas."
            )

    #  Calcular la suma total de fitness
    # Esta suma se usa para obtener probabilidades relativas:
    #   p_i = fitness_i / suma_total

    total_fitness = sum(individual.fitness for individual in population.individuals)

    #  Caso especial: si la suma total es 0
    # Si todas las fitness son 0, no podemos construir probabilidades
    # proporcionales.
 
    if total_fitness == 0:
        selected = []
        for _ in range(n_select):
            chosen = random.choice(population.individuals)
            selected.append(chosen.copy())
        return selected


    # Construir las probabilidades acumuladas
    cumulative_probs = []
    cumulative = 0.0

    for individual in population.individuals:
        relative_prob = individual.fitness / total_fitness
        cumulative += relative_prob
        cumulative_probs.append(cumulative)

    # Por robustez numérica, nos aseguramos de que el último valor sea 1.0
    cumulative_probs[-1] = 1.0

    # Realizar n_select selecciones
    selected = []

    for _ in range(n_select):
        # Tiramos un valor aleatorio en [0,1)
        r = random.random()

        # Buscamos el primer individuo cuya probabilidad acumulada
        # sea mayor o igual que r.
        for idx, threshold in enumerate(cumulative_probs):
            if r <= threshold:
                selected.append(population.individuals[idx].copy())
                break

    return selected