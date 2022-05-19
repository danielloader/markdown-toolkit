# pylint: disable=line-too-long
from inspect import cleandoc
from pathlib import Path

from markdown_toolkit import MarkdownDocument, bold
from markdown_toolkit.utils import code, header, italic, link, list_item, quote


def test_static_testfile():
    """An end to end test against a known static markdown document."""
    expected = cleandoc(
        """
        # Markdown: Syntax

        *   [Overview](#overview)
            *   [Philosophy](#philosophy)
            *   [Inline HTML](#html)
            *   [Automatic Escaping for Special Characters](#autoescape)
        *   [Block Elements](#block)
            *   [Paragraphs and Line Breaks](#p)
            *   [Headers](#header)
            *   [Blockquotes](#blockquote)
            *   [Lists](#list)
            *   [Code Blocks](#precode)
            *   [Horizontal Rules](#hr)
        *   [Span Elements](#span)
            *   [Links](#link)
            *   [Emphasis](#em)
            *   [Code](#code)
            *   [Images](#img)
        *   [Miscellaneous](#misc)
            *   [Backslash Escapes](#backslash)
            *   [Automatic Links](#autolink)


        **Note:** This document is itself written using Markdown; you
        can [see the source for it by adding '.text' to the URL](/projects/markdown/syntax.text).

        ----

        ## Overview

        ### Philosophy

        Markdown is intended to be as easy-to-read and easy-to-write as is feasible.

        Readability, however, is emphasized above all else. A Markdown-formatted
        document should be publishable as-is, as plain text, without looking
        like it's been marked up with tags or formatting instructions. While
        Markdown's syntax has been influenced by several existing text-to-HTML
        filters -- including [Setext](http://docutils.sourceforge.net/mirror/setext.html), [atx](http://www.aaronsw.com/2002/atx/), [Textile](http://textism.com/tools/textile/), [reStructuredText](http://docutils.sourceforge.net/rst.html),
        [Grutatext](http://www.triptico.com/software/grutatxt.html), and [EtText](http://ettext.taint.org/doc/) -- the single biggest source of
        inspiration for Markdown's syntax is the format of plain text email.

        ## Block Elements

        ### Paragraphs and Line Breaks

        A paragraph is simply one or more consecutive lines of text, separated
        by one or more blank lines. (A blank line is any line that looks like a
        blank line -- a line containing nothing but spaces or tabs is considered
        blank.) Normal paragraphs should not be indented with spaces or tabs.

        The implication of the "one or more consecutive lines of text" rule is
        that Markdown supports "hard-wrapped" text paragraphs. This differs
        significantly from most other text-to-HTML formatters (including Movable
        Type's "Convert Line Breaks" option) which translate every line break
        character in a paragraph into a `<br />` tag.

        When you *do* want to insert a `<br />` break tag using Markdown, you
        end a line with two or more spaces, then type return.

        ### Headers

        Markdown supports two styles of headers, [Setext] [1] and [atx] [2].

        Optionally, you may "close" atx-style headers. This is purely
        cosmetic -- you can use this if you think it looks better. The
        closing hashes don't even need to match the number of hashes
        used to open the header. (The number of opening hashes
        determines the header level.)


        ### Blockquotes

        Markdown uses email-style `>` characters for blockquoting. If you're
        familiar with quoting passages of text in an email message, then you
        know how to create a blockquote in Markdown. It looks best if you hard
        wrap the text and put a `>` before every line:

        > This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
        > consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
        > Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
        > 
        > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
        > id sem consectetuer libero luctus adipiscing.

        Markdown allows you to be lazy and only put the `>` before the first
        line of a hard-wrapped paragraph:

        > This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
        consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
        Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.

        > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
        id sem consectetuer libero luctus adipiscing.

        Blockquotes can be nested (i.e. a blockquote-in-a-blockquote) by
        adding additional levels of `>`:

        > This is the first level of quoting.
        > 
        > > This is nested blockquote.
        > 
        > Back to the first level.

        Blockquotes can contain other Markdown elements, including headers, lists,
        and code blocks:

        > ## This is a header.
        > 
        > 1.  This is the first list item.
        > 2.  This is the second list item.
        > 
        > Here's some example code:
        > 
        >     return shell_exec("echo $input | $markdown_script");

        Any decent text editor should make email-style quoting easy. For
        example, with BBEdit, you can make a selection and choose Increase
        Quote Level from the Text menu.


        ### Lists

        Markdown supports ordered (numbered) and unordered (bulleted) lists.

        Unordered lists use asterisks, pluses, and hyphens -- interchangably
        -- as list markers:

        *   Red
        *   Green
        *   Blue

        is equivalent to:

        +   Red
        +   Green
        +   Blue

        and:

        -   Red
        -   Green
        -   Blue

        Ordered lists use numbers followed by periods:

        1.  Bird
        2.  McHale
        3.  Parish

        It's important to note that the actual numbers you use to mark the
        list have no effect on the HTML output Markdown produces. The HTML
        Markdown produces from the above list is:

        If you instead wrote the list in Markdown like this:

        1.  Bird
        1.  McHale
        1.  Parish

        or even:

        3.  Bird
        1.  McHale
        8.  Parish

        you'd get the exact same HTML output. The point is, if you want to,
        you can use ordinal numbers in your ordered Markdown lists, so that
        the numbers in your source match the numbers in your published HTML.
        But if you want to be lazy, you don't have to.

        To make lists look nice, you can wrap items with hanging indents:

        *   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
            Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
            viverra nec, fringilla in, laoreet vitae, risus.
        *   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
            Suspendisse id sem consectetuer libero luctus adipiscing.

        But if you want to be lazy, you don't have to:

        *   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
        Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
        viverra nec, fringilla in, laoreet vitae, risus.
        *   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
        Suspendisse id sem consectetuer libero luctus adipiscing.

        List items may consist of multiple paragraphs. Each subsequent
        paragraph in a list item must be indented by either 4 spaces
        or one tab:

        1.  This is a list item with two paragraphs. Lorem ipsum dolor
            sit amet, consectetuer adipiscing elit. Aliquam hendrerit
            mi posuere lectus.

            Vestibulum enim wisi, viverra nec, fringilla in, laoreet
            vitae, risus. Donec sit amet nisl. Aliquam semper ipsum
            sit amet velit.

        2.  Suspendisse id sem consectetuer libero luctus adipiscing.

        It looks nice if you indent every line of the subsequent
        paragraphs, but here again, Markdown will allow you to be
        lazy:

        *   This is a list item with two paragraphs.

            This is the second paragraph in the list item. You're
        only required to indent the first line. Lorem ipsum dolor
        sit amet, consectetuer adipiscing elit.

        *   Another item in the same list.

        To put a blockquote within a list item, the blockquote's `>`
        delimiters need to be indented:

        *   A list item with a blockquote:

            > This is a blockquote
            > inside a list item.

        To put a code block within a list item, the code block needs
        to be indented *twice* -- 8 spaces or two tabs:

        *   A list item with a code block:

                <code goes here>

        ### Code Blocks

        Pre-formatted code blocks are used for writing about programming or
        markup source code. Rather than forming normal paragraphs, the lines
        of a code block are interpreted literally. Markdown wraps a code block
        in both `<pre>` and `<code>` tags.

        To produce a code block in Markdown, simply indent every line of the
        block by at least 4 spaces or 1 tab.

        This is a normal paragraph:

            This is a code block.

        Here is an example of AppleScript:

            tell application "Foo"
                beep
            end tell

        A code block continues until it reaches a line that is not indented
        (or the end of the article).

        Within a code block, ampersands (`&`) and angle brackets (`<` and `>`)
        are automatically converted into HTML entities. This makes it very
        easy to include example HTML source code using Markdown -- just paste
        it and indent it, and Markdown will handle the hassle of encoding the
        ampersands and angle brackets. For example, this:

            <div class="footer">
                &copy; 2004 Foo Corporation
            </div>

        Regular Markdown syntax is not processed within code blocks. E.g.,
        asterisks are just literal asterisks within a code block. This means
        it's also easy to use Markdown to write about Markdown's own syntax.

        ```
        tell application "Foo"
            beep
        end tell
        ```

        ## Span Elements

        ### Links

        Markdown supports two style of links: *inline* and *reference*.

        In both styles, the link text is delimited by [square brackets].

        To create an inline link, use a set of regular parentheses immediately
        after the link text's closing square bracket. Inside the parentheses,
        put the URL where you want the link to point, along with an *optional*
        title for the link, surrounded in quotes. For example:

        This is [an example](http://example.com/) inline link.

        [This link](http://example.net/) has no title attribute.

        ### Emphasis

        Markdown treats asterisks (`*`) and underscores (`_`) as indicators of
        emphasis. Text wrapped with one `*` or `_` will be wrapped with an
        HTML `<em>` tag; double `*`'s or `_`'s will be wrapped with an HTML
        `<strong>` tag. E.g., this input:

        *single asterisks*

        _single underscores_

        **double asterisks**

        __double underscores__

        ### Code

        To indicate a span of code, wrap it with backtick quotes (`` ` ``).
        Unlike a pre-formatted code block, a code span indicates code within a
        normal paragraph. For example:

        Use the `printf()` function.
    """
    )

    doc = MarkdownDocument()
    with doc.heading("Markdown: Syntax"):
        with doc.list(item=link("#overview", text="Overview")):
            doc.list(link("#philosophy", text="Philosophy"))
            doc.list(link("#html", text="Inline HTML"))
            doc.list(
                link("#autoescape", text="Automatic Escaping for Special Characters")
            )
        with doc.list(link("#block", text="Block Elements")):
            doc.list(link("#p", text="Paragraphs and Line Breaks"))
            doc.list(link("#header", text="Headers"))
            doc.list(link("#blockquote", text="Blockquotes"))
            doc.list(link("#list", text="Lists"))
            doc.list(link("#precode", text="Code Blocks"))
            doc.list(link("#hr", text="Horizontal Rules"))
        with doc.list(link("#span", text="Span Elements")):
            doc.list(link("#link", text="Links"))
            doc.list(link("#em", text="Emphasis"))
            doc.list(link("#code", text="Code"))
            doc.list(link("#img", text="Images"))
        with doc.list(link("#misc", text="Miscellaneous")):
            doc.list(link("#backslash", text="Backslash Escapes"))
            doc.list(link("#autolink", text="Automatic Links"))
        doc.linebreak()
        doc.linebreak()
        doc.text(bold("Note:") + " This document is itself written using Markdown; you")
        doc.text(
            f"""can {link('/projects/markdown/syntax.text',text="see the source for it by adding '.text' to the URL")}."""
        )
        doc.horizontal_line()
        with doc.heading("Overview"):
            with doc.heading("Philosophy"):
                doc.paragraph(
                    "Markdown is intended to be as easy-to-read and easy-to-write as is feasible."
                )
                doc.paragraph(
                    f"""Readability, however, is emphasized above all else. A Markdown-formatted
                    document should be publishable as-is, as plain text, without looking
                    like it's been marked up with tags or formatting instructions. While
                    Markdown's syntax has been influenced by several existing text-to-HTML
                    filters -- including {link("http://docutils.sourceforge.net/mirror/setext.html", text="Setext")}, {link("http://www.aaronsw.com/2002/atx/", text="atx")}, {link("http://textism.com/tools/textile/",text="Textile")}, {link("http://docutils.sourceforge.net/rst.html", text="reStructuredText")},
                    [Grutatext](http://www.triptico.com/software/grutatxt.html), and [EtText](http://ettext.taint.org/doc/) -- the single biggest source of
                    inspiration for Markdown's syntax is the format of plain text email.""",
                )

        with doc.heading("Block Elements"):
            with doc.heading("Paragraphs and Line Breaks"):
                doc.paragraph(
                    """A paragraph is simply one or more consecutive lines of text, separated
                    by one or more blank lines. (A blank line is any line that looks like a
                    blank line -- a line containing nothing but spaces or tabs is considered
                    blank.) Normal paragraphs should not be indented with spaces or tabs.""",
                )
                doc.paragraph(
                    f"""The implication of the "one or more consecutive lines of text" rule is
                    that Markdown supports "hard-wrapped" text paragraphs. This differs
                    significantly from most other text-to-HTML formatters (including Movable
                    Type's "Convert Line Breaks" option) which translate every line break
                    character in a paragraph into a {code("<br />")} tag."""
                )
                doc.paragraph(
                    """When you *do* want to insert a `<br />` break tag using Markdown, you
                    end a line with two or more spaces, then type return."""
                )
            with doc.heading("Headers"):
                doc.paragraph(
                    "Markdown supports two styles of headers, [Setext] [1] and [atx] [2]."
                )
                doc.paragraph(
                    """Optionally, you may "close" atx-style headers. This is purely
                    cosmetic -- you can use this if you think it looks better. The
                    closing hashes don't even need to match the number of hashes
                    used to open the header. (The number of opening hashes
                    determines the header level.)"""
                )
                doc.linebreak()
            with doc.heading("Blockquotes"):
                doc.paragraph(
                    f"""Markdown uses email-style {code(">")} characters for blockquoting. If you're
                    familiar with quoting passages of text in an email message, then you
                    know how to create a blockquote in Markdown. It looks best if you hard
                    wrap the text and put a {code(">")} before every line:"""
                )
                doc.paragraph(
                    quote(
                        """This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
                        consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
                        Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.

                        Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
                        id sem consectetuer libero luctus adipiscing.""",
                        qoute_all_lines=True,
                    )
                )
                doc.paragraph(
                    f"""Markdown allows you to be lazy and only put the {code(">")} before the first
                    line of a hard-wrapped paragraph:"""
                )
                doc.paragraph(
                    quote(
                        """This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
                        consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
                        Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.""",
                    )
                )
                doc.paragraph(
                    quote(
                        """Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
                        id sem consectetuer libero luctus adipiscing."""
                    )
                )
                doc.paragraph(
                    f"""Blockquotes can be nested (i.e. a blockquote-in-a-blockquote) by
                    adding additional levels of {code(">")}:"""
                )
                doc.paragraph(
                    quote(
                        f"""This is the first level of quoting.

                        {quote("This is nested blockquote.")}

                        Back to the first level.""",
                        qoute_all_lines=True,
                    )
                )
                doc.paragraph(
                    "Blockquotes can contain other Markdown elements, including headers, lists,\nand code blocks:"
                )
                doc.paragraph(
                    quote(
                        f"""{header("This is a header.", level=2)}
                        
                        {list_item("This is the first list item.", ordered=True, prefix="1.")}
                        {list_item("This is the second list item.", ordered=True, prefix="2.")}

                        Here's some example code:

                            return shell_exec("echo $input | $markdown_script");
                        """,
                        qoute_all_lines=True,
                    )
                )
                doc.paragraph(
                    """Any decent text editor should make email-style quoting easy. For
                    example, with BBEdit, you can make a selection and choose Increase
                    Quote Level from the Text menu.""",
                    linebreak=2,
                )
            with doc.heading("Lists"):
                doc.paragraph(
                    "Markdown supports ordered (numbered) and unordered (bulleted) lists."
                )
                doc.paragraph(
                    """Unordered lists use asterisks, pluses, and hyphens -- interchangably
                    -- as list markers:"""
                )
                doc.list("Red")
                doc.list("Green")
                doc.list("Blue")
                doc.linebreak()
                doc.paragraph("is equivalent to:")
                doc.list("Red", prefix="+")
                doc.list("Green", prefix="+")
                doc.list("Blue", prefix="+")
                doc.linebreak()
                doc.paragraph("and:")
                doc.list("Red", prefix="-")
                doc.list("Green", prefix="-")
                doc.list("Blue", prefix="-")
                doc.linebreak()
                doc.paragraph("Ordered lists use numbers followed by periods:")
                doc.list("Bird", prefix="1.")
                doc.list("McHale", prefix="2.")
                doc.list("Parish", prefix="3.")
                doc.linebreak()
                doc.paragraph(
                    """It's important to note that the actual numbers you use to mark the
                    list have no effect on the HTML output Markdown produces. The HTML
                    Markdown produces from the above list is:"""
                )
                doc.paragraph("If you instead wrote the list in Markdown like this:")
                doc.list("Bird", ordered=True)
                doc.list("McHale", ordered=True)
                doc.list("Parish", ordered=True)
                doc.linebreak()
                doc.paragraph("or even:")
                doc.list("Bird", prefix="3.")
                doc.list("McHale", prefix="1.")
                doc.list("Parish", prefix="8.")
                doc.linebreak()
                doc.paragraph(
                    """you'd get the exact same HTML output. The point is, if you want to,
                    you can use ordinal numbers in your ordered Markdown lists, so that
                    the numbers in your source match the numbers in your published HTML.
                    But if you want to be lazy, you don't have to."""
                )
                doc.paragraph(
                    "To make lists look nice, you can wrap items with hanging indents:"
                )
                doc.list(
                    """
                    Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                        Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
                        viverra nec, fringilla in, laoreet vitae, risus."""
                )
                doc.list(
                    """
                    Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
                        Suspendisse id sem consectetuer libero luctus adipiscing."""
                )
                doc.linebreak()
                doc.paragraph("But if you want to be lazy, you don't have to:")
                doc.paragraph(
                    """*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
                    viverra nec, fringilla in, laoreet vitae, risus.
                    *   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
                    Suspendisse id sem consectetuer libero luctus adipiscing."""
                )
                doc.paragraph(
                    """List items may consist of multiple paragraphs. Each subsequent
                    paragraph in a list item must be indented by either 4 spaces
                    or one tab:"""
                )
                with doc.list(
                    """
                    This is a list item with two paragraphs. Lorem ipsum dolor
                        sit amet, consectetuer adipiscing elit. Aliquam hendrerit
                        mi posuere lectus.""",
                    prefix="1.",
                ):
                    doc.linebreak()
                    doc.paragraph(
                        """Vestibulum enim wisi, viverra nec, fringilla in, laoreet
                        vitae, risus. Donec sit amet nisl. Aliquam semper ipsum
                        sit amet velit."""
                    )
                doc.list(
                    "Suspendisse id sem consectetuer libero luctus adipiscing.",
                    prefix="2.",
                )
                doc.linebreak()
                doc.paragraph(
                    """It looks nice if you indent every line of the subsequent
                    paragraphs, but here again, Markdown will allow you to be
                    lazy:"""
                )
                doc.list("This is a list item with two paragraphs.")
                doc.linebreak()
                doc.paragraph(
                    """
                        This is the second paragraph in the list item. You're
                    only required to indent the first line. Lorem ipsum dolor
                    sit amet, consectetuer adipiscing elit."""
                )
                doc.list("Another item in the same list.")
                doc.linebreak()
                doc.paragraph(
                    """To put a blockquote within a list item, the blockquote's `>`
                    delimiters need to be indented:"""
                )
                with doc.list("A list item with a blockquote:"):
                    doc.linebreak()
                    doc.text(quote("This is a blockquote"))
                    doc.text(quote("inside a list item."))
                doc.linebreak()
                doc.paragraph(
                    """To put a code block within a list item, the code block needs
                    to be indented *twice* -- 8 spaces or two tabs:"""
                )
                with doc.list("A list item with a code block:"):
                    doc.linebreak()
                    with doc.indentblock():
                        doc.text("<code goes here>")
                    doc.linebreak()
            with doc.heading("Code Blocks"):
                doc.paragraph(
                    f"""Pre-formatted code blocks are used for writing about programming or
                    markup source code. Rather than forming normal paragraphs, the lines
                    of a code block are interpreted literally. Markdown wraps a code block
                    in both {code("<pre>")} and {code("<code>")} tags."""
                )
                doc.paragraph(
                    """To produce a code block in Markdown, simply indent every line of the
                    block by at least 4 spaces or 1 tab."""
                )
                doc.paragraph("This is a normal paragraph:")
                with doc.indentblock():
                    doc.text("This is a code block.")
                doc.linebreak()
                doc.paragraph("Here is an example of AppleScript:")
                with doc.indentblock():
                    doc.paragraph(
                        """tell application "Foo"
                        beep
                    end tell"""
                    )
                doc.paragraph(
                    """A code block continues until it reaches a line that is not indented
                    (or the end of the article)."""
                )
                doc.paragraph(
                    """Within a code block, ampersands (`&`) and angle brackets (`<` and `>`)
                    are automatically converted into HTML entities. This makes it very
                    easy to include example HTML source code using Markdown -- just paste
                    it and indent it, and Markdown will handle the hassle of encoding the
                    ampersands and angle brackets. For example, this:"""
                )
                with doc.indentblock():
                    doc.paragraph(
                        """<div class="footer">
                            &copy; 2004 Foo Corporation
                        </div>"""
                    )
                doc.paragraph(
                    """Regular Markdown syntax is not processed within code blocks. E.g.,
                    asterisks are just literal asterisks within a code block. This means
                    it's also easy to use Markdown to write about Markdown's own syntax."""
                )
                with doc.codeblock():
                    doc.paragraph(
                        """tell application "Foo"
                            beep
                        end tell""",
                        linebreak=False,
                    )
                doc.linebreak()
        with doc.heading("Span Elements"):
            with doc.heading("Links"):
                doc.paragraph(
                    "Markdown supports two style of links: *inline* and *reference*."
                )
                doc.paragraph(
                    "In both styles, the link text is delimited by [square brackets]."
                )
                doc.paragraph(
                    """To create an inline link, use a set of regular parentheses immediately
                    after the link text's closing square bracket. Inside the parentheses,
                    put the URL where you want the link to point, along with an *optional*
                    title for the link, surrounded in quotes. For example:"""
                )
                doc.paragraph(
                    f"This is {link('http://example.com/', text='an example')} inline link."
                )
                doc.paragraph(
                    f"{link('http://example.net/', text='This link')} has no title attribute."
                )
            with doc.heading("Emphasis"):
                doc.paragraph(
                    """Markdown treats asterisks (`*`) and underscores (`_`) as indicators of
                    emphasis. Text wrapped with one `*` or `_` will be wrapped with an
                    HTML `<em>` tag; double `*`'s or `_`'s will be wrapped with an HTML
                    `<strong>` tag. E.g., this input:"""
                )
                doc.paragraph("*single asterisks*")
                doc.paragraph(italic("single underscores"))
                doc.paragraph(bold("double asterisks"))
                doc.paragraph("__double underscores__")
            with doc.heading("Code"):
                doc.paragraph(
                    """To indicate a span of code, wrap it with backtick quotes (`` ` ``).
                    Unlike a pre-formatted code block, a code span indicates code within a
                    normal paragraph. For example:"""
                )
                doc.text(f"Use the {code('printf()')} function.")

    assert doc.render() == expected
