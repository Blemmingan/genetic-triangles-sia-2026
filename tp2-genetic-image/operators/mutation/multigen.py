import random
from typing import Any


def _clip_01(value: float) -> float:
    """
    Recorta un valor al intervalo [0, 1].

    Todos los parámetros del individuo están normalizados
    en ese rango:
    - coordenadas
    - color
    - alpha
    """
    return max(0.0, min(1.0, value))


def _mutate_scalar(old_value: float, mutation_mode: str, sigma: float) -> float:
    """
    Aplica la mutación a un único valor escalar.

    Parámetros
    ----------
    old_value : float
        Valor actual del gen escalar.
    mutation_mode : str
        Estrategia de mutación:
        - "reset": reemplaza por un valor aleatorio nuevo
        - "delta": agrega una perturbación gaussiana
    sigma : float
        Intensidad de la mutación si mutation_mode == "delta"
    """

    if mutation_mode == "delta":
        delta = random.gauss(0.0, sigma)
        return _clip_01(old_value + delta)

    # Modo "reset"
    return random.random()


def mutate(individual: Any, **kwargs) -> Any:
    """
    Mutación multigen.

    Idea general
    ------------
    A diferencia de la mutación gen, que modifica un único parámetro,
    esta versión modifica VARIOS parámetros del individuo en una sola vez.

    Esto suele ser mucho más útil cuando:
    - el cromosoma es grande
    - una sola mutación resulta demasiado débil
    - queremos que las soluciones cambien de forma más visible

    Parámetros esperados en kwargs
    ------------------------------
    mutation_rate : float
        Probabilidad de aplicar la mutación al individuo.
        Default: 0.1

    mutation_mode : str
        Puede ser:
        - "reset"
        - "delta"

    sigma : float
        Intensidad de la mutación si mutation_mode == "delta".
        Default: 0.05

    min_genes : int
        Cantidad mínima de genes escalares a mutar.
        Default: 1

    max_genes : int | None
        Cantidad máxima de genes escalares a mutar.
        Si es None, se toma todo el cromosoma escalar disponible.

    Definición de "gen" en esta implementación
    ------------------------------------------
    Aunque el individuo está organizado como lista de triángulos,
    para la mutación consideramos como gen elemental a cada parámetro
    escalar del triángulo:
        [x1, y1, x2, y2, x3, y3, r, g, b, a]

    Entonces, si un individuo tiene:
        num_triangles = 20
    la cantidad total de genes escalares es:
        20 * 10 = 200

    Retorna
    -------
    Any
        Una copia mutada del individuo.
    """

    mutation_rate = kwargs.get("mutation_rate", 0.1)
    mutation_mode = kwargs.get("mutation_mode", "delta")
    sigma = kwargs.get("sigma", 0.05)
    min_genes = kwargs.get("min_genes", 1)
    max_genes = kwargs.get("max_genes", None)

    mutated = individual.copy()

    # -------------------------------------------------------------
    # 1) Casos borde
    # -------------------------------------------------------------
    if not mutated.chromosome:
        return mutated

    n_triangles = len(mutated.chromosome)
    triangle_size = len(mutated.chromosome[0]) if n_triangles > 0 else 0
    total_scalar_genes = n_triangles * triangle_size

    if total_scalar_genes == 0:
        return mutated

    # -------------------------------------------------------------
    # 2) Decidir si el individuo muta o no
    # -------------------------------------------------------------
    if random.random() > mutation_rate:
        return mutated

    # -------------------------------------------------------------
    # 3) Determinar cuántos genes escalares mutar
    # -------------------------------------------------------------
    if max_genes is None:
        max_genes = total_scalar_genes

    # Aseguramos que los límites sean válidos
    min_genes = max(1, min(min_genes, total_scalar_genes))
    max_genes = max(min_genes, min(max_genes, total_scalar_genes))

    n_mutations = random.randint(min_genes, max_genes)

    # -------------------------------------------------------------
    # 4) Elegir genes escalares únicos a mutar
    # -------------------------------------------------------------
    # Cada gen escalar se indexa como un entero en:
    # [0, total_scalar_genes - 1]
    #
    # Luego convertimos ese índice plano a:
    # - triangle_idx
    # - gene_idx
    selected_flat_indices = random.sample(range(total_scalar_genes), n_mutations)

    for flat_idx in selected_flat_indices:
        triangle_idx = flat_idx // triangle_size
        gene_idx = flat_idx % triangle_size

        old_value = mutated.chromosome[triangle_idx][gene_idx]
        new_value = _mutate_scalar(
            old_value=old_value,
            mutation_mode=mutation_mode,
            sigma=sigma
        )

        mutated.chromosome[triangle_idx][gene_idx] = new_value

    # -------------------------------------------------------------
    # 5) Invalidar fitness
    # -------------------------------------------------------------
    mutated.fitness = None

    return mutated