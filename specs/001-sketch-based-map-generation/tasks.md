# Implementation Tasks: Sketch-Based Map Generation

**Feature**: `001-sketch-based-map-generation` | **Status**: Ready for Implementation

---

## Phase 1: Setup & Foundation

### Environment Setup
- [ ] [T001] Create project directory structure (src/sketchmap/, tests/, examples/, docs/)
- [ ] [T002] Initialize pyproject.toml with project metadata and dependencies
- [ ] [T003] Configure development tools (pytest, mypy, ruff, black) in pyproject.toml
- [ ] [T004] Create requirements.txt with pinned dependency versions
- [ ] [T005] Create .gitignore for Python, models, and generated outputs
- [ ] [T006] [P] Create README.md with project overview and installation instructions
- [ ] [T007] [P] Create docs/palette_guide.md documenting color-to-terrain mappings

### Core Data Models - Testing First
- [ ] [T008] Create tests/test_palette.py with test cases for ColorPalette class
- [ ] [T009] Create src/sketchmap/palette.py with TerrainType enum and ColorPalette class
- [ ] [T010] Implement ColorPalette.quantize_color() method with RGB distance calculation
- [ ] [T011] Implement ColorPalette.get_terrain_type() method
- [ ] [T012] Verify all tests/test_palette.py tests pass

- [ ] [T013] Create tests/test_config.py with test cases for GenerationConfig validation
- [ ] [T014] Create src/sketchmap/config.py with GenerationConfig dataclass
- [ ] [T015] Implement GenerationConfig.validate() method
- [ ] [T016] Verify all tests/test_config.py tests pass

- [ ] [T017] Create tests/test_sketch.py with test cases for SketchInput class
- [ ] [T018] Create src/sketchmap/sketch.py with SketchInput class
- [ ] [T019] [US1] Implement SketchInput.__init__() with image loading and validation (PNG/JPG)
- [ ] [T020] Implement SketchInput.extract_scribble() using Canny edge detection in src/sketchmap/preprocessing.py
- [ ] [T021] Verify all tests/test_sketch.py tests pass

---

## Phase 2: Single ControlNet Pipeline

### Generator Setup - Testing First
- [ ] [T022] Create tests/test_generator.py with test cases for MapGenerator initialization
- [ ] [T023] Create src/sketchmap/generator.py with MapGenerator class
- [ ] [T024] [US1] Implement MapGenerator.__init__() to load Stable Diffusion 1.5 and ControlNet Scribble
- [ ] [T025] Implement MapGenerator._build_prompt() to combine base and terrain prompts
- [ ] [T026] [US1] Implement MapGenerator.generate() for single-ControlNet generation
- [ ] [T027] Verify basic generation tests pass in tests/test_generator.py

### Integration Testing
- [ ] [T028] Create tests/integration/test_end_to_end.py for full pipeline tests
- [ ] [T029] [US1] Add end-to-end test: load sketch → generate map → verify output format
- [ ] [T030] Add test for reproducibility: same seed produces identical output
- [ ] [T031] Create tests/fixtures/sample_sketches/ with simple test sketches
- [ ] [T032] Verify all integration tests pass

### CLI Tool
- [ ] [T033] Create src/sketchmap/cli.py with argparse setup
- [ ] [T034] [US1] Implement CLI command: load sketch, run generation, save output
- [ ] [T035] [US5] Add --seed parameter for reproducible generation
- [ ] [T036] [US3] Add --prompt parameter for style control
- [ ] [T037] [P] Add --output parameter for specifying output path
- [ ] [T038] [P] Test CLI with example sketches

---

## Phase 3: Multi-ControlNet & Color Palette

### Color Segmentation - Testing First
- [ ] [T039] Add test cases to tests/test_sketch.py for segmentation map extraction
- [ ] [T040] [US1] Implement SketchInput.extract_segmentation_map() in src/sketchmap/sketch.py
- [ ] [T041] Add integration test for color quantization accuracy in tests/integration/test_palette_mapping.py
- [ ] [T042] Verify segmentation tests pass

### Multi-ControlNet Pipeline
- [ ] [T043] Add test cases to tests/test_generator.py for multi-ControlNet setup
- [ ] [T044] [US1] Update MapGenerator to load ControlNet Seg model (lllyasviel/control_v11p_sd15_seg)
- [ ] [T045] [US1] Update MapGenerator to initialize multi-ControlNet pipeline
- [ ] [T046] [US4] Update GenerationConfig to include controlnet_scribble_weight and controlnet_seg_weight
- [ ] [T047] [US1] Update MapGenerator.generate() to use both scribble and segmentation maps
- [ ] [T048] Update MapGenerator._build_prompt() to include terrain-specific prompts
- [ ] [T049] Verify multi-ControlNet tests pass

### Terrain Type Testing
- [ ] [T050] Create tests/integration/test_terrain_accuracy.py
- [ ] [T051] [US1] Add test: blue regions generate water (verify with image analysis)
- [ ] [T052] [US1] Add test: green regions generate vegetation
- [ ] [T053] [US1] Add test: brown regions generate mountains
- [ ] [T054] [P] Create examples/simple_water.png test sketch
- [ ] [T055] [P] Create examples/forest_mountain.png test sketch
- [ ] [T056] [P] Create examples/complex_world.png test sketch
- [ ] [T057] Verify terrain accuracy meets 95% success criteria

---

## Phase 4: Unconstrained Region Handling

### Mask Extraction - Testing First
- [ ] [T058] Add test cases to tests/test_sketch.py for unconstrained mask extraction
- [ ] [T059] [US2] Implement SketchInput.extract_unconstrained_mask() in src/sketchmap/sketch.py
- [ ] [T060] [US2] Add method to identify white/unmarked regions
- [ ] [T061] Verify mask extraction tests pass

### Infill Strategy
- [ ] [T062] Create tests/integration/test_infill.py for unconstrained region tests
- [ ] [T063] [US2] Research and document infill approach (lower conditioning weight vs inpainting)
- [ ] [T064] [US2] Implement chosen infill strategy in MapGenerator.generate()
- [ ] [T065] [US2] Add GenerationConfig parameter for infill creativity control
- [ ] [T066] [US2] Test fully white sketch generates coherent unconstrained map
- [ ] [T067] [US2] Test sparse sketch with smooth blending between constrained/unconstrained
- [ ] [T068] Verify all infill tests pass

---

## Phase 5: Web Interface (Gradio)

### UI Foundation
- [ ] [T069] Create src/sketchmap/ui.py with Gradio app setup
- [ ] [T070] [US10] Implement image upload component with drag-and-drop support
- [ ] [T071] [US7] Create color palette reference display component
- [ ] [T072] [US10] [US3] Add text input for style/theme prompt
- [ ] [T073] [US4] Add slider for control strength parameter (0.0-1.0)
- [ ] [T074] [US5] Add optional seed input field
- [ ] [T075] [US9] Add output resolution selector (512x512, 1024x1024)

### UI Generation & Display
- [ ] [T076] [US10] Implement generation button and progress indicator
- [ ] [T077] [US10] Create side-by-side display for input sketch and generated output
- [ ] [T078] [US9] Add download button for generated maps (PNG export)
- [ ] [T079] [US6] Implement result gallery to preserve previous generations
- [ ] [T080] [US6] Add "Generate Variation" button for multiple outputs from same sketch
- [ ] [T081] Test web interface end-to-end workflow

---

## Phase 6: Error Handling & Robustness

### Input Validation
- [ ] [T082] [US8] Add color validation and quantization warning in SketchInput
- [ ] [T083] [US8] Implement color mapping feedback display in UI
- [ ] [T084] Add file format validation with clear error messages in src/sketchmap/sketch.py
- [ ] [T085] Add file size validation (max 10MB) with error messages
- [ ] [T086] Add dimension validation (max 1024x1024, divisible by 8)
- [ ] [T087] Create tests/test_validation.py for all validation scenarios

### Resource Management
- [ ] [T088] Implement GPU/CPU detection in src/sketchmap/generator.py
- [ ] [T089] Add CPU fallback mode with performance warning
- [ ] [T090] Add memory check and error handling for insufficient GPU memory
- [ ] [T091] Implement timeout handling (60s max) with user feedback
- [ ] [T092] Test error handling with invalid inputs (corrupted files, wrong formats)

---

## Phase 7: Performance Optimization

### Model Optimization
- [ ] [T093] Enable fp16 quantization in MapGenerator pipeline initialization
- [ ] [T094] Implement model caching to avoid re-loading on each generation
- [ ] [T095] Add torch.compile() for faster inference (if compatible)
- [ ] [T096] Create benchmarking script in tests/benchmark_performance.py
- [ ] [T097] Verify 512x512 generation completes in <30s on GPU (GTX 1660 equivalent)
- [ ] [T098] Verify 1024x1024 generation completes in <90s on GPU

### Output Quality
- [ ] [T099] Test and tune default generation parameters (inference steps, guidance scale)
- [ ] [T100] Test and tune ControlNet conditioning weights for best results
- [ ] [T101] Verify smooth transitions between terrain types in generated maps
- [ ] [T102] Create visual quality checklist for manual validation

---

## Phase 8: Documentation & Polish

### User Documentation
- [ ] [T103] [P] Create docs/usage.md with complete user guide
- [ ] [T104] [P] Create docs/tutorial.md with step-by-step walkthrough
- [ ] [T105] [P] Update README.md with installation, quickstart, and examples
- [ ] [T106] [P] Add example outputs to examples/ directory with descriptions

### Developer Documentation
- [ ] [T107] [P] Create docs/architecture.md documenting technical design
- [ ] [T108] [P] Add comprehensive docstrings to all public classes and methods
- [ ] [T109] [P] Document GPU requirements and troubleshooting in README.md
- [ ] [T110] [P] Create CONTRIBUTING.md with development setup instructions

### Final Quality Gates
- [ ] [T111] Run full test suite and verify 80%+ coverage
- [ ] [T112] Run mypy type checking in strict mode, verify no errors
- [ ] [T113] Run ruff linting, verify no violations
- [ ] [T114] Run black formatting, verify all files formatted
- [ ] [T115] Manual testing of all user stories against acceptance criteria
- [ ] [T116] Create CHANGELOG.md documenting v1.0.0 features
- [ ] [T117] Tag release v1.0.0 and create release notes

---

## Summary

**Total Tasks**: 117
**Estimated Phases**: 8
**Status**: Ready for implementation

### Phase Breakdown
- Phase 1 (Setup & Foundation): T001-T021 (21 tasks)
- Phase 2 (Single ControlNet): T022-T038 (17 tasks)
- Phase 3 (Multi-ControlNet): T039-T057 (19 tasks)
- Phase 4 (Infill Handling): T058-T068 (11 tasks)
- Phase 5 (Web Interface): T069-T081 (13 tasks)
- Phase 6 (Error Handling): T082-T092 (11 tasks)
- Phase 7 (Performance): T093-T102 (10 tasks)
- Phase 8 (Documentation): T103-T117 (15 tasks)

### Parallelization Opportunities
Tasks marked with [P] can be executed in parallel with adjacent tasks in the same phase.

### Testing Strategy
- Tests written BEFORE implementation (TDD approach)
- Unit tests for all data models
- Integration tests for pipeline components
- End-to-end tests for complete workflows
- Manual validation for visual quality

### Success Criteria Alignment
All tasks map to acceptance criteria in spec.md and align with constitutional principles:
- ✅ Test-driven development
- ✅ Type safety (mypy strict mode)
- ✅ Modularity and clear separation
- ✅ Documentation requirements
- ✅ Performance targets
