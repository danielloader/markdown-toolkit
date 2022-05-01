"""Dogfooding the toolkit to write the README.md."""
from markdown_toolkit import MarkdownBuilder, from_file

with MarkdownBuilder() as doc:
    with doc.heading("Markdown Toolkit"):
        doc.info("This readme is dynamically generated via `generate_readme.py`.")
        doc.text.paragraph("A python library for creating markdown.")
        doc.text.paragraph("""
        This library heavily utilises context managers to encapsulate 
        logical blocks in the markdown. Primarily this is used to keep 
        track of the heading levels, so nested `heading` context
        managers will keep track of the header level.
        """)
        with doc.heading("Examples"):
            doc.info("More examples can be found in the `examples` directory")
            doc.text.bold("Source:")
            doc.code(source=from_file(
                "examples/readme_example.py"), language="python")
            doc.text.important("Output:")
            doc.code(source=from_file("examples/example.md"),
                     language="markdown")


with open("README.md", "w", encoding="UTF-8") as file:
    doc.write(file)
