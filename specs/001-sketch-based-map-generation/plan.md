# Implementation Plan: Sketch-Based Map Generation

**Feature**: `001-sketch-based-map-generation` | **Created**: 2026-01-03 | **Status**: Draft

## Technical Context

### Tech Stack
- **Language**: Python 3.11+
- **Framework**: Gradio (for web UI), or CLI-based tool
- **Core Libraries**:
  - `diffusers` (Hugging Face) - Stable Diffusion pipelines
  - `transformers` - Model loading and management
  - `torch` (PyTorch) - Deep learning backend
  - `controlnet-aux` - Preprocessing for ControlNet
  - `opencv-python` - Image processing
  - `pillow` - Image I/O
  - `numpy` - Array operations
- **Testing**: pytest, mypy, ruff
- **Model Backend**: Stable Diffusion 1.5 or SDXL with ControlNet

### Architecture Decisions

#### Decision 1: Multi-ControlNet Approach
**Chosen**: Stable Diffusion + ControlNet Scribble + ControlNet Semantic Segmentation
**Rationale**:
- Combines structural sketch control (scribble) with semantic color hints (segmentation)
- Both ControlNets are well-documented and have pretrained models available
- Proven composability - multiple ControlNets work together effectively
- Provides maximum flexibility for user input

**Alternatives Considered**:
- **T2I-Adapter**: More lightweight (5-18M params vs 77M) with explicit color palette support, but less mature ecosystem and fewer pretrained models
- **Single ControlNet (Seg only)**: Simpler but loses sketch structure control, requires precise segmentation maps
- **Regional Prompting + Inpainting**: More complex preprocessing, harder to maintain global coherence

**Tradeoffs**:
- ✅ Maximum control and flexibility
- ✅ Strong community support and pretrained models
- ❌ Higher computational cost (2 ControlNets)
- ❌ More complex pipeline to implement

#### Decision 2: Phased Implementation Strategy
**Chosen**: Start with single ControlNet, progressively add capabilities
**Rationale**:
- Validates core functionality early
- Reduces initial complexity
- Allows learning and iteration
- Each phase delivers usable feature

**Phase Breakdown**:
1. **Phase 1**: Single ControlNet (Scribble OR Seg) - Basic sketch-to-map
2. **Phase 2**: Multi-ControlNet composition - Add color palette hints
3. **Phase 3**: Unconstrained region handling - Infill unmarked areas
4. **Phase 4**: Polish and optimization - Performance, UX, refinement

#### Decision 3: Color Palette Design
**Chosen**: 6-8 predefined terrain colors with configurable mappings
**Rationale**:
- Small palette is easy for users to remember and use in paint tools
- High contrast colors are easier for model to distinguish
- Predefined mappings ensure consistent results
- Allows future expansion for custom palettes

**Tradeoffs**:
- ✅ Simple user experience
- ✅ Consistent, predictable results
- ❌ Less flexibility than freeform prompting
- ❌ Requires upfront palette design

### Dependencies

**Core**:
- `diffusers>=0.25.0` - Hugging Face diffusion models
- `transformers>=4.36.0` - Model infrastructure
- `torch>=2.1.0` - PyTorch deep learning
- `controlnet-aux>=0.0.7` - ControlNet preprocessing utilities
- `accelerate>=0.25.0` - Model optimization and multi-GPU

**Image Processing**:
- `opencv-python>=4.8.0` - Edge detection, image manipulation
- `pillow>=10.0.0` - Image I/O
- `numpy>=1.24.0` - Array operations
- `scipy>=1.11.0` - Scientific computing

**Optional (Web UI)**:
- `gradio>=4.0.0` - Web interface for interactive use
- `fastapi>=0.104.0` - API backend (if building service)

**Development**:
- `pytest>=7.4.0` - Testing
- `mypy>=1.7.0` - Type checking
- `ruff>=0.1.0` - Linting
- `black>=23.0.0` - Code formatting

---

## Data Model Design

### Entities

#### ColorPalette
```python
from enum import Enum
from typing import Dict

class TerrainType(Enum):
    """Enumeration of supported terrain types."""

    WATER = "water"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    DESERT = "desert"
    GRASSLAND = "grassland"
    CITY = "city"
    UNCONSTRAINED = "unconstrained"


class ColorPalette:
    """Defines the color-to-terrain mapping for sketch input."""

    color_map: Dict[str, TerrainType]  # Hex color -> terrain type
    terrain_prompts: Dict[TerrainType, str]  # Terrain -> descriptive prompt

    def __init__(self):
        self.color_map = {
            "#0000FF": TerrainType.WATER,
            "#00FF00": TerrainType.FOREST,
            "#8B4513": TerrainType.MOUNTAIN,
            "#FFFF00": TerrainType.DESERT,
            "#90EE90": TerrainType.GRASSLAND,
            "#808080": TerrainType.CITY,
            "#FFFFFF": TerrainType.UNCONSTRAINED,
        }

        self.terrain_prompts = {
            TerrainType.WATER: "clear blue water, rivers, lakes, ocean",
            TerrainType.FOREST: "dense forest, lush vegetation, trees",
            TerrainType.MOUNTAIN: "mountains, rocky peaks, highlands",
            TerrainType.DESERT: "desert, sand dunes, arid landscape",
            TerrainType.GRASSLAND: "grassland, plains, meadows",
            TerrainType.CITY: "settlements, towns, urban areas",
            TerrainType.UNCONSTRAINED: "natural terrain",
        }

    def quantize_color(self, rgb: tuple[int, int, int]) -> str:
        """Find nearest palette color to given RGB."""
        # Implementation: Euclidean distance in RGB space
        ...

    def get_terrain_type(self, color_hex: str) -> TerrainType:
        """Get terrain type for a palette color."""
        return self.color_map.get(color_hex, TerrainType.UNCONSTRAINED)
```

**Validation Rules**:
- Colors must be unique in palette
- Each terrain type must have associated prompt
- Hex colors must be valid 6-character format

---

#### SketchInput
```python
from PIL import Image
import numpy as np

class SketchInput:
    """User-provided sketch image with color hints."""

    image: Image.Image  # Original sketch from user
    width: int  # Image width
    height: int  # Image height
    palette: ColorPalette  # Associated color palette

    def __init__(self, image_path: str, palette: ColorPalette):
        self.image = Image.open(image_path).convert("RGB")
        self.width, self.height = self.image.size
        self.palette = palette

    def extract_scribble(self) -> np.ndarray:
        """Extract edge/scribble map for ControlNet Scribble."""
        # Use Canny edge detection or similar
        ...

    def extract_segmentation_map(self) -> np.ndarray:
        """Create segmentation map from color palette."""
        # Quantize colors and map to class IDs
        ...

    def extract_unconstrained_mask(self) -> np.ndarray:
        """Create mask for unconstrained regions (white areas)."""
        # Identify pixels matching UNCONSTRAINED color
        ...
```

**Validation Rules**:
- Image must be RGB format
- Dimensions must be divisible by 8 (SD requirement)
- Maximum size: 1024x1024 (adjustable)

---

#### GenerationConfig
```python
from dataclasses import dataclass

@dataclass
class GenerationConfig:
    """Configuration for map generation process."""

    # Base settings
    prompt: str  # Overall style/theme prompt
    negative_prompt: str  # Things to avoid
    num_inference_steps: int = 30  # Sampling steps (20-50)
    guidance_scale: float = 7.5  # Prompt adherence (7-12)
    seed: int | None = None  # Random seed for reproducibility

    # ControlNet settings
    controlnet_scribble_weight: float = 0.8  # Scribble influence (0-1)
    controlnet_seg_weight: float = 0.7  # Segmentation influence (0-1)

    # Output settings
    output_resolution: tuple[int, int] = (512, 512)  # Output size

    def validate(self) -> bool:
        """Validate configuration parameters."""
        assert 1 <= self.num_inference_steps <= 100
        assert 1.0 <= self.guidance_scale <= 20.0
        assert 0.0 <= self.controlnet_scribble_weight <= 1.0
        assert 0.0 <= self.controlnet_seg_weight <= 1.0
        return True
```

---

#### MapGenerator
```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch

class MapGenerator:
    """Main map generation engine using Stable Diffusion + ControlNets."""

    pipeline: StableDiffusionControlNetPipeline
    controlnet_scribble: ControlNetModel
    controlnet_seg: ControlNetModel
    device: str  # "cuda" or "cpu"

    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5"):
        """Initialize pipeline with pretrained models."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load ControlNet models
        self.controlnet_scribble = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11p_sd15_scribble"
        )
        self.controlnet_seg = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11p_sd15_seg"
        )

        # Create multi-ControlNet pipeline
        self.pipeline = StableDiffusionControlNetPipeline.from_pretrained(
            model_id,
            controlnet=[self.controlnet_scribble, self.controlnet_seg],
            torch_dtype=torch.float16,
        ).to(self.device)

    def generate(
        self,
        sketch: SketchInput,
        config: GenerationConfig,
    ) -> Image.Image:
        """Generate map from sketch input."""
        # Extract control images
        scribble_map = sketch.extract_scribble()
        seg_map = sketch.extract_segmentation_map()

        # Build prompt from palette and config
        full_prompt = self._build_prompt(sketch, config)

        # Run generation
        result = self.pipeline(
            prompt=full_prompt,
            negative_prompt=config.negative_prompt,
            image=[scribble_map, seg_map],
            num_inference_steps=config.num_inference_steps,
            guidance_scale=config.guidance_scale,
            controlnet_conditioning_scale=[
                config.controlnet_scribble_weight,
                config.controlnet_seg_weight,
            ],
            generator=torch.manual_seed(config.seed) if config.seed else None,
        )

        return result.images[0]

    def _build_prompt(self, sketch: SketchInput, config: GenerationConfig) -> str:
        """Combine base prompt with terrain-specific prompts."""
        # Start with base prompt
        prompt = config.prompt

        # Add terrain type descriptions
        terrain_types = sketch.get_present_terrains()
        for terrain in terrain_types:
            terrain_prompt = sketch.palette.terrain_prompts[terrain]
            prompt += f", {terrain_prompt}"

        return prompt
```

---

### Relationships
- `SketchInput` → `ColorPalette`: Each sketch uses one palette (1:1)
- `GenerationConfig` → `MapGenerator`: Config consumed by generator (N:1)
- `MapGenerator` → `ControlNetModel`: Generator uses multiple ControlNets (1:N)

---

## Implementation Phases

### Phase 1: Foundation & Single ControlNet
**Goal**: Basic sketch-to-map generation with single control method

**Tasks**:
1. Set up project structure and dependencies
2. Implement `ColorPalette` class with default terrain mapping
3. Implement `SketchInput` class with image loading
4. Implement edge extraction (Canny) for scribble control
5. Create `MapGenerator` with single ControlNet (Scribble)
6. Implement basic `GenerationConfig`
7. Create CLI tool for testing
8. Write unit tests for data models

**Deliverables**:
- [ ] Project structure in place
- [ ] Dependencies installed and working
- [ ] Can load sketch image
- [ ] Can extract scribble/edge map
- [ ] Single ControlNet generation works
- [ ] CLI tool functional
- [ ] Tests passing

**Success Criteria**:
- Given a simple black-and-white sketch, generate a coherent map
- Output respects major structural boundaries from sketch
- Generation completes in <30 seconds on GPU

---

### Phase 2: Multi-ControlNet & Color Palette
**Goal**: Add semantic color conditioning for terrain hints

**Tasks**:
1. Implement color quantization in `ColorPalette`
2. Implement segmentation map extraction in `SketchInput`
3. Add ControlNet Seg model to `MapGenerator`
4. Implement multi-ControlNet pipeline
5. Create terrain-specific prompt building
6. Add conditioning weight controls to config
7. Test with colored sketches
8. Write integration tests

**Deliverables**:
- [ ] Color palette mapping works
- [ ] Segmentation map correctly identifies terrains
- [ ] Multi-ControlNet pipeline functional
- [ ] Color hints influence generation appropriately
- [ ] Prompt building incorporates terrain types
- [ ] Integration tests passing

**Success Criteria**:
- Blue regions generate as water
- Green regions generate as forests
- Brown regions generate as mountains
- Color hints are respected but not overly rigid
- Smooth transitions between terrain types

---

### Phase 3: Unconstrained Region Handling
**Goal**: Seamlessly infill unmarked areas while respecting constraints

**Tasks**:
1. Implement unconstrained mask extraction
2. Research and test infill strategies:
   - Lower conditioning weight for white regions
   - Inpainting pipeline for unmarked areas
   - Region-aware diffusion if needed
3. Implement chosen approach
4. Test blending between constrained and unconstrained
5. Add user controls for infill creativity
6. Write tests for mask generation

**Deliverables**:
- [ ] Unconstrained regions identified correctly
- [ ] Infill generates coherent, natural terrain
- [ ] Smooth transitions at boundaries
- [ ] User can control infill style
- [ ] Tests cover edge cases

**Success Criteria**:
- White/unmarked regions generate plausible terrain
- No jarring transitions between constrained/unconstrained
- Infill respects global map coherence
- User has control over infill creativity level

---

### Phase 4: Polish, Optimization & UX
**Goal**: Production-ready tool with good performance and user experience

**Tasks**:
1. Performance optimization:
   - Model quantization (fp16)
   - Batch processing if applicable
   - Caching preprocessed models
2. Add Gradio web UI:
   - Canvas for sketching or upload
   - Color palette selector
   - Generation parameter sliders
   - Result gallery
3. Implement export options (PNG, high-res)
4. Add example sketches and presets
5. Write comprehensive documentation
6. Create tutorial/guide
7. Performance benchmarking
8. Final testing and bug fixes

**Deliverables**:
- [ ] Optimized inference performance
- [ ] Web UI functional and intuitive
- [ ] Export works correctly
- [ ] Example gallery available
- [ ] Documentation complete
- [ ] Tutorial written
- [ ] All quality gates passing

**Success Criteria**:
- Generation time <20 seconds on GPU, <2 min on CPU
- Web UI is responsive and easy to use
- Users can sketch → generate → export workflow smoothly
- Documentation covers all features
- Code quality meets constitutional standards

---

## Testing Strategy

### Unit Tests
**Scope**: Individual classes and functions
**Framework**: pytest
**Coverage Target**: 80% minimum

**Key Test Cases**:
- `ColorPalette`:
  - Color quantization accuracy
  - Terrain type lookup
  - Invalid color handling
- `SketchInput`:
  - Image loading from various formats
  - Edge extraction produces valid maps
  - Segmentation map class assignment
  - Unconstrained mask generation
- `GenerationConfig`:
  - Parameter validation
  - Invalid values rejected
  - Default values correct

---

### Integration Tests
**Scope**: Component interactions, end-to-end generation
**Approach**: Test full pipeline with sample sketches

**Key Test Cases**:
- **End-to-End Generation**:
  - Load sketch → process → generate → output image
  - Verify output dimensions match config
  - Verify output is valid image
- **Multi-ControlNet Composition**:
  - Both ControlNets receive correct inputs
  - Conditioning weights applied correctly
  - No conflicts between conditions
- **Palette Consistency**:
  - Same sketch + same seed = same output
  - Different colors produce different terrains

---

### Manual Testing / Validation
**Scope**: Visual quality, user experience
**Approach**: Human evaluation with diverse sketches

**Test Scenarios**:
1. Simple sketch: Just blue water blob
2. Complex sketch: Multiple terrain types with boundaries
3. Sparse sketch: Few colored regions, mostly unconstrained
4. Dense sketch: Fully colored, no infill needed
5. Edge cases: Single pixel regions, very large regions

**Quality Criteria**:
- Visual coherence and realism
- Terrain types match colors
- Smooth transitions
- No obvious artifacts or glitches

---

## Quality Gates

### Pre-Commit
- [ ] All tests pass (`pytest`)
- [ ] Type checking passes (`mypy src/ --strict`)
- [ ] Linting passes (`ruff check src/ tests/`)
- [ ] Code formatted (`black src/ tests/`)
- [ ] Test coverage ≥ 80%
- [ ] No security vulnerabilities

### Pre-Merge
- [ ] Code reviewed
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Documentation updated
- [ ] Performance benchmarks met:
  - GPU: <30s for 512x512 generation
  - CPU: <3min for 512x512 generation
- [ ] Example outputs validated

---

## File Structure

```
src/
  sketchmap/
    __init__.py
    palette.py          # ColorPalette, TerrainType
    sketch.py           # SketchInput processing
    generator.py        # MapGenerator, pipeline
    config.py           # GenerationConfig
    preprocessing.py    # Image preprocessing utilities
    cli.py              # Command-line interface
    ui.py               # Gradio web interface (Phase 4)

tests/
  test_palette.py       # ColorPalette tests
  test_sketch.py        # SketchInput tests
  test_generator.py     # MapGenerator tests
  test_config.py        # Config validation tests
  integration/
    test_end_to_end.py  # Full pipeline tests
    test_multi_control.py  # Multi-ControlNet tests
  fixtures/
    sample_sketches/    # Test input images
    expected_outputs/   # Reference outputs

examples/
  simple_water.png      # Example sketch files
  forest_mountain.png
  complex_world.png

docs/
  usage.md              # User guide
  tutorial.md           # Step-by-step tutorial
  architecture.md       # Technical architecture
  palette_guide.md      # Color palette reference
```

---

## Constitutional Alignment

**Simplicity**:
- Clear separation of concerns (palette, sketch, generator)
- Minimal abstractions - each class has single responsibility
- Direct, readable code over clever optimization

**TDD**:
- Write tests before implementation for each phase
- Unit tests for all data models
- Integration tests for pipeline
- Manual validation for visual quality

**Type Safety**:
- Full type hints on all functions and classes
- Mypy strict mode enabled
- Explicit type enums for terrain types
- No `Any` types without justification

**Modularity**:
- `palette` module independent of generation
- `sketch` module handles all preprocessing
- `generator` module isolates diffusion logic
- Each can be tested and modified independently

**Documentation**:
- Docstrings on all public classes and methods
- Type hints serve as inline documentation
- Comprehensive user guide and tutorial
- Architecture document for developers

---

## Risks & Mitigation

### Risk 1: ControlNet Composition Conflicts
**Impact**: High
**Description**: Multiple ControlNets may conflict, producing incoherent outputs
**Mitigation**:
- Extensive testing with weight combinations
- Allow user to adjust conditioning weights
- Fallback to single ControlNet mode if needed
- Phase 1 validates single-ControlNet works first

### Risk 2: Model Download Size & Bandwidth
**Impact**: Medium
**Description**: Stable Diffusion + 2 ControlNets = ~8GB of models to download
**Mitigation**:
- Use fp16 quantization (halves size)
- Provide model caching instructions
- Document bandwidth/storage requirements upfront
- Consider offering lightweight model option (SD 1.4 vs SDXL)

### Risk 3: Poor Infill Quality in Unconstrained Regions
**Impact**: Medium
**Description**: Unconstrained areas may not blend well or look coherent
**Mitigation**:
- Research multiple infill strategies in Phase 3
- Allow user control over infill creativity
- Default prompts guide toward coherent terrain
- Provide examples of good sketch practices

### Risk 4: GPU Memory Constraints
**Impact**: Medium
**Description**: Multi-ControlNet + high resolution may exceed GPU memory
**Mitigation**:
- Start with 512x512 resolution
- Implement tiling for larger outputs
- Provide CPU fallback (with warning about speed)
- Document GPU requirements clearly

### Risk 5: Color Palette Ambiguity
**Impact**: Low
**Description**: Users may use colors not in palette, causing confusion
**Mitigation**:
- Color quantization maps similar colors to nearest palette color
- Provide visual palette reference in UI
- Show warning if sketch contains unexpected colors
- Palette validator in CLI mode

---

## Notes

### Model Selection Considerations
- **SD 1.5**: Most ControlNet models available, faster, smaller
- **SD 2.1**: Better quality, fewer ControlNet models
- **SDXL**: Best quality, much larger, slower, fewer ControlNets
- **Recommendation**: Start with SD 1.5 for compatibility and speed

### Future Enhancements (Out of Scope for v1)
- Custom palette creation UI
- Fine-tuned map generation model
- Tiling support for seamless large worlds
- Interactive refinement (re-generate specific regions)
- Style transfer (realistic, fantasy, satellite, etc.)
- Export to game engine formats
- 3D terrain generation from 2D map

### Research References
See `prior-work.md` for comprehensive literature review and technical background.

---

**Ready for Task Generation**: Yes - Plan is complete and ready for task breakdown
