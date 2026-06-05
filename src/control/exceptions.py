class ParseError(ValueError):
    """Control layer input parsing failure."""


class ValidationError(ValueError):
    """Control layer validation failure (entity errors mapped here)."""
