from __future__ import annotations
from collections import defaultdict
from typing import Optional, Union
from contextlib import contextmanager
from pathlib import Path
import re


def bold(text: str) -> str:
    """Bold wrapper."""
    return f"**{text}**"


def italic(text: str) -> str:
    """Bold wrapper."""
    return f"_{text}_"


def strikethrough(text: str) -> str:
    """Strikethrough wrapper."""
    return f"~~{text}~~"


def header(level, heading: str) -> str:
    """Heading wrapper."""
    return f"{'#'*level} {heading}"


def image(uri: str, title: Optional[str] = None):
    """Add an image to the document."""
    return f"![{title or uri}]({uri})"


def link(self, uri: str, title: Optional[str] = None):
    """Add an link to the document."""
    return f"[{title or uri}]({uri})"


class DocumentInjector:
    class Inject:
        def __init__(self, file_buffer, start, end):
            self.file_buffer:list = file_buffer
            self.start = start
            self.end = end
        
        def read(self):
            return "".join(self.file_buffer[self.start: self.end-1])

        def write(self, text):
            del self.file_buffer[self.start: self.end-1]
            self.file_buffer.insert(self.start, text)

    def __init__(self, path: Union[Path,str]):
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
                    id = start.groups()[0].strip()
                    if "start" in tags[id]:
                        raise ValueError()
                    tags[id]["start"] = idx+1
                if end:
                    id = end.groups()[0].strip()
                    if "end" in tags[id]:
                        raise ValueError()
                    tags[id]["end"] = idx+1
        
        ranges = []
        for lines in tags.values():
            ranges.append(set(range(lines["start"], lines["end"])))
        overlaps= set.intersection(*ranges)
        if overlaps:
            raise IndexError("Overlapping anchors", overlaps)
        
        self.tags = tags
        for id, lines in tags.items():
            setattr(self, id, self.Inject(self.file_buffer, lines["start"], lines["end"]))


class MarkdownDocument:
    class MarkdownHeading:
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
                self.doc.buffer.append(self.__str__())
            if not self.level:
                self.doc.heading_level += 1
            return self

        def __exit__(self, *args):
            if not self.level:
                self.doc.heading_level -= 1

        def __str__(self) -> str:
            level = self.level or self.doc.heading_level
            return f"{'#'*level} {self.heading}"

    def __init__(self):
        self.buffer: list[str] = []
        self.line_buffer: list[str] = []
        self.indent_level: int = -1
        self.list_level: int = -1
        self.heading_level = 1
        self.newline_character: str = "\n"

    @property
    def _in_list(self):
        if self.indent_level > -1:
            return True
        return False

    @property
    def _indent(self):
        indent_muliplier = self.indent_level * 4
        if self._in_list:
            indent_muliplier += 4
        return " " * indent_muliplier

    def heading(
        self,
        heading: Optional[str] = None,
        silent: bool = False,
        level: Optional[int] = None,
    ):
        return self.MarkdownHeading(self, heading=heading, silent=silent, level=level)

    @property
    @contextmanager
    def list(self):
        self.indent_level += 1
        self.list_level += 1
        yield
        self.indent_level -= 1
        self.list_level -= 1

    @contextmanager
    def padding(self, lines=1):
        yield
        self.buffer.extend([self.newline_character for _ in range(lines)])

    def unordered_item(self, item):
        self.buffer.append(f"{' '*self.indent_level*4}{'*'.ljust(4)}{item}  ")

    def ordered_item(self, item):
        self.buffer.append(f"{' '*self.indent_level*4}{'1.'.ljust(4)}{item}  ")

    def raw(self, text):
        self.buffer.append(text)

    def text(self, text):
        self.buffer.append(f"{self._indent}{text}")

    def paragraph(self, text):
        with self.padding():
            self.text(text)

    def render(self) -> str:
        return "\n".join(self.buffer) + "\n"

