# Markdown Toolkit 

_A python library for creating and manipulating markdown with an object oriented interface._

This library has two primary aims:

* Generation of markdown with python to create documents or fragments of documents:

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

* Injection of text; static or generated, into existing documents:

    === "examples/injection_quickstart.py"

        ```python
        --8<-- "docs/examples/injection_quickstart.py"
        ```

    === "Source"

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