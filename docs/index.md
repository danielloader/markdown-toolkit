---
title: Markdown-Toolkit - Python
description: A python library for creating and manipulating markdown with an object oriented interface.
hide:
  - toc
---

# Markdown Toolkit 

_A python library for creating and manipulating markdown with an object oriented interface._

**This library has two primary aims:**

1. _Generation_ of markdown with python to create documents or fragments of documents:

    === "examples/document_quickstart.py"

        ```python
        --8<-- "docs/examples/document_quickstart.py"
        ```

    === "Result"

        ```python exec="true" result="markdown"
        --8<-- "docs/examples/document_quickstart.py"
        ```

    === "Rendered"

        ```python exec="true"
        --8<-- "docs/examples/document_quickstart.py"
        ```

1. _Injection_ of text; static or generated, into existing documents:

    === "examples/injection_quickstart.py"

        ```python
        --8<-- "docs/examples/injection_quickstart.py"
        ```

    === "examples/injection_source.md"

        ```markdown
        --8<-- "docs/examples/injection_source.md"
        ```

    === "Result"

        ```python exec="true" result="markdown"
        --8<-- "docs/examples/injection_quickstart.py"
        ```

    === "Rendered"

        ```python exec="true"
        --8<-- "docs/examples/injection_quickstart.py"
        ```

## Installation

To install the library directly for use in scripts you can install it directly with `pip`:

```shell
pip install markdown-toolkit
```

If you want to include it in a larger `poetry` project:
```shell
poetry add markdown-toolkit
```

