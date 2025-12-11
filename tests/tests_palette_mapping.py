import pytest

from master_color_mixer.data.palette_catalog import PARENT_MAP, validate_parent_map


def test_parent_map_validity():
    # test that all colors in PARENT_MAP have valid parent colors
    try:
        validate_parent_map(PARENT_MAP)
    except ValueError as e:
        pytest.fail(f"Parent map validation failed: {e}")


def test_parent_map_detects_unknown_child():
    # invalid parent map with an unknown child color
    invalid_parent_map = {
        "unknown_color": ("red", "blue"),
    }

    with pytest.raises(ValueError) as excinfo:
        validate_parent_map(invalid_parent_map)

    error_message = str(excinfo.value)
    assert "unknown_color" in error_message


def test_parent_map_detects_unknown_parent_first():
    # invalid parent map with an unknown parent color
    invalid_parent_map = {
        "green": ("unknown_parent1", "yellow"),
    }

    with pytest.raises(ValueError) as excinfo:
        validate_parent_map(invalid_parent_map)

    error_message = str(excinfo.value)
    assert "unknown_parent1" in error_message


def test_parent_map_detects_unknown_second_parent():
    # invalid parent map with an unknown second parent color
    invalid_parent_map = {
        "purple": ("red", "unknown_parent2"),
    }

    with pytest.raises(ValueError) as excinfo:
        validate_parent_map(invalid_parent_map)

    error_message = str(excinfo.value)
    assert "unknown_parent2" in error_message


def test_parent_map_detects_self_parenting():
    # create an invalid parent map with self-parenting
    invalid_parent_map = {
        "red": ("red", "blue"),
    }

    with pytest.raises(ValueError) as excinfo:
        validate_parent_map(invalid_parent_map)

    error_message = str(excinfo.value)
    # match the actual message from validate_parent_map
    assert "cannot use itself as a parent" in error_message