"""Helper functions."""
from __future__ import annotations
import importlib
from typing import Optional, List, Callable, Any, get_type_hints
from inspect import isclass, isfunction
from .generator import Heading, MarkdownBuilder


def _atribute_labeller(object: Callable, attribute_name: str, attribute_value: Any) -> str:
    parts = []
    parts.append(f"**{attribute_name}**:")
    if get_type_hints(object).get(attribute_name):
        parts.append(f"_{get_type_hints(object).get(attribute_name)}_")
    parts.append(f"`{str(attribute_value)}`")
    return " ".join(parts)


def _module_callable_builder(document: MarkdownBuilder, module_callable: Callable):
    """Return docstring on Class or Function provided.

    Args:
        document (MarkdownBuilder): Root document to append.
        module_callable (Callable): Callable to inspect for __doc__.
    """
    if isclass(module_callable):
        with Heading(document, f"__Class__: `{module_callable.__name__}`"):
            document.code(module_callable.__doc__)
            attribute_list = []
            callable_list = []
            for attr in [a for a in dir(module_callable) if not a.startswith('__')]:
                item = getattr(module_callable, attr)
                if callable(item):
                    callable_list.append(item)
                else:
                    attribute_list.append(_atribute_labeller(module_callable, attr, item))
            with Heading(document, "_Attributes_:"):
                document.list(attribute_list)
            for item in callable_list:
                with Heading(document, f"_Method_: `{attr}`"):
                    document.code(item.__doc__.strip())
    if isfunction(module_callable):
        with Heading(document, f"__Function__: `{module_callable.__name__}`"):
            document.code(module_callable.__doc__.strip())
    document.horizontal_bar()


def module_block(
    document: MarkdownBuilder,
    module: str,
) -> List[Optional[str]]:
    """Generate markdown representation of a python module.

    Args:
        module (str): Literal string representation of the module path.

    Returns:
        List[Optional[str]]: List of strings to concatenate into markdown.
    """
    imported_module = importlib.import_module(module)
    module_attributes = []
    module_callables = []
    with Heading(document, imported_module.__name__):
        document.paragraph(imported_module.__doc__)
        for callable_name in imported_module.__all__:
            module_object = getattr(imported_module, callable_name)
            if callable(module_object):
                module_callables.append(module_object)
            else:
                module_attributes.append(_atribute_labeller(imported_module, callable_name, module_object))
        with Heading(document, "Module Attributes"):
            document.list(module_attributes)
        with Heading(document, "Module Callables"):
            for module_callable in module_callables:
                _module_callable_builder(document, module_callable)
