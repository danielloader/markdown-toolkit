from __future__ import annotations
from typing import Optional
from contextlib import contextmanager


def bold(string):
    return f"**{string}**"


def header(level, heading):
    return f"{'#'*level} {heading}"


class MarkdownList:
    def __init__(self, document: MarkdownDocument):
        self.doc = document

    def __enter__(self):
        self.doc.indent_level += 1
        self.doc.list_level += 1

    def __exit__(self, *args):
        self.doc.indent_level -= 1
        self.doc.list_level -= 1


class MarkdownHeading:
    def __init__(
        self,
        document: MarkdownDocument,
        heading: str,
        silent=False,
        level: Optional[int] = None,
    ):
        print(locals())
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
        print(level)
        return f"{'#'*level} {self.heading}"


class MarkdownDocument:
    def __init__(self):
        self.buffer: list[str] = []
        self.line_buffer: list[str] = []
        self.indent_level: int = -1
        self.list_level: int = -1
        self.heading_level = 1
        self.nl: str = "\n"

    @property
    def _in_list(self):
        if self.indent_level > -1:
            return True
        return False

    @property
    def _indent(self):
        if self._in_list:
            return " " * (self.indent_level * 4 + 4)
        return " " * (self.indent_level * 4)

    def heading(
        self,
        heading: Optional[str] = None,
        silent: bool = False,
        level: Optional[int] = None,
    ):
        return MarkdownHeading(self, heading=heading, silent=silent, level=level)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        print(self.buffer)

    def list(self):
        return MarkdownList(self)


    @contextmanager
    def padding(self):
        yield
        self.buffer.append(self.nl)

    def unordered_item(self, item):
        self.buffer.append(f"{' '*self.indent_level*4}{'*'.ljust(4)}{item}  ")

    def ordered_item(self, item):
        self.buffer.append(f"{' '*self.indent_level*4}{'1.'.ljust(4)}{item}  ")

    def raw(self, string):
        self.buffer.append(string)

    def text(self, string):
        self.buffer.append(f"{self._indent}{string}")

    def paragraph(self, string):
        with self.padding():
            self.text(string)


with MarkdownDocument() as doc:
    with doc.heading("Title"):
        with doc.list():
            doc.unordered_item(doc.heading("List Subtitle"))
            doc.paragraph(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ac odio euismod, sodales ipsum id, scelerisque nisl. Etiam erat odio, faucibus ut augue nec, tristique imperdiet ligula. Sed lacinia massa sed ante facilisis, eu finibus arcu fermentum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Morbi commodo, urna sit amet gravida luctus, nunc mauris aliquam orci, non laoreet lectus nulla sed mi. Nulla consectetur et tortor vel lacinia. Donec hendrerit condimentum ante id aliquet. Aenean condimentum nisl at ultrices ultricies. Donec ullamcorper nisl quis consectetur accumsan. Fusce posuere velit a augue bibendum tincidunt. Nullam suscipit turpis velit. Aenean a porttitor lorem. In sodales turpis in placerat egestas. Phasellus eros lectus, pharetra non augue at, vestibulum feugiat dolor."
            )
            doc.paragraph(
                "Interdum et malesuada fames ac ante ipsum primis in faucibus. Etiam luctus mollis lacus ac luctus. Praesent justo mauris, lacinia ut neque vel, semper viverra ipsum. Nulla facilisi. Proin gravida augue eget blandit tincidunt. Nullam viverra iaculis semper. Nam quis turpis varius, euismod dui ac, rhoncus orci."
            )
        with doc.list():
            doc.unordered_item(doc.heading("List Subtitle"))
            doc.paragraph(
                "Example of a paragraph explaining a nested ordered list below."
            )
            with doc.list():
                doc.ordered_item(bold("Bold List Item"))
                doc.paragraph(
                    "Mauris vel magna id ipsum consequat vulputate. Nulla id turpis non eros tincidunt aliquet eleifend id orci. Proin leo odio, finibus nec fermentum vitae, bibendum sed eros. Sed sapien lectus, euismod vitae risus in, lobortis rutrum purus. Proin at velit ut risus euismod aliquam. Donec vitae iaculis mi. Etiam quis aliquet ligula. Ut gravida velit ac porttitor sagittis. Donec pretium lacus in nibh malesuada, at rutrum mi sollicitudin. Sed maximus sodales elit non egestas. Curabitur nec efficitur libero. Nullam mattis euismod ligula nec cursus."
                )
                doc.ordered_item(bold("Bold List Item"))
                doc.ordered_item(bold("Bold List Item"))


with open("WhatamIdoing.md", "w") as file:
    file.write("\n".join(doc.buffer))
