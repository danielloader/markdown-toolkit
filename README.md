![https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg](https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg)
# Markdown Toolkit

> **INFO:** This readme is dynamically generated via [`generate_readme.py`](generate_readme.py). **_No changes to this file will be persistent between Github Actions runs._**

A python library for creating and manipulating markdown.

This library heavily utilises context managers to encapsulate 
logical blocks in the markdown. Primarily this is used to keep 
track of the heading levels, so nested `heading` context
managers will keep track of the header level.

## Examples

> **INFO:** More examples can be found in the `examples` directory

**Source:**
`examples/readme_example.py`
```python
from markdown_toolkit import MarkdownDocument

doc = MarkdownDocument()
with doc.heading("Markdown Toolkit"):
    doc.paragraph("Example Paragraph.")
    with doc.heading("Nested Header"):
        doc.paragraph("Nested.")

with open("example.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())

```
**_Output:_**
`examples/example.md`
```markdown
# Markdown Toolkit

Example Paragraph.

## Nested Header

Nested.


```