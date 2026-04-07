import random
from typing import Any


def _clip_01(value: float) -> float:
    """
    Recorta un valor al intervalo [0, 1].

    Esto es importante porque todos los parámetros de nuestros triángulos
    están normalizados en ese rango:
    - coordenadas
    - colores
    - alpha

    Si una mutación generara un valor fuera de rango, lo corregimos acá.
    """
    return max(0.0, min(1.0, value))


def mutate(individual: Any, **kwargs) -> Any:
    """
    Mutación de gen (single-gene mutation).
    Esta mutación modifica UN solo parámetro escalar del individuo.

    Aunque el individuo está organizado como una lista de triángulos,
    para esta primera implementación vamos a considerar como "gen elemental"
    a uno de los 10 parámetros de un triángulo:
        [x1, y1, x2, y2, x3, y3, r, g, b, a]

    Entonces la mutación consiste en:
    1. decidir si el individuo muta o no según mutation_rate
    2. elegir un triángulo al azar
    3. elegir un parámetro de ese triángulo al azar
    4. modificar solo ese parámetro

    Parámetros esperados en kwargs
    ------------------------------
    mutation_rate : float
        Probabilidad de aplicar la mutación al individuo.
        Valor por default: 0.1

    mutation_mode : str
        Estrategia para mutar el parámetro elegido.
        Puede ser:
        - "reset": reemplaza el valor por uno nuevo aleatorio en [0,1]
        - "delta": suma una pequeña perturbación al valor actual

    sigma : float
        Desvío estándar usado si mutation_mode == "delta".
        Valor por default: 0.1

    Parámetros
    ----------
    individual : Any
        Individuo a mutar.

    Retorna
    -------
    Any
        Una COPIA mutada del individuo.

    Nota importante
    ---------------
    No mutamos el objeto original in-place.
    Devolvemos una copia para evitar efectos colaterales en el flujo del GA.
    """

    # Leer hiperparámetros de mutación
    mutation_rate = kwargs.get("mutation_rate", 0.1)
    mutation_mode = kwargs.get("mutation_mode", "reset")
    sigma = kwargs.get("sigma", 0.1)

    #  Crear una copia del individuo
    # Esto evita modificar accidentalmente al padre original.
    mutated = individual.copy()

    # Casos borde: si no hay cromosoma, devolvemos la copia
    if not mutated.chromosome:
        return mutated

    # Decidir si el individuo muta o no
    # Si el valor aleatorio supera mutation_rate, no se muta.
    if random.random() > mutation_rate:
        return mutated

    #  Elegir un triángulo al azar
    triangle_idx = random.randrange(len(mutated.chromosome))
    triangle = mutated.chromosome[triangle_idx]

    # Protección adicional por si el triángulo estuviera vacío
    if not triangle:
        return mutated

    # Elegir un parámetro del triángulo al azar
    gene_idx = random.randrange(len(triangle))

    # Valor actual antes de mutar
    old_value = triangle[gene_idx]

    # Aplicar la mutación
    if mutation_mode == "delta":
        # Mutación suave:
        # agregamos una pequeña perturbación gaussiana.
        delta = random.gauss(0.0, sigma)
        new_value = _clip_01(old_value + delta)

    else:
        # Mutación tipo "reset":
        # reemplazamos el valor por uno completamente nuevo en [0,1].
        new_value = random.random()

    # Guardamos el nuevo valor mutado
    mutated.chromosome[triangle_idx][gene_idx] = new_value

    # Invalidar la fitness
    mutated.fitness = None

    return mutated
