from markdown_toolkit import MarkdownBuilder, Heading

with MarkdownBuilder() as doc:
    with Heading(doc, "Document Title"):
        doc.paragraph("A short story on running into the woods.")
        with Heading(doc, "Preparation"):
            doc.text("**WARNING**: ")
            doc.paragraph("Bring spare socks.")
            doc.image("placeholder", "https://picsum.photos/200/300")
            doc.link("Google Homepage", "https://www.google.com")
            with Heading(doc, "Food"):
                doc.paragraph("Bring lots of food.")
                doc.list(["Cheese", "Cake"], ordered=True)
                doc.list(["Cheese", "Cake"], ordered=False)


with open("document.md", "w", encoding="UTF-8") as file:
    doc.write(file)
