"""Helper functions."""
from __future__ import annotations

import importlib
import inspect

from docstring_parser import parse

from ..generator import MarkdownBuilder


class ClassDocBlock:
    """Class documentation helper"""

    def __init__(self, doc: MarkdownBuilder, module: str, name: str):
        self.doc = doc
        self.class_ = self._get_class(module, name)
        self.render_class(name, self.class_)

    @staticmethod
    def _get_class(module, name):
        module = importlib.import_module(module)
        return getattr(module, name)

    def _render_method(self, obj, attr):
        doc_string = inspect.getdoc(getattr(obj, attr))
        if doc_string:
            parsed = parse(doc_string)
        doc = self.doc
        with doc.heading(f"Method: `{attr}`"):
            spec = str(inspect.signature(getattr(obj, attr)))
            doc.text.paragraph(f"**Signature**: `{spec}`")
            if parsed:
                if parsed.short_description:
                    doc.text.paragraph(parsed.short_description)
                if parsed.long_description:
                    doc.text.paragraph(parsed.long_description)
                with doc.heading("Arguments"):
                    with doc.list.unordered_list() as params:
                        for param in parsed.params:
                            params.append(
                                f"`{param.arg_name}` _({param.type_name})_ - {param.description}"
                            )
                with doc.heading("Returns"):
                    with doc.list.unordered_list(
                        "_(None)_ - Implicit return."
                    ) as returns:
                        for ret in parsed.many_returns:
                            returns.append(f"_({ret.type_name})_ - {ret.description}")

    def _render_attribute(self, obj, attr):
        with self.doc.list.unordered_list() as attrs:
            attrs.append(f"**{attr}**")
            with self.doc.list.unordered_list() as at:
                at.append(f"_Type_: `{getattr(obj, attr).__class__.__name__}`")
                at.append(f"_Default_: `{getattr(obj, attr)}`")

    def render_class(self, name, obj):
        doc = self.doc
        attributes = []
        methods = []
        with self.doc.heading(name):
            doc.text.paragraph(inspect.getdoc(obj))
            for attr in [a for a in dir(obj) if not a.startswith("__")]:
                if callable(getattr(obj, attr)):
                    methods.append((obj, attr))
                if not callable(getattr(obj, attr)):
                    attributes.append((obj, attr))
            if attributes:
                with doc.heading("Attributes"):
                    for attribute in attributes:
                        self._render_attribute(*attribute)
            if methods:
                for method in methods:
                    self._render_method(*method)
            doc.horizontal_bar()
