from .boltzmann import select as boltzmann
from .elite import select as elite
from .ranking import select as ranking
from .roulette import select as roulette
from .tournament_deterministic import select as tournament_deterministic
from .tournament_probabilistic import select as tournament_probabilistic
from .universal import select as universal

__all__ = [
    "elite",
    "roulette",
    "universal",
    "boltzmann",
    "tournament_deterministic",
    "tournament_probabilistic",
    "ranking",
]
