from markdown_toolkit import MarkdownInjector, MarkdownDocument


with open("README.md", "r", encoding="UTF-8") as source:
    source_file = MarkdownInjector(source)
with open("readme_example.py", "r", encoding="UTF-8") as code:
    doc = MarkdownDocument(offset=1)
    with doc.codeblock(language="python"):
        doc.paragraph(code.read(), linebreak=False)
    source_file.readme_example.write(doc.render())

with open(__file__, "r", encoding="UTF-8") as this_file:
    doc = MarkdownDocument(offset=1)
    with doc.codeblock(language="python"):
        doc.paragraph(this_file.read(), linebreak=False)
    source_file.abc.write(doc.render())
    print(source_file.file_buffer)
# with open("README.md", "w", encoding="UTF-8") as source:
#     source.write(source_file.render())
