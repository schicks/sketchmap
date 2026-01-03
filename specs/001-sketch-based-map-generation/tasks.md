# Implementation Tasks: Sketch-Based Map Generation

**Feature**: `001-sketch-based-map-generation` | **Status**: Ready for Implementation

---

## Phase 1: Setup & Foundation

### Environment Setup
- [X] [T001] Create project directory structure (src/sketchmap/, tests/, examples/, docs/)
- [X] [T002] Initialize pyproject.toml with project metadata and dependencies
- [X] [T003] Configure development tools (pytest, mypy, ruff, black) in pyproject.toml
- [X] [T004] Create .gitignore for Python, models, and generated outputs
- [X] [T005] [P] Create README.md with project overview and installation instructions
- [X] [T006] [P] Create docs/palette_guide.md documenting color-to-terrain mappings

### Core Data Models - Testing First
- [X] [T007] Create tests/test_palette.py with test cases for ColorPalette class
- [X] [T008] Create src/sketchmap/palette.py with TerrainType enum and ColorPalette class
- [X] [T009] Implement ColorPalette.quantize_color() method with RGB distance calculation
- [X] [T010] Implement ColorPalette.get_terrain_type() method
- [X] [T011] Verify all tests/test_palette.py tests pass

- [X] [T012] Create tests/test_config.py with test cases for GenerationConfig validation
- [X] [T013] Create src/sketchmap/config.py with GenerationConfig dataclass
- [X] [T014] Implement GenerationConfig.validate() method
- [X] [T015] Verify all tests/test_config.py tests pass

- [ ] [T016] Create tests/test_sketch.py with test cases for SketchInput class
- [ ] [T017] Create src/sketchmap/sketch.py with SketchInput class
- [ ] [T018] [US1] Implement SketchInput.__init__() with image loading and validation (PNG/JPG)
- [ ] [T019] Implement SketchInput.extract_scribble() using Canny edge detection in src/sketchmap/preprocessing.py
- [ ] [T020] Verify all tests/test_sketch.py tests pass

---

## Phase 2: Single ControlNet Pipeline

### Generator Setup - Testing First
- [ ] [T021] Create tests/test_generator.py with test cases for MapGenerator initialization
- [ ] [T022] Create src/sketchmap/generator.py with MapGenerator class
- [ ] [T023] [US1] Implement MapGenerator.__init__() to load Stable Diffusion 1.5 and ControlNet Scribble
- [ ] [T024] Implement MapGenerator._build_prompt() to combine base and terrain prompts
- [ ] [T025] [US1] Implement MapGenerator.generate() for single-ControlNet generation
- [ ] [T026] Verify basic generation tests pass in tests/test_generator.py

### Integration Testing
- [ ] [T027] Create tests/integration/test_end_to_end.py for full pipeline tests
- [ ] [T028] [US1] Add end-to-end test: load sketch → generate map → verify output format
- [ ] [T029] Add test for reproducibility: same seed produces identical output
- [ ] [T030] Create tests/fixtures/sample_sketches/ with simple test sketches
- [ ] [T031] Verify all integration tests pass

### CLI Tool
- [ ] [T032] Create src/sketchmap/cli.py with argparse setup
- [ ] [T033] [US1] Implement CLI command: load sketch, run generation, save output
- [ ] [T034] [US5] Add --seed parameter for reproducible generation
- [ ] [T035] [US3] Add --prompt parameter for style control
- [ ] [T036] [P] Add --output parameter for specifying output path
- [ ] [T037] [P] Test CLI with example sketches

---

## Phase 3: Multi-ControlNet & Color Palette

### Color Segmentation - Testing First
- [ ] [T038] Add test cases to tests/test_sketch.py for segmentation map extraction
- [ ] [T039] [US1] Implement SketchInput.extract_segmentation_map() in src/sketchmap/sketch.py
- [ ] [T040] Add integration test for color quantization accuracy in tests/integration/test_palette_mapping.py
- [ ] [T041] Verify segmentation tests pass

### Multi-ControlNet Pipeline
- [ ] [T042] Add test cases to tests/test_generator.py for multi-ControlNet setup
- [ ] [T043] [US1] Update MapGenerator to load ControlNet Seg model (lllyasviel/control_v11p_sd15_seg)
- [ ] [T044] [US1] Update MapGenerator to initialize multi-ControlNet pipeline
- [ ] [T045] [US4] Update GenerationConfig to include controlnet_scribble_weight and controlnet_seg_weight
- [ ] [T046] [US1] Update MapGenerator.generate() to use both scribble and segmentation maps
- [ ] [T047] Update MapGenerator._build_prompt() to include terrain-specific prompts
- [ ] [T048] Verify multi-ControlNet tests pass

### Terrain Type Testing
- [ ] [T049] Create tests/integration/test_terrain_accuracy.py
- [ ] [T050] [US1] Add test: blue regions generate water (verify with image analysis)
- [ ] [T051] [US1] Add test: green regions generate vegetation
- [ ] [T052] [US1] Add test: brown regions generate mountains
- [ ] [T053] [P] Create examples/simple_water.png test sketch
- [ ] [T054] [P] Create examples/forest_mountain.png test sketch
- [ ] [T055] [P] Create examples/complex_world.png test sketch
- [ ] [T056] Verify terrain accuracy meets 95% success criteria

---

## Phase 4: Unconstrained Region Handling

### Mask Extraction - Testing First
- [ ] [T057] Add test cases to tests/test_sketch.py for unconstrained mask extraction
- [ ] [T058] [US2] Implement SketchInput.extract_unconstrained_mask() in src/sketchmap/sketch.py
- [ ] [T059] [US2] Add method to identify white/unmarked regions
- [ ] [T060] Verify mask extraction tests pass

### Infill Strategy
- [ ] [T061] Create tests/integration/test_infill.py for unconstrained region tests
- [ ] [T062] [US2] Research and document infill approach (lower conditioning weight vs inpainting)
- [ ] [T063] [US2] Implement chosen infill strategy in MapGenerator.generate()
- [ ] [T064] [US2] Add GenerationConfig parameter for infill creativity control
- [ ] [T065] [US2] Test fully white sketch generates coherent unconstrained map
- [ ] [T066] [US2] Test sparse sketch with smooth blending between constrained/unconstrained
- [ ] [T067] Verify all infill tests pass

---

## Phase 5: Web Interface (Gradio)

### UI Foundation
- [ ] [T068] Create src/sketchmap/ui.py with Gradio app setup
- [ ] [T069] [US10] Implement image upload component with drag-and-drop support
- [ ] [T070] [US7] Create color palette reference display component
- [ ] [T071] [US10] [US3] Add text input for style/theme prompt
- [ ] [T072] [US4] Add slider for control strength parameter (0.0-1.0)
- [ ] [T073] [US5] Add optional seed input field
- [ ] [T074] [US9] Add output resolution selector (512x512, 1024x1024)

### UI Generation & Display
- [ ] [T075] [US10] Implement generation button and progress indicator
- [ ] [T076] [US10] Create side-by-side display for input sketch and generated output
- [ ] [T077] [US9] Add download button for generated maps (PNG export)
- [ ] [T078] [US6] Implement result gallery to preserve previous generations
- [ ] [T079] [US6] Add "Generate Variation" button for multiple outputs from same sketch
- [ ] [T080] Test web interface end-to-end workflow

---

## Phase 6: Error Handling & Robustness

### Input Validation
- [ ] [T081] [US8] Add color validation and quantization warning in SketchInput
- [ ] [T082] [US8] Implement color mapping feedback display in UI
- [ ] [T083] Add file format validation with clear error messages in src/sketchmap/sketch.py
- [ ] [T084] Add file size validation (max 10MB) with error messages
- [ ] [T085] Add dimension validation (max 1024x1024, divisible by 8)
- [ ] [T086] Create tests/test_validation.py for all validation scenarios

### Resource Management
- [ ] [T087] Implement GPU/CPU detection in src/sketchmap/generator.py
- [ ] [T088] Add CPU fallback mode with performance warning
- [ ] [T089] Add memory check and error handling for insufficient GPU memory
- [ ] [T090] Implement timeout handling (60s max) with user feedback
- [ ] [T091] Test error handling with invalid inputs (corrupted files, wrong formats)

---

## Phase 7: Performance Optimization

### Model Optimization
- [ ] [T092] Enable fp16 quantization in MapGenerator pipeline initialization
- [ ] [T093] Implement model caching to avoid re-loading on each generation
- [ ] [T094] Add torch.compile() for faster inference (if compatible)
- [ ] [T095] Create benchmarking script in tests/benchmark_performance.py
- [ ] [T096] Verify 512x512 generation completes in <30s on GPU (GTX 1660 equivalent)
- [ ] [T097] Verify 1024x1024 generation completes in <90s on GPU

### Output Quality
- [ ] [T098] Test and tune default generation parameters (inference steps, guidance scale)
- [ ] [T099] Test and tune ControlNet conditioning weights for best results
- [ ] [T100] Verify smooth transitions between terrain types in generated maps
- [ ] [T101] Create visual quality checklist for manual validation

---

## Phase 8: Documentation & Polish

### User Documentation
- [ ] [T102] [P] Create docs/usage.md with complete user guide
- [ ] [T103] [P] Create docs/tutorial.md with step-by-step walkthrough
- [ ] [T104] [P] Update README.md with installation, quickstart, and examples
- [ ] [T105] [P] Add example outputs to examples/ directory with descriptions

### Developer Documentation
- [ ] [T106] [P] Create docs/architecture.md documenting technical design
- [ ] [T107] [P] Add comprehensive docstrings to all public classes and methods
- [ ] [T108] [P] Document GPU requirements and troubleshooting in README.md
- [ ] [T109] [P] Create CONTRIBUTING.md with development setup instructions

### Final Quality Gates
- [ ] [T110] Run full test suite and verify 80%+ coverage
- [ ] [T111] Run mypy type checking in strict mode, verify no errors
- [ ] [T112] Run ruff linting, verify no violations
- [ ] [T113] Run black formatting, verify all files formatted
- [ ] [T114] Manual testing of all user stories against acceptance criteria
- [ ] [T115] Create CHANGELOG.md documenting v1.0.0 features
- [ ] [T116] Tag release v1.0.0 and create release notes

---

## Summary

**Total Tasks**: 116
**Estimated Phases**: 8
**Status**: Ready for implementation

### Phase Breakdown
- Phase 1 (Setup & Foundation): T001-T020 (20 tasks)
- Phase 2 (Single ControlNet): T021-T037 (17 tasks)
- Phase 3 (Multi-ControlNet): T038-T056 (19 tasks)
- Phase 4 (Infill Handling): T057-T067 (11 tasks)
- Phase 5 (Web Interface): T068-T080 (13 tasks)
- Phase 6 (Error Handling): T081-T091 (11 tasks)
- Phase 7 (Performance): T092-T101 (10 tasks)
- Phase 8 (Documentation): T102-T116 (15 tasks)

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
