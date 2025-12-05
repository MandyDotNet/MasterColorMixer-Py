#temp file for mimicking a database

from dataclasses import dataclass
from os import strerror
from typing import Dict, Iterable, Tuple, FrozenSet

#decorate immutable class
@dataclass(frozen=True)
class ColorDef:
    name: str
    r: int
    y: int
    b: int
    is_base: bool = False

BASE_COLORS: Tuple[ColorDef, ...] = (
    ColorDef("red", 255, 0, 0, True),
    ColorDef("yellow", 0, 255, 0, True),
    ColorDef("blue", 0, 0, 255, True),
    )

#create internal dict for quick lookups

#create predefined table with combinations for base colors

#create mix_colors algorithm
