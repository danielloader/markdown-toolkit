# import requests
import json
from markdown_toolkit import MarkdownInjector, MarkdownBuilder
from markdown_toolkit.helpers.callables import ClassDocBlock



with MarkdownBuilder() as doc:
    with doc.heading("Example Module"):
        ClassDocBlock(doc, module="example_module.classes", name="ExampleClass")
    #     with doc.list.unordered_list() as a:
    #         a.append("Item")
    #         with doc.list.unordered_list() as b:
    #             b.append("Second Layer")
    #             with doc.list.unordered_list() as c:
    #                 c.append("Third Layer")
    #                 with doc.list.unordered_list() as d:
    #                     d.append("Fourth Layer")
    #     with doc.list.ordered_list() as a:
    #         a.append("Item")
    #         with doc.list.ordered_list() as b:
    #             b.append("Second Layer")
    #             with doc.list.ordered_list() as c:
    #                 c.append("Third Layer")
    #                 with doc.list.ordered_list() as d:
    #                     d.append("Fourth Layer")
    #                     doc.newline()
    #                     doc.text.paragraph("Dongs")


with open("/tmp/README.md", "w", encoding="UTF-8") as file:
    doc.write(file)