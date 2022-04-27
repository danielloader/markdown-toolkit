from markdown_toolkit import MarkdownBuilder, Heading

with MarkdownBuilder() as doc:
    with Heading(doc, "Markdown Toolkit"):
        doc.paragraph("Example Paragraph.")
        with Heading(doc, "Nested Header"):
            doc.paragraph("Nested.")

with open("example.md", "w", encoding="UTF-8") as file:
    doc.write(file)