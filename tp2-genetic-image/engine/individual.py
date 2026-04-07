import random
from copy import deepcopy
from typing import Optional, Tuple

from PIL import Image


class Individual:
    """
    Representa un individuo del algoritmo genético.

    En este problema:
    - individuo = imagen candidata
    - cromosoma = lista de triángulos
    - cada triángulo se representa como:
        [x1, y1, x2, y2, x3, y3, r, g, b, a]

    Todas las variables se guardan normalizadas en [0, 1].
    """

    TRIANGLE_SIZE = 10

    def __init__(self, num_triangles: int, chromosome=None):
        self.num_triangles = num_triangles
        self.chromosome = chromosome if chromosome is not None else []
        self.fitness = None

    def random_init(self):
        """
        Inicialización completamente aleatoria.
        """
        self.chromosome = []

        for _ in range(self.num_triangles):
            triangle = [random.random() for _ in range(self.TRIANGLE_SIZE)]
            self.chromosome.append(triangle)

        self.fitness = None

    def _clip_01(self, value: float) -> float:
        """
        Recorta un valor al intervalo [0, 1].
        """
        return max(0.0, min(1.0, value))

    def _sample_target_color(self, target_image: Image.Image, x: float, y: float) -> Tuple[float, float, float]:
        """
        Toma el color RGB de la imagen objetivo en la posición normalizada (x, y).

        Parámetros
        ----------
        target_image : Image.Image
            Imagen objetivo.
        x, y : float
            Coordenadas normalizadas en [0,1].

        Retorna
        -------
        Tuple[float, float, float]
            Color RGB normalizado en [0,1].
        """
        width, height = target_image.size

        px = int(self._clip_01(x) * (width - 1))
        py = int(self._clip_01(y) * (height - 1))

        image_rgb = target_image.convert("RGB")
        r, g, b = image_rgb.getpixel((px, py))

        return r / 255.0, g / 255.0, b / 255.0

    def guided_init(
        self,
        target_image: Image.Image,
        alpha_range: Tuple[float, float] = (0.2, 0.8),
        triangle_size_range: Tuple[float, float] = (0.05, 0.35),
        color_jitter: float = 0.05,
    ):
        """
        Inicialización guiada por la imagen objetivo.

        Idea general
        ------------
        En vez de crear triángulos completamente aleatorios:
        - elegimos un centro aleatorio (cx, cy)
        - tomamos el color de la imagen objetivo en esa zona
        - generamos un triángulo alrededor de ese centro
        - agregamos un pequeño ruido al color para no hacer clones exactos

        Esto hace que la población inicial ya tenga:
        - colores más parecidos a la imagen objetivo
        - cierta estructura espacial útil

        Parámetros
        ----------
        target_image : Image.Image
            Imagen objetivo.

        alpha_range : (float, float)
            Rango de alpha para los triángulos.

        triangle_size_range : (float, float)
            Rango de tamaños relativos del triángulo.

        color_jitter : float
            Cantidad de perturbación aleatoria agregada al color.
        """
        self.chromosome = []

        alpha_min, alpha_max = alpha_range
        size_min, size_max = triangle_size_range

        for _ in range(self.num_triangles):
            # -----------------------------------------------------
            # 1) Elegir un centro aleatorio en la imagen
            # -----------------------------------------------------
            cx = random.random()
            cy = random.random()

            # -----------------------------------------------------
            # 2) Tomar color de la imagen objetivo en ese centro
            # -----------------------------------------------------
            r, g, b = self._sample_target_color(target_image, cx, cy)

            # Pequeña perturbación para mantener diversidad
            r = self._clip_01(r + random.uniform(-color_jitter, color_jitter))
            g = self._clip_01(g + random.uniform(-color_jitter, color_jitter))
            b = self._clip_01(b + random.uniform(-color_jitter, color_jitter))

            # -----------------------------------------------------
            # 3) Definir tamaño del triángulo
            # -----------------------------------------------------
            scale = random.uniform(size_min, size_max)

            # Generamos 3 puntos alrededor del centro.
            # Esta versión es simple: cada vértice se desplaza
            # aleatoriamente alrededor de (cx, cy).
            x1 = self._clip_01(cx + random.uniform(-scale, scale))
            y1 = self._clip_01(cy + random.uniform(-scale, scale))

            x2 = self._clip_01(cx + random.uniform(-scale, scale))
            y2 = self._clip_01(cy + random.uniform(-scale, scale))

            x3 = self._clip_01(cx + random.uniform(-scale, scale))
            y3 = self._clip_01(cy + random.uniform(-scale, scale))

            # -----------------------------------------------------
            # 4) Alpha razonable
            # -----------------------------------------------------
            a = random.uniform(alpha_min, alpha_max)

            triangle = [x1, y1, x2, y2, x3, y3, r, g, b, a]
            self.chromosome.append(triangle)

        self.fitness = None

    def copy(self):
        """
        Devuelve una copia profunda del individuo.
        """
        new_individual = Individual(
            num_triangles=self.num_triangles,
            chromosome=deepcopy(self.chromosome)
        )
        new_individual.fitness = self.fitness
        return new_individual

    def __len__(self):
        return len(self.chromosome)

    def __repr__(self):
        return f"Individual(num_triangles={self.num_triangles}, fitness={self.fitness})"