# Markdown Toolkit

> **INFO**: _This readme is dynamically generated via `generate_readme.py`._

A python library for creating markdown.


This library heavily utilises context managers to encapsulate 
logical blocks in the markdown. Primarily this is used to keep 
track of the heading levels, so nested `heading` context
managers will keep track of the header level.


## Examples

> **INFO**: _More examples can be found in the `examples` directory_

__Source:__
```python
from markdown_toolkit import MarkdownBuilder

with MarkdownBuilder() as doc:
    with doc.heading("Markdown Toolkit"):
        doc.text.paragraph("Example Paragraph.")
        with doc.heading("Nested Header"):
            doc.text.paragraph("Nested.")

with open("example.md", "w", encoding="UTF-8") as file:
    doc.write(file)
```
***Output:***
```markdown
# Markdown Toolkit

Example Paragraph.

## Nested Header

Nested.


```
