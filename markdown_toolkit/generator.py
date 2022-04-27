from __future__ import annotations


class Padding:
    """Add newlines around objects."""
    def __init__(self, document: MarkdownBuilder, pre=0, suf=1):
        self.document = document
        self.pre = pre
        self.suf = suf

    def __enter__(self):
        for _ in range(self.pre):
            self.document.newline()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for _ in range(self.suf):
            self.document.newline()


class Heading:
    """Add nested Heading to document."""
    def __init__(self, document: MarkdownBuilder, header: str):
        self.document = document
        self.header = header

    def __enter__(self):
        self.document.heading_level = self.document.heading_level + 1
        header_prefix = "".join(
            ["#" for _ in range(self.document.heading_level)])
        # with Padding(self.document):
        self.document.buffer.append(f"{header_prefix} {self.header}")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.document.heading_level = self.document.heading_level - 1


class MarkdownBuilder:
    """Document class for building Markdown documents."""
    def __init__(self, newline_character="\n"):
        self.newline_character = newline_character
        self.buffer = []
        self.heading_level = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("\n".join(self.buffer))

    def write(self, filelike_object):
        """Write document buffer to filelike object."""
        filelike_object.write(self.newline_character.join(self.buffer))

    def newline(self):
        """Add newline to document."""
        self.buffer.append(self.newline_character)

    def text(self, text: str):
        """Add text to document."""
        self.buffer.append(text)

    def paragraph(self, text: str):
        """Add pargraph to document."""
        with Padding(self):
            self.text(text)

    def image(self, title: str, uri: str):
        """Add an image to the document."""
        image = f"![{title}]({uri})"
        with Padding(self):
            self.buffer.append(image)

    def link(self, title: str, uri: str):
        """Add an link to the document."""
        link = f"[{title}]({uri})"
        self.buffer.append(link)

    def list(self, items, ordered=False):
        # with Padding(self):
        list_seperator = "1." if ordered else "*"
        list_items = [f"{list_seperator} {item}" for item in items]
        self.buffer.extend(list_items)

