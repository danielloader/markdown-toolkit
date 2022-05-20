"""Dogfooding the toolkit to write the README.md."""
from pathlib import Path

from markdown_toolkit import (
    MarkdownDocument,
    bold,
    code,
    from_file,
    link,
    quote,
)

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
