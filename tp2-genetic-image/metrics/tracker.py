import json
import matplotlib.pyplot as plt
from typing import List, Dict, Any


class MetricsTracker:
    """
    Lleva el seguimiento de métricas del algoritmo genético
    a lo largo de las generaciones.

    Qué guarda
    ----------
    Para cada generación vamos a registrar, al menos:
    - best_fitness
    - avg_fitness
    - worst_fitness

    ¿Para qué sirve?
    ----------------
    - ver si el algoritmo mejora con el tiempo
    - comparar configuraciones distintas
    - detectar estancamiento
    - generar evidencia para el informe / presentación
    """

    def __init__(self):
        """
        Inicializa las estructuras internas para guardar el historial.

        Usamos dos formatos al mismo tiempo:

        1. listas separadas
           Útiles para graficar rápido

        2. lista de registros (dicts)
           Útil para guardar a JSON y exportar fácilmente
        """

        # Historial del mejor fitness por generación
        self.best_fitness_history: List[float] = []

        # Historial del fitness promedio por generación
        self.avg_fitness_history: List[float] = []

        # Historial del peor fitness por generación
        self.worst_fitness_history: List[float] = []

        # Lista de generaciones registradas
        self.generations: List[int] = []

        # Historial completo como lista de diccionarios
        # Cada entrada tendrá por ejemplo:
        # {
        #   "generation": 0,
        #   "best_fitness": 0.82,
        #   "avg_fitness": 0.61,
        #   "worst_fitness": 0.42
        # }
        self.records: List[Dict[str, Any]] = []

    def record(self, generation: int, population: Any):
        """
        Analiza la población actual y guarda sus métricas.

        Parámetros
        ----------
        generation : int
            Número de generación actual.

        population : Any
            Objeto Population ya evaluado.

        Qué hace
        --------
        1. obtiene mejor individuo
        2. obtiene peor individuo
        3. calcula fitness promedio
        4. guarda todo en las estructuras internas
        """

        # ---------------------------------------------------------
        # 1) Obtener métricas básicas desde la población
        # ---------------------------------------------------------
        best = population.get_best()
        worst = population.get_worst()
        avg = population.get_average_fitness()

        # ---------------------------------------------------------
        # 2) Guardar en listas simples
        # ---------------------------------------------------------
        self.generations.append(generation)
        self.best_fitness_history.append(best.fitness)
        self.avg_fitness_history.append(avg)
        self.worst_fitness_history.append(worst.fitness)

        # ---------------------------------------------------------
        # 3) Guardar también en formato estructurado
        # ---------------------------------------------------------
        self.records.append({
            "generation": generation,
            "best_fitness": best.fitness,
            "avg_fitness": avg,
            "worst_fitness": worst.fitness,
        })

    def save_json(self, path: str):
        """
        Guarda el historial de métricas en formato JSON.

        Parámetros
        ----------
        path : str
            Ruta de salida del archivo JSON.

        Resultado
        ---------
        Se genera un archivo con todos los registros por generación.
        Esto es útil para:
        - análisis posterior
        - guardar resultados del experimento
        - incluir evidencia en el TP
        """

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=4)

    def plot(self, path: str):
        """
        Genera un gráfico simple de fitness vs generación y lo guarda.

        Parámetros
        ----------
        path : str
            Ruta donde se guardará la imagen del gráfico.

        Qué muestra
        -----------
        - mejor fitness
        - fitness promedio
        - peor fitness

        Esto permite ver si:
        - el algoritmo mejora
        - la población converge
        - hay mucha diferencia entre el mejor individuo y el promedio
        """

        # ---------------------------------------------------------
        # 1) Validar que haya datos registrados
        # ---------------------------------------------------------
        if not self.records:
            raise ValueError(
                "No hay métricas registradas. "
                "Primero debés llamar a record()."
            )

        # ---------------------------------------------------------
        # 2) Crear figura
        # ---------------------------------------------------------
        plt.figure(figsize=(10, 6))

        # ---------------------------------------------------------
        # 3) Dibujar las curvas
        # ---------------------------------------------------------
        plt.plot(self.generations, self.best_fitness_history, label="Best Fitness")
        plt.plot(self.generations, self.avg_fitness_history, label="Average Fitness")
        plt.plot(self.generations, self.worst_fitness_history, label="Worst Fitness")

        # ---------------------------------------------------------
        # 4) Etiquetas y formato
        # ---------------------------------------------------------
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Fitness evolution across generations")
        plt.legend()
        plt.grid(True)

        # ---------------------------------------------------------
        # 5) Guardar y cerrar figura
        # ---------------------------------------------------------
        plt.tight_layout()
        plt.savefig(path)
        plt.close()