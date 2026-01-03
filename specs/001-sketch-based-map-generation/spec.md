# Feature: Sketch-Based Map Generation

**Status**: Draft | **Priority**: P1 | **Created**: 2026-01-03

## Overview

A tool that generates detailed world maps from simple user-provided sketches with color hints. Users can create rough sketches using basic paint tools where each color from a constrained palette indicates what type of terrain or feature should appear in that region (water, forests, mountains, etc.). Unmarked or white regions are automatically filled with appropriate terrain that blends naturally with the constrained areas.

### Goals
- Enable non-artists to create detailed, professional-looking world maps from simple sketches
- Provide intuitive color-based control over terrain types and features
- Generate coherent, visually appealing maps that respect user constraints while filling in creative details
- Support both highly constrained (fully colored) and loosely constrained (sparse hints) sketch inputs

## User Stories

### [US1] Generate Map from Color-Coded Sketch (Priority: P1)
**As a** game designer or worldbuilder
**I want** to sketch a rough map with colored regions and have it generate a detailed map
**So that** I can quickly visualize and iterate on world designs without artistic skills

**Acceptance Criteria**:
- [ ] User can provide a sketch image file (PNG, JPG) with colored regions
- [ ] Blue regions generate as water bodies (oceans, lakes, rivers)
- [ ] Green regions generate as vegetated areas (forests, jungles)
- [ ] Brown regions generate as mountainous terrain
- [ ] Yellow regions generate as arid terrain (deserts, beaches)
- [ ] Gray regions generate as settlements or developed areas
- [ ] Generated map maintains the spatial layout and boundaries from the sketch
- [ ] Output is a high-quality image suitable for presentation or further editing

---

### [US2] Automatic Infill of Unconstrained Regions (Priority: P1)
**As a** user creating a sparse sketch
**I want** unmarked white regions to be automatically filled with appropriate terrain
**So that** I only need to define key features and the tool handles the rest

**Acceptance Criteria**:
- [ ] White/unmarked regions are recognized as unconstrained
- [ ] Unconstrained regions generate plausible, natural-looking terrain
- [ ] Automatically generated terrain blends smoothly with user-defined regions
- [ ] Transitions between constrained and unconstrained areas appear natural
- [ ] Infilled areas maintain thematic consistency with the overall map

---

### [US3] Control Map Style and Theme (Priority: P1)
**As a** user
**I want** to specify the overall style or theme of the generated map
**So that** I can create maps for different purposes (fantasy, realistic, topographic, etc.)

**Acceptance Criteria**:
- [ ] User can specify a text description of the desired map style
- [ ] Maps can be generated in different visual styles (fantasy, satellite, hand-drawn, topographic)
- [ ] The specified style is consistently applied across the entire map
- [ ] Style affects visual appearance but not the terrain type meanings of colors

---

### [US4] Adjust Control Strength of Sketch (Priority: P2)
**As a** user
**I want** to control how strictly the generator follows my sketch
**So that** I can balance between precise control and creative freedom

**Acceptance Criteria**:
- [ ] User can set a control strength/influence parameter
- [ ] Higher control strength makes output closely follow the sketch
- [ ] Lower control strength allows more creative interpretation
- [ ] Control strength can be adjusted without changing the sketch
- [ ] Default control strength produces good results for typical use cases

---

### [US5] Reproducible Generation with Seeds (Priority: P2)
**As a** user
**I want** to be able to reproduce the exact same map from a sketch
**So that** I can share configurations or make incremental changes

**Acceptance Criteria**:
- [ ] User can optionally specify a random seed value
- [ ] Same sketch + same seed + same settings produces identical output
- [ ] Generated maps include the seed value used for reproduction
- [ ] Random seed is automatically generated if not provided

---

### [US6] Iterate on Generated Results (Priority: P2)
**As a** user
**I want** to generate multiple variations from the same sketch
**So that** I can explore different interpretations and choose the best one

**Acceptance Criteria**:
- [ ] User can generate multiple outputs from the same sketch without re-uploading
- [ ] Each generation (without seed) produces a unique variation
- [ ] Previous generations are preserved for comparison
- [ ] User can save preferred results

---

### [US7] Preview Color Palette Reference (Priority: P3)
**As a** new user
**I want** to see which colors map to which terrain types
**So that** I know what colors to use in my sketch

**Acceptance Criteria**:
- [ ] Color palette with terrain mappings is clearly displayed
- [ ] Each color shows its hex code and terrain type name
- [ ] Palette includes example images or icons of what each terrain generates
- [ ] Palette is accessible before and during sketch upload

---

### [US8] Handle Invalid or Unexpected Colors (Priority: P3)
**As a** user who accidentally uses off-palette colors
**I want** the tool to handle non-palette colors gracefully
**So that** minor color variations don't break the generation

**Acceptance Criteria**:
- [ ] Colors similar to palette colors are automatically mapped to nearest palette color
- [ ] User receives feedback if sketch contains unexpected colors
- [ ] Color quantization is performed automatically
- [ ] User can see which palette color their sketch colors mapped to

---

### [US9] Export Generated Maps (Priority: P2)
**As a** user
**I want** to export generated maps in various formats and resolutions
**So that** I can use them in different contexts (web, print, game engines)

**Acceptance Criteria**:
- [ ] Maps can be exported as PNG files
- [ ] User can choose output resolution (512x512, 1024x1024, etc.)
- [ ] Exported files have clear, descriptive filenames
- [ ] Export preserves image quality without compression artifacts

---

### [US10] Use Tool via Web Interface (Priority: P1)
**As a** user without technical expertise
**I want** to access the tool through a simple web interface
**So that** I don't need to install software or use command line tools

**Acceptance Criteria**:
- [ ] Web interface is accessible via browser
- [ ] Interface provides image upload functionality
- [ ] Interface shows color palette reference
- [ ] Interface displays generated results
- [ ] Interface allows adjusting generation parameters
- [ ] Interface provides download button for results

---

## Functional Requirements

### Core Requirements
- **FR-001**: System shall accept image files in PNG and JPG formats as sketch input
- **FR-002**: System shall support sketch images up to 1024x1024 pixels
- **FR-003**: System shall recognize and process a predefined color palette of 6-8 terrain types
- **FR-004**: System shall generate output maps that maintain spatial layout of input sketch
- **FR-005**: System shall complete map generation within 60 seconds for 512x512 output on GPU
- **FR-006**: System shall support text prompts to control overall map style and theme
- **FR-007**: System shall automatically infill unconstrained (white) regions with appropriate terrain
- **FR-008**: System shall ensure smooth visual transitions between different terrain types
- **FR-009**: System shall produce deterministic output when provided with a random seed
- **FR-010**: System shall allow generation of multiple variations from the same sketch

### Data Requirements
- **DR-001**: System shall maintain mapping between hex color codes and terrain types
- **DR-002**: System shall validate sketch images meet size and format requirements
- **DR-003**: System shall quantize non-palette colors to nearest palette color
- **DR-004**: Generated images shall be stored in lossless format
- **DR-005**: Generation parameters (seed, prompts, settings) shall be preserved with outputs

### User Interface Requirements
- **UIR-001**: Interface shall display the predefined color palette with terrain type labels
- **UIR-002**: Interface shall provide image upload area supporting drag-and-drop
- **UIR-003**: Interface shall display both input sketch and generated output side-by-side
- **UIR-004**: Interface shall allow adjustment of control strength parameter (0.0 to 1.0)
- **UIR-005**: Interface shall provide text input for style/theme prompts
- **UIR-006**: Interface shall show generation progress indication
- **UIR-007**: Interface shall provide download button for generated maps
- **UIR-008**: Interface shall allow optional random seed input

### Performance Requirements
- **PR-001**: System shall generate 512x512 maps in under 30 seconds on GPU hardware
- **PR-002**: System shall support CPU-based generation with appropriate performance warnings
- **PR-003**: System shall provide fallback behavior if GPU memory is insufficient
- **PR-004**: Interface shall remain responsive during generation process

## Key Entities

### Sketch
**Description**: User-provided image containing color-coded hints for map generation

**Attributes**:
- `image_data` (binary): The actual image file content
- `width` (integer): Width in pixels
- `height` (integer): Height in pixels
- `format` (string): File format (PNG, JPG)
- `upload_timestamp` (datetime): When the sketch was provided

**Relationships**:
- Associated with one or more GeneratedMaps
- Uses one ColorPalette

---

### ColorPalette
**Description**: Mapping between colors and terrain types that defines sketch interpretation

**Attributes**:
- `colors` (list): Collection of color-to-terrain mappings
- `terrain_types` (list): Supported terrain categories
- `default_unconstrained_color` (color): Color representing unmarked regions

**Relationships**:
- Used by Sketches for interpretation
- Defines TerrainTypes

---

### TerrainType
**Description**: A category of terrain or feature that can be generated

**Attributes**:
- `name` (string): Human-readable name (e.g., "Water", "Forest")
- `color` (hex string): Associated color code
- `description` (text): Description of what this terrain represents

**Relationships**:
- Belongs to ColorPalette
- Referenced in GenerationConfig

---

### GenerationConfig
**Description**: Parameters controlling how a map is generated from a sketch

**Attributes**:
- `style_prompt` (text): Description of desired visual style
- `control_strength` (float): How strictly to follow sketch (0.0-1.0)
- `random_seed` (integer, optional): Seed for reproducible generation
- `output_resolution` (dimensions): Desired output size
- `inference_steps` (integer): Quality/speed tradeoff parameter

**Relationships**:
- Applied to Sketch to produce GeneratedMap
- References TerrainTypes

---

### GeneratedMap
**Description**: Output image produced from a sketch and configuration

**Attributes**:
- `image_data` (binary): The generated map image
- `width` (integer): Width in pixels
- `height` (integer): Height in pixels
- `format` (string): Output format (PNG)
- `generation_timestamp` (datetime): When map was generated
- `seed_used` (integer): Random seed used (for reproduction)

**Relationships**:
- Generated from one Sketch
- Created using one GenerationConfig

---

## Success Criteria

### User Experience
- [ ] Users can create a sketch in MS Paint and generate a usable map in under 2 minutes (including upload and generation)
- [ ] 80% of generated maps require no more than 2 regenerations to achieve desired result
- [ ] New users can understand the color palette without external documentation
- [ ] Generated maps are visually coherent and aesthetically pleasing to non-expert viewers

### System Performance
- [ ] 512x512 map generation completes in under 30 seconds on NVIDIA GTX 1660 or equivalent
- [ ] 1024x1024 map generation completes in under 90 seconds on NVIDIA GTX 1660 or equivalent
- [ ] System successfully processes 95% of valid sketch inputs without errors
- [ ] Color quantization correctly maps sketch colors to palette colors with 90% accuracy
- [ ] Web interface loads in under 3 seconds on standard broadband connection

### Output Quality
- [ ] Generated maps respect user-defined terrain boundaries from sketch
- [ ] Water regions appear as water 95% of the time
- [ ] Forest regions appear as vegetation 95% of the time
- [ ] Mountain regions appear as elevated/rocky terrain 95% of the time
- [ ] Transitions between terrains appear natural (no jarring boundaries)
- [ ] Unconstrained regions blend seamlessly with constrained regions
- [ ] Same sketch with same seed produces byte-identical output

## Edge Cases & Error Scenarios

### Edge Cases
1. **Fully white sketch**: Should generate a completely unconstrained map with natural terrain distribution
2. **Single color pixel region**: Should generate terrain type even for very small regions (with diminished influence)
3. **No white regions (fully colored)**: Should respect all color constraints with no infill
4. **Very large contiguous region**: Should maintain terrain consistency across entire region
5. **Checkerboard pattern**: Should handle rapid terrain transitions gracefully
6. **Sketch smaller than output resolution**: Should upscale while maintaining layout
7. **Sketch larger than output resolution**: Should downscale while preserving color information
8. **Identical adjacent colors**: Should generate continuous terrain, not boundaries

### Error Handling
1. **Invalid file format**: Display clear error message specifying supported formats (PNG, JPG)
2. **File too large**: Display error with maximum file size and current file size
3. **Corrupted image file**: Display error indicating file cannot be read
4. **Unsupported dimensions**: Display error with dimension requirements or auto-resize with warning
5. **Generation timeout**: Display timeout message and offer to retry or reduce quality settings
6. **Insufficient memory**: Display error suggesting lower resolution or provide CPU fallback
7. **No colors detected**: Warn user that sketch appears blank and offer to continue with unconstrained generation
8. **Network interruption (web)**: Preserve user inputs and allow resume after reconnection

## Acceptance Scenarios

### Scenario 1: Simple Water and Land Map (Happy Path)
**Given** a user has created a sketch with blue region (water) and green region (land)
**When** they upload the sketch and click "Generate"
**Then** a map is produced showing water in blue areas, vegetation in green areas, with smooth coastlines

### Scenario 2: Sparse Sketch with Mostly Infill
**Given** a user uploads a sketch with only a few small colored regions and mostly white space
**When** generation completes
**Then** the small colored regions show the specified terrain types and white regions are filled with coherent, natural terrain that complements the constrained areas

### Scenario 3: Complex Multi-Terrain Map
**Given** a user uploads a sketch containing all palette colors (water, forest, mountain, desert, grassland, city)
**When** generation completes
**Then** each colored region displays its corresponding terrain type, boundaries between terrains are natural, and overall map is visually coherent

### Scenario 4: Style Variation with Prompts
**Given** a user has uploaded a sketch and entered style prompt "fantasy map, hand-drawn style"
**When** generation completes
**Then** the output has a fantasy aesthetic with artistic, hand-drawn appearance while maintaining terrain type accuracy

### Scenario 5: Reproducible Generation
**Given** a user has generated a map and noted the random seed
**When** they upload the same sketch again with the same seed and settings
**Then** the generated map is identical to the previous generation

### Scenario 6: Multiple Variations
**Given** a user has uploaded a sketch
**When** they click "Generate" multiple times without changing the sketch
**Then** each generation produces a visually distinct variation that respects the sketch constraints

### Scenario 7: Control Strength Adjustment
**Given** a user has a sketch uploaded
**When** they set control strength to maximum (1.0) and generate
**Then** output very precisely follows sketch boundaries
**When** they set control strength to low (0.3) and generate
**Then** output uses sketch as loose inspiration with more creative freedom

### Scenario 8: Color Quantization
**Given** a user uploads a sketch with slightly off-palette colors (e.g., #0033FF instead of pure #0000FF blue)
**When** generation begins
**Then** system automatically maps colors to nearest palette colors and shows user the mapping
**And** generation proceeds with quantized colors

### Scenario 9: Invalid File Format Error
**Given** a user attempts to upload a TIFF or BMP file
**When** they click upload
**Then** system displays error: "Unsupported format. Please use PNG or JPG files."

### Scenario 10: Export at Different Resolutions
**Given** a map has been generated
**When** user selects 1024x1024 resolution and clicks "Download"
**Then** a high-resolution PNG file is downloaded with the map at requested resolution

## Out of Scope

### Excluded from Initial Release
- Custom color palette creation (v1 uses predefined palette only)
- Interactive sketch editing within the tool (users must use external paint tools)
- 3D terrain generation or heightmap export
- Animated or time-lapse map generation
- Multi-page or tiled map generation for very large worlds
- Integration with game engines or external software
- Fine-tuning or training custom models
- Batch processing of multiple sketches simultaneously
- User accounts, authentication, or cloud storage
- Collaborative sketch editing
- Mobile app version (web interface should be mobile-responsive but not a native app)
- Real-time preview during sketching

### Future Considerations
- Custom palette builder for specialized use cases
- Region-specific regeneration (re-generate just one area)
- Terrain continuity for seamless tiling
- Export to specialized formats (game engines, GIS tools)
- API for programmatic access
- Advanced features like roads, rivers, settlements as separate layers
- Style transfer from reference images
- Community gallery for sharing results

## Notes

### Design Philosophy
This tool aims to democratize map creation by providing an intuitive, paint-by-numbers approach to world building. The constrained color palette reduces complexity while the AI infill handles artistic details, allowing users to focus on high-level geography and layout.

### Technical Constraints
- Generation quality depends on availability of GPU acceleration
- Initial model download (5-8GB) required on first use
- Internet connection required for web interface but not for generation itself (if self-hosted)

### Accessibility Considerations
- Color palette should be distinguishable to colorblind users (consider patterns or labels in addition to colors)
- Web interface should support keyboard navigation
- Alternative text for generated images should describe terrain composition

### Privacy & Data
- User sketches and generated maps are not stored long-term unless explicitly saved
- No personal data collection required for core functionality
- Users should have option to clear their session data

---

**Clarifications Needed**: None - Specification is complete and ready for planning phase
