"""Color palette and terrain type definitions for sketch-based map generation."""

from enum import Enum
from typing import Dict


class TerrainType(Enum):
    """Enumeration of supported terrain types for map generation."""

    WATER = "water"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    DESERT = "desert"
    GRASSLAND = "grassland"
    CITY = "city"
    UNCONSTRAINED = "unconstrained"


class ColorPalette:
    """Defines the color-to-terrain mapping for sketch input.

    This class manages the predefined color palette used to interpret user sketches.
    Each color in the palette corresponds to a specific terrain type that will be
    generated in the final map.

    Attributes:
        color_map: Dictionary mapping hex color codes to terrain types
        terrain_prompts: Dictionary mapping terrain types to descriptive prompts
    """

    def __init__(self) -> None:
        """Initialize the color palette with predefined terrain mappings."""
        # Define the predefined color palette
        self.color_map: Dict[str, TerrainType] = {
            "#0000FF": TerrainType.WATER,  # Pure blue
            "#00FF00": TerrainType.FOREST,  # Pure green
            "#8B4513": TerrainType.MOUNTAIN,  # Saddle brown
            "#FFFF00": TerrainType.DESERT,  # Pure yellow
            "#90EE90": TerrainType.GRASSLAND,  # Light green
            "#808080": TerrainType.CITY,  # Gray
            "#FFFFFF": TerrainType.UNCONSTRAINED,  # White
        }

        # Define descriptive prompts for each terrain type
        self.terrain_prompts: Dict[TerrainType, str] = {
            TerrainType.WATER: "clear blue water, rivers, lakes, ocean",
            TerrainType.FOREST: "dense forest, lush vegetation, trees",
            TerrainType.MOUNTAIN: "mountains, rocky peaks, highlands",
            TerrainType.DESERT: "desert, sand dunes, arid landscape",
            TerrainType.GRASSLAND: "grassland, plains, meadows",
            TerrainType.CITY: "settlements, towns, urban areas",
            TerrainType.UNCONSTRAINED: "natural terrain",
        }

    def quantize_color(self, rgb: tuple[int, int, int]) -> str:
        """Find the nearest palette color to the given RGB value.

        Uses Euclidean distance in RGB color space to find the closest
        palette color to the input RGB value.

        Args:
            rgb: Tuple of (red, green, blue) values in range 0-255

        Returns:
            Hex color string of the nearest palette color (e.g., "#0000FF")

        Example:
            >>> palette = ColorPalette()
            >>> palette.quantize_color((0, 0, 255))
            '#0000FF'
            >>> palette.quantize_color((10, 10, 250))
            '#0000FF'
        """
        r, g, b = rgb

        min_distance = float("inf")
        closest_color = "#FFFFFF"  # Default to unconstrained

        for hex_color in self.color_map.keys():
            # Convert hex to RGB
            palette_r = int(hex_color[1:3], 16)
            palette_g = int(hex_color[3:5], 16)
            palette_b = int(hex_color[5:7], 16)

            # Calculate Euclidean distance in RGB space
            distance = (
                (r - palette_r) ** 2 + (g - palette_g) ** 2 + (b - palette_b) ** 2
            ) ** 0.5

            if distance < min_distance:
                min_distance = distance
                closest_color = hex_color

        return closest_color

    def get_terrain_type(self, color_hex: str) -> TerrainType:
        """Get the terrain type for a given palette color.

        Args:
            color_hex: Hex color string (e.g., "#0000FF")

        Returns:
            TerrainType corresponding to the color, or UNCONSTRAINED if not found

        Example:
            >>> palette = ColorPalette()
            >>> palette.get_terrain_type("#0000FF")
            <TerrainType.WATER: 'water'>
            >>> palette.get_terrain_type("#UNKNOWN")
            <TerrainType.UNCONSTRAINED: 'unconstrained'>
        """
        return self.color_map.get(color_hex, TerrainType.UNCONSTRAINED)
