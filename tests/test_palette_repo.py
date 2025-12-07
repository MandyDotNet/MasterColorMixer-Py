from pathlib import Path
from src.master_color_mixer.data.repo import PaletteRepository, BASE_COLORS, ColorRecord, MAX_COLORS

def test_repo_bootstraps_with_base_colors(tmp_path):
    db_path = tmp_path / "test_palette.db"
    repo = PaletteRepository(db_path)

    palette = repo.load_palette()
    names = {c.name for c in palette}

    for base in BASE_COLORS:
        assert base.name in names

def test_repo_respects_max_colors(tmp_path):
    db_path = tmp_path / "test_palette.db"
    repo = PaletteRepository(db_path)

    # fill up to MAX_COLORS starting from whatever the current size is
    palette = repo.load_palette()
    start_len = len(palette)

    for i in range(start_len, MAX_COLORS):
        inserted = repo.add_color(ColorRecord(f"extra_{i}", i, i, i))
        assert inserted is True

    palette = repo.load_palette()
    assert len(palette) == MAX_COLORS

    # try to add one more --> should not insert
    inserted = repo.add_color(ColorRecord("too_many", 1, 2, 3))
    assert inserted is False

    palette2 = repo.load_palette()
    assert len(palette2) == MAX_COLORS