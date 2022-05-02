"""Example Module containing a class and two functions.
This exists to demonstrate the document builder."""

from .classes import ExampleClass
from .functions import add, subtract

MODULE_CONSTANT: str = "foo"

__all__ = ["ExampleClass", "add", "subtract", "MODULE_CONSTANT"]
