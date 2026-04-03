import numpy as np
from PIL import Image
from typing import Tuple

def load_image(path: str) -> Image.Image:
    """
    Loads an image from the specified path using Pillow.
    
    :param path: File path.
    :return: A PIL Image object.
    """
    raise NotImplementedError("load_image stub")

def to_pixel_array(image: Image.Image) -> np.ndarray:
    """
    Converts a Pillow image into a NumPy pixel array for easy manipulation/fitness checking.
    
    :param image: A PIL Image object.
    :return: A numpy array representing the image pixels.
    """
    raise NotImplementedError("to_pixel_array stub")

def resize(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """
    Resizes an image to the specified width and height.
    
    :param image: Image to resize.
    :param size: Tuple (width, height).
    :return: A resized PIL Image.
    """
    raise NotImplementedError("resize stub")
