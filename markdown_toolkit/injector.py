"""Markdown Toolkit document injector."""
from __future__ import annotations

import re
from collections import defaultdict
from types import SimpleNamespace
from typing import TextIO, Optional, List

from markdown_toolkit.utils import sanitise_attribute


class Anchors(SimpleNamespace):
    def __getattr__(self, __name: str) -> MarkdownAnchor:
        raise ValueError("Anchor '%s' not found", __name)


class MarkdownInjector:
    """Finds anchors in a markdown document and exposes
    the `anchors` attribute, which has sub attributes of all the valid
    anchors found in the document.

    Raises:
        ValueError: Can not find pair of anchors for each anchor defined.
    """

    matcher = re.compile(r".*<!---\s?markdown-toolkit:(.*)\s?--->.*")

    def __init__(self, file_obj: TextIO):
        self.file_buffer = file_obj.read().splitlines()
        self._anchors = self._find_anchors()

    @staticmethod
    def _find_overlaps(ranges: dict):
        for anchor, range_extents in ranges.items():
            if len(range_extents) != 2:
                raise ValueError("Failed to find matching tags")
            ranges[anchor] = set(range(range_extents[0], range_extents[1] + 1))
        if len(ranges.values()) < 2:
            return
        overlaps = set.intersection(*ranges.values())
        if overlaps:
            raise ValueError(f"Overlaps found at lines {[idx+1 for idx in overlaps]}")

    def _find_anchors(self) -> SimpleNamespace:
        """Finds pairs of anchors and returns a simple object.

        Each attribute of the namedtuple is an anchor, which returns
        a MarkdownAnchor class for that anchor.
        """
        anchors = Anchors()
        start_end_checker: dict[list] = defaultdict(list)
        for idx, line in enumerate(self.file_buffer):
            match = self.matcher.match(line)
            if match:
                anchor = match.groups()[0].strip()
                start_end_checker[anchor].append(idx)
        self._find_overlaps(start_end_checker)
        for anchor, line_numbers in start_end_checker.items():
            anchor_object = MarkdownAnchor(self, anchor)
            setattr(anchors, sanitise_attribute(anchor), anchor_object)
        return anchors

    @property
    def anchors(self) -> SimpleNamespace:
        """Returns anchors found as class attributes.

        Access to these anchors is done by way of standard dot object notation.

        ```python
        document.anchors.anchorname
        ```

        These anchor names are sanitised from strings using `sanitise_attribute` utility.

        Returns:
            SimpleNamespace: Class with MarkdownAnchor classes as attributes per anchor.
        """

        return self._anchors

    def render(self, trailing_whitespace: bool = False) -> str:
        """Renders the final document with modifications.

        Args:
            trailing_whitespace (bool, optional): Add whitespace to end of the document.
                Defaults to False.

        Returns:
            str: Rendered document.
        """

        document = "\n".join(self.file_buffer)
        if trailing_whitespace:
            return document + "\n"
        return document


class MarkdownAnchor:
    """This class represents the document object between two anchor points."""

    def __init__(self, document: MarkdownInjector, anchor: str):
        self.doc = document
        self.anchor = anchor
        self.matcher = re.compile(
            rf"(.*)<!---\s?markdown-toolkit:{self.anchor}\s?--->.*"
        )

    def __repr__(self) -> str:
        _start, _end, _indent, _value = self._index_finder()
        return (
            f"({self.__class__.__name__}={self.anchor}) "
            f"start={_start} end={_end} indent={_indent} value={_value}"
        )

    def _index_finder(self) -> tuple[int, int, str]:
        """Finds the current line index and value of text between them.

        Runs at on every access or mutation as the document may have changed.

        Returns:
            tuple(int, int, int, str): Start index, end index, indent and value of text.
        """
        start: Optional[int] = None
        end: Optional[int] = None
        indent: Optional[str] = None
        for idx, line in enumerate(self.doc.file_buffer):
            match = self.matcher.match(line)
            if match:
                if start is None:
                    start: int = idx
                    indent: str = match.groups()[0]
                else:
                    end: int = idx
                    return (start, end, indent, self.doc.file_buffer[start + 1 : end])
        raise ValueError("No matching anchor pair found in document")

    @property
    def start(self) -> int:
        """Start index of the tags.

        Note: Indexes are zero indexed, so line numbers are indexes + 1.

        Returns:
            int: List index value of the opening tag.
        """
        start, _, _, _ = self._index_finder()
        return start

    @property
    def end(self) -> int:
        """End index of the tags.

        Note: Indexes are zero indexed, so line numbers are indexes + 1.

        Returns:
            int: List index value of the closing tag.
        """
        _, end, _, _ = self._index_finder()
        return end

    @property
    def indent(self) -> int:
        """Indent level in spaces.

        Returns:
            int: Count of whitespace before tags.
        """
        _, _, indent, _ = self._index_finder()
        return len(indent)

    @property
    def value(self) -> str:
        """Text between the anchor comments.

        To read the value simply assign the value of this property:
        ```python
        text_between_anchors = document.anchors.anchorname.value
        ```

        To set the value, thereby overwriting the lines in the document
        between the anchors:
        ```python
        document.anchors.anchorname.value = "This text will replace the lines"
        ```

        Returns:
            str: Raw text between the anchors.
        """
        _, _, _, value = self._index_finder()
        text = "\n".join(value)
        return text.encode("UTF-8")

    @value.setter
    def value(self, text: str):
        start, end, indent, _ = self._index_finder()
        del self.doc.file_buffer[start + 1 : end]
        text_lines = "\n".join([indent + line for line in text.splitlines()])
        self.doc.file_buffer.insert(start + 1, text_lines)

    @value.deleter
    def value(self):
        start, end, _, _ = self._index_finder()
        del self.doc.file_buffer[start + 1 : end]
