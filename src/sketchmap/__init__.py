"""Sketchmap - Sketch-based map generation using AI."""

__version__ = "0.1.0"

from sketchmap.config import GenerationConfig
from sketchmap.palette import ColorPalette, TerrainType
from sketchmap.sketch import SketchInput

__all__ = ["ColorPalette", "GenerationConfig", "SketchInput", "TerrainType"]
