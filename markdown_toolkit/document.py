"""Markdown Toolkit main classes."""
from __future__ import annotations

import itertools
from contextlib import contextmanager
from inspect import cleandoc
from io import StringIO
from typing import Optional, Union

from markdown_toolkit.utils import (
    fileobj_open,
    header,
    list_item,
    remove_duplicates,
    sanitise_attribute,
)


class MarkdownDocument:
    """Markdown document builder class.

    The purpose of this class is to generate markdown programatically with an
    object oriented interface.

    The document is created by initalising this class:
    ```python
    doc = MarkdownDocument()
    ```

    From here the object has methods to manipulate the document.
    """

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
            """Bulk add rows from a list of dicts."""
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
            else:
                self.doc._heading_level = self.level + 1
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
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
    ) -> _MarkdownHeading:
        """Adds a Markdown Heading to the document.

        There's two entrypoints using this method:

        * As a context manager:
            This is used if you want to use nested headings, in a heading level aware
            context.

            Repeatedly nesting more headings increases the heading level.

            ```python
            with doc.heading("Title"):
                text.paragraph("Blurb under the title heading")
            ```

        * As a document element:
            This is used to inject a heading as is, at the current document header level,
            or if the level argument is used, at a specific level.

            ```python
            doc.header("Sub Sub Heading", level=3)
            ```


        Args:
            heading (Optional[str], optional): Text to be used as a heading. Defaults to None.
            silent (bool, optional): Skip printing the heading. Defaults to False.
            level (Optional[int], optional): Static level to assign to the heading. Defaults to None.

        Returns:
            _MarkdownHeading: Heading object.
        """

        return self._MarkdownHeading(self, heading=heading, silent=silent, level=level)

    def table(
        self,
        raw_table: Optional[list[dict]] = None,
        *,
        titles: Optional[list] = None,
        sort_by: Optional[str] = None,
    ) -> _MarkdownTable:
        """Adds a Markdown Table to the document.

        This method produces github flavoured markdown tables.

        There's two entrypoints using this method:

        * As a context manager:
            This is if you do not want to wrangle a large dataset in one go, so
            you can lazy add to the table row at a time.

            You have to define the table title headings at initialisation time.

            ```python
            with doc.table(titles=["example","headings]) as table:
                table.add_row(example="abc", headings="123")
            ```

        * As a document element:
            This is if you have a list of dictionaries and you just want to render them
            using the dictionary key value pairs.

            ```python
            doc.table(
                [
                    {"key": 123, "value": "example"},
                    {"key": 456, "value": "another field"}
                ]
            )
            ```

        Args:
            raw_table (Optional[list[dict]], optional): Raw table to render. Defaults to None.
            titles (Optional[list], optional): Table titles. Defaults to None.
            sort_by (Optional[str], optional): Table title to sort by. Defaults to None.

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
        return None

    def list(
        self, item: str, ordered: bool = False, prefix: Optional[str] = None
    ) -> _MarkdownList:
        """Adds a Markdown List to the document.

        This method produces ordered and unordered lists.

        There's two entrypoints using this method:

        * As a context manager:
            This method creates a nested list context.

            The context manager creates a new list item, but inside the with block
            any new created lists will be children of this list.

            ```python
            with doc.list("Parent Item"):
                doc.list("Child Item")
            ```

        * As a document element:
            This method creates a list item as is, at the current document indentation
            level.

            ```python
            doc.list("List item", ordered=True)
            ```

        Args:
            item (str): List item string to be used.
            ordered (bool, optional): If the list is ordered or not. Defaults to False.
            prefix (Optional[str], optional): Custom prefix on list items. Defaults to None.

        Returns:
            _MarkdownList: _description_
        """
        return self._MarkdownList(
            item=item, ordered=ordered, document=self, prefix=prefix
        )

    @contextmanager
    def collapsed(self, summary: str):
        """Adds collapsable section to the document.

        Uses html tags to add a details block, with summary.

        Args:
            summary (str): Summary for the collapsed block..
        """
        self.linebreak()
        self.text("<details><summary>" + summary + "</summary>")
        self.linebreak()
        yield
        self.text("</details>")
        self.linebreak()

    @contextmanager
    def codeblock(self, language: str = ""):
        """Codeblock context manager.

        Wraps paragraphs in codeblock backticks with optional syntax highlighting.

        ```python
        with doc.codeblock(language="python"):
            doc.paragraph(
            \"""
            for i in range(100):
                print(i)
            \"""
            )
        ```

        Args:
            language (str): Syntax highlighting language.
        """
        self.text("```" + language)
        yield
        self.text("```")

    @contextmanager
    def indentblock(self):
        """Returns indented context manager.

        All elements defined in this with section will be indented.

        ```python
        with doc.indentblock():
            doc.text("This text will be indented by 4 spaces")
        ```
        """
        self._indent_level += 1
        yield
        self._indent_level -= 1

    def add(self, text: str):
        """Unmodified raw string injection into the document.

        Args:
            text (str): Text to inject.
        """
        self._buffer.append(text)

    def text(self, text: str = ""):
        """Add text to document, taking into account indent level.

        Args:
            text (str, optional): Text to add to the document. Defaults to "".
        """

        self._buffer.append(f"{self._indent}{text}")

    def paragraph(self, text: str, linebreak: Union[int, bool] = True):
        """Adds a paragraph to the document.

        This differs from adding `text` to the document in the `text` method in a few ways:

        * By default it adds a linebreak after the text to force a
        paragraph break in the document.
        * It uses the cleandoc function to clean multitline indentation whitespace up.

        Args:
            text (str): Text to add to the document.
            linebreak (Union[int, bool], optional): Enables the trailing linebreak. Defaults to True.
        """
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
        """Add inline comment to use as an injector anchor.

        Using and abusing html comments, as they are not rendered in markdown.

        Renders `<!--- markdown-toolkit:anchor --->` tags into the document.

        Args:
            anchor (str): Unique identifier string for the anchor.
        """
        self.text(f"<!--- markdown-toolkit:{anchor} --->")
        yield
        self.text(f"<!--- markdown-toolkit:{anchor} --->")

    def render(self, trailing_whitespace=False) -> str:
        """Renders document to multiline string.

        Args:
            trailing_whitespace (bool, optional): Add linebreak to the end of the document.
                Defaults to False.

        Returns:
            str: Rendered document.
        """
        document = "\n".join(self._buffer)
        if trailing_whitespace:
            return document + "\n"
        return document

    def write(self, file: Union[str, StringIO]):
        """Helper method to write the document contents to a file or filelike object.

        Args:
            file (Union[str, StringIO]): Path to file, or filelike object already opened.
        """
        with fileobj_open(file) as file_object:
            file_object.write(self.render())
