
from dataclasses import dataclass
from typing import List

from ..data.repo import PaletteRepository, ColorRecord, MAX_COLORS
#todo - import mix_colors

@dataclass(frozen=True)
class MixResult:
    result: ColorRecord
    added_to_palette: bool
    palette_size: int

class ColorMixerService:

    def __init__(self, repo: PaletteRepository | None = None) -> None:
        self._repo = repo or PaletteRepository()

    #create get_palette
    
    #create clear_palette

    #create mix