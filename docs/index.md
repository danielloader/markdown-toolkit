---
title: Markdown-Toolkit - Python
description: A python library for creating and manipulating markdown with an object oriented interface.
hide:
  - toc
---

# Markdown Toolkit 

<p align="center">
<img src="img/markdown-mark.svg"><br>
<em>A python library for creating and manipulating markdown with an object oriented interface.</em><br>
<a href="https://github.com/danielloader/markdown-toolkit/actions/workflows/tests.yml" target="_blank">
    <img src="https://github.com/danielloader/markdown-toolkit/actions/workflows/tests.yml/badge.svg?branch=main&event=push" alt="Tests">
</a>
<a href="https://pypi.org/project/markdown-toolkit" target="_blank">
    <img src="https://img.shields.io/pypi/v/markdown-toolkit?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/markdown-toolkit" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/markdown-toolkit.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

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

