"""OS-backed random value generation for Alpha v1."""

from __future__ import annotations

import secrets


class LibRandom:
    """Generate Alpha v1 random values using the operating system CSPRNG."""

    _PRINTABLE_ASCII_MIN = 32
    _PRINTABLE_ASCII_MAX = 126

    def __init__(self) -> None:
        self._rng = secrets.SystemRandom()

    def random_int(self, min: int = 0, max: int = 99) -> int:
        """Return a random integer in the inclusive range [min, max]."""
        self._validate_range(min, max)
        return self._rng.randrange(min, max + 1)

    def random_float(self, min: float = 0.0, max: float = 1.0) -> float:
        """Return a random float in the inclusive conceptual range [min, max]."""
        self._validate_range(min, max)
        if min == max:
            return float(min)
        return self._rng.uniform(min, max)

    def random_char(self, min: str = "A", max: str = "Z") -> str:
        """Return a random printable ASCII character in the inclusive range [min, max]."""
        min_code = self._validate_printable_char("min", min)
        max_code = self._validate_printable_char("max", max)
        self._validate_range(min_code, max_code)
        return chr(self._rng.randrange(min_code, max_code + 1))

    def get_random_int(self, low: int = 0, high: int = 99) -> int:
        """Backward-compatible alias for random_int."""
        return self.random_int(min=low, max=high)

    def get_random_float(self, low: float = 0.0, high: float = 1.0) -> float:
        """Backward-compatible alias for random_float."""
        return self.random_float(min=low, max=high)

    def get_random_char(self, low: str | int = "A", high: str | int = "Z") -> str:
        """Backward-compatible alias for random_char.

        Older versions accepted printable ASCII code points. Alpha v1 prefers
        single-character strings, but code points are still accepted here.
        """
        return self.random_char(min=self._coerce_char(low), max=self._coerce_char(high))

    @staticmethod
    def _validate_range(min_value: int | float, max_value: int | float) -> None:
        if min_value > max_value:
            raise ValueError("Invalid range: min must be less than or equal to max")

    @classmethod
    def _validate_printable_char(cls, name: str, value: str) -> int:
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError(f"Invalid character range: {name} must be one character")

        code = ord(value)
        if code < cls._PRINTABLE_ASCII_MIN or code > cls._PRINTABLE_ASCII_MAX:
            raise ValueError(f"Invalid character range: {name} must be printable ASCII")

        return code

    @classmethod
    def _coerce_char(cls, value: str | int) -> str:
        if isinstance(value, int):
            return chr(value)
        return value


_DEFAULT_RANDOMIZER = LibRandom()


def random_int(min: int = 0, max: int = 99) -> int:
    """Return a random integer in the inclusive range [min, max]."""
    return _DEFAULT_RANDOMIZER.random_int(min=min, max=max)


def random_float(min: float = 0.0, max: float = 1.0) -> float:
    """Return a random float in the inclusive conceptual range [min, max]."""
    return _DEFAULT_RANDOMIZER.random_float(min=min, max=max)


def random_char(min: str = "A", max: str = "Z") -> str:
    """Return a random printable ASCII character in the inclusive range [min, max]."""
    return _DEFAULT_RANDOMIZER.random_char(min=min, max=max)


randomInt = random_int
randomFloat = random_float
randomChar = random_char
