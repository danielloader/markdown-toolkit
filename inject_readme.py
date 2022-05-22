from markdown_toolkit import MarkdownInjector, MarkdownDocument

# Open the document to manipulate and read it into the injector
with open("README.md", "r", encoding="UTF-8") as source:
    source_file = MarkdownInjector(source)

# Open a second file to inject into the document
with open("readme_example.py", "r", encoding="UTF-8") as code:
    doc = MarkdownDocument()
    # Wrap the raw document in code tags
    with doc.codeblock(language="python"):
        doc.paragraph(code.read(), linebreak=False)
    # Replace text between anchor tags with value of file
    source_file.anchors.readme_example.value = doc.render()

# Open _this_ file to inject into the document
with open(__file__, "r", encoding="UTF-8") as this_file:
    doc = MarkdownDocument()
    with doc.codeblock(language="python"):
        doc.paragraph(this_file.read(), linebreak=False)
    source_file.anchors.pycode.value = doc.render()

# Always try to render the resulting document before writing,
# so any failures don't result in an empty or corrupted file
resulting_document = source_file.render()
with open("README.md", "w", encoding="UTF-8") as source:
    source.write(resulting_document)
