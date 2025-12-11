
from dataclasses import dataclass
from typing import List

from ..data.repo import PaletteRepository, ColorRecord, MAX_COLORS
from ..data.palette_catalog import mix_colors

@dataclass(frozen=True)
class MixResult:
    result: ColorRecord
    added_to_palette: bool
    palette_size: int

class ColorMixerService:

    def __init__(self, repo: PaletteRepository | None = None) -> None:
        self._repo = repo or PaletteRepository()

    def get_palette(self) -> List[ColorRecord]:
        return self._repo.load_palette()

    def clear_palette(self) -> List[ColorRecord]:
        self._repo.clear_palette_to_base()
        return self._repo.load_palette()
        
    # mix two colors and store new color if capacity allows
    def mix(self, color_a: str, color_b: str) -> MixResult:
        result_color = mix_colors(color_a, color_b)
        result_name = result_color.name.lower()

        # Black / White are unlockable, but not added to palette
        if result_name in ("black", "white"):
            added = False
        else:
            added = self._repo.add_color(result_color)

        palette_size = len(self._repo.load_palette())

        return MixResult(
            result = result_color,
            added_to_palette = added,
            palette_size = palette_size,
        )