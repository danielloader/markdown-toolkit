"""Functions module."""

from typing import Union


def add(
        first_number: Union[int, float],
        second_number: Union[int, float]) -> Union[int, float]:
    """Addition of numbers.

    Args:
        first_number (Union[int, float]): First number.
        second_number (Union[int, float]): Second number.

    Returns:
        Union[int, float]: Addition sum of two numbers.
    """
    return first_number + second_number


def subtract(
        first_number: Union[int, float],
        second_number: Union[int, float]) -> Union[int, float]:
    """Subtraction of numbers.

    Args:
        first_number (Union[int, float]): First number.
        second_number (Union[int, float]): Second number.

    Returns:
        Union[int, float]: Subtraction of two numbers.
    """
    return first_number - second_number
