![https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg](https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg)
# Markdown Toolkit

> **INFO:** This readme is dynamically generated via [`generate_readme.py`](generate_readme.py). **_No changes to this file will be persistent between Github Actions runs._**

A python library for creating and manipulating markdown.

This library heavily utilises context managers to encapsulate 
logical blocks in the markdown. Primarily this is used to keep 
track of the heading levels, so nested `heading` context
managers will keep track of the header level.

## Examples

> **INFO:** Examples here are automatically taken from the `examples` directory and shown below.

### `examples/example_tables.py`

```python
from markdown_toolkit import MarkdownDocument

doc = MarkdownDocument()
# You can use a table as a context manager and lazily add rows
with doc.table(titles=["Apple Type", "Grown Count"], sort_by="Grown Count") as table:
    table.add_row(apple_type="Granny Smith", grown_count=3)
    table.add_row(apple_type="Golden Delicious", grown_count=1)

with doc.table(titles=["Ticker", "Stock Percentage"]) as table:
    table.add_row(ticker="AAPL", stock_percentage="7.14%")
    table.add_row(ticker="MSFT", stock_percentage="6.1%")
    table.add_row(ticker="AMZN", stock_percentage="3.8%")
    table.add_row(ticker="TSLA", stock_percentage="2.5%")
    table.add_row(ticker="GOOGL", stock_percentage="2.2%")

# Or render a list of dictionaries in a table in one go
raw_table_data = [
    {"Major": "Biology", "GPA": "2.4", "Name": "Edward"},
    {"Major": "Physics", "GPA": "2.9", "Name": "Emily"},
    {"Major": "Mathematics", "GPA": "3.5", "Name": "Sarah"},
]
doc.table(raw_table_data)

with open("examples/example_tables.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())

```
**_Markdown Output:_**
`examples/example_tables.md`
```markdown
| Apple Type | Grown Count |
| --- | --- |
| Golden Delicious | 1 |
| Granny Smith | 3 |

| Ticker | Stock Percentage |
| --- | --- |
| AAPL | 7.14% |
| MSFT | 6.1% |
| AMZN | 3.8% |
| TSLA | 2.5% |
| GOOGL | 2.2% |

| Major | GPA | Name |
| --- | --- | --- |
| Biology | 2.4 | Edward |
| Physics | 2.9 | Emily |
| Mathematics | 3.5 | Sarah |

```
**_Markdown Rendered:_**
| Apple Type | Grown Count |
| --- | --- |
| Golden Delicious | 1 |
| Granny Smith | 3 |

| Ticker | Stock Percentage |
| --- | --- |
| AAPL | 7.14% |
| MSFT | 6.1% |
| AMZN | 3.8% |
| TSLA | 2.5% |
| GOOGL | 2.2% |

| Major | GPA | Name |
| --- | --- | --- |
| Biology | 2.4 | Edward |
| Physics | 2.9 | Emily |
| Mathematics | 3.5 | Sarah |


----

### `examples/example_headings.py`

```python
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

```
**_Markdown Output:_**
`examples/example_headings.md`
```markdown
# Markdown Toolkit

Items added inside the context manager respect the heading level.

## Nested Header

Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Vestibulum ornare magna tincidunt, luctus neque eu, iaculis nisl. 
Duis porta pharetra hendrerit. Donec ac bibendum purus. Phasellus 
sagittis tincidunt metus, a condimentum enim malesuada ut. 
Integer porta pellentesque tempus. Vivamus erat est, imperdiet 
id enim in, rutrum luctus nisi. Praesent in nibh eleifend, 
consequat est quis, ultricies dolor. 

```
**_Markdown Rendered:_**
# Markdown Toolkit

Items added inside the context manager respect the heading level.

## Nested Header

Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Vestibulum ornare magna tincidunt, luctus neque eu, iaculis nisl. 
Duis porta pharetra hendrerit. Donec ac bibendum purus. Phasellus 
sagittis tincidunt metus, a condimentum enim malesuada ut. 
Integer porta pellentesque tempus. Vivamus erat est, imperdiet 
id enim in, rutrum luctus nisi. Praesent in nibh eleifend, 
consequat est quis, ultricies dolor. 


----

### `examples/example_lists.py`

```python
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

```
**_Markdown Output:_**
`examples/example_lists.md`
```markdown
*   Example Item
*   List Item that has children
    *   Child Item
    *   Child Item
    *   Child Item
1.  Ordered lists are possible too
1.  And children can be ordered
    1.  First Child
    1.  Second Child
    1.  Third Child
        1.  First Grandchild
*   You can nest Paragraphs too!

    This is quite helpful when you're using lists for document breaks rather than items.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ornare magna 
    tincidunt, luctus neque eu, iaculis nisl. Duis porta pharetra hendrerit. Donec ac 
    bibendum purus. Phasellus sagittis tincidunt metus, a condimentum enim malesuada ut.
    Integer porta pellentesque tempus. Vivamus erat est, imperdiet id enim in, rutrum
    luctus nisi. Praesent in nibh eleifend, consequat est quis, ultricies dolor. 

    [Links supported too](https://github.com/danielloader/markdown-toolkit)
    *   And you can nest children from this too.
    *   Should you want to.
```
**_Markdown Rendered:_**
*   Example Item
*   List Item that has children
    *   Child Item
    *   Child Item
    *   Child Item
1.  Ordered lists are possible too
1.  And children can be ordered
    1.  First Child
    1.  Second Child
    1.  Third Child
        1.  First Grandchild
*   You can nest Paragraphs too!

    This is quite helpful when you're using lists for document breaks rather than items.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ornare magna 
    tincidunt, luctus neque eu, iaculis nisl. Duis porta pharetra hendrerit. Donec ac 
    bibendum purus. Phasellus sagittis tincidunt metus, a condimentum enim malesuada ut.
    Integer porta pellentesque tempus. Vivamus erat est, imperdiet id enim in, rutrum
    luctus nisi. Praesent in nibh eleifend, consequat est quis, ultricies dolor. 

    [Links supported too](https://github.com/danielloader/markdown-toolkit)
    *   And you can nest children from this too.
    *   Should you want to.

----
