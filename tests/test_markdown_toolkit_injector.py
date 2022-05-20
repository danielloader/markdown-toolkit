"""Tests for the DocumentInjector class."""
from inspect import cleandoc
from pathlib import Path
from io import StringIO, BytesIO, TextIOWrapper

from markdown_toolkit.injector import MarkdownInjector
from markdown_toolkit.document import MarkdownDocument

RELATIVE_PATH = Path(__file__).parent


def test_string_replacement():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        Text to be replaced.
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        Text successfully replaced.
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    document.dynamicblock.write("Text successfully replaced.")
    assert document.render() == expected_result


def test_bytes_replacement():
    source_document = BytesIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        Text to be replaced.
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        ).encode("UTF-8")
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        Text successfully replaced.
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    ).encode("UTF-8")

    document = MarkdownInjector(TextIOWrapper(source_document, encoding="UTF-8"))
    document.dynamicblock.write("Text successfully replaced.")
    assert document.render() == expected_result.decode("UTF-8")


def test_dynamic_list():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        Text to be replaced.
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        *   One
        *   Two
        *   Three
        *   Four
        *   Five
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    document_fragement = MarkdownDocument()
    for list_item in ["One", "Two", "Three", "Four", "Five"]:
        document_fragement.list(list_item)
    document.dynamicblock.write(document_fragement.render())
    assert document.render() == expected_result


def test_anchor_name_replacement():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:Dynamic-Block --->
        Text to be replaced.
        <!--- markdown-toolkit:end:Dynamic-Block --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:Dynamic-Block --->
        Text successfully replaced.
        <!--- markdown-toolkit:end:Dynamic-Block --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    document.dynamic_block.write("Text successfully replaced.")
    assert document.render() == expected_result


def test_empty_replacement():
    source_document = StringIO(
        cleandoc(
            """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
        )
    )
    expected_result = cleandoc(
        """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        Text successfully replaced.
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """
    )

    document = MarkdownInjector(source_document)
    document.dynamicblock.write("Text successfully replaced.")
    assert document.render() == expected_result
