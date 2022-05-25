"""Tests for the DocumentInjector class."""
from inspect import cleandoc
from io import StringIO
from pathlib import Path

import pytest
from testfixtures import compare

from markdown_toolkit.document import MarkdownDocument
from markdown_toolkit.injector import MarkdownInjector

RELATIVE_PATH = Path(__file__).parent


def test_string_replacement():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        Text successfully replaced.
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    document.anchors.dynamicblock.value = "Text successfully replaced."
    compare(document.render(), expected_result)


def test_dynamic_list():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        Text to be replaced.
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        *   One
        *   Two
        *   Three
        *   Four
        *   Five
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    document_fragement = MarkdownDocument()
    for list_item in ["One", "Two", "Three", "Four", "Five"]:
        document_fragement.list(list_item)
    document.anchors.dynamicblock.value = document_fragement.render()
    compare(document.render(), expected_result)


def test_dynamic_nested_list():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        * Parent List
            <!--- markdown-toolkit:dynamicblock --->
            <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        * Parent List
            <!--- markdown-toolkit:dynamicblock --->
            *   One
            *   Two
            *   Three
            *   Four
            *   Five
            <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    document_fragement = MarkdownDocument()
    for list_item in ["One", "Two", "Three", "Four", "Five"]:
        document_fragement.list(list_item)
    document.anchors.dynamicblock.value = document_fragement.render()
    compare(document.render(), expected_result)


def test_anchor_name_replacement():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:Dynamic-Block --->
        Text to be replaced.
        <!--- markdown-toolkit:Dynamic-Block --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:Dynamic-Block --->
        Text successfully replaced.
        <!--- markdown-toolkit:Dynamic-Block --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    document.anchors.dynamic_block.value = "Text successfully replaced."
    compare(document.render(), expected_result)


def test_empty_replacement():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        Text successfully replaced.
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    document.anchors.dynamicblock.value = "Text successfully replaced."
    compare(document.render(), expected_result)


def test_multiple_replacements():
    source_document = StringIO(
        cleandoc(
            """
        <!--- markdown-toolkit:blockone --->
        Example of some text.
        <!--- markdown-toolkit:blockone --->
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:blocktwo --->
        <!--- markdown-toolkit:blocktwo --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        <!--- markdown-toolkit:blockthree --->
        <!--- markdown-toolkit:blockthree --->
        """
        )
    )
    expected_result = cleandoc(
        """
        <!--- markdown-toolkit:blockone --->
        Text successfully replaced.
        <!--- markdown-toolkit:blockone --->
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:blocktwo --->
        More successful replacement.
        <!--- markdown-toolkit:blocktwo --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        <!--- markdown-toolkit:blockthree --->
        End of file injection.
        <!--- markdown-toolkit:blockthree --->
        """
    )

    document = MarkdownInjector(source_document)
    document.anchors.blockone.value = "Text successfully replaced."
    document.anchors.blocktwo.value = "More successful replacement."
    document.anchors.blockthree.value = "End of file injection."
    compare(document.render(), expected_result)


def test_missing_anchor():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )

    with pytest.raises(ValueError):
        document = MarkdownInjector(source_document)
        document.anchors.dynamicblock.value = "Text successfully replaced."


def test_overlapping_anchors():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        A
        <!--- markdown-toolkit:broken --->
        B
        <!--- markdown-toolkit:dynamicblock --->
        C
        <!--- markdown-toolkit:broken --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )

    with pytest.raises(ValueError):
        MarkdownInjector(source_document)


def test_three_overlapping_anchors_with_mismatch():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        A
        <!--- markdown-toolkit:broken --->
        B
        <!--- markdown-toolkit:onetag --->
        <!--- markdown-toolkit:dynamicblock --->
        C
        <!--- markdown-toolkit:broken --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )

    with pytest.raises(ValueError):
        MarkdownInjector(source_document)


def test_no_anchors():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    compare(document.render(), expected_result)


def test_missing_anchor():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )

    document = MarkdownInjector(source_document)
    with pytest.raises(ValueError):
        document.anchors.dynamicblock.value = "Text successfully replaced."


def test_string_replacement_with_trailing_whitespace():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
        + "\n"
    )
    expected_result = (
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        Text successfully replaced.
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
        + "\n"
    )

    document = MarkdownInjector(source_document)
    document.anchors.dynamicblock.value = "Text successfully replaced."
    compare(document.render(trailing_whitespace=True), expected_result)


def test_anchor_repr():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = "(MarkdownAnchor=dynamicblock) start=2 end=4 indent=0 value=['Text successfully replaced.']"

    document = MarkdownInjector(source_document)
    document.anchors.dynamicblock.value = "Text successfully replaced."
    compare(str(document.anchors.dynamicblock), expected_result)


def test_anchor_start_attribute():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = 2

    document = MarkdownInjector(source_document)
    document.anchors.dynamicblock.value = "Text successfully replaced."
    compare(document.anchors.dynamicblock.start, expected_result)


def test_anchor_end_attribute():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = 4

    document = MarkdownInjector(source_document)
    document.anchors.dynamicblock.value = "Text successfully replaced."
    compare(document.anchors.dynamicblock.end, expected_result)


def test_anchor_indent_attribute():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

            <!--- markdown-toolkit:dynamicblock --->
            <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = 4

    document = MarkdownInjector(source_document)
    document.anchors.dynamicblock.value = "Text successfully replaced."
    compare(document.anchors.dynamicblock.indent, expected_result)


def test_anchor_value_attribute():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = "Text successfully replaced."

    document = MarkdownInjector(source_document)
    document.anchors.dynamicblock.value = "Text successfully replaced."
    compare(document.anchors.dynamicblock.value, expected_result)


def test_anchor_delete():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        Delete me.
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:dynamicblock --->
        <!--- markdown-toolkit:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )
    document = MarkdownInjector(source_document)
    del document.anchors.dynamicblock.value
    compare(document.render(trailing_whitespace=False), expected_result)
