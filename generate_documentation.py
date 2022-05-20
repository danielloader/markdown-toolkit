"""Dogfooding the toolkit to write the README.md."""
from pathlib import Path

from markdown_toolkit import (
    MarkdownDocument,
    bold,
    code,
    from_file,
    image,
    italic,
    link,
    quote,
)

# Initalise an empty document
doc = MarkdownDocument()

# Add image to top of the document
doc.text(
    image(
        uri="https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg"
    )
)
# Add title to document
with doc.heading("Markdown Toolkit"):
    # Example of a paragraph with inline formatting
    doc.paragraph(
        quote(
            f"{bold('INFO:')} This readme is dynamically generated via {link(__file__, text=code(__file__))}. {bold(italic('No changes to this file will be persistent between Github Actions runs.'))}"
        )
    )

    # Example of a single line paragaph
    doc.paragraph("A python library for creating and manipulating markdown.")
    # Example of a multline paragraph
    doc.paragraph(
        """
        This library heavily utilises context managers to encapsulate 
        logical blocks in the markdown. Primarily this is used to keep 
        track of the heading levels, so nested `heading` context
        managers will keep track of the header level.
    """
    )
    # Example of nested header scopes
    with doc.heading("Quickstart"):
        with doc.list("Install package", ordered=True):
            with doc.codeblock(language="shell"):
                doc.text("pip install markdown-toolkit")
        with doc.list("Write a simple test document", ordered=True):
            with doc.codeblock(language="python"):
                doc.paragraph(
                    """
                    from markdown_toolkit import MarkdownDocument

                    doc = MarkdownDocument()

                    with doc.heading("Title"):
                        doc.paragraph("Example Paragraph.")

                    print(doc.render())
                    """,
                    linebreak=False,
                )
            doc.paragraph("Which yields an output of:")
            with doc.codeblock(language="markdown"):
                doc.paragraph(
                    """
                    # Title

                    Example Paragraph.
                    """,
                    linebreak=False,
                )

        doc.paragraph(
            "In addition to generating documents, or partial documents, you can inject markdown into existing documents."
        )
        doc.paragraph(
            "Take the following source document example (assumed to be `sourcedocument.md`):"
        )
        with doc.codeblock(language="markdown"):
            doc.paragraph(
                """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        Text to be replaced.
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """,
                linebreak=False,
            )
        doc.paragraph("To adjust this file:")
        with doc.codeblock(language="python"):
            doc.paragraph(
                """
                with open("sourcedocument.md", "r", encoding="UTF-8) as file:
                    doc = DocumentInjector(file)
                doc.dynamicblock.write("Text successfully replaced.")
                with open("sourcedocument.md", "w", encoding="UTF-8") as file:
                    file.write(doc.render())
            """
            )
        doc.paragraph("Should result in:")
        with doc.codeblock(language="markdown"):
            doc.paragraph(
                """
        Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

        <!--- markdown-toolkit:start:dynamicblock --->
        Text successfully replaced.
        <!--- markdown-toolkit:end:dynamicblock --->

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
        """,
                linebreak=False,
            )
        doc.paragraph(
            "Combining the two is flexible, allowing dynamic generation of markdown partial documents, and injection of those into human edited pages."
        )

    with doc.heading("Examples"):
        doc.paragraph(
            f"Further more detailed examples can be found in the {link('./examples', text='Examples')} and in the {link('./tests', text='Unit Tests')} directories."
        )

# Save resulting document to file
with open("README.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())

del doc  # Start new document
doc = MarkdownDocument()
with doc.heading("Examples"):
    doc.paragraph(
        quote(
            f"{bold('INFO:')} Examples here are automatically taken from the `examples` directory and shown below."
        )
    )

    # Example of loop of files in a directory for templated markdown blocks
    for source_file in sorted(
        [f for f in Path("examples").iterdir() if f.suffix == ".py"]
    ):
        print(source_file)
        with doc.heading(link(uri=source_file, text=code(source_file))):
            with doc.codeblock(language="python"):
                doc.text(from_file(source_file))

            with doc.collapsed("Markdown Output:"):
                result = source_file.with_suffix(".md")
                with doc.codeblock(language="markdown"):
                    doc.text(from_file(result))

            with doc.collapsed("Markdown Rendered:"):
                doc.text(from_file(result))
        doc.horizontal_line()


with open("examples/README.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())
