"""Dogfooding the toolkit to write the README.md."""
from markdown_toolkit import (
    MarkdownDocument,
    from_file,
    quote,
    bold,
    italic,
    image,
    code,
    link,
)
from pathlib import Path

doc = MarkdownDocument()
doc.text(
    image(
        uri="https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg"
    )
)
with doc.heading("Markdown Toolkit"):
    doc.paragraph(
        quote(
            f"{bold('INFO:')} This readme is dynamically generated via {link('generate_readme.py', text=code('generate_readme.py'))}. {bold(italic('No changes to this file will be persistent between Github Actions runs.'))}"
        )
    )

    doc.paragraph("A python library for creating markdown.")
    doc.paragraph(
        """
        This library heavily utilises context managers to encapsulate 
        logical blocks in the markdown. Primarily this is used to keep 
        track of the heading levels, so nested `heading` context
        managers will keep track of the header level.
    """
    )
    with doc.injector(anchor="badges"):
        pass
    with doc.heading("Examples"):
        doc.paragraph(
            quote(
                f"{bold('INFO:')} More examples can be found in the `examples` directory"
            )
        )
        doc.text(bold("Source:"))
        source = Path("examples/readme_example.py")
        doc.text(code(source))
        with doc.codeblock(language="python"):
            doc.text(from_file(source))

        doc.text((bold(italic("Output:"))))
        result = Path("examples/example.md")
        doc.text(code(result))
        with doc.codeblock(language="markdown"):
            doc.text(from_file(result))


with open("README.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())
