"""Classes module."""


class ExampleClass:
    """String casting utility class."""
    TOPLEVEL_VALUE: int = 1
    ATTRIBUTE_DICT: dict = {"example": "value"}
    
    @staticmethod
    def to_int(string: str) -> int:
        """Convert string to integer.

        Args:
            string (str): Input string.

        Raises:
            exc: Failed to cast string to integer.

        Returns:
            int: Casted integer value.
        """

        try:
            return int(string)
        except Exception as exc:
            raise exc

    @staticmethod
    def to_float(string: str) -> float:
        """Convert string to float.

        Args:
            string (str): Input string.

        Raises:
            exc: Failed to cast string to float.

        Returns:
            int: Casted float value.
        """

        try:
            return float(string)
        except Exception as exc:
            raise exc
