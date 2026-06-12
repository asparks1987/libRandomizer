"""Backward-compatible import shim for older LibRandom users."""

try:
    from librandomizer import LibRandom, randomChar, randomFloat, randomInt, random_char, random_float, random_int
except ModuleNotFoundError:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
    from librandomizer import LibRandom, randomChar, randomFloat, randomInt, random_char, random_float, random_int

__all__ = [
    "LibRandom",
    "random_int",
    "random_float",
    "random_char",
    "randomInt",
    "randomFloat",
    "randomChar",
]
