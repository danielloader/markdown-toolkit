"""Markdown Toolkit document injector."""
from __future__ import annotations

import re
from collections import defaultdict
from typing import TextIO

from markdown_toolkit.utils import sanitise_attribute


class DocumentInjector:
    """Class for injected text into Markdown Documents."""

    class Inject:
        """Inject text between start and end lines."""

        def __init__(self, file_buffer, start, end):
            self.file_buffer: list = file_buffer
            self.start = start
            self.end = end

        def read(self) -> str:
            """Return text between anchors."""
            return "".join(self.file_buffer[self.start : self.end - 1])

        def write(self, text: str):
            """Replace text between anchors."""
            del self.file_buffer[self.start : self.end - 1]
            self.file_buffer.insert(self.start, text)

    def __init__(
        self,
        file_obj: TextIO,
    ):

        self.file_buffer: list[str] = file_obj.read().splitlines()
        self._find_tags()
        self.tags = {}

    def render(self, trailing_whitespace=False) -> str:
        """Renders document to string.

        Returns:
            str: Rendered document.
        """
        document = "\n".join(self.file_buffer)
        if trailing_whitespace:
            return document + "\n"
        return document

    def __getattr__(self, attr):
        raise ValueError(attr)

    def _find_tags(self):
        tags = defaultdict(dict)

        for idx, line in enumerate(self.file_buffer):
            if line.startswith("<!--"):
                start = re.match(r"^<!--.*markdown-toolkit:start:(.*).*-->$", line)
                end = re.match(r"^<!--.*markdown-toolkit:end:(.*).*-->$", line)
                if start:
                    anchor = start.groups()[0].strip()
                    if "start" in tags[anchor]:
                        raise ValueError()
                    tags[anchor]["start"] = idx + 1
                if end:
                    anchor = end.groups()[0].strip()
                    if "end" in tags[anchor]:
                        raise ValueError()
                    tags[anchor]["end"] = idx + 1

        ranges = []
        for lines in tags.values():
            ranges.append(set(range(lines["start"], lines["end"])))
        if len(ranges) > 1:
            overlaps = set.intersection(*ranges)
            if overlaps:
                raise IndexError("Overlapping anchors", overlaps)

        self.tags = tags
        for anchor, lines in tags.items():
            setattr(
                self,
                sanitise_attribute(anchor),
                self.Inject(self.file_buffer, lines["start"], lines["end"]),
            )
