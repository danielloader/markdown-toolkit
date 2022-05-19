from markdown_toolkit import MarkdownDocument, link, bold, italic

doc = MarkdownDocument()
doc.list("Example Item")
with doc.list("List Item that has children"):
    doc.list("Child Item")
    doc.list("Child Item")
    doc.list("Child Item")

doc.list("Ordered lists are possible too", ordered=True)
with doc.list("And children can be ordered", ordered=True):
    doc.list("First Child", ordered=True)
    doc.list("Second Child", ordered=True)
    with doc.list("Third Child", ordered=True):
        doc.list("First Grandchild", ordered=True)

with doc.list("You can nest Paragraphs too!"):
    doc.linebreak()
    doc.paragraph(
        "This is quite helpful when you're using lists for document breaks rather than items."
    )
    doc.paragraph(
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ornare magna 
        tincidunt, luctus neque eu, iaculis nisl. Duis porta pharetra hendrerit. Donec ac 
        bibendum purus. Phasellus sagittis tincidunt metus, a condimentum enim malesuada ut.
        Integer porta pellentesque tempus. Vivamus erat est, imperdiet id enim in, rutrum
        luctus nisi. Praesent in nibh eleifend, consequat est quis, ultricies dolor. 
    """
    )
    doc.text(
        link(
            uri="https://github.com/danielloader/markdown-toolkit",
            text="Links supported too",
        )
    )
    doc.list("And you can nest children from this too.")
    doc.list("Should you want to.")


with open("examples/example_lists.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())
