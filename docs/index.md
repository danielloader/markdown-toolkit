---
description: A python library for creating and manipulating markdown with an object oriented interface.
hide:
  - toc
---

# Markdown Toolkit 

<p align="center">
<img src="img/markdown-mark.svg"><br><br>
<em>A python library for creating and manipulating markdown with an object oriented interface.</em><br>
<br>
<a href="https://github.com/danielloader/markdown-toolkit/actions/workflows/tests.yml?query=branch%3Amain" target="_blank">
    <img src="https://github.com/danielloader/markdown-toolkit/actions/workflows/tests.yml/badge.svg?branch=main&event=push" alt="Tests">
</a>
<a href="https://pylint.pycqa.org/en/latest/" target="_blank">
    <img src="img/badge-pylint.svg" alt="Pylint">
</a>
<a href="https://codecov.io/gh/danielloader/markdown-toolkit">
    <img src="https://img.shields.io/codecov/c/github/danielloader/markdown-toolkit?color=%2334D058" alt="Coverage" />
</a>
<a href="https://pypi.org/project/markdown-toolkit" target="_blank">
    <img src="https://img.shields.io/pypi/v/markdown-toolkit?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/markdown-toolkit" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/markdown-toolkit.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

This library is split into two aims:

* Generation of markdown with python to create documents or fragments of documents.
* Injection of static text, file contents, or dynamically generated markdown into existing documents.

1. ## Generation 

    This example reaches out to a public API, grabs a response and generates a document
    using those dynamic responses using the [MarkdownDocument](reference/makdowndocument.md#markdowndocument) class.

    === "Source"

        ```python title="examples/document_quickstart.py"
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

1. ## Injection

    This example takes a source document and uses a script
    to inject dynamically generated table markdown from an external HTTP request using both the 
    [MarkdownDocument](reference/makdowndocument.md#markdowndocument) and 
    [MarkdownInjector](reference/markdowninjector.md#markdowninjector) classes.

    === "Source"

        ```python title="examples/injection_quickstart.py"
        --8<-- "docs/examples/injection_quickstart.py"
        ```

    === "Source Document"

        ```markdown title="examples/injection_source.md"
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

!!! Warning

    This library hasn't reached API stability, when it does it'll be bumped to version `1.0.0`. Until then, make sure you pin your library versions.

To install the library directly for use in scripts you can install it directly with `pip`:

```shell
pip install markdown-toolkit
```

If you want to include it in a larger `poetry` project:
```shell
poetry add markdown-toolkit
```

