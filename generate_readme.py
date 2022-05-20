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
            f"{bold('INFO:')} This readme is dynamically generated via {link('generate_readme.py', text=code('generate_readme.py'))}. {bold(italic('No changes to this file will be persistent between Github Actions runs.'))}"
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


# Save resulting document to file
with open("README.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())
