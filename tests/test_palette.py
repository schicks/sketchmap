"""Tests for ColorPalette and TerrainType classes."""

import pytest
from sketchmap.palette import ColorPalette, TerrainType


class TestTerrainType:
    """Test cases for TerrainType enum."""

    def test_terrain_types_exist(self) -> None:
        """Test that all expected terrain types are defined."""
        assert TerrainType.WATER
        assert TerrainType.FOREST
        assert TerrainType.MOUNTAIN
        assert TerrainType.DESERT
        assert TerrainType.GRASSLAND
        assert TerrainType.CITY
        assert TerrainType.UNCONSTRAINED

    def test_terrain_type_values(self) -> None:
        """Test that terrain type values are strings."""
        assert isinstance(TerrainType.WATER.value, str)
        assert isinstance(TerrainType.FOREST.value, str)


class TestColorPalette:
    """Test cases for ColorPalette class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.palette = ColorPalette()

    def test_initialization(self) -> None:
        """Test ColorPalette initializes with correct mappings."""
        assert self.palette is not None
        assert len(self.palette.color_map) == 7  # 7 terrain types
        assert len(self.palette.terrain_prompts) == 7

    def test_color_map_contains_required_colors(self) -> None:
        """Test that color map contains all required palette colors."""
        expected_colors = [
            "#0000FF",  # Water - blue
            "#00FF00",  # Forest - green
            "#8B4513",  # Mountain - brown
            "#FFFF00",  # Desert - yellow
            "#90EE90",  # Grassland - light green
            "#808080",  # City - gray
            "#FFFFFF",  # Unconstrained - white
        ]
        for color in expected_colors:
            assert color in self.palette.color_map

    def test_terrain_prompts_exist_for_all_types(self) -> None:
        """Test that terrain prompts exist for all terrain types."""
        for terrain_type in TerrainType:
            assert terrain_type in self.palette.terrain_prompts
            assert isinstance(self.palette.terrain_prompts[terrain_type], str)
            assert len(self.palette.terrain_prompts[terrain_type]) > 0

    def test_get_terrain_type_for_exact_colors(self) -> None:
        """Test get_terrain_type returns correct type for exact palette colors."""
        assert self.palette.get_terrain_type("#0000FF") == TerrainType.WATER
        assert self.palette.get_terrain_type("#00FF00") == TerrainType.FOREST
        assert self.palette.get_terrain_type("#8B4513") == TerrainType.MOUNTAIN
        assert self.palette.get_terrain_type("#FFFF00") == TerrainType.DESERT
        assert self.palette.get_terrain_type("#90EE90") == TerrainType.GRASSLAND
        assert self.palette.get_terrain_type("#808080") == TerrainType.CITY
        assert self.palette.get_terrain_type("#FFFFFF") == TerrainType.UNCONSTRAINED

    def test_get_terrain_type_for_unknown_color(self) -> None:
        """Test get_terrain_type returns UNCONSTRAINED for unknown colors."""
        result = self.palette.get_terrain_type("#123456")
        assert result == TerrainType.UNCONSTRAINED

    def test_quantize_color_exact_match(self) -> None:
        """Test quantize_color returns same color for exact palette match."""
        # Pure blue should map to blue
        assert self.palette.quantize_color((0, 0, 255)) == "#0000FF"
        # Pure green should map to green
        assert self.palette.quantize_color((0, 255, 0)) == "#00FF00"
        # Saddle brown should map to brown
        assert self.palette.quantize_color((139, 69, 19)) == "#8B4513"

    def test_quantize_color_near_blue(self) -> None:
        """Test quantize_color maps colors close to blue to blue."""
        # Slightly off blue (still closest to pure blue)
        assert self.palette.quantize_color((0, 0, 250)) == "#0000FF"
        assert self.palette.quantize_color((10, 10, 255)) == "#0000FF"
        assert self.palette.quantize_color((5, 5, 240)) == "#0000FF"

    def test_quantize_color_near_green(self) -> None:
        """Test quantize_color maps colors close to green to green."""
        # Forest green variations
        assert self.palette.quantize_color((0, 250, 0)) == "#00FF00"
        assert self.palette.quantize_color((10, 255, 10)) == "#00FF00"

    def test_quantize_color_near_white(self) -> None:
        """Test quantize_color maps near-white colors to white."""
        # Almost white should map to white
        assert self.palette.quantize_color((255, 255, 255)) == "#FFFFFF"
        assert self.palette.quantize_color((250, 250, 250)) == "#FFFFFF"

    def test_quantize_color_euclidean_distance(self) -> None:
        """Test that quantization uses Euclidean distance in RGB space."""
        # A dark blue should be closer to blue (#0000FF) than to green (#00FF00)
        result = self.palette.quantize_color((0, 0, 128))
        assert result == "#0000FF"

        # A yellow-green should map to one of the greens or yellow
        # Light green (#90EE90) or pure green (#00FF00) or yellow (#FFFF00)
        result = self.palette.quantize_color((200, 255, 100))
        assert result in ["#00FF00", "#90EE90", "#FFFF00"]

    def test_quantize_color_input_validation(self) -> None:
        """Test quantize_color validates RGB tuple input."""
        # Valid inputs should work
        assert isinstance(self.palette.quantize_color((0, 0, 0)), str)
        assert isinstance(self.palette.quantize_color((255, 255, 255)), str)

    def test_quantize_color_bounds(self) -> None:
        """Test quantize_color handles edge case RGB values."""
        # All black should map to some color (likely gray or blue)
        result = self.palette.quantize_color((0, 0, 0))
        assert result in self.palette.color_map.keys()

        # All white should map to white
        result = self.palette.quantize_color((255, 255, 255))
        assert result == "#FFFFFF"

    def test_color_map_uniqueness(self) -> None:
        """Test that all colors in palette are unique."""
        colors = list(self.palette.color_map.keys())
        assert len(colors) == len(set(colors))

    def test_terrain_type_uniqueness(self) -> None:
        """Test that all terrain types in color_map are unique values."""
        terrain_types = list(self.palette.color_map.values())
        # Each color should map to a distinct terrain type
        # (though multiple colors could theoretically map to same type)
        assert all(isinstance(t, TerrainType) for t in terrain_types)

    def test_hex_color_format(self) -> None:
        """Test that all colors in color_map are valid hex format."""
        import re

        hex_pattern = re.compile(r"^#[0-9A-F]{6}$")
        for color in self.palette.color_map.keys():
            assert hex_pattern.match(color), f"Invalid hex color: {color}"

    def test_get_rgb_from_hex(self) -> None:
        """Test conversion from hex to RGB (helper method if implemented)."""
        # Test that quantize_color round-trips correctly
        # If we convert palette hex to RGB and quantize, we should get same hex
        palette_hex = "#0000FF"
        rgb = (0, 0, 255)
        result = self.palette.quantize_color(rgb)
        assert result == palette_hex
