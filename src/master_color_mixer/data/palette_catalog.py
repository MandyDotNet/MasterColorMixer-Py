# I looked into using an existing library to more easily detect the mixed color
# but my app is based on RYB not RGB so I did not use it 
# --> https://webcolors.readthedocs.io/en/stable/contents.html

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple, FrozenSet, List

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
    ColorDef("orange",     255, 180,   0),
    ColorDef("green",        0, 255, 180),
    ColorDef("purple",     220,   0, 255),

    #--- Neutrals / Earthy Tones ---
    ColorDef("white",      255, 255, 255),
    ColorDef("brown",      150,  90,  40),
    ColorDef("grey",       128, 128, 128),
    ColorDef("beige",      230, 210, 180),
    ColorDef("sienna",     160,  82,  45),
    ColorDef("olive",      128, 128,   0),
    ColorDef("mustard",    255, 219,  88),
    ColorDef("gold",       255, 223,   0),
    ColorDef("amber",      255, 126,   0),
    ColorDef("steel-grey",  67,  70,  75),
    ColorDef("black",        0,   0,   0),

    #--- Blues / Greens / Cool Tones ---
    ColorDef("turquoise",   64, 244, 208),
    ColorDef("teal",         28, 88, 132),
    ColorDef("marine-blue",      10,  80, 150),
    ColorDef("lime",        50, 205,  50),
    ColorDef("mint",        62, 180, 137),
    ColorDef("indigo",     111,   0, 255),

    #--- Reds / Warm Tones ---
    ColorDef("magenta",    255,   0, 255),
    ColorDef("pink",       255, 192, 203),
    ColorDef("peach",      255, 229, 180),
    ColorDef("maroon",     128,   0,   0),
    ColorDef("crimson",    220,  20,  60),
    ColorDef("violet",     127,   0, 255),
    )

# predefined mixes that result in black, not to be added to ALL_COLORS
BLACK_PARENTS: Tuple[Tuple[str, str], ...] = (
    ("olive", "brown"),
    ("olive", "grey"),
    ("grey",  "brown"),
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

    "olive": ("orange", "green"),
    "brown": ("orange", "purple"),
    "grey": ("green", "purple"),

    "indigo": ("blue", "purple"),
    "turquoise": ("blue", "green"),
    "maroon": ("purple", "yellow"),
    "magenta": ("purple", "red"),
    "amber": ("yellow", "maroon"),
    "beige": ("brown", "yellow"),
    "sienna": ("orange", "blue"),
    "marine-blue": ("blue", "magenta"),
    "violet": ("marine-blue", "purple"),
    "mustard": ("orange", "yellow"),
    "peach": ("orange", "pink"),
    "gold": ("sienna", "yellow"),
    "crimson": ("magenta", "red"),
    "steel-grey": ("grey", "blue"),

    "teal": ("white", "turquoise"),
    "pink": ("white", "red"),
    "lime": ("white", "green"),
    "mint": ("white", "teal"),
}

# helper method: validate PARENT_MAP
def validate_parent_map(parent_map: Dict[str, Tuple[str, str]]) -> None:
    # All valid color names (lowercase) from the palette
    defined_names = set(_COLOR_BY_NAME.keys())

    for raw_child, (raw_p1, raw_p2) in parent_map.items():
        child = raw_child.lower()
        p1 = raw_p1.lower()
        p2 = raw_p2.lower()

        # every child exists as a defined color
        if child not in defined_names:
            raise ValueError(
                f"PARENT_MAP child '{raw_child}' has no ColorDef defined."
            )

        # every parent exists as a defined color
        if p1 not in defined_names:
            raise ValueError(
                f"PARENT_MAP parent '{raw_p1}' for '{raw_child}' "
                f"has no ColorDef defined."
            )

        if p2 not in defined_names:
            raise ValueError(
                f"PARENT_MAP parent '{raw_p2}' for '{raw_child}' "
                f"has no ColorDef defined."
            )

        # no color lists itself as a parent
        if child == p1 or child == p2:
            raise ValueError(
                f"PARENT_MAP entry '{raw_child}' "
                f"cannot use itself as a parent ({raw_p1}, {raw_p2})."
            )

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

    if (color_a, color_b) in BLACK_PARENTS or (color_a, color_b) in BLACK_PARENTS:
        return _COLOR_BY_NAME["black"]
    
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
