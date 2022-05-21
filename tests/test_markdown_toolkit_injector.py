"""Tests for the DocumentInjector class."""
from inspect import cleandoc
from io import StringIO
from pathlib import Path

from markdown_toolkit.document import MarkdownDocument
from markdown_toolkit.injector import MarkdownInjector
from testfixtures import compare

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
