"""Markdown Toolkit main classes."""
from __future__ import annotations

from contextlib import contextmanager
from inspect import cleandoc
from typing import Optional, Union
import itertools
from markdown_toolkit.utils import (
    header,
    list_item,
    sanitise_attribute,
    remove_duplicates,
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

        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.doc._indent_level -= 1
            self.doc._list_level -= 1

    class _MarkdownTable:
        """Table renderer."""

        def __init__(
            self,
            document: MarkdownDocument,
            titles: list,
            sort_by: Optional[str] = None,
        ):
            self.doc = document
            self.titles = titles
            self.normalized_titles = list(map(sanitise_attribute, titles))
            self.column_count = len(self.normalized_titles)
            self.rows = []
            self.sort_by = titles.index(sort_by) if sort_by else None

        def bulk_add_rows(self, rows: list[dict]):
            for row in rows:
                row_buffer = []
                for title in self.titles:
                    row_buffer.append(str(row[title]))
                self.rows.append(row_buffer)

        def add_row(self, **columns):
            """Add row to table helper."""
            if columns is None:
                raise ValueError("No data submitted.")
            for column in columns:
                if column not in self.normalized_titles:
                    raise ValueError("Column not found in headers.")
            row_buffer = []
            for title in self.normalized_titles:
                row_buffer.append(str(columns.get(title, "")))
            self.rows.append(row_buffer)

        def _render(self):
            buffer = []
            buffer.append("| " + " | ".join(self.titles) + " |")
            buffer.append(
                "| " + " | ".join(["---" for _ in range(self.column_count)]) + " |"
            )
            if self.sort_by:
                self.rows.sort(key=lambda x: x[self.sort_by])
            for row in self.rows:
                buffer.append("| " + " | ".join(row) + " |")

            return "\n".join(buffer)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.doc.paragraph(self._render())

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

        def __exit__(self, exc_type, exc_value, exc_traceback):
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

    def table(
        self,
        raw_table: Optional[list[dict]] = None,
        *,
        titles: Optional[list] = None,
        sort_by: Optional[str] = None,
    ) -> _MarkdownTable:
        """Table rendering helper.

        Args:
            titles (list): List of titles for the columns.

        Returns:
            _MarkdownTable: Object with helper methods.
        """
        if not raw_table:
            return self._MarkdownTable(self, titles=titles, sort_by=sort_by)
        all_titles = remove_duplicates(
            itertools.chain(*[dictionary.keys() for dictionary in raw_table])
        )
        with self._MarkdownTable(self, titles=all_titles, sort_by=sort_by) as table:
            table.bulk_add_rows(raw_table)

    def list(self, item: str, ordered: bool = False, prefix: Optional[str] = None):
        """Returns list context manager, can be used directly."""
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
        """Returns indented context manager."""
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

    @contextmanager
    def injector(self, anchor: str):
        """Add inline comment to use as an injector anchor."""
        self.text(f"<!--- markdown-toolkit:start:{anchor} --->")
        yield
        self.text(f"<!--- markdown-toolkit:end:{anchor} --->")

    def render(self, trailing_whitespace=False) -> str:
        """Renders document to string.

        Returns:
            str: Rendered document.
        """
        document = "\n".join(self._buffer)
        if trailing_whitespace:
            return document + "\n"
        return document
