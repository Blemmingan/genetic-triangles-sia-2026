import math
from typing import Any

import numpy as np
from PIL import Image

from rendering.renderer import render


def image_to_array_rgb(image: Image.Image) -> np.ndarray:
    """
    Convierte una imagen Pillow a un array NumPy RGB normalizado en [0,1].

    Retorna
    -------
    np.ndarray
        Array de shape (alto, ancho, 3), dtype float32.
    """
    image = image.convert("RGB")
    return np.asarray(image, dtype=np.float32) / 255.0


def rgb_to_grayscale(rgb_array: np.ndarray) -> np.ndarray:
    """
    Convierte un array RGB normalizado a escala de grises.

    Usamos la combinación luminancia estándar aproximada:
        Y = 0.299 R + 0.587 G + 0.114 B

    Retorna
    -------
    np.ndarray
        Array 2D normalizado en [0,1].
    """
    return (
        0.299 * rgb_array[..., 0]
        + 0.587 * rgb_array[..., 1]
        + 0.114 * rgb_array[..., 2]
    ).astype(np.float32)


def compute_edge_map(gray_array: np.ndarray) -> np.ndarray:
    """
    Calcula un mapa de bordes robusto usando el operador de Sobel.

    Idea
    ----
    Para cada píxel medimos cambios usando kernels 3x3 para
    las direcciones horizontal y vertical, lo que refuerza contornos
    importantes y descarta ruido pequeño.
    """
    padded = np.pad(gray_array, pad_width=1, mode="edge")

    p_tl = padded[0:-2, 0:-2]
    p_tc = padded[0:-2, 1:-1]
    p_tr = padded[0:-2, 2:]

    p_cl = padded[1:-1, 0:-2]
    p_cr = padded[1:-1, 2:]

    p_bl = padded[2:, 0:-2]
    p_bc = padded[2:, 1:-1]
    p_br = padded[2:, 2:]

    gx = (p_tr - p_tl) + 2.0 * (p_cr - p_cl) + (p_br - p_bl)
    gy = (p_bl - p_tl) + 2.0 * (p_bc - p_tc) + (p_br - p_tr)

    magnitude = np.sqrt(gx**2 + gy**2)

    # Normalización: max theoretical sobel is around 4.24
    magnitude /= 4.0

    return np.clip(magnitude, 0.0, 1.0).astype(np.float32)


def compute_mse(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calcula el error cuadrático medio entre dos arrays del mismo shape.
    """
    if a.shape != b.shape:
        raise ValueError(f"Shapes incompatibles: {a.shape} vs {b.shape}")

    return float(np.mean((a - b) ** 2))


def compute_color_mse(target_image: Image.Image, rendered_image: Image.Image) -> float:
    """
    Calcula MSE usando solamente RGB.
    """
    target_rgb = image_to_array_rgb(target_image)
    rendered_rgb = image_to_array_rgb(rendered_image)
    return compute_mse(target_rgb, rendered_rgb)


def compute_edge_mse(target_image: Image.Image, rendered_image: Image.Image) -> float:
    """
    Calcula MSE entre mapas de bordes de ambas imágenes.
    """
    target_rgb = image_to_array_rgb(target_image)
    rendered_rgb = image_to_array_rgb(rendered_image)

    target_gray = rgb_to_grayscale(target_rgb)
    rendered_gray = rgb_to_grayscale(rendered_rgb)

    target_edges = compute_edge_map(target_gray)
    rendered_edges = compute_edge_map(rendered_gray)

    return compute_mse(target_edges, rendered_edges)


def compute_fitness(
    individual: Any,
    target_image: Image.Image,
    color_weight: float = 0.75,
    edge_weight: float = 0.25,
) -> float:
    """
    Calcula la fitness de un individuo usando una combinación de:

    1. error de color (RGB MSE)
    2. error de bordes (edge MSE)

    Fórmula
    -------
    combined_error =
        color_weight * color_mse +
        edge_weight * edge_mse

    fitness = 1 - combined_error

    Interpretación
    --------------
    - fitness alta = mejor aproximación
    - fitness baja = peor aproximación

    ¿Por qué esto ayuda?
    --------------------
    Porque una imagen puede parecerse bastante en color promedio y aun así
    tener malas formas. El término de bordes obliga a respetar mejor las
    estructuras y contornos principales.
    """
    if color_weight < 0 or edge_weight < 0:
        raise ValueError("Los pesos de fitness deben ser no negativos.")

    total_weight = color_weight + edge_weight
    if total_weight <= 0:
        raise ValueError("La suma de pesos debe ser mayor que 0.")

    # Normalizamos pesos por robustez
    color_weight = color_weight / total_weight
    edge_weight = edge_weight / total_weight

    image_size = target_image.size
    rendered_image = render(individual, image_size, target_image=target_image)

    color_mse = compute_color_mse(target_image, rendered_image)
    edge_mse = compute_edge_mse(target_image, rendered_image)

    combined_error = color_weight * color_mse + edge_weight * edge_mse

    fitness = 1.0 - combined_error
    fitness = max(0.0, min(1.0, fitness))

    return fitness
