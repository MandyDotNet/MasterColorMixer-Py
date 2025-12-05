# I looked into using an existing library to more easily detect the mixed color
# but my app is based on RYB not RGB so I did not use it 
# --> https://webcolors.readthedocs.io/en/stable/contents.html

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple, FrozenSet

#decorate immutable class
@dataclass(frozen=True)
class ColorDef:
    name: str
    r: int
    y: int
    b: int
    is_base: bool = False

# immutable with Type hint for clarity - primaries are always in the palette
BASE_COLORS: Tuple[ColorDef, ...] = (
    ColorDef("red", 255, 0, 0, True),
    ColorDef("yellow", 0, 255, 0, True),
    ColorDef("blue", 0, 0, 255, True),
    )

EXTENDED_COLORS: Tuple[ColorDef, ...] = (
    #--- Secondaries ---
    ColorDef("orange",        255, 180,   0),
    ColorDef("green",           0, 255, 180),
    ColorDef("purple",        220,   0, 255),

    #--- Tertiarie Classics ---
    ColorDef("red-orange",    255, 140,   0),
    ColorDef("yellow-orange", 255, 220,  80),
    ColorDef("yellow-green",   80, 255, 120),
    ColorDef("blue-green",      0, 180, 230),
    ColorDef("blue-purple",   160,   0, 255),
    ColorDef("red-purple",    255,   0, 160),

    #--- Greens/Blues ---
    ColorDef("teal",            0, 170, 170),
    ColorDef("mint",            80, 255, 200),
    ColorDef("lime",           140, 255, 100),
    ColorDef("sky-blue",        80, 140, 255),
    ColorDef("azure",           80, 120, 255),
    ColorDef("turquoise",       40, 200, 210),
    ColorDef("emerald",         20, 200,  80),
    ColorDef("sage",           120, 180, 120),
    ColorDef("aqua",            40, 220, 220),
    ColorDef("cyan",            20, 200, 230),
    ColorDef("periwinkle",     160, 140, 255),
    ColorDef("cerulean",        20, 100, 220),
    ColorDef("seafoam",         80, 230, 200),
    ColorDef("chartreuse",     160, 255,  40),

    #--- Reds/Pinks/Oragnes ---
    ColorDef("magenta",        255,   0, 255),
    ColorDef("peach",          255, 180, 120),
    ColorDef("coral",          255, 140, 120),
    ColorDef("crimson",        180,   0,  40),
    ColorDef("scarlet",        255,  40,   0),
    ColorDef("maroon",         120,  20,  40),
    ColorDef("fuchsia",        255,  40, 255),
    ColorDef("salmon",         255, 160, 140),
    ColorDef("tangerine",      255, 140,  40),
    ColorDef("amber",          255, 200,  40),
    ColorDef("apricot",        255, 200, 120),

    #--- Purples ---
    ColorDef("lavender",       220, 160, 255),
    ColorDef("violet",         200,  80, 255),
    ColorDef("amethyst",       180,  60, 255),
    ColorDef("lilac",          220, 180, 255),
    ColorDef("mauve",          180, 120, 200),

    #--- Neutrals ---
    ColorDef("beige",          230, 210, 180),
    ColorDef("taupe",          160, 140, 120),
    ColorDef("khaki",          190, 200, 140),
    ColorDef("sienna",         160,  90,  40),
    ColorDef("olive",          140, 160,  40),
    ColorDef("ivory",          245, 240, 220),
    ColorDef("onyx",            20,  20,  30),
    ColorDef("pewter",         160, 170, 180),
    ColorDef("ebony",           10,  10,  20),
    ColorDef("indigo",          40,  20, 120),

    )

ALL_COLORS: Tuple[ColorDef, ...] = BASE_COLORS + EXTENDED_COLORS

# lookup (lowercase for safety)
_COLOR_BY_NAME: Dict[str, ColorDef] = {c.name.lower(): c for c in ALL_COLORS}

# PARENT_MAP: for every extended color, define two parents.
# This guarantees there is at least one mix that produces it.
PARENT_MAP: Dict[str, Tuple[str, str]] = {
    #--- Secondaries ---
    "orange": ("red", "yellow"),
    "green": ("blue", "yellow"),
    "purple": ("red", "blue"),

    #--- Tertiarie Classics ---
    "red-orange": ("red", "orange"),
    "yellow-orange": ("yellow", "orange"),
    "yellow-green": ("yellow", "green"),
    "blue-green": ("blue", "green"),
    "blue-purple": ("blue", "magenta"), # slightly brighter blue-purple
    "red-purple": ("red", "purple"),

    #--- Greens/Blues ---
    "teal": ("cyan", "green"),
    "mint": ("green", "ivory"),
    "lime": ("yellow", "yellow-green"),
    "sky-blue": ("blue", "mint"),
    "azure": ("blue", "sky-blue"),
    "aqua": ("green", "sky-blue"),
    "turquoise": ("blue-green", "aqua"),
    "emerald": ("green", "blue-green"),
    "sage": ("green", "beige"),
    "cyan": ("blue", "aqua"),
    "periwinkle": ("blue", "lavender"),
    "cerulean": ("blue", "azure"),
    "seafoam": ("mint", "aqua"),
    "chartreuse": ("yellow-green", "lime"),

    #--- Reds/Pinks/Oragnes ---
    "magenta": ("red", "violet"),
    "scarlet": ("red", "yellow-orange"),
    "tangerine": ("orange", "red-orange"),
    "amber": ("yellow", "yellow-orange"),
    "peach": ("orange", "ivory"),
    "coral": ("orange", "magenta"),
    "maroon": ("red", "onyx"),
    "crimson": ("red", "indigo"),
    "salmon": ("orange", "peach"),
    "apricot": ("peach", "yellow"),
    "fuchsia": ("magenta", "peach"),

    #--- Purples ---
    "lavender": ("purple", "ivory"),
    "violet": ("purple", "blue"),
    "amethyst": ("violet", "indigo"),
    "lilac": ("lavender", "peach"),
    "mauve": ("purple", "beige"),

    #--- Neutrals ---
    "sienna": ("orange", "green"),  # “brown” from orange + green
    "beige": ("yellow", "sienna"),
    "olive": ("green", "sienna"),
    "ivory": ("yellow", "beige"),
    "onyx": ("blue", "sienna"),
    "taupe": ("beige", "onyx"),
    "khaki": ("yellow", "taupe"),
    "pewter": ("blue", "taupe"),
    "ebony": ("onyx", "purple"),
    "indigo": ("blue", "ebony"),
}

RYB_NAME_MAP: Dict[FrozenSet[str], str] = {
    frozenset({p1, p2}): child
    for child, (p1, p2) in PARENT_MAP.items()
}

# helper method: custom map to return predefined name, or a generic 'a/b mix' label
def get_ryb_mix_name(name_a: str, name_b: str) -> str:
    na = name_a.lower()
    nb = name_b.lower()
    key = frozenset({na, nb})

    if key in RYB_NAME_MAP:
        return RYB_NAME_MAP[key]

    sorted_names = sorted(list(key))
    return f"{sorted_names[0]}/{sorted_names[1]} mix"


# concrete mapping from color pairs -> ColorDef result
MIX_TABLE: Dict[FrozenSet[str], ColorDef] = {
    combo: _COLOR_BY_NAME[result_name]
    for combo, result_name in RYB_NAME_MAP.items()
    if result_name in _COLOR_BY_NAME
}

def mix_colors(name_a: str, name_b: str) -> ColorDef:
    na = name_a.lower()
    nb = name_b.lower()

    color_a = _COLOR_BY_NAME.get(na)
    color_b = _COLOR_BY_NAME.get(nb)

    if color_a is None:
        raise ValueError(f"Unknown color {name_a!r}")
    if color_b is None:
        raise ValueError(f"Unknown color {name_b!r}")

    # case: self-mix
    if na == nb: 
        return color_a
    
    key = frozenset({na, nb})

    # case : theory-driven mix --> use explicit mapping if it exists
    if key in RYB_NAME_MAP:
        result_name = RYB_NAME_MAP[key]
        # the color should always exist, but check anyway
        existing = _COLOR_BY_NAME.get(result_name.lower())
        if existing is not None:
            return existing

    # case: dynamic mix --> calculate the average R, Y, B values
    avg_r = (color_a.r + color_b.r) // 2
    avg_y = (color_a.y + color_b.y) // 2
    avg_b = (color_a.b + color_b.b) // 2
    new_name = get_ryb_mix_name(na, nb) # get name based on mix

    # If that name already exists in the catalog, snap to it
    existing = _COLOR_BY_NAME.get(new_name.lower())
    if existing is not None:
        return existing

    # Return a new, dynamically (ad-hoc) created ColorDef object
    return ColorDef(
        name = new_name,
        r = avg_r,
        y = avg_y,
        b = avg_b,
        is_base = False
    )
