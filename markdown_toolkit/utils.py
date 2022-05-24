"""Utilities for inline manipulating strings."""

import re
from contextlib import contextmanager
from inspect import cleandoc
from io import StringIO
from pathlib import Path
from typing import Optional, Union
from urllib.parse import quote as urlquote

from markdown_toolkit import constants

__all__ = [
    "badge",
    "bold",
    "code",
    "from_file",
    "header",
    "image",
    "italic",
    "link",
    "quote",
    "strikethrough",
]


def sanitise_attribute(string) -> str:
    """Converts any string into a safe python attribute string."""
    return re.sub(r"\W|^(?=\d)", "_", string.casefold())


def from_file(path: Union[Path, str], start: int = 1, end: int = None) -> str:
    """File reader helper.

    Args:
        path (Union[Path,str]): File path to open.
        start (int, optional): Start Line. Defaults to None.
        end (int, optional): End Line. Defaults to None.

    Returns:
        str: Text block.
    """
    with open(Path(path), "r", encoding="UTF-8") as file:
        return "".join(file.readlines()[start - 1 : end])


def badge(label: str, color: str, message: Optional[str] = None, alt: str = "") -> str:
    """Shields.io badge helper.

    Args:
        label (str): Badge label.
        color (str): Badge color.
        message (Optional[str], optional): Badge message. Defaults to None.
        alt (str, optional): Alt tag for the badge. Defaults to "".

    Returns:
        str: _description_
    """
    badge_url = (
        f"https://img.shields.io/static/v1?label="
        f"{urlquote(str(label))}&color={urlquote(str(color))}"
    )
    if message:
        badge_url += f"&message={urlquote(str(message))}"
    return link(uri="https://shields.io/", text=image(uri=badge_url, text=alt))


def list_item(item: str, ordered=False, prefix=None):
    """Returns a list item."""
    if not prefix:
        prefix = constants.ORDERED_LIST if ordered else constants.UNORDERED_LIST
    return f"{prefix.ljust(4)}{cleandoc(item)}"


def quote(text: str, qoute_all_lines=False) -> str:
    """Quotes text."""
    buffer = []
    multiline_text = iter(cleandoc(text).splitlines(keepends=True))
    first = next(multiline_text)
    buffer.append(f"> {first}")

    for line in multiline_text:
        buffer.append(f'{"> " if qoute_all_lines else ""}{line}')
    return "".join(buffer)


def bold(text: str) -> str:
    """Bold wrapper."""
    return f"**{text}**"


def italic(text: str) -> str:
    """Bold wrapper."""
    return f"_{text}_"


def code(text: str) -> str:
    """Code wrapper."""
    return f"`{text}`"


def strikethrough(text: str) -> str:
    """Strikethrough wrapper."""
    return f"~~{text}~~"


def header(heading: str, level: int) -> str:
    """Heading wrapper."""
    return f"{'#'*level} {heading}"


def image(uri: str, *, text: Optional[str] = None, title: Optional[str] = None) -> str:
    """Add an image to the document."""
    return f"!{link(uri, text=text, title=title)}"


def link(uri: str, *, text: Optional[str] = None, title: Optional[str] = None) -> str:
    """Add an link to the document."""
    rendered_link = f"[{text or uri}]({uri}"
    if title:
        rendered_link += f' "{title}"'
    return f"{rendered_link})"


def remove_duplicates(seq) -> list:
    """Remove duplicates in a sequence and retain order.

    Args:
        seq (iterable): Any sequence.

    Returns:
        list: Ordered, unique values.
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


@contextmanager
def fileobj_open(path_or_file: Union[str, StringIO]) -> StringIO:
    """Fileobject or Path opener.

    Args:
        path_or_file (Union[str, StringIO]): Fileobject or Path.

    Returns:
        StringIO: Document fileobject.

    Yields:
        Iterator[StringIO]: Document fileobject.
    """
    if isinstance(path_or_file, str):
        file = file_to_close = open(path_or_file, "r", encoding="UTF-8")
    else:
        file = path_or_file
        file_to_close = None

    try:
        yield file
    finally:
        if file_to_close:
            file_to_close.close()
