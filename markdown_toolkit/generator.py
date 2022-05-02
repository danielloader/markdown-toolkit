from __future__ import annotations

import logging
import re
from contextlib import contextmanager
from textwrap import dedent

logger = logging.Logger(__name__)


class MarkdownInjector:
    def __init__(self, path: str, anchor: str, encoding: str = "UTF-8") -> None:
        self.path = path
        self.file_buffer = []
        self.encoding = encoding
        self.start = 0
        self.partial: tuple(list, list) = ([], [])
        self.end = 0
        self.anchor = anchor

    def find_anchors(self, anchor):
        matching_line_numbers = []
        for idx, line in enumerate(self.file_buffer):
            if line.startswith("<!--"):
                if re.match(rf"^<!--.*(markdown-toolkit):({anchor}*).*-->$", line):
                    matching_line_numbers.append(idx)
        if len(matching_line_numbers) != 2:
            raise ValueError(
                "More than two anchors of the same id found in source document"
            )
        self.start = min(matching_line_numbers) + 1
        self.end = max(matching_line_numbers)

    def writelines(self, lines: list[str]):
        print(lines)
        self.new_document = self.partial[0] + lines + self.partial[1]
        print(self.new_document)

    @property
    def start_line(self):
        return self.start + 1

    @property
    def end_line(self):
        return self.end

    def __enter__(self):
        with open(self.path, "r", encoding=self.encoding) as file:
            self.file_buffer: list[str] = file.readlines()
            print(self.file_buffer)
        self.find_anchors(self.anchor)
        self.partial = (self.file_buffer[: self.start], self.file_buffer[self.end :])
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass
        if self.new_document:
            with open(self.path, "w") as file:
                file.writelines(self.new_document)


def from_file(path, start=None, end=None):
    with open(path, "r", encoding="UTF-8") as file:
        lines = file.readlines()
    lines_needed = lines[start:end]
    return "".join(lines_needed)


class MarkdownList:
    class UnorderedList:
        def __init__(self, document: MarkdownBuilder):
            self.buffer = []
            self.doc = document

        def add(self, item: str):
            self.buffer.append(f"* {item}")

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            if self.buffer:
                with self.doc.padding():
                    for item in self.buffer:
                        self.doc._buffer.append(item)
                        self.doc.newline()

    def __init__(self, document: MarkdownBuilder):
        self.doc = document

    def unordered_list(self):
        return self.UnorderedList(self.doc)


class MarkdownText:
    def __init__(self, document: MarkdownBuilder):
        self.doc = document

    def heading(self, text: str, level: int):
        header_prefix = "".join(["#" for _ in range(level)])
        with self.doc.padding(after=2):
            self.doc._buffer.append(f"{header_prefix} {text}")

    def raw(self, text: str):
        self.doc._buffer.append(text)

    def italic(self, text: str):
        self.doc._buffer.append(f"_{text}_")

    def bold(self, text: str):
        self.doc._buffer.append(f"__{text}__")

    def important(self, text: str):
        self.doc._buffer.append(f"***{text}***")

    def strikethrough(self, text: str):
        self.doc._buffer.append(f"~~{text}~~")

    def quote(self, text: str):
        self.doc._buffer.append(f"> {text}")

    def paragraph(self, text: str, padding: int = 1):
        with self.doc.padding(after=padding):
            self.raw(dedent(str(text)))
            self.doc.newline()


class MarkdownBuilder:
    """Document class for building Markdown documents."""

    def __init__(self, newline_character="\n"):
        self._newline_character = newline_character
        self._buffer = []
        self._heading_level = 0
        self.print_on_exit = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.print_on_exit:
            print(self._buffer)
            document = "".join(self._buffer)
            print(document)

    def write(self, filelike_object):
        """Write document buffer to filelike object."""
        filelike_object.writelines(self._buffer)

    def newline(self):
        """Add newline to document."""
        self._buffer.append(self._newline_character)

    @contextmanager
    def padding(self, before: int = 0, after: int = 1):
        for _ in range(before):
            self.newline()
        yield
        for _ in range(after):
            self.newline()

    @contextmanager
    def heading(self, text):
        self._heading_level = self._heading_level + 1
        if self._heading_level > 6:
            logger.warning(
                "Header depth (%s) greater than 6 - This can render incorrectly.",
                self._heading_level,
            )
        self.text.heading(text, self._heading_level)
        yield
        self._heading_level = self._heading_level - 1

    @property
    def text(self):
        """Method providing helper methods for adding various textual items."""
        return MarkdownText(self)

    def image(self, title: str, uri: str):
        """Add an image to the document."""
        image = f"![{title}]({uri})"
        with self.padding(after=1):
            self._buffer.append(image)

    def link(self, title: str, uri: str):
        """Add an link to the document."""
        link = f"[{title}]({uri})"
        self._buffer.append(link)

    @property
    def list(self):
        return MarkdownList(self)
        # """Add lists to document."""
        # list_seperator = "1." if ordered else "*"
        # list_items = [f"{list_seperator} {item}" for item in items]
        # with self.padding(after = 1):
        #     self._buffer.extend(list_items)

    def code(self, source: str, language=""):
        """Add codeblock to document."""
        with self.padding(before=1, after=1):
            self._buffer.append(f"```{language}")
            self.newline()
            self._buffer.append(dedent(source))
            self.newline()
            self._buffer.append("```")

    def horizontal_bar(self):
        """Add horizontal bar to document."""
        with self.padding(after=2):
            self._buffer.append("#")

    def warning(self, message: str):
        """Add warning block to document."""
        with self.padding(after=2):
            self._buffer.append(f"> **WARNING**: _{message}_")

    def info(self, message: str):
        """Add info block to document."""
        with self.padding(after=2):
            self._buffer.append(f"> **INFO**: _{message}_")
