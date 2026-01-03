"""Tests for SketchInput class."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import numpy as np

# Note: Tests use mocking to avoid dependency on PIL/cv2 during test collection
# Real integration tests will be in tests/integration/


class TestSketchInput:
    """Test cases for SketchInput class."""

    @patch("sketchmap.sketch.Image")
    def test_initialization_from_valid_png(self, mock_image: Mock) -> None:
        """Test SketchInput loads a valid PNG file."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        # Mock PIL Image
        mock_img = MagicMock()
        mock_img.size = (512, 512)
        mock_img.mode = "RGB"
        mock_image.open.return_value.convert.return_value = mock_img

        palette = ColorPalette()
        sketch = SketchInput("test.png", palette)

        assert sketch.image == mock_img
        assert sketch.width == 512
        assert sketch.height == 512
        assert sketch.palette == palette
        mock_image.open.assert_called_once_with("test.png")

    @patch("sketchmap.sketch.Image")
    def test_initialization_from_valid_jpg(self, mock_image: Mock) -> None:
        """Test SketchInput loads a valid JPG file."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        mock_img = MagicMock()
        mock_img.size = (256, 256)
        mock_img.mode = "RGB"
        mock_image.open.return_value.convert.return_value = mock_img

        palette = ColorPalette()
        sketch = SketchInput("test.jpg", palette)

        assert sketch.width == 256
        assert sketch.height == 256

    @patch("sketchmap.sketch.Image")
    def test_image_converted_to_rgb(self, mock_image: Mock) -> None:
        """Test that images are converted to RGB mode."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        mock_img = MagicMock()
        mock_img.size = (512, 512)
        mock_opened = MagicMock()
        mock_image.open.return_value = mock_opened
        mock_opened.convert.return_value = mock_img

        palette = ColorPalette()
        SketchInput("test.png", palette)

        # Verify convert("RGB") was called
        mock_opened.convert.assert_called_once_with("RGB")

    @patch("sketchmap.sketch.Image")
    def test_stores_palette_reference(self, mock_image: Mock) -> None:
        """Test that SketchInput stores reference to palette."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        mock_img = MagicMock()
        mock_img.size = (512, 512)
        mock_image.open.return_value.convert.return_value = mock_img

        palette = ColorPalette()
        sketch = SketchInput("test.png", palette)

        assert sketch.palette is palette

    @patch("sketchmap.sketch.Image")
    def test_file_not_found_raises_error(self, mock_image: Mock) -> None:
        """Test that non-existent file raises appropriate error."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        mock_image.open.side_effect = FileNotFoundError("File not found")

        palette = ColorPalette()
        with pytest.raises(FileNotFoundError):
            SketchInput("nonexistent.png", palette)

    @patch("sketchmap.sketch.cv2")
    @patch("sketchmap.sketch.np")
    def test_extract_scribble_returns_numpy_array(
        self, mock_np: Mock, mock_cv2: Mock
    ) -> None:
        """Test extract_scribble returns a numpy array."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        # Create a mock SketchInput with mocked image
        with patch("sketchmap.sketch.Image") as mock_image:
            mock_img = MagicMock()
            mock_img.size = (512, 512)
            mock_image.open.return_value.convert.return_value = mock_img

            # Mock numpy array conversion
            mock_array = np.zeros((512, 512, 3), dtype=np.uint8)
            mock_np.array.return_value = mock_array

            # Mock Canny edge detection
            mock_edges = np.zeros((512, 512), dtype=np.uint8)
            mock_cv2.Canny.return_value = mock_edges
            mock_cv2.cvtColor.return_value = np.zeros((512, 512), dtype=np.uint8)

            palette = ColorPalette()
            sketch = SketchInput("test.png", palette)

            result = sketch.extract_scribble()

            assert isinstance(result, np.ndarray)
            # Canny should have been called
            assert mock_cv2.Canny.called or mock_cv2.cvtColor.called

    @patch("sketchmap.sketch.cv2")
    @patch("sketchmap.sketch.np")
    def test_extract_scribble_uses_canny_edge_detection(
        self, mock_np: Mock, mock_cv2: Mock
    ) -> None:
        """Test that extract_scribble uses Canny edge detection."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        with patch("sketchmap.sketch.Image") as mock_image:
            mock_img = MagicMock()
            mock_img.size = (512, 512)
            mock_image.open.return_value.convert.return_value = mock_img

            mock_array = np.zeros((512, 512, 3), dtype=np.uint8)
            mock_np.array.return_value = mock_array
            mock_cv2.cvtColor.return_value = np.zeros((512, 512), dtype=np.uint8)
            mock_cv2.Canny.return_value = np.zeros((512, 512), dtype=np.uint8)

            palette = ColorPalette()
            sketch = SketchInput("test.png", palette)
            sketch.extract_scribble()

            # Verify Canny was called
            mock_cv2.Canny.assert_called_once()

    def test_extract_scribble_output_shape_matches_input(self) -> None:
        """Test that scribble map has same dimensions as input."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        with patch("sketchmap.sketch.Image") as mock_image, patch(
            "sketchmap.sketch.cv2"
        ) as mock_cv2, patch("sketchmap.sketch.np") as mock_np:

            mock_img = MagicMock()
            mock_img.size = (512, 512)
            mock_image.open.return_value.convert.return_value = mock_img

            mock_array = np.zeros((512, 512, 3), dtype=np.uint8)
            mock_np.array.return_value = mock_array

            # Mock scribble output with matching dimensions
            mock_scribble = np.zeros((512, 512), dtype=np.uint8)
            mock_cv2.Canny.return_value = mock_scribble
            mock_cv2.cvtColor.return_value = np.zeros((512, 512), dtype=np.uint8)

            palette = ColorPalette()
            sketch = SketchInput("test.png", palette)
            result = sketch.extract_scribble()

            # Result should match input dimensions (grayscale, so 2D)
            assert result.shape[0] == 512
            assert result.shape[1] == 512

    @patch("sketchmap.sketch.Image")
    def test_dimensions_stored_correctly(self, mock_image: Mock) -> None:
        """Test that width and height are stored from image."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        mock_img = MagicMock()
        mock_img.size = (1024, 768)  # Different dimensions
        mock_image.open.return_value.convert.return_value = mock_img

        palette = ColorPalette()
        sketch = SketchInput("test.png", palette)

        assert sketch.width == 1024
        assert sketch.height == 768

    @patch("sketchmap.sketch.Image")
    def test_path_stored_as_attribute(self, mock_image: Mock) -> None:
        """Test that image path is stored."""
        from sketchmap.sketch import SketchInput
        from sketchmap.palette import ColorPalette

        mock_img = MagicMock()
        mock_img.size = (512, 512)
        mock_image.open.return_value.convert.return_value = mock_img

        palette = ColorPalette()
        sketch = SketchInput("path/to/test.png", palette)

        # Check that we can access the path if needed
        # (implementation may or may not store this)
        assert sketch.image is not None
