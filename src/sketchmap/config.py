"""Configuration dataclass for map generation parameters."""

from dataclasses import dataclass


@dataclass
class GenerationConfig:
    """Configuration for map generation process.

    This class encapsulates all parameters controlling how a map is generated
    from a sketch, including prompts, sampling parameters, and ControlNet weights.

    Attributes:
        prompt: Overall style/theme prompt describing desired map appearance
        negative_prompt: Things to avoid in the generated map
        num_inference_steps: Number of denoising steps (higher = better quality, slower)
        guidance_scale: How strictly to follow the prompt (higher = more literal)
        seed: Random seed for reproducibility (None for random)
        controlnet_scribble_weight: Influence of scribble/edge control (0.0-1.0)
        controlnet_seg_weight: Influence of segmentation/color control (0.0-1.0)
        output_resolution: Desired output image size as (width, height)

    Example:
        >>> config = GenerationConfig(
        ...     prompt="fantasy map, detailed",
        ...     negative_prompt="blurry, low quality",
        ...     seed=42
        ... )
        >>> config.validate()
        True
    """

    # Required parameters
    prompt: str
    negative_prompt: str

    # Sampling parameters with defaults
    num_inference_steps: int = 30  # 20-50 is typical range
    guidance_scale: float = 7.5  # 7-12 is typical range
    seed: int | None = None  # None means random

    # ControlNet conditioning weights
    controlnet_scribble_weight: float = 0.8  # Scribble/edge influence
    controlnet_seg_weight: float = 0.7  # Segmentation/color influence

    # Output settings
    output_resolution: tuple[int, int] = (512, 512)

    def validate(self) -> bool:
        """Validate configuration parameters are within acceptable ranges.

        Returns:
            True if all parameters are valid

        Raises:
            AssertionError: If any parameter is outside valid range

        Example:
            >>> config = GenerationConfig("test", "bad")
            >>> config.validate()
            True
            >>> config.num_inference_steps = 0
            >>> config.validate()
            Traceback (most recent call last):
                ...
            AssertionError
        """
        # Validate num_inference_steps
        assert (
            1 <= self.num_inference_steps <= 100
        ), f"num_inference_steps must be 1-100, got {self.num_inference_steps}"

        # Validate guidance_scale
        assert (
            1.0 <= self.guidance_scale <= 20.0
        ), f"guidance_scale must be 1.0-20.0, got {self.guidance_scale}"

        # Validate controlnet_scribble_weight
        assert (
            0.0 <= self.controlnet_scribble_weight <= 1.0
        ), f"controlnet_scribble_weight must be 0.0-1.0, got {self.controlnet_scribble_weight}"

        # Validate controlnet_seg_weight
        assert (
            0.0 <= self.controlnet_seg_weight <= 1.0
        ), f"controlnet_seg_weight must be 0.0-1.0, got {self.controlnet_seg_weight}"

        return True
