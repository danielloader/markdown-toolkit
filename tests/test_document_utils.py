import pytest
from pathlib import Path

from markdown_toolkit.utils import (
    badge,
    bold,
    code,
    from_file,
    header,
    image,
    italic,
    link,
    quote,
    strikethrough,
)


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            {"label": "test", "color": "green", "message": "example"},
            "[![https://img.shields.io/static/v1?label=test&color=green&message=example](https://img.shields.io/static/v1?label=test&color=green&message=example)](https://shields.io/)",
        ),
        (
            {"label": 1, "color": "red", "message": 2},
            "[![https://img.shields.io/static/v1?label=1&color=red&message=2](https://img.shields.io/static/v1?label=1&color=red&message=2)](https://shields.io/)",
        ),
    ],
)
def test_badge(inputs, expected):
    assert badge(**inputs) == expected


@pytest.mark.parametrize("inputs,expected", [({"text": "1"}, "> 1")])
def test_quote(inputs, expected):
    assert quote(**inputs) == expected


@pytest.mark.parametrize("inputs,expected", [({"text": "1"}, "**1**")])
def test_bold(inputs, expected):
    assert bold(**inputs) == expected


@pytest.mark.parametrize("inputs,expected", [({"text": "1"}, "_1_")])
def test_italic(inputs, expected):
    assert italic(**inputs) == expected


@pytest.mark.parametrize("inputs,expected", [({"text": "1"}, "`1`")])
def test_code(inputs, expected):
    assert code(**inputs) == expected


@pytest.mark.parametrize("inputs,expected", [({"text": "1"}, "~~1~~")])
def test_image(inputs, expected):
    assert strikethrough(**inputs) == expected


@pytest.mark.parametrize(
    "inputs,expected",
    [
        ({"level": 1, "heading": "Heading"}, "# Heading"),
        ({"level": 2, "heading": "Heading"}, "## Heading"),
        ({"level": 3, "heading": "Heading"}, "### Heading"),
        ({"level": 4, "heading": "Heading"}, "#### Heading"),
        ({"level": 5, "heading": "Heading"}, "##### Heading"),
        ({"level": 6, "heading": "Heading"}, "###### Heading"),
    ],
)
def test_strikethough(inputs, expected):
    assert header(**inputs) == expected


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            {"uri": "https://picsum.photos/200/300"},
            "![https://picsum.photos/200/300](https://picsum.photos/200/300)",
        ),
        (
            {"uri": "https://picsum.photos/200/300", "text": "abc"},
            "![abc](https://picsum.photos/200/300)",
        ),
        (
            {"uri": "https://picsum.photos/200/300", "text": "abc", "title": "def"},
            '![abc](https://picsum.photos/200/300 "def")',
        ),
    ],
)
def test_image(inputs, expected):
    assert image(**inputs) == expected


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            {"uri": "https://example.com"},
            "[https://example.com](https://example.com)",
        ),
        (
            {"uri": "https://example.com", "text": "abc"},
            "[abc](https://example.com)",
        ),
        (
            {"uri": "https://example.com", "text": "abc", "title": "def"},
            '[abc](https://example.com "def")',
        ),
    ],
)
def test_link(inputs, expected):
    assert link(**inputs) == expected


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            {
                "path": Path(__file__).parent / Path("test_static_file.md"),
                "start": 0,
                "end": 3,
            },
            ["# Markdown: Syntax", "", "*   [Overview](#overview)"],
        ),
        (
            {
                "path": Path(__file__).parent / Path("test_static_file.md"),
                "start": 60,
                "end": 63,
            },
            [
                "### Headers",
                "",
                "Markdown supports two styles of headers, [Setext] [1] and [atx] [2].",
            ],
        ),
        (
            {
                "path": Path(__file__).parent / Path("test_static_file.md"),
                "start": 107,
                "end": 115,
            },
            [
                "> ## This is a header.",
                "> ",
                "> 1.   This is the first list item.",
                "> 2.   This is the second list item.",
                "> ",
                "> Here's some example code:",
                "> ",
                '>     return shell_exec("echo $input | $markdown_script");',
            ],
        ),
        (
            {
                "path": Path(__file__).parent / Path("test_static_file.md"),
                "start": 121,
                "end": 131,
            },
            [
                "### Lists",
                "",
                "Markdown supports ordered (numbered) and unordered (bulleted) lists.",
                "",
                "Unordered lists use asterisks, pluses, and hyphens -- interchangably",
                "-- as list markers:",
                "",
                "*   Red",
                "*   Green",
                "*   Blue",
            ],
        ),
    ],
)
def test_from_file(inputs, expected):
    content = from_file(**inputs).splitlines()
    assert content == expected
