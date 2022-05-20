![https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg](https://raw.githubusercontent.com/dcurtis/markdown-mark/99572b4a4f71b4ea2b1186a30f440ff2fcf66d27/svg/markdown-mark.svg)
# Markdown Toolkit

> **INFO:** This readme is dynamically generated via [`generate_documentation.py`](generate_documentation.py). **_No changes to this file will be persistent between Github Actions runs._**

A python library for creating and manipulating markdown.

_**WARNING**:_ _This project isn't version 1.0.0 yet, API subject to change, pin the version._
This library has two primary aims:
* Generation of markdown via python to create documents or fragments of documents.
* Injection of text into existing documents, for dynamic partial sections of documentation.


This library heavily utilises context managers to encapsulate 
logical blocks in the markdown. Primarily this is used to keep 
track of the heading levels, so nested `heading` context
managers will keep track of the header level.

## Quickstart

1.  Install package (Preferably in your python [virtual environment](https://docs.python.org/3/library/venv.html)).
    ```shell
    pip install markdown-toolkit
    ```
1.  Write a simple test document 
    <!-- markdown-toolkit:start:readme_example -->
    ```python
    """README.md Example Code."""
    import requests
    from markdown_toolkit import MarkdownDocument
    
    doc = MarkdownDocument()
    
    quotes = requests.get("http://ron-swanson-quotes.herokuapp.com/v2/quotes/10")
    with doc.heading("Ron Swanson Quotes"):
        doc.paragraph("This list is generated from a JSON serving REST API call.")
        for quote in quotes.json():
            doc.list(quote)
    
    print(doc.render())
    ```
    <!-- markdown-toolkit:end:readme_example -->
    Which gives a result of:
    ```markdown 
    # Ron Swanson Quotes

    This list is generated from a JSON serving REST API call.

    *   In my opinion, not enough people have looked their dinner in the eyes and considered the circle of life.
    *   Barbecues should be about one thing: good shared meat.
    *   It's an impossible puzzle, and I love puzzles!
    *   Under my tutelage, you will grow from boys to men. From men into gladiators. And from gladiators into Swansons.
    *   I love riddles!
    *   If any of you need anything at all, too bad. Deal with your problems yourselves, like adults.
    *   I like Tom. He doesn’t do a lot of work around here. He shows zero initiative. He’s not a team player. He’s never wanted to go that extra mile. Tom is exactly what I’m looking for in a government employee.
    *   When I eat, it is the food that is scared.
    *   Once a year, every branch of this government meets in a room and announces what they intend to waste taxpayer money on.
    *   Give 100%. 110% is impossible. Only idiots recommend that.
    ```
1. Inject it into an existing document
    
    > This README.md file itself has injection anchors to put the content of the `readme_example.py`.

Combining the two is flexible, allowing dynamic generation of markdown partial documents, and injection of those into human edited pages.

## Examples

Further more detailed examples can be found in the [Examples](./examples) and in the [Unit Tests](./tests) directories.
