"""Sketch input handling and preprocessing for map generation."""

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from PIL import Image as PILImage
else:
    try:
        from PIL import Image
    except ImportError:
        Image = None  # type: ignore

try:
    import cv2
except ImportError:
    cv2 = None  # type: ignore

from sketchmap.palette import ColorPalette


class SketchInput:
    """User-provided sketch image with color hints for map generation.

    This class handles loading, validation, and preprocessing of sketch images.
    Sketches are expected to use colors from a predefined palette to indicate
    desired terrain types, with white regions left unconstrained for AI infill.

    Attributes:
        image: PIL Image object of the loaded sketch (RGB mode)
        width: Width of the sketch image in pixels
        height: Height of the sketch image in pixels
        palette: ColorPalette instance for terrain type mapping

    Example:
        >>> palette = ColorPalette()
        >>> sketch = SketchInput("my_map.png", palette)
        >>> scribble_map = sketch.extract_scribble()
    """

    def __init__(self, image_path: str, palette: ColorPalette) -> None:
        """Initialize SketchInput by loading and validating an image file.

        Args:
            image_path: Path to the sketch image file (PNG or JPG)
            palette: ColorPalette instance for color-to-terrain mapping

        Raises:
            FileNotFoundError: If image file doesn't exist
            ImportError: If PIL is not installed
            ValueError: If image format is unsupported

        Example:
            >>> palette = ColorPalette()
            >>> sketch = SketchInput("sketch.png", palette)
        """
        if Image is None:
            raise ImportError(
                "PIL/Pillow is required for image loading. "
                "Install with: pip install pillow"
            )

        # Load image and convert to RGB
        self.image = Image.open(image_path).convert("RGB")
        self.width, self.height = self.image.size
        self.palette = palette

    def extract_scribble(self) -> np.ndarray:
        """Extract edge/scribble map for ControlNet Scribble conditioning.

        Uses Canny edge detection to extract structural information from the
        sketch. This provides spatial layout control for map generation.

        Returns:
            Numpy array of edge map (grayscale, same dimensions as input)

        Raises:
            ImportError: If opencv-python is not installed

        Example:
            >>> sketch = SketchInput("map.png", palette)
            >>> edges = sketch.extract_scribble()
            >>> edges.shape
            (512, 512)
        """
        if cv2 is None:
            raise ImportError(
                "opencv-python is required for edge detection. "
                "Install with: pip install opencv-python"
            )

        # Convert PIL Image to numpy array
        img_array = np.array(self.image)

        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Apply Canny edge detection
        # Thresholds chosen for sketch-style input (not too sensitive)
        edges = cv2.Canny(gray, threshold1=100, threshold2=200)

        return edges
