"""Markdown Toolkit main classes."""
from __future__ import annotations
from collections import defaultdict
from typing import Optional, Union
from inspect import cleandoc
from contextlib import contextmanager
from pathlib import Path
import re

from .utils import code, from_file, header, list_item


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

    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)
        with open(self.path, "r", encoding="UTF-8") as file:
            self.file_buffer: list[str] = file.readlines()
        self._find_tags()
        self.tags = {}

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
        overlaps = set.intersection(*ranges)
        if overlaps:
            raise IndexError("Overlapping anchors", overlaps)

        self.tags = tags
        for anchor, lines in tags.items():
            setattr(
                self,
                anchor,
                self.Inject(self.file_buffer, lines["start"], lines["end"]),
            )


class MarkdownDocument:
    """Markdown document builder class."""

    class _MarkdownList:
        def __init__(
            self,
            item: str,
            document: MarkdownDocument,
            ordered: bool = False,
            prefix: Optional[str] = None,
        ):
            self.doc = document
            self.doc.text(list_item(ordered=ordered, item=item, prefix=prefix))

        def __enter__(self):
            self.doc._indent_level += 1
            self.doc._list_level += 1

        def __exit__(self, *args):
            self.doc._indent_level -= 1
            self.doc._list_level -= 1

    class _MarkdownTable:
        """Table renderer."""

        def __init__(self, document: MarkdownDocument, titles: list):
            self.doc = document
            self.titles = titles
            self.rows = []

        def add_row(self, columns: list):
            """Add row to table helper.

            Args:
                columns (list): List if elements to add.
            """
            self.rows.append(columns)

        def _render(self):
            buffer = []
            buffer.append(" | ".join(self.titles))
            buffer.append(" | ".join(["---" for _ in range(len(self.titles))]))
            for row in self.rows:
                buffer.append(" | ".join(row))

            return "\n".join(buffer)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.doc.paragraph(self._render())
            self.doc.text()

    class _MarkdownHeading:
        """Heading context manager."""

        def __init__(
            self,
            document: MarkdownDocument,
            heading: str,
            silent=False,
            level: Optional[int] = None,
        ):
            self.doc = document
            self.heading = heading
            self.silent = silent
            self.level = level

        def __enter__(self):
            if not self.silent:
                self.doc._buffer.append(self.__str__())
                self.doc.linebreak()
            if not self.level:
                self.doc._heading_level += 1
            return self

        def __exit__(self, *args):
            if not self.level:
                self.doc._heading_level -= 1

        def __str__(self) -> str:
            """String representation.

            Returns:
                str: Representation of class as string.
            """
            level = self.level or self.doc._heading_level
            return header(self.heading, level)

    def __init__(self, newline_character: str = "\n"):
        self._buffer: list[str] = []
        self._indent_level: int = -1
        self._list_level: int = -1
        self._heading_level = 1
        self._newline_character: str = newline_character

    @property
    def _in_list(self) -> bool:
        """Helper method to tell if inside a list context.

        Returns:
            bool: In list or not.
        """
        if self._indent_level > -1:
            return True
        return False

    @property
    def _indent(self) -> str:
        """Helper method to indent text in document context.

        Returns:
            str: Indented text.
        """
        indent_muliplier = self._indent_level * 4
        if self._in_list:
            indent_muliplier += 4
        return " " * indent_muliplier

    def heading(
        self,
        heading: Optional[str] = None,
        silent: bool = False,
        level: Optional[int] = None,
    ):
        """_summary_

        Args:
            heading (Optional[str], optional): Text to head with. Defaults to None.
            silent (bool, optional): Increment heading level silently. Defaults to False.
            level (Optional[int], optional): Override heading level. Defaults to None.
        """
        return self._MarkdownHeading(self, heading=heading, silent=silent, level=level)

    def table(self, titles: list) -> _MarkdownTable:
        """Table rendering helper.

        Args:
            titles (list): List of titles for the columns.

        Returns:
            _MarkdownTable: Object with helper methods.
        """
        return self._MarkdownTable(self, titles=titles)

    def list(self, item: str, ordered: bool = False, prefix: Optional[str] = None):
        return self._MarkdownList(
            item=item, ordered=ordered, document=self, prefix=prefix
        )

    @contextmanager
    def codeblock(self, language: str = ""):
        """Codeblock context manager."""
        self.text("```" + language)
        yield
        self.text("```")

    @contextmanager
    def indentblock(self):
        self._indent_level += 1
        yield
        self._indent_level -= 1

    def add(self, text):
        """Unmodified text injection into document."""
        self._buffer.append(text)

    def text(self, text: str = ""):
        """Add text to document, taking into account indent level."""
        self._buffer.append(f"{self._indent}{text}")

    def paragraph(self, text: str, linebreak: Union[int, bool] = True):
        """Add triplequote python multiline strings to document."""
        buffer = cleandoc(text).split("\n")
        for line in buffer:
            self.text(line)
        if linebreak:
            for _ in range(int(linebreak)):
                self.linebreak()

    def linebreak(self):
        """Adds a linebreak to the document."""
        self.add("")

    def horizontal_line(self):
        """Add horizontal line to document."""
        self.text()
        self.text("----")
        self.text()

    def render(self, trailing_whitespace=False) -> str:
        """Renders document to string.

        Returns:
            str: Rendered document.
        """
        document = "\n".join(self._buffer)
        if trailing_whitespace:
            return document + "\n"
        return document
