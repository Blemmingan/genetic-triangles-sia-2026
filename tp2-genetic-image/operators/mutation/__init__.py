from .gen import mutate as gen
from .multigen import mutate as multigen
from .uniform import mutate as uniform
from .non_uniform import mutate as non_uniform

__all__ = ["gen", "multigen", "uniform", "non_uniform"]
