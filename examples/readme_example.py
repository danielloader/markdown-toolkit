from markdown_toolkit import MarkdownDocument

doc = MarkdownDocument()
with doc.heading("Markdown Toolkit"):
    doc.paragraph("Example Paragraph.")
    with doc.heading("Nested Header"):
        doc.paragraph("Nested.")

with open("example.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())
