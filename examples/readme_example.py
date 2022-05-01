from markdown_toolkit import MarkdownBuilder

with MarkdownBuilder() as doc:
    with doc.heading("Markdown Toolkit"):
        doc.text.paragraph("Example Paragraph.")
        with doc.heading("Nested Header"):
            doc.text.paragraph("Nested.")

with open("example.md", "w", encoding="UTF-8") as file:
    doc.write(file)