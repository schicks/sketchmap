# Prior Work: Sketch-Based Map Generation with Stable Diffusion

**Feature**: `001-sketch-based-map-generation` | **Created**: 2026-01-03 | **Document Type**: Literature Review & Technical Analysis

## Executive Summary

This document reviews prior work and existing techniques for building a sketch-based map generation tool using Stable Diffusion. The tool enables users to provide simple color-coded sketch inputs (similar to MS Paint) where each color in a constrained palette hints at terrain/feature types to generate, with unmarked regions open for creative infill.

**Key Finding**: Multiple mature technical approaches exist (ControlNet, T2I-Adapter, regional conditioning) that can be combined to achieve this use case. The most promising approach combines **ControlNet Scribble** for sketch control with **semantic segmentation conditioning** for color-based terrain hints.

---

## 1. Core Technologies for Sketch-Based Control

### 1.1 ControlNet

**Overview**: ControlNet is a neural network architecture that adds spatial conditioning controls to pretrained text-to-image diffusion models without modifying the base model.

**Key Characteristics**:
- Locks production-ready diffusion models and reuses their deep encoding layers
- Adds conditional control through additional neural network layers (~77M parameters for base, 18M for small, 5M for tiny)
- Supports multiple control types: sketch/scribble, depth, pose, edges, segmentation maps
- **Composable**: Multiple ControlNets can be combined for multi-condition control

**ControlNet Scribble Mode**:
- Specifically designed for hand-drawn sketch inputs
- Works with sparse, rough sketches with distinct lines
- Enables direct manual annotation of desired features
- Suitable for stylized effects and concept iteration
- Revolutionizes the design process by allowing rapid iterations with sketches

**Relevance to Project**: ControlNet Scribble is ideal for accepting user sketch input and converting it into structured generation guidance. The composability feature allows combining sketch control with other conditioning types.

**Sources**:
- [ControlNet GitHub Repository](https://github.com/lllyasviel/ControlNet)
- [ControlNet: A Complete Guide](https://stable-diffusion-art.com/controlnet/)
- [ControlNet Scribble Guide](https://blog.segmind.com/controlnet-scribble/)
- [Stable Diffusion Control Nets and Concept Design Sketches](https://www.aienvisions.com/2024/02/16/stable-diffusion-control-nets-and-concept-design-sketches/)

---

### 1.2 T2I-Adapter

**Overview**: T2I-Adapter is a lightweight alternative to ControlNet that learns simple adapters to align internal knowledge with external control signals while freezing the original T2I models.

**Key Characteristics**:
- More lightweight than ControlNet (base: ~77M params, small: 18M, tiny: 5M)
- Designed specifically for **sparse control signals** (condition maps have higher sparsity than natural images)
- Supports composable conditions: color, depth, sketch, semantic segmentation, keypose
- Assigns different adapter sizes based on control granularity:
  - Tiny version (5M params) for sketch guidance
  - Small version (18M params) for spatial color palette (coarse-grained control)
  - Base version for other structure guidance

**Spatial Color Palette Control**:
- Accepts 4-channel input: 1 channel for image edges (Canny), 3 channels for quantized image colors
- Uses vector quantization, matching, and "dequantization" for extreme palette transfers
- Novel training loss measures match between color distribution in control and generated images

**Relevance to Project**: T2I-Adapter's focus on sparse controls and explicit spatial color palette support makes it highly relevant. The lightweight architecture could provide better performance than ControlNet for our constrained-palette use case.

**Sources**:
- [T2I-Adapter Paper (arXiv)](https://arxiv.org/abs/2302.08453)
- [T2I-Adapter GitHub Repository](https://github.com/TencentARC/T2I-Adapter)
- [ControlNet and T2I-Adapter Comparison](https://medium.com/@catmus2048/controlnet-and-t2i-adapter-the-icebreaker-solution-for-precise-control-of-ai-image-generation-ef61258139c3)
- [Applying a Color Palette with Local Control using Diffusion Models](https://ar5iv.labs.arxiv.org/html/2307.02698)

---

## 2. Color and Palette-Based Conditioning

### 2.1 Color Palette Transfer and Control

**Key Research Findings**:

1. **Palette Transfer Pipeline**:
   - Vector quantization of source colors
   - Color matching between palette and image regions
   - "Dequantization" using diffusion model with specialized loss
   - Enables extreme palette transfers while maintaining semantic coherence

2. **Multi-ControlNet Color Approach**:
   - Second ControlNet unit introduces color palette as foundation
   - "Shuffle" control type allows model to creatively distribute colors
   - Works in combination with line art/sketch control

3. **Interactive Colorization**:
   - User input via color scribbles or clicks
   - Text prompts can guide colorization without canvas interaction
   - Combining scribbles with text produces more vivid results

**Palette Models**:
- **Palette: Image-to-Image Diffusion Models**: Framework for image-to-image translation with diffusion
- Uses unified framework for colorization, inpainting, and other I2I tasks

**Relevance to Project**: These techniques show proven methods for color-based conditioning. The multi-ControlNet approach (sketch + color palette) closely matches our use case of constrained color hints.

**Sources**:
- [Transforming Sketch Art into Colorful Masterpieces](https://www.nextdiffusion.ai/tutorials/vibrant-sketch-colorization-stable-diffusion-controlnet)
- [ColorizeNet: Stable Diffusion for Image Colorization](https://medium.com/@rensortino/colorizenet-stable-diffusion-for-image-colorization-bdc9c35121fa)
- [Diffusing Colors: Image Colorization with Text Guided Diffusion](https://arxiv.org/html/2312.04145v1)
- [Palette: Image-to-Image Diffusion Models](https://iterative-refinement.github.io/palette/)

---

## 3. Region-Based and Spatial Control

### 3.1 Region-Aware Diffusion (RAD)

**Overview**: Recent research (2024) on region-specific control in diffusion models.

**Key Innovation**:
- Assigns **different noise schedules to each pixel**
- Enables some areas to be completely denoised while others retain noise
- Naturally emulates inpainting by adding noise only to target regions
- Enables asynchronous region generation and localized control
- Large efficiency improvements over standard inpainting

**Relevance to Project**: RAD's per-pixel noise scheduling could enable our "unconstrained space" feature - regions without color hints could use different generation strategies than constrained regions.

**Sources**:
- [RAD: Region-Aware Diffusion Models for Image Inpainting](https://arxiv.org/html/2412.09191v3)

---

### 3.2 Regional Prompter and Multi-Region Control

**Overview**: Tools and techniques for controlling different regions with different prompts/conditions.

**Key Features**:
- Divide image into regions with different prompts per region
- Control composition precisely in Stable Diffusion
- Combine with ControlNet for region-specific structural control

**Spatial Conditioning in Standard Inpainting**:
- UNet with 5 additional input channels: 4 for encoded masked-image, 1 for mask
- Weights zero-initialized for these channels
- Finetuned specifically for inpainting tasks at 512x512

**Relevance to Project**: Regional prompting could allow different terrain types (forests, mountains, water) to have specialized prompts while maintaining global coherence.

**Sources**:
- [Regional Prompter: Control image composition in Stable Diffusion](https://stable-diffusion-art.com/regional-prompter/)
- [Stable Diffusion Inpainting Documentation](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-inpainting)
- [Stable Diffusion Inpainting Overview](https://www.emergentmind.com/topics/stable-diffusion-inpainting)

---

## 4. Composable Multi-Conditional Systems

### 4.1 Compositional Visual Generation

**Overview**: Research on combining multiple diffusion models and conditions during inference.

**Key Concepts**:
- **Composable Diffusion Models**: Multiple models composed during inference without additional training
- **Boolean Logic Operators**:
  - Conjunction (AND): Combine multiple conditions
  - Negation (NOT): Exclude certain features
- Generate images containing all concepts described in inputs

**Composer Framework**:
- Multi-conditional diffusion model with U-Net backbone
- Conditions combined using Boolean logic
- Complex specifications customized to specific needs
- Supports both local conditions (spatial) and global conditions (style, mood)

**Uni-ControlNet**:
- Categorizes conditions into local and global groups
- Local control adapter for spatial/structural control
- Global control adapter for overall image properties
- All-in-one control architecture

**Relevance to Project**: Composable conditions are essential for our use case - we need to combine sketch structure + color hints + text prompts + unconstrained generation. Boolean operators could help specify "water AND not-land" type constraints.

**Sources**:
- [Compositional Visual Generation with Composable Diffusion Models](https://energy-based-model.github.io/Compositional-Visual-Generation-with-Composable-Diffusion-Models/)
- [Composer: Creative and Controllable Image Synthesis](https://proceedings.mlr.press/v202/huang23b/huang23b.pdf)
- [Uni-ControlNet: All-in-One Control](https://shihaozhaozsh.github.io/unicontrolnet/)

---

## 5. AI-Powered Map and Terrain Generation

### 5.1 Terrain Generation with Diffusion Models

**Terrain Diffusion Project**:
- AI-powered terrain generation framework
- Replaces traditional procedural noise (Perlin noise) with generative model
- Fast, high-fidelity, infinitely tileable terrain generation
- Demonstrates diffusion models for game/world terrain

**Key Advantages Over Traditional Methods**:
- Higher variability than procedural noise
- Better global consistency
- Learned patterns from real terrain data
- Can be conditioned on specific terrain features

**Sources**:
- [Terrain Diffusion GitHub](https://github.com/xandergos/terrain-diffusion)
- [Improving procedural terrain generation using deep learning](https://medium.com/@lars.sluijter/improving-procedural-terrain-generation-using-a-single-deep-learning-model-5ad1eac09bd1)

---

### 5.2 Map Diffusion and Game Map Generation

**Map Diffusion**:
- Text-promptable map generation model
- Generates maps based on textual descriptions
- Users describe a region, model generates corresponding map
- Published at ACM SIGSPATIAL 2024

**Game Map Editing with Diffusion**:
- **BrushGAN** and **BrushCLDM**: Smart brush tools for game map editing
- GANs: Faster training/inference, fine-grained textures
- Diffusion models: Higher variability, better global consistency
- Context-aware generation for seamless editing

**Fantasy Map Generation**:
- Commercial tools (CGDream, Venice AI) use Flux/Stable Diffusion
- Text-to-image diffusion with DiT (Diffusion Transformer) architecture
- Civitai models specifically trained for D&D/fantasy maps

**Relevance to Project**: These projects demonstrate that diffusion models are actively used for map generation. The combination of text prompts + spatial control + learned map patterns is proven to work well.

**Sources**:
- [Map Diffusion Paper](https://dl.acm.org/doi/10.1145/3615900.3628787)
- [Smart Brush for Game Map Editing](https://arxiv.org/html/2503.19793v1)
- [DnD Map Generator - Civitai](https://civitai.com/models/5012/dnd-map-generator)
- [AI Fantasy Map Generator](https://cgdream.ai/features/ai-fantasy-map-generator)

---

## 6. Semantic Segmentation as Conditioning

### 6.1 Class-Label Conditioning for Diffusion

**Overview**: Using semantic segmentation maps (colored regions representing classes) as conditioning input.

**Key Approaches**:

1. **Class-Conditioned Generation**:
   - Add class embedding to timestamp embedding in diffusion process
   - Each color/class guides generation of specific content type
   - Well-established technique in conditional diffusion models

2. **Diffusion Models for Segmentation**:
   - Intermediate activations in diffusion models capture semantic information
   - Excellent pixel-level representations for segmentation tasks
   - Can work bidirectionally: segmentation → generation or generation → segmentation

3. **MaskDiffusion**:
   - Uses pretrained Stable Diffusion for open-vocabulary segmentation
   - No additional training needed
   - Demonstrates semantic understanding in diffusion models

**Relevance to Project**: Our color palette is essentially a sparse semantic segmentation map. Each color represents a class (water, forest, mountain, etc.). This is a proven conditioning method for diffusion models.

**Sources**:
- [Label-Efficient Semantic Segmentation with Diffusion Models](https://arxiv.org/abs/2112.03126)
- [MaskDiffusion: Exploiting Pre-trained Diffusion Models for Semantic Segmentation](https://arxiv.org/html/2403.11194v1)
- [DiffuMask: Synthesizing Images with Pixel-level Annotations](https://weijiawu.github.io/DiffusionMask/)

---

## 7. Technical Approaches Comparison

### Approach 1: ControlNet + Semantic Segmentation
**Architecture**: Base Stable Diffusion + ControlNet (Seg) + Text Prompts

**Pros**:
- Mature, well-documented
- Direct color → class mapping
- Strong community support
- Many pretrained models available

**Cons**:
- Requires well-defined segmentation map (less flexible for sketches)
- May be less forgiving of rough/sparse input
- Heavier computational load (~77M params)

---

### Approach 2: T2I-Adapter + Color Palette
**Architecture**: Base Stable Diffusion + T2I-Adapter (Color + Sketch) + Text Prompts

**Pros**:
- Designed for sparse inputs
- Explicit color palette support
- Lightweight (5-18M params for tiny/small versions)
- Composable conditions

**Cons**:
- Less mature than ControlNet
- Smaller community/fewer tutorials
- May require more custom integration work

---

### Approach 3: Multi-ControlNet (Scribble + Seg)
**Architecture**: Base Stable Diffusion + ControlNet Scribble + ControlNet Seg + Text Prompts

**Pros**:
- Combines structural sketch control with semantic color hints
- Proven composability
- Leverages strengths of both control types
- Maximum flexibility

**Cons**:
- Higher computational cost (multiple ControlNets)
- More complex pipeline
- Potential conflicts between conditions

---

### Approach 4: Regional Prompting + Inpainting
**Architecture**: Region-based prompting + Stable Diffusion Inpainting + Masks

**Pros**:
- Can have different prompts per terrain type
- Native inpainting support for unconstrained regions
- Fine-grained control over each area

**Cons**:
- Requires segmenting sketch into regions first
- More preprocessing overhead
- Harder to maintain global coherence
- Manual region management complexity

---

## 8. Recommended Technical Approach

### Primary Recommendation: Multi-ControlNet (Scribble + Semantic Seg)

**Rationale**:
1. **Scribble ControlNet** handles rough sketch structure and boundaries
2. **Semantic Segmentation ControlNet** maps colors to terrain types
3. Text prompts provide global style/theme guidance
4. Unconstrained regions can use masked inpainting or lower conditioning strength

**Architecture**:
```
User Input (Sketch with Color Palette)
         ↓
┌────────┴────────┐
│  Preprocessing  │
│  - Extract edges/scribbles
│  - Create segmentation map from colors
│  - Generate inpainting mask (unconstrained areas)
└────────┬────────┘
         ↓
┌────────┴────────┐
│ Stable Diffusion│
│   Base Model    │
└────────┬────────┘
         ↓
    ┌────┴────┬─────────┬───────────┐
    │         │         │           │
┌───▼──┐  ┌──▼──┐  ┌───▼────┐  ┌──▼────┐
│Text  │  │Scrib│  │Semantic│  │Inpaint│
│Prompt│  │-ble │  │  Seg   │  │ Mask  │
│      │  │     │  │ (color)│  │       │
└──────┘  └─────┘  └────────┘  └───────┘
         ControlNet  ControlNet  Native
```

**Implementation Phases**:

**Phase 1**: Single ControlNet (Scribble OR Seg)
- Validate basic sketch → map generation
- Establish color palette → terrain mapping
- Test with simple prompts

**Phase 2**: Multi-ControlNet Composition
- Combine scribble structure + semantic colors
- Balance conditioning strengths
- Optimize for coherent output

**Phase 3**: Unconstrained Region Handling
- Implement masked inpainting for unmarked areas
- Test variable conditioning strength
- Achieve seamless blending

**Phase 4**: Refinement
- Fine-tune color palette
- Optimize performance
- User experience polish

---

### Alternative Recommendation: T2I-Adapter (if performance is critical)

If computational efficiency is a primary concern, T2I-Adapter with color palette + sketch modes offers:
- 70% parameter reduction (tiny: 5M vs ControlNet: 77M)
- Purpose-built for sparse controls
- Explicit color palette support

**Trade-off**: Less community support and fewer pretrained models than ControlNet.

---

## 9. Key Implementation Considerations

### 9.1 Color Palette Design
- **Limited palette size**: 5-10 distinct colors recommended
- **High contrast colors**: Easier for model to distinguish
- **Semantic mapping**: Each color → terrain type + descriptive prompt
- **Background/unconstrained color**: Special handling (e.g., white = infill)

**Example Palette**:
```
#0000FF (Blue)    → Water, lakes, rivers
#00FF00 (Green)   → Forest, vegetation
#8B4513 (Brown)   → Mountains, hills
#FFFF00 (Yellow)  → Desert, beaches
#808080 (Gray)    → Cities, roads
#FFFFFF (White)   → Unconstrained infill
```

---

### 9.2 Sketch Processing Pipeline
1. **Load user sketch** (PNG/JPG from paint tool)
2. **Color quantization**: Map similar colors to palette
3. **Edge extraction**: Canny or similar for scribble control
4. **Segmentation map**: Color → class ID mapping
5. **Mask generation**: Identify unconstrained regions
6. **Condition strength**: Allow user to control how strict hints are

---

### 9.3 Prompt Engineering Strategy
- **Base prompt**: Overall map style (fantasy, realistic, satellite, topographic)
- **Per-class prompts**: Specific descriptions for each terrain type
- **Composition prompts**: Global coherence (lighting, weather, perspective)
- **Negative prompts**: Avoid unwanted features

**Example**:
```
Base: "fantasy world map, top-down view, artistic style"
Blue regions: "+ clear blue water, rivers and lakes"
Green regions: "+ lush forests, dense vegetation"
Unconstrained: "+ natural terrain transitions, realistic geography"
Negative: "blurry, text, labels, low quality"
```

---

### 9.4 Quality and Performance Optimization
- **Resolution**: Start with 512x512, scale to 1024x1024 or higher
- **Sampling steps**: 20-50 steps (balance quality vs speed)
- **Guidance scale**: 7-12 (control prompt adherence)
- **ControlNet strength**: 0.6-1.0 (adjustable per user preference)
- **Model selection**: Choose appropriate SD checkpoint (v1.5, v2.1, SDXL)

---

## 10. Open Research Questions

1. **Optimal condition balance**: How to weight scribble vs color vs text?
2. **Unconstrained infill quality**: Best approach for seamless blending?
3. **Interactive refinement**: Can users iteratively refine generations?
4. **Fine-tuning needs**: Would a map-specific fine-tuned model improve results?
5. **Tiling/continuity**: Can generated maps tile seamlessly for larger worlds?

---

## 11. Conclusion

The sketch-based map generation tool is **highly feasible** with current diffusion technology. The combination of ControlNet/T2I-Adapter for spatial control with semantic segmentation for color-based hints is well-supported by existing research and tools.

**Key Success Factors**:
1. Well-designed constrained color palette with clear semantic meanings
2. Effective combination of multiple conditioning signals
3. Thoughtful handling of unconstrained regions
4. Iterative user workflow for refinement

**Next Steps**:
1. Create detailed feature specification
2. Design implementation plan with chosen architecture
3. Build prototype with single ControlNet
4. Iterate based on results

---

## References

### ControlNet and Sketch-Based Control
- [Stable Diffusion Control Nets and Concept Design Sketches](https://www.aienvisions.com/2024/02/16/stable-diffusion-control-nets-and-concept-design-sketches/)
- [ControlNet GitHub Repository](https://github.com/lllyasviel/ControlNet)
- [ControlNet Scribble Guide](https://blog.segmind.com/controlnet-scribble/)
- [ControlNet: A Complete Guide](https://stable-diffusion-art.com/controlnet/)

### T2I-Adapter and Sparse Control
- [T2I-Adapter Paper (arXiv)](https://arxiv.org/abs/2302.08453)
- [T2I-Adapter GitHub Repository](https://github.com/TencentARC/T2I-Adapter)
- [ControlNet and T2I-Adapter Comparison](https://medium.com/@catmus2048/controlnet-and-t2i-adapter-the-icebreaker-solution-for-precise-control-of-ai-image-generation-ef61258139c3)

### Color Palette and Conditioning
- [Applying a Color Palette with Local Control using Diffusion Models](https://ar5iv.labs.arxiv.org/html/2307.02698)
- [Transforming Sketch Art into Colorful Masterpieces](https://www.nextdiffusion.ai/tutorials/vibrant-sketch-colorization-stable-diffusion-controlnet)
- [Diffusing Colors: Image Colorization with Text Guided Diffusion](https://arxiv.org/html/2312.04145v1)
- [Palette: Image-to-Image Diffusion Models](https://iterative-refinement.github.io/palette/)

### Region-Based Control and Inpainting
- [RAD: Region-Aware Diffusion Models for Image Inpainting](https://arxiv.org/html/2412.09191v3)
- [Regional Prompter: Control image composition in Stable Diffusion](https://stable-diffusion-art.com/regional-prompter/)
- [Stable Diffusion Inpainting Documentation](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-inpainting)

### Composable Multi-Conditional Systems
- [Compositional Visual Generation with Composable Diffusion Models](https://energy-based-model.github.io/Compositional-Visual-Generation-with-Composable-Diffusion-Models/)
- [Composer: Creative and Controllable Image Synthesis](https://proceedings.mlr.press/v202/huang23b/huang23b.pdf)
- [Uni-ControlNet: All-in-One Control](https://shihaozhaozsh.github.io/unicontrolnet/)

### Map and Terrain Generation
- [Terrain Diffusion GitHub](https://github.com/xandergos/terrain-diffusion)
- [Map Diffusion Paper](https://dl.acm.org/doi/10.1145/3615900.3628787)
- [Smart Brush for Game Map Editing](https://arxiv.org/html/2503.19793v1)
- [DnD Map Generator - Civitai](https://civitai.com/models/5012/dnd-map-generator)

### Semantic Segmentation Conditioning
- [Label-Efficient Semantic Segmentation with Diffusion Models](https://arxiv.org/abs/2112.03126)
- [MaskDiffusion: Exploiting Pre-trained Diffusion Models for Semantic Segmentation](https://arxiv.org/html/2403.11194v1)
- [DiffuMask: Synthesizing Images with Pixel-level Annotations](https://weijiawu.github.io/DiffusionMask/)

---

**Document Status**: Complete - Ready for Feature Specification Phase
