"""Tests for GenerationConfig dataclass."""

import pytest
from sketchmap.config import GenerationConfig


class TestGenerationConfig:
    """Test cases for GenerationConfig class."""

    def test_initialization_with_defaults(self) -> None:
        """Test GenerationConfig initializes with default values."""
        config = GenerationConfig(
            prompt="fantasy map",
            negative_prompt="blurry, low quality",
        )
        assert config.prompt == "fantasy map"
        assert config.negative_prompt == "blurry, low quality"
        assert config.num_inference_steps == 30
        assert config.guidance_scale == 7.5
        assert config.seed is None
        assert config.controlnet_scribble_weight == 0.8
        assert config.controlnet_seg_weight == 0.7
        assert config.output_resolution == (512, 512)

    def test_initialization_with_custom_values(self) -> None:
        """Test GenerationConfig with all custom values."""
        config = GenerationConfig(
            prompt="realistic satellite map",
            negative_prompt="cartoon, artwork",
            num_inference_steps=50,
            guidance_scale=10.0,
            seed=42,
            controlnet_scribble_weight=0.9,
            controlnet_seg_weight=0.6,
            output_resolution=(1024, 1024),
        )
        assert config.num_inference_steps == 50
        assert config.guidance_scale == 10.0
        assert config.seed == 42
        assert config.controlnet_scribble_weight == 0.9
        assert config.controlnet_seg_weight == 0.6
        assert config.output_resolution == (1024, 1024)

    def test_validate_with_valid_config(self) -> None:
        """Test validate returns True for valid configuration."""
        config = GenerationConfig(
            prompt="test map",
            negative_prompt="bad quality",
        )
        assert config.validate() is True

    def test_validate_with_valid_edge_cases(self) -> None:
        """Test validate accepts edge case valid values."""
        # Minimum values
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            num_inference_steps=1,
            guidance_scale=1.0,
            controlnet_scribble_weight=0.0,
            controlnet_seg_weight=0.0,
        )
        assert config.validate() is True

        # Maximum values
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            num_inference_steps=100,
            guidance_scale=20.0,
            controlnet_scribble_weight=1.0,
            controlnet_seg_weight=1.0,
        )
        assert config.validate() is True

    def test_validate_rejects_too_few_steps(self) -> None:
        """Test validate rejects num_inference_steps < 1."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            num_inference_steps=0,
        )
        with pytest.raises(AssertionError):
            config.validate()

    def test_validate_rejects_too_many_steps(self) -> None:
        """Test validate rejects num_inference_steps > 100."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            num_inference_steps=101,
        )
        with pytest.raises(AssertionError):
            config.validate()

    def test_validate_rejects_low_guidance_scale(self) -> None:
        """Test validate rejects guidance_scale < 1.0."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            guidance_scale=0.5,
        )
        with pytest.raises(AssertionError):
            config.validate()

    def test_validate_rejects_high_guidance_scale(self) -> None:
        """Test validate rejects guidance_scale > 20.0."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            guidance_scale=25.0,
        )
        with pytest.raises(AssertionError):
            config.validate()

    def test_validate_rejects_negative_scribble_weight(self) -> None:
        """Test validate rejects controlnet_scribble_weight < 0.0."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            controlnet_scribble_weight=-0.1,
        )
        with pytest.raises(AssertionError):
            config.validate()

    def test_validate_rejects_high_scribble_weight(self) -> None:
        """Test validate rejects controlnet_scribble_weight > 1.0."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            controlnet_scribble_weight=1.5,
        )
        with pytest.raises(AssertionError):
            config.validate()

    def test_validate_rejects_negative_seg_weight(self) -> None:
        """Test validate rejects controlnet_seg_weight < 0.0."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            controlnet_seg_weight=-0.1,
        )
        with pytest.raises(AssertionError):
            config.validate()

    def test_validate_rejects_high_seg_weight(self) -> None:
        """Test validate rejects controlnet_seg_weight > 1.0."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            controlnet_seg_weight=1.1,
        )
        with pytest.raises(AssertionError):
            config.validate()

    def test_seed_can_be_none(self) -> None:
        """Test that seed can be None (random generation)."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            seed=None,
        )
        assert config.seed is None
        assert config.validate() is True

    def test_seed_can_be_integer(self) -> None:
        """Test that seed can be a specific integer."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            seed=12345,
        )
        assert config.seed == 12345
        assert config.validate() is True

    def test_output_resolution_default(self) -> None:
        """Test default output resolution is 512x512."""
        config = GenerationConfig(prompt="test", negative_prompt="")
        assert config.output_resolution == (512, 512)

    def test_output_resolution_custom(self) -> None:
        """Test custom output resolution can be set."""
        config = GenerationConfig(
            prompt="test",
            negative_prompt="",
            output_resolution=(1024, 1024),
        )
        assert config.output_resolution == (1024, 1024)

    def test_prompts_are_strings(self) -> None:
        """Test that prompts are stored as strings."""
        config = GenerationConfig(
            prompt="fantasy world map",
            negative_prompt="blurry, low quality, distorted",
        )
        assert isinstance(config.prompt, str)
        assert isinstance(config.negative_prompt, str)
        assert len(config.prompt) > 0

    def test_empty_negative_prompt_allowed(self) -> None:
        """Test that negative prompt can be empty string."""
        config = GenerationConfig(prompt="test map", negative_prompt="")
        assert config.negative_prompt == ""
        assert config.validate() is True

    def test_dataclass_equality(self) -> None:
        """Test that two configs with same values are equal."""
        config1 = GenerationConfig(
            prompt="test",
            negative_prompt="bad",
            num_inference_steps=30,
            seed=42,
        )
        config2 = GenerationConfig(
            prompt="test",
            negative_prompt="bad",
            num_inference_steps=30,
            seed=42,
        )
        assert config1 == config2

    def test_dataclass_inequality(self) -> None:
        """Test that configs with different values are not equal."""
        config1 = GenerationConfig(prompt="test1", negative_prompt="bad")
        config2 = GenerationConfig(prompt="test2", negative_prompt="bad")
        assert config1 != config2
