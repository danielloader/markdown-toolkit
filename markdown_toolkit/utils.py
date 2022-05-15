"""Utilities for inline manipulating strings."""

from urllib.parse import quote as urlquote

from typing import Optional

def quote(text: str) -> str:
    """Quotes text."""
    return f"> {text}"


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


def header(level, heading: str) -> str:
    """Heading wrapper."""
    return f"{'#'*level} {heading}"


def image(uri: str, *, text: Optional[str] = None, title: Optional[str] = None) -> str:
    """Add an image to the document."""
    return f"!{link(uri, text=text, title=title)}"


def link(uri: str, *, text: Optional[str] = None, title: Optional[str] = None) -> str:
    """Add an link to the document."""
    rendered_link = f"[{text or uri}]({urlquote(uri)}"
    if title:
        rendered_link += f' "{title}"'
    return f"{rendered_link})"
