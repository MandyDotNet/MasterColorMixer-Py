from src.master_color_mixer.core.mixing import ColorMixerService
from src.master_color_mixer.data.repo import PaletteRepository, ColorRecord, MAX_COLORS

def make_service(tmp_path) -> ColorMixerService:
    db_path = tmp_path / "mcm_feature.db"
    repo = PaletteRepository(db_path)
    return ColorMixerService(repo)

def test_mix_red_and_blue_produces_purple(tmp_path):
    service = make_service(tmp_path)
    result = service.mix("red", "blue")

    assert result.result.name == "purple"
    # matches ColorDef("purple", 220, 0, 255, ...)
    assert result.result.r == 220
    assert result.result.y == 0
    assert result.result.b == 255

def test_mix_adds_new_color_to_palette(tmp_path):
    service = make_service(tmp_path)
    before_len = len(service.get_palette())

    result = service.mix("red", "blue")  # purple
    after_len = len(service.get_palette())

    if result.added_to_palette:
        assert after_len == before_len + 1
    else:
        assert after_len == before_len

def test_palette_never_exceeds_max_colors(tmp_path):
    # case: when palette is full, mixing should not push it over MAX_COLORS.

    service = make_service(tmp_path)
    repo = service._repo  

    # fill palette to MAX_COLORS with synthetic colors
    palette = repo.load_palette()
    for i in range(len(palette), MAX_COLORS):
        palette.append(ColorRecord(f"fill_{i}", i, i, i))
    repo.save_palette(palette)

    # mix something that would normally add a new color
    result = service.mix("red", "blue")

    final_palette = repo.load_palette()
    assert len(final_palette) == MAX_COLORS
    assert not result.added_to_palette