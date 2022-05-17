from markdown_toolkit import (
    MarkdownDocument,
    badge,
    bold,
    from_file,
    image,
    link,
    quote,
)


def build_doc():
    """Example function to build a document."""
    doc = MarkdownDocument()
    doc.paragraph(quote("Inspirational Quote."))
    doc.add(badge(label="Cool factor", message="high", color="green"))
    doc.add(badge(label="Fucks given", message="0", color="red"))
    doc.add(badge(label="Impressive?", message="maybe", color="orange"))
    with doc.heading("Example Document"):
        with doc.list:
            doc.unordered_item(doc.heading("Paragraphs"))
            doc.paragraph(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ac odio euismod, sodales ipsum id, scelerisque nisl. Etiam erat odio, faucibus ut augue nec, tristique imperdiet ligula. Sed lacinia massa sed ante facilisis, eu finibus arcu fermentum."
            )
            doc.paragraph(
                "Interdum et malesuada fames ac ante ipsum primis in faucibus. Etiam luctus mollis lacus ac luctus. Praesent justo mauris, lacinia ut neque vel, semper viverra ipsum. Nulla facilisi. Proin gravida augue eget blandit tincidunt. Nullam viverra iaculis semper. Nam quis turpis varius, euismod dui ac, rhoncus orci."
            )
            doc.unordered_item(doc.heading("File snippets"))
            doc.multiline(from_file("README.md", start=1, end=14))
        with doc.list:
            doc.unordered_item(doc.heading("Other Examples"))
            doc.paragraph(
                "Example of a paragraph explaining a nested ordered list below."
            )
            with doc.list:
                doc.ordered_item(bold("Nested Table and Paragraph"))
                with doc.table(titles=["Column A", "Column B"]) as table:
                    table.add_row(["1", "3"])
                    table.add_row(["45", "12"])
                doc.paragraph(
                    "Mauris vel magna id ipsum consequat vulputate. Nulla id turpis non eros tincidunt aliquet eleifend id orci. Proin leo odio, finibus nec fermentum vitae, bibendum sed eros. Sed sapien lectus, euismod vitae risus in, lobortis rutrum purus. Proin at velit ut risus euismod aliquam. Donec vitae iaculis mi. Etiam quis aliquet ligula."
                )
                doc.ordered_item(bold("Nested List Image"))
                doc.paragraph(image("https://picsum.photos/200/300"))
                doc.ordered_item(bold("Nested Link in Text"))
                doc.paragraph(
                    f'Inline links are quite {link(text="easy", uri="https://www.google.com", title="tooltip example")}.'
                )
                doc.ordered_item(bold("Images as Links"))
                doc.paragraph(
                    link(
                        "https://www.google.com",
                        text=image("https://picsum.photos/240/320"),
                    )
                )
                doc.ordered_item(bold("Nested Code Block"))
                doc.paragraph("Simple Code example:")
                with doc.codeblock(language="python"):
                    doc.multiline(
                        """
                    def example(x, y):
                        return x + y
                    """
                    )
    doc.horizontal_line()

    return doc.render()


with open("output.md", "w", encoding="UTF-8") as file:
    file.write(build_doc())
