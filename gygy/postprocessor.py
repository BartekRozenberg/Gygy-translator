"""Postprocessing utilities for Gygy morpheme output."""


def postprocess(text: str) -> str:
    """Clean and merge model tokens."""
    return text.strip()
