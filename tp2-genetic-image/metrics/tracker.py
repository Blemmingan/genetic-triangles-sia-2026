import json
import matplotlib.pyplot as plt
from typing import List, Dict, Any

class MetricsTracker:
    """
    Tracks and records fitness metrics (best, average, etc.) across generations.
    """

    def __init__(self):
        """
        Initialize lists to store fitness history.
        """
        self.best_fitness_history: List[float] = []
        self.avg_fitness_history: List[float] = []
        raise NotImplementedError("MetricsTracker init stub")

    def record(self, generation: int, population: Any):
        """
        Analyzes the population and appends best/avg fitness to the history.
        
        :param generation: The current generation number.
        :param population: The current Population object.
        """
        raise NotImplementedError("record stub")

    def save_json(self, path: str):
        """
        Dumps the tracked metrics to a JSON file.
        
        :param path: Output file path.
        """
        raise NotImplementedError("save_json stub")

    def plot(self, path: str):
        """
        Generates a matplotlib plot of the fitness over generations and saves it to a file.
        
        :param path: Output file path for the plot image.
        """
        raise NotImplementedError("plot stub")
