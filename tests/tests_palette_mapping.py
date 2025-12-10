import pytest

from master_color_mixer.data.palette_catalog import PARENT_MAP, validate_parent_map

def test_parent_map_validity():
    # test that all colors in PARENT_MAP have valid parent colors
    try:
        validate_parent_map(PARENT_MAP)
    except ValueError as e:
        pytest.fail(f"Parent map validation failed: {e}")

def test_parent_map_detects_unknown_child_or_parents():
    # create an invalid parent map with unknown child and parents
    invalid_parent_map = {
        "unknown_color": ("red", "blue"),
        "green": ("unknown_parent1", "yellow"),
        "purple": ("red", "unknown_parent2"),
    }
    with pytest.raises(ValueError) as excinfo:
        validate_parent_map(invalid_parent_map)
    
    error_message = str(excinfo.value)
    assert "unknown_color" in error_message
    assert "unknown_parent1" in error_message
    assert "unknown_parent2" in error_message

def test_parent_map_detects_self_parenting():
    # create an invalid parent map with self-parenting
    invalid_parent_map = {
        "red": ("red", "blue"),
        "green": ("green", "yellow"),
    }
    with pytest.raises(ValueError) as excinfo:
        validate_parent_map(invalid_parent_map)
    
    error_message = str(excinfo.value)
    assert "self-parenting" in error_message