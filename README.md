![https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg](https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg)
# Markdown Toolkit

> **INFO:** This readme is dynamically generated via [`generate_documentation.py`](generate_documentation.py). **_No changes to this file will be persistent between Github Actions runs._**

A python library for creating and manipulating markdown.

_**WARNING**:_ _This project isn't version 1.0.0 yet, API subject to change, pin the version._

This library heavily utilises context managers to encapsulate 
logical blocks in the markdown. Primarily this is used to keep 
track of the heading levels, so nested `heading` context
managers will keep track of the header level.

## Quickstart

1.  Install package
    ```shell
    pip install markdown-toolkit
    ```
1.  Write a simple test document
    ```python
    from markdown_toolkit import MarkdownDocument
    
    doc = MarkdownDocument()
    
    with doc.heading("Title"):
        doc.paragraph("Example Paragraph.")
    
    print(doc.render())
    ```
    Which yields an output of:

    ```markdown
    # Title
    
    Example Paragraph.
    ```
In addition to generating documents, or partial documents, you can inject markdown into existing documents.

Take the following source document example (assumed to be `sourcedocument.md`):

```markdown
Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

<!--- markdown-toolkit:start:dynamicblock --->
Text to be replaced.
<!--- markdown-toolkit:end:dynamicblock --->

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
```
To adjust this file:

```python
with open("sourcedocument.md", "r", encoding="UTF-8) as file:
    doc = DocumentInjector(file)
doc.dynamicblock.write("Text successfully replaced.")
with open("sourcedocument.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())

```
Should result in:

```markdown
Vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt.

<!--- markdown-toolkit:start:dynamicblock --->
Text successfully replaced.
<!--- markdown-toolkit:end:dynamicblock --->

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.
```
Combining the two is flexible, allowing dynamic generation of markdown partial documents, and injection of those into human edited pages.

## Examples

Further more detailed examples can be found in the [Examples](./examples) and in the [Unit Tests](./tests) directories.
