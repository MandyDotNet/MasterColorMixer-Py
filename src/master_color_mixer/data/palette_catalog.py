#temp file for mimicking a database

from typing import List
from master_color_mixer.alg import merge_sort

BASE_COLORS: List[str] = ["yellow", "red", "blue"]
UNLOCKED_COLORS: List[str] = []

def get_all_colors_sorted() -> List[str]:

    all_colors = BASE_COLORS + UNLOCKED_COLORS
    return merge_sort(all_colors)


def add_unlocked_color(name: str) -> None:
    if name not in UNLOCKED_COLORS:
        UNLOCKED_COLORS.append(name)