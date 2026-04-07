from typing import Any, Tuple

from PIL import Image, ImageDraw


def get_average_color(image: Image.Image) -> Tuple[int, int, int, int]:
    if not hasattr(image, "avg_color"):
        import numpy as np
        arr = np.asarray(image.convert("RGB"))
        avg = arr.mean(axis=(0,1))
        # Cache the color inside the object directly to avoid recomputing millions of times
        image.avg_color = (int(avg[0]), int(avg[1]), int(avg[2]), 255)
    return image.avg_color

def render(individual: Any, image_size: Tuple[int, int], target_image: Image.Image = None) -> Image.Image:
    """
    Convierte un individuo en una imagen Pillow.

    Esta versión compone correctamente cada triángulo translúcido
    sobre el canvas usando alpha compositing.

    Eso es importante porque en este problema:
    - el orden de los triángulos importa
    - la transparencia importa
    - el resultado visual final debe parecerse a la imagen objetivo
    """

    width, height = image_size

    # Dynamic average background if target_image is provided, otherwise white fallback
    bg_color = get_average_color(target_image) if target_image else (255, 255, 255, 255)
    canvas = Image.new("RGBA", (width, height), bg_color)

    for triangle in individual.chromosome:
        x1, y1, x2, y2, x3, y3, r, g, b, a = triangle

        # Coordenadas en píxeles
        px1 = int(x1 * width)
        py1 = int(y1 * height)
        px2 = int(x2 * width)
        py2 = int(y2 * height)
        px3 = int(x3 * width)
        py3 = int(y3 * height)

        points = [(px1, py1), (px2, py2), (px3, py3)]

        # Color RGBA en [0,255]
        pr = max(0, min(255, int(round(r * 255))))
        pg = max(0, min(255, int(round(g * 255))))
        pb = max(0, min(255, int(round(b * 255))))
        pa = max(0, min(255, int(round(a * 255))))

        color = (pr, pg, pb, pa)

        # ---------------------------------------------------------
        # Clave importante:
        # dibujamos el triángulo en una capa transparente separada
        # y luego la componemos sobre el canvas.
        #
        # Esto hace que la transparencia funcione de forma visualmente
        # correcta.
        # ---------------------------------------------------------
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay, "RGBA")
        draw.polygon(points, fill=color)

        canvas = Image.alpha_composite(canvas, overlay)

    return canvas
