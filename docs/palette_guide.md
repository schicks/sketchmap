# Color Palette Guide

## Overview

Sketchmap uses a predefined color palette to interpret your sketch and generate detailed maps. Each color in the palette corresponds to a specific terrain type that will be generated in the final map.

## Color-to-Terrain Mappings

### Water - Blue
**Hex Color**: `#0000FF` (Pure Blue)
**RGB**: (0, 0, 255)
**Terrain Type**: Water bodies, oceans, lakes, rivers
**Description**: Blue regions will generate as water features. This includes oceans, lakes, rivers, and other bodies of water. The AI will add realistic water textures and appropriate details.

### Forest - Green
**Hex Color**: `#00FF00` (Pure Green)
**RGB**: (0, 255, 0)
**Terrain Type**: Dense forests, vegetation, jungles
**Description**: Green regions will generate as forested areas with dense vegetation. The AI will create realistic tree coverage and lush plant life.

### Mountain - Brown
**Hex Color**: `#8B4513` (Saddle Brown)
**RGB**: (139, 69, 19)
**Terrain Type**: Mountains, rocky peaks, highlands
**Description**: Brown regions will generate as mountainous terrain with rocky peaks and elevated landscapes. Expect dramatic elevation changes and rugged terrain.

### Desert - Yellow
**Hex Color**: `#FFFF00` (Pure Yellow)
**RGB**: (255, 255, 0)
**Terrain Type**: Deserts, sand dunes, arid landscapes
**Description**: Yellow regions will generate as arid desert terrain with sand dunes and sparse vegetation. The AI will create realistic desert features.

### Grassland - Light Green
**Hex Color**: `#90EE90` (Light Green)
**RGB**: (144, 238, 144)
**Terrain Type**: Grasslands, plains, meadows
**Description**: Light green regions will generate as open grasslands and plains. Expect rolling meadows and open landscapes with grass coverage.

### City/Settlement - Gray
**Hex Color**: `#808080` (Gray)
**RGB**: (128, 128, 128)
**Terrain Type**: Settlements, towns, urban areas
**Description**: Gray regions will generate as developed areas with settlements or urban features. The AI will add structures and signs of civilization.

### Unconstrained - White
**Hex Color**: `#FFFFFF` (Pure White)
**RGB**: (255, 255, 255)
**Terrain Type**: Auto-generated natural terrain
**Description**: White (unmarked) regions are unconstrained and will be automatically filled with appropriate terrain that blends naturally with your colored regions. This allows you to define only the key features and let the AI fill in the rest.

## Using the Palette

### In Paint Programs

1. **Use Exact Colors**: For best results, use the exact hex color values listed above
2. **Color Picker**: Copy the hex codes directly into your paint program's color picker
3. **Brush Tool**: Use solid, opaque brushes - transparency may cause issues
4. **Fill Tool**: Bucket fill is perfect for large regions

### Color Tolerance

Don't worry if your colors aren't exactly perfect! Sketchmap automatically maps similar colors to the nearest palette color:

- Colors close to `#0000FF` will be interpreted as water
- Slight variations in color (e.g., `#0033FF` or `#0000CC`) will be quantized to the nearest palette color
- The system will show you which palette colors your sketch mapped to before generation

### Tips for Best Results

1. **High Contrast**: Use distinct colors that don't blend together
2. **Clear Boundaries**: Define clear edges between different terrain types
3. **Mix Constrained and Unconstrained**: Use white space strategically to let the AI add creative details
4. **Start Simple**: Begin with 2-3 terrain types before creating complex multi-terrain maps

## Example Workflows

### Simple Island Map
1. Draw a blue blob for ocean
2. Leave center white or use light green for land
3. Generate to see a natural island with varied terrain

### Fantasy World
1. Blue for oceans and lakes
2. Brown for mountain ranges
3. Green for forests
4. Light green for plains
5. White for unconstrained regions
6. Generate to see a complete fantasy world map

### Desert Oasis
1. Yellow for desert regions
2. Small blue spots for oases
3. Green patches for vegetation near water
4. White for natural transitions

## Technical Notes

- **Color Quantization**: Non-palette colors are automatically mapped using Euclidean distance in RGB color space
- **File Formats**: Use PNG for lossless color preservation; JPG may introduce color artifacts
- **Resolution**: Works best with sketches between 256x256 and 1024x1024 pixels
- **Precision**: Exact palette colors give most predictable results

## Troubleshooting

**Q: My colors aren't being recognized**
A: Make sure you're using RGB mode (not CMYK or grayscale) and check that colors are opaque (no transparency)

**Q: Can I use custom colors?**
A: In v1.0, only the predefined palette is supported. Custom palettes may be added in future versions.

**Q: What if I use the wrong color?**
A: The system will map it to the closest palette color and show you the mapping before generation.

---

**Version**: 1.0.0 | **Last Updated**: 2026-01-03
