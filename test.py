from markdown_toolkit import MarkdownBuilder
from markdown_toolkit.helpers import module_block

with MarkdownBuilder() as doc:
    module_block(doc, "example_module")

with open("document.md", "w", encoding="UTF-8") as file:
    doc.write(file)
