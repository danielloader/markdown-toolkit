"""Helper functions."""
from __future__ import annotations

import importlib
import inspect

from docstring_parser import parse

from .generator import MarkdownBuilder


class ClassDocBlock:
    def __init__(self, doc: MarkdownBuilder, module: str, name: str):

        self.doc = doc
        self.class_ = self._get_class(module, name)
        with self.doc.heading(name):
            self.render_class(self.class_)

    @staticmethod
    def _get_class(module, name):
        module = importlib.import_module(module)
        return getattr(module, name)

    def _render_method(self, obj, attr, parsed):
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
                            params.add(
                                f"`{param.arg_name}` _{param.type_name}_ - {param.description}"
                            )
                with doc.heading("Returns"):
                    with doc.list.unordered_list() as returns:
                        for ret in parsed.many_returns:
                            returns.add(f"_{ret.type_name}_ - {ret.description}")
                        if len(returns.buffer) == 0:
                            returns.add("None")

                    # doc.code(doc_string)
            self.doc.horizontal_bar()

    def _render_attribute(self, obj, attr, parsed):
        return f"**{attr}** _{getattr(obj, attr).__class__.__name__}_ `{getattr(obj, attr)}`"

    def render_class(self, obj):
        doc = self.doc
        attributes = []
        methods = []
        doc.text.paragraph(inspect.getdoc(obj))
        for attr in [a for a in dir(obj) if not a.startswith("__")]:
            doc_string = inspect.getdoc(getattr(obj, attr))
            if doc_string:
                parsed = parse(doc_string)
            if callable(getattr(obj, attr)):
                methods.append((obj, attr, parsed))
            if not callable(getattr(obj, attr)):
                attributes.append((obj, attr, parsed))
        if attributes:
            with doc.heading("Attributes"):
                with doc.list.unordered_list() as attrs:
                    for attribute in attributes:
                        attrs.add(self._render_attribute(*attribute))
        if methods:
            for method in methods:
                self._render_method(*method)
