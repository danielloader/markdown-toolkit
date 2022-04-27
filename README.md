# Markdown Toolkit
> **INFO**: _This readme is dynamically generated via `generate_readme.py`._


A python library for creating markdown.


This library heavily utilises context managers
        to encapsulate logical blocks in the markdown. Primarily this is used
        to keep track of the heading levels, so nested `Heading` context
        managers will be aware of the parent header level.


## Example Usage


```python
from markdown_toolkit import MarkdownBuilder, Heading

with MarkdownBuilder() as doc:
    with Heading(doc, "Markdown Toolkit"):
        doc.paragraph("Example Paragraph.")
        with Heading(doc, "Nested Header"):
            doc.paragraph("Nested.")

with open("example.md", "w", encoding="UTF-8") as file:
    doc.write(file)
```

