"""Example test to verify pytest is working."""

import sketchmap


def test_version() -> None:
    """Test that version is defined."""
    assert sketchmap.__version__ == "0.1.0"


def test_import() -> None:
    """Test that package can be imported."""
    assert sketchmap is not None
