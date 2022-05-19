from markdown_toolkit import MarkdownDocument

doc = MarkdownDocument()
with doc.heading("Markdown Toolkit"):
    doc.paragraph("Items added inside the context manager respect the heading level.")
    with doc.heading("Nested Header"):
        doc.paragraph(
            """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Vestibulum ornare magna tincidunt, luctus neque eu, iaculis nisl. 
        Duis porta pharetra hendrerit. Donec ac bibendum purus. Phasellus 
        sagittis tincidunt metus, a condimentum enim malesuada ut. 
        Integer porta pellentesque tempus. Vivamus erat est, imperdiet 
        id enim in, rutrum luctus nisi. Praesent in nibh eleifend, 
        consequat est quis, ultricies dolor. 
        """
        )

with open("examples/example_headings.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())
