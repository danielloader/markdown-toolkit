"""Dogfooding the toolkit to write the README.md."""
from markdown_toolkit import MarkdownBuilder, Heading, from_file

with MarkdownBuilder() as doc:
    with Heading(doc, "Markdown Toolkit"):
        doc.info("This readme is dynamically generated via `generate_readme.py`.")
        doc.paragraph("A python library for creating markdown.")
        doc.paragraph("""This library heavily utilises context managers
        to encapsulate logical blocks in the markdown. Primarily this is used
        to keep track of the heading levels, so nested `Heading` context
        managers will be aware of the parent header level.""")
        with Heading(doc, "Example Usage"):
            doc.code(code=from_file("readme_example.py"), language="python")


with open("README.md", "w", encoding="UTF-8") as file:
    doc.write(file)
