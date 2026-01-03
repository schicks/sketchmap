"""Image preprocessing utilities for sketch-based map generation.

This module provides preprocessing functions for preparing sketch images
for use with ControlNet models.
"""

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    import cv2 as cv2_type
else:
    try:
        import cv2
    except ImportError:
        cv2 = None  # type: ignore


def extract_edges_canny(
    image: np.ndarray,
    low_threshold: int = 100,
    high_threshold: int = 200,
) -> np.ndarray:
    """Extract edges from an image using Canny edge detection.

    This function applies Canny edge detection to extract structural information
    from images. It's designed for sketch-based inputs where clear edges define
    the spatial layout.

    Args:
        image: Input image as numpy array (can be RGB or grayscale)
        low_threshold: Lower threshold for edge detection (default: 100)
        high_threshold: Upper threshold for edge detection (default: 200)

    Returns:
        Binary edge map as numpy array (same height/width as input, grayscale)

    Raises:
        ImportError: If opencv-python is not installed
        ValueError: If image is not a valid numpy array

    Example:
        >>> import numpy as np
        >>> img = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        >>> edges = extract_edges_canny(img)
        >>> edges.shape
        (512, 512)

    Notes:
        - Threshold values control sensitivity:
          - Lower values detect more edges (more sensitive)
          - Higher values detect fewer edges (less sensitive)
        - Typical range: 50-200 for low, 100-300 for high
        - For sketches: 100/200 works well (not too sensitive)
    """
    if cv2 is None:
        raise ImportError(
            "opencv-python is required for edge detection. "
            "Install with: pip install opencv-python"
        )

    if not isinstance(image, np.ndarray):
        raise ValueError("Image must be a numpy array")

    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image

    # Apply Canny edge detection
    edges = cv2.Canny(gray, low_threshold, high_threshold)

    return edges
