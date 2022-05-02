# import requests
import json
from markdown_toolkit import MarkdownInjector, MarkdownBuilder
from markdown_toolkit.helpers import ClassDocBlock



with MarkdownBuilder() as doc:
    with doc.heading("Example Module"):
        ClassDocBlock(doc, module="example_module.classes", name="ExampleClass")

with open("/tmp/README.md", "w", encoding="UTF-8") as file:
    doc.write(file)