"""Tests for the MarkdownDocument class."""
from inspect import cleandoc
from io import StringIO
from textwrap import dedent

import pytest
from testfixtures import compare

from markdown_toolkit.document import MarkdownDocument


def test_linebreak():
    expected_lines = cleandoc(
        """
        test

        linebreak
        """
    )
    doc = MarkdownDocument()
    doc.add("test")
    doc.linebreak()
    doc.add("linebreak")
    assert doc.render() == expected_lines


def test_without_whitespace():
    expected_lines = cleandoc(
        """
        test
        """
    )
    doc = MarkdownDocument()
    doc.add("test")
    assert doc.render(trailing_whitespace=False) == expected_lines


def test_with_whitespace():
    expected_lines = (
        cleandoc(
            """
        test
        """
        )
        + "\n"
    )
    doc = MarkdownDocument()
    doc.add("test")
    assert doc.render(trailing_whitespace=True) == expected_lines


def test_injector():
    expected_lines = cleandoc(
        """
        <!--- markdown-toolkit:anchor --->
        Baseline.
        <!--- markdown-toolkit:anchor --->
        """
    )
    doc = MarkdownDocument()
    with doc.injector("anchor"):
        doc.text("Baseline.")
    assert doc.render() == expected_lines


def test_ordered_list():
    expected_lines = cleandoc(
        """
        *   One
        *   Two
        *   Three
        """
    )
    doc = MarkdownDocument()
    doc.list("One")
    doc.list("Two")
    doc.list("Three")
    assert doc.render() == expected_lines


def test_unordered_list():
    expected_lines = cleandoc(
        """
        1.  One
        1.  Two
        1.  Three
        """
    )
    doc = MarkdownDocument()
    doc.list("One", ordered=True)
    doc.list("Two", ordered=True)
    doc.list("Three", ordered=True)
    assert doc.render() == expected_lines


def test_nested_unordered_list():
    expected_lines = cleandoc(
        """
        *   One
            *   A
        *   Two
            *   B
        *   Three
            *   C
        """
    )
    doc = MarkdownDocument()
    with doc.list("One"):
        doc.list("A")
    with doc.list("Two"):
        doc.list("B")
    with doc.list("Three"):
        doc.list("C")
    assert doc.render() == expected_lines


def test_nested_ordered_list():
    expected_lines = cleandoc(
        """
        1.  One
            1.  A
        1.  Two
            1.  B
        1.  Three
            1.  C
        """
    )
    doc = MarkdownDocument()
    with doc.list("One", ordered=True):
        doc.list("A", ordered=True)
    with doc.list("Two", ordered=True):
        doc.list("B", ordered=True)
    with doc.list("Three", ordered=True):
        doc.list("C", ordered=True)
    assert doc.render() == expected_lines


def test_nested_mixed_list():
    expected_lines = cleandoc(
        """
        1.  One
            *   A
        1.  Two
            *   B
        1.  Three
            *   C
        """
    )
    doc = MarkdownDocument()
    with doc.list("One", ordered=True):
        doc.list("A")
    with doc.list("Two", ordered=True):
        doc.list("B")
    with doc.list("Three", ordered=True):
        doc.list("C")
    assert doc.render() == expected_lines


def test_horizontal_line():
    expected_lines = cleandoc(
        """
        First Section

        ----

        New Section
        """
    )
    doc = MarkdownDocument()
    doc.text("First Section")
    doc.horizontal_line()
    doc.text("New Section")
    assert doc.render() == expected_lines


def test_paragraphs():
    expected_lines = cleandoc(
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sed lectus nibh. Quisque eleifend rutrum lacus eu malesuada. Donec in lacus eget mi suscipit commodo eget sit amet lacus. Nam eget eros augue. Quisque consequat turpis vitae urna accumsan feugiat scelerisque a augue. Curabitur et lorem pharetra, viverra sapien vel, vehicula erat. Morbi ut ornare purus, dapibus dictum metus. Fusce maximus ipsum massa. Nunc elit metus, tincidunt eget orci id, tincidunt viverra eros. Aliquam lobortis diam vitae massa luctus lobortis. Ut id varius massa. Nullam id dictum leo.

        Interdum et malesuada fames ac ante ipsum primis in faucibus. Fusce lacinia cursus odio quis sollicitudin. Integer vel scelerisque nisl. Quisque at nibh enim. Duis mollis diam sed urna sagittis consectetur. Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed suscipit purus non quam suscipit pharetra. Integer tristique mi ligula, sit amet varius nisl maximus nec. Sed facilisis tellus id ipsum maximus, ac aliquet justo sodales.

        EOF
        """
    )
    doc = MarkdownDocument()
    doc.paragraph(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sed lectus nibh. Quisque eleifend rutrum lacus eu malesuada. Donec in lacus eget mi suscipit commodo eget sit amet lacus. Nam eget eros augue. Quisque consequat turpis vitae urna accumsan feugiat scelerisque a augue. Curabitur et lorem pharetra, viverra sapien vel, vehicula erat. Morbi ut ornare purus, dapibus dictum metus. Fusce maximus ipsum massa. Nunc elit metus, tincidunt eget orci id, tincidunt viverra eros. Aliquam lobortis diam vitae massa luctus lobortis. Ut id varius massa. Nullam id dictum leo."
    )
    doc.paragraph(
        "Interdum et malesuada fames ac ante ipsum primis in faucibus. Fusce lacinia cursus odio quis sollicitudin. Integer vel scelerisque nisl. Quisque at nibh enim. Duis mollis diam sed urna sagittis consectetur. Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed suscipit purus non quam suscipit pharetra. Integer tristique mi ligula, sit amet varius nisl maximus nec. Sed facilisis tellus id ipsum maximus, ac aliquet justo sodales."
    )
    doc.add("EOF")

    assert doc.render() == expected_lines


def test_headers():
    expected_lines = cleandoc(
        """
        # Title

        ## Subtitle

        ### Sub Subtitle

        #### Almost Useless Title

        ##### Basically Bold

        ###### Absolutely Pointless Title

        EOF
        """
    )
    doc = MarkdownDocument()
    with doc.heading("Title"):
        with doc.heading("Subtitle"):
            with doc.heading("Sub Subtitle"):
                with doc.heading("Almost Useless Title"):
                    with doc.heading("Basically Bold"):
                        with doc.heading("Absolutely Pointless Title"):
                            doc.add("EOF")
    assert doc.render() == expected_lines


def test_partial_headers():
    expected_lines = cleandoc(
        """
        ### Sub Subtitle

        #### Almost Useless Title

        ##### Basically Bold

        ###### Absolutely Pointless Title

        EOF
        """
    )
    doc = MarkdownDocument()
    with doc.heading("Sub Subtitle", level=3):
        with doc.heading("Almost Useless Title"):
            with doc.heading("Basically Bold"):
                with doc.heading("Absolutely Pointless Title"):
                    doc.add("EOF")
    assert doc.render() == expected_lines


def test_text():
    expected_lines = cleandoc(
        """
        Example line of text.
        Without padding between lines.
        Just newline breaks.
        """
    )
    doc = MarkdownDocument()
    doc.text("Example line of text.")
    doc.text("Without padding between lines.")
    doc.text("Just newline breaks.")
    assert doc.render() == expected_lines


def test_indentblock():
    expected_lines = cleandoc(
        """
        Example line of text.
            Rendered as code block.
        Just newline breaks.
        """
    )
    doc = MarkdownDocument()
    doc.text("Example line of text.")
    with doc.indentblock():
        doc.text("Rendered as code block.")
    doc.text("Just newline breaks.")
    assert doc.render() == expected_lines


def test_codeblock():
    expected_lines = cleandoc(
        """
        ```python
        print("Hello world!")
        ```
        """
    )
    doc = MarkdownDocument()

    with doc.codeblock(language="python"):
        doc.text('print("Hello world!")')
    assert doc.render() == expected_lines


def test_table_building():
    """Test the table generator class."""
    expected_lines = cleandoc(
        """
        | Apple Type | Grown Count |
        | --- | --- |
        | Golden Delicious | 2 |
        | Granny Smith | 3 |

        EOF
        """
    )
    doc = MarkdownDocument()
    with doc.table(
        titles=["Apple Type", "Grown Count"], sort_by="Grown Count"
    ) as table:
        table.add_row(apple_type="Granny Smith", grown_count=3)
        table.add_row(apple_type="Golden Delicious", grown_count=2)

    doc.add("EOF")
    assert doc.render() == expected_lines


def test_table_missing_title():
    """Test the table generator class."""
    doc = MarkdownDocument()
    with pytest.raises(ValueError):
        with doc.table(
            titles=["Apple Type", "Grown Count"], sort_by="Grown Count"
        ) as table:
            table.add_row(missing_title="Granny Smith", grown_count=3)


def test_table_add_without_column():
    """Test the table generator class."""
    doc = MarkdownDocument()
    with pytest.raises(ValueError):
        with doc.table(
            titles=["Apple Type", "Grown Count"], sort_by="Grown Count"
        ) as table:
            table.add_row()


def test_table_bulk_add_rows():
    """Test adding a list of dicts to a table."""
    expected_lines = (
        cleandoc(
            """
        | Apple Type | Grown Count |
        | --- | --- |
        | Golden Delicious | 2 |
        | Granny Smith | 3 |
        """
        )
        + "\n"
    )
    raw_table = [
        {"Apple Type": "Golden Delicious", "Grown Count": 2},
        {"Apple Type": "Granny Smith", "Grown Count": 3},
    ]
    doc = MarkdownDocument()
    doc.table(raw_table)
    compare(doc.render(), expected_lines)


def test_collapsed_section():
    expected_lines = (
        "\n"
        + cleandoc(
            """
            <details><summary>Test Section</summary>

            Content to be hidden.
            </details>
            """
        )
        + "\n"
    )
    doc = MarkdownDocument()
    with doc.collapsed(summary="Test Section"):
        doc.text("Content to be hidden.")
    assert doc.render(trailing_whitespace=False) == expected_lines


def test_document_write():
    file_object = StringIO()
    expected_lines = cleandoc(
        """
        *   One
        *   Two
        *   Three
        """
    )
    doc = MarkdownDocument()
    doc.list("One")
    doc.list("Two")
    doc.list("Three")
    doc.write(file_object)
    file_object.seek(0)
    assert file_object.read() == expected_lines
