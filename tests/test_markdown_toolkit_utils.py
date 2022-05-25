from inspect import cleandoc
from pathlib import Path
from io import StringIO

import pytest

from markdown_toolkit.utils import (
    badge,
    bold,
    code,
    fileobj_open,
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


@pytest.mark.parametrize("inputs,expected", [({"text": "1"}, "~~1~~")])
def test_strikethrough(inputs, expected):
    assert strikethrough(**inputs) == expected


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
                "start": 1,
                "end": 3,
            },
            [
                "Markdown supports ordered (numbered) and unordered (bulleted) lists.",
                "",
                "Unordered lists use asterisks, pluses, and hyphens -- interchangably",
            ],
        ),
        (
            {
                "start": 6,
                "end": 8,
            },
            ["*   Red", "*   Green", "*   Blue"],
        ),
        (
            {
                "start": 18,
                "end": 20,
            },
            [
                "-   Red",
                "-   Green",
                "-   Blue",
            ],
        ),
        (
            {
                "start": 24,
                "end": 26,
            },
            [
                "1.  Bird",
                "2.  McHale",
                "3.  Parish",
            ],
        ),
    ],
)
def test_from_file(inputs, expected, tmp_path):
    dir: Path = tmp_path / "from_file"
    dir.mkdir()
    temp_file = dir / "from_file.md"
    temp_file.write_text(
        cleandoc(
            """
        Markdown supports ordered (numbered) and unordered (bulleted) lists.

        Unordered lists use asterisks, pluses, and hyphens -- interchangably
        -- as list markers:

        *   Red
        *   Green
        *   Blue

        is equivalent to:

        +   Red
        +   Green
        +   Blue

        and:

        -   Red
        -   Green
        -   Blue

        Ordered lists use numbers followed by periods:

        1.  Bird
        2.  McHale
        3.  Parish
        """
        )
    )

    content = from_file(path=temp_file, **inputs).splitlines()
    assert content == expected


def test_fileobj_path(tmp_path):
    expected = cleandoc(
        """
        Markdown supports ordered (numbered) and unordered (bulleted) lists.

        Unordered lists use asterisks, pluses, and hyphens -- interchangably
        -- as list markers:

        *   Red
        *   Green
        *   Blue

        is equivalent to:

        +   Red
        +   Green
        +   Blue

        and:

        -   Red
        -   Green
        -   Blue

        Ordered lists use numbers followed by periods:

        1.  Bird
        2.  McHale
        3.  Parish
        """
    )
    dir: Path = tmp_path / "from_file"
    dir.mkdir()
    temp_file = dir / "from_file.md"
    temp_file.write_text(expected)
    with fileobj_open(temp_file) as file:
        assert file.read() == expected


def test_fileobj_str(tmp_path):
    expected = cleandoc(
        """
        Markdown supports ordered (numbered) and unordered (bulleted) lists.

        Unordered lists use asterisks, pluses, and hyphens -- interchangably
        -- as list markers:

        *   Red
        *   Green
        *   Blue

        is equivalent to:

        +   Red
        +   Green
        +   Blue

        and:

        -   Red
        -   Green
        -   Blue

        Ordered lists use numbers followed by periods:

        1.  Bird
        2.  McHale
        3.  Parish
        """
    )
    dir: Path = tmp_path / "from_file"
    dir.mkdir()
    temp_file = dir / "from_file.md"
    temp_file.write_text(expected)
    with fileobj_open(str(temp_file.resolve())) as file:
        assert file.read() == expected


def test_fileobj_obj():
    expected = StringIO(
        cleandoc(
            """
        Markdown supports ordered (numbered) and unordered (bulleted) lists.

        Unordered lists use asterisks, pluses, and hyphens -- interchangably
        -- as list markers:

        *   Red
        *   Green
        *   Blue

        is equivalent to:

        +   Red
        +   Green
        +   Blue

        and:

        -   Red
        -   Green
        -   Blue

        Ordered lists use numbers followed by periods:

        1.  Bird
        2.  McHale
        3.  Parish
        """
        )
    )

    with fileobj_open(expected) as file:
        content = file.read()
        expected.seek(0)
        assert content == expected.read()
