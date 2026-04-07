from typing import Any, Optional


class StoppingCriteria:
    """
    Maneja los criterios de parada del algoritmo genético.

    Esta clase permite decidir si el algoritmo debe detenerse
    en una generación dada.

    Criterios implementados en esta primera versión
    -----------------------------------------------
    1. max_generations
       Se detiene cuando se alcanza la cantidad máxima de generaciones.

    2. fitness_threshold
       Se detiene cuando el mejor individuo alcanza o supera
       una fitness objetivo.

    3. no_improvement_generations
       Se detiene si el mejor fitness no mejora durante una cierta
       cantidad de generaciones consecutivas.

    ¿Por qué estos criterios?
    -------------------------
    Porque son:
    - fáciles de entender
    - fáciles de justificar en el TP
    - muy usados en la práctica
    - suficientes para una primera implementación sólida

    Nota
    ----
    El criterio de "no mejora" corresponde a una forma práctica de
    criterio de contenido:
    si el mejor valor de fitness deja de mejorar por muchas generaciones,
    asumimos que el algoritmo está estancado.
    """

    def __init__(
        self,
        max_generations: Optional[int] = None,
        fitness_threshold: Optional[float] = None,
        no_improvement_generations: Optional[int] = None,
        improvement_epsilon: float = 1e-9,
    ):
        """
        Parámetros
        ----------
        max_generations : int | None
            Cantidad máxima de generaciones permitidas.
            Si es None, este criterio no se usa.

        fitness_threshold : float | None
            Umbral de fitness para detener el algoritmo.
            Si el mejor individuo alcanza o supera este valor, se frena.

        no_improvement_generations : int | None
            Cantidad de generaciones consecutivas sin mejora permitidas.
            Si es None, este criterio no se usa.

        improvement_epsilon : float
            Mejora mínima considerada "real".
            Sirve para evitar que pequeñas diferencias numéricas debidas
            a precisión flotante sean contadas como mejora significativa.
        """

        self.max_generations = max_generations
        self.fitness_threshold = fitness_threshold
        self.no_improvement_generations = no_improvement_generations
        self.improvement_epsilon = improvement_epsilon

        # Mejor fitness global observado hasta el momento
        self.best_fitness_seen: Optional[float] = None

        # Cantidad de generaciones consecutivas sin mejora real
        self.generations_without_improvement = 0

        # Razón de parada, útil para debug o logs
        self.stop_reason: Optional[str] = None

    def reset(self):
        """
        Reinicia el estado interno del criterio de parada.

        Esto es útil si se reutiliza el mismo objeto para correr
        más de un experimento.
        """
        self.best_fitness_seen = None
        self.generations_without_improvement = 0
        self.stop_reason = None

    def update(self, population: Any):
        """
        Actualiza el estado interno del criterio usando la población actual.

        Parámetros
        ----------
        population : Any
            Objeto Population ya evaluado.

        Qué hace
        --------
        1. obtiene el mejor fitness actual
        2. lo compara con el mejor histórico
        3. actualiza el contador de generaciones sin mejora
        """

        current_best = population.get_best().fitness

        if current_best is None:
            raise ValueError(
                "La población debe estar evaluada antes de actualizar "
                "los criterios de parada."
            )

        # Si todavía no habíamos visto ningún fitness, lo inicializamos.
        if self.best_fitness_seen is None:
            self.best_fitness_seen = current_best
            self.generations_without_improvement = 0
            return

        # Si hubo mejora real, actualizamos el mejor histórico
        # y reseteamos el contador de estancamiento.
        if current_best > self.best_fitness_seen + self.improvement_epsilon:
            self.best_fitness_seen = current_best
            self.generations_without_improvement = 0
        else:
            # Si no hubo mejora significativa, sumamos una generación
            # sin mejora.
            self.generations_without_improvement += 1

    def should_stop(self, generation: int, population: Any) -> bool:
        """
        Decide si el algoritmo debe detenerse.

        Parámetros
        ----------
        generation : int
            Número de generación actual.
        population : Any
            Población actual, ya evaluada.

        Retorna
        -------
        bool
            True si el algoritmo debe frenarse.
            False si debe continuar.

        Lógica
        ------
        Antes de chequear condiciones, actualizamos el estado interno.
        Luego probamos cada criterio activo.
        """

        # ---------------------------------------------------------
        # 1) Actualizar estado interno con la población actual
        # ---------------------------------------------------------
        self.update(population)

        current_best = population.get_best().fitness

        # ---------------------------------------------------------
        # 2) Criterio: max_generations
        # ---------------------------------------------------------
        # Si generation >= max_generations, frenamos.
        #
        # Ejemplo:
        # max_generations = 100
        # generaciones válidas: 0..100
        if self.max_generations is not None:
            if generation >= self.max_generations:
                self.stop_reason = (
                    f"Se alcanzó max_generations = {self.max_generations}"
                )
                return True

        # ---------------------------------------------------------
        # 3) Criterio: fitness_threshold
        # ---------------------------------------------------------
        if self.fitness_threshold is not None:
            if current_best >= self.fitness_threshold:
                self.stop_reason = (
                    f"Se alcanzó fitness_threshold = {self.fitness_threshold}"
                )
                return True

        # ---------------------------------------------------------
        # 4) Criterio: no_improvement_generations
        # ---------------------------------------------------------
        if self.no_improvement_generations is not None:
            if self.generations_without_improvement >= self.no_improvement_generations:
                self.stop_reason = (
                    "No hubo mejora durante "
                    f"{self.no_improvement_generations} generaciones consecutivas"
                )
                return True

        # Si ningún criterio se cumplió, seguimos.
        return False

    def get_stop_reason(self) -> Optional[str]:
        """
        Devuelve la razón por la cual el algoritmo se detuvo.
        """
        return self.stop_reason
