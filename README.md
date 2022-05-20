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

### [`examples/example_aws.py`](examples/example_aws.py)

```python
"""Example to generate tables of AWS Org Units in Markdown."""
from collections import defaultdict
from typing import List

import boto3
import moto

from markdown_toolkit import MarkdownDocument
from examples.utils.aws_org import setup_accounts

mock = moto.mock_organizations()
mock.start()
org = boto3.client("organizations")
setup_accounts(org)


def get_all_accounts(parentid, org_client):
    org_units = org_client.list_children(
        ParentId=parentid, ChildType="ORGANIZATIONAL_UNIT"
    )
    for org_unit in org_units["Children"]:
        yield from get_all_accounts(org_unit["Id"], org_client)

    org_accounts = org_client.list_children(ParentId=parentid, ChildType="ACCOUNT")
    for child in org_accounts["Children"]:
        ou_name = org_client.describe_organizational_unit(
            OrganizationalUnitId=parentid
        ).get("OrganizationalUnit", {"Name": "root"})["Name"]
        account_info = org_client.describe_account(AccountId=child["Id"])["Account"]
        yield (ou_name, account_info)


root_id = org.list_roots()["Roots"][0]["Id"]
collated_accounts = defaultdict(list)
for name, account in get_all_accounts(root_id, org):
    collated_accounts[name].append(account)

doc = MarkdownDocument()
for org_unit, table in collated_accounts.items():
    with doc.heading(level=3, heading=org_unit):
        doc.table(table)

with open("examples/example_aws.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())

mock.stop()

```

<details><summary>Markdown Output:</summary>

```markdown
### customers

| Id | Arn | Email | Name | Status | JoinedMethod | JoinedTimestamp |
| --- | --- | --- | --- | --- | --- | --- |
| 052305242565 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/052305242565 | account+customer1@example.com | customer1 | ACTIVE | CREATED | 2022-05-20 09:19:00.463806+00:00 |
| 564734818981 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/564734818981 | account+customer2@example.com | customer2 | ACTIVE | CREATED | 2022-05-20 09:19:00.467967+00:00 |
| 687880000825 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/687880000825 | account+customer3@example.com | customer3 | ACTIVE | CREATED | 2022-05-20 09:19:00.470816+00:00 |

### root

| Id | Arn | Email | Name | Status | JoinedMethod | JoinedTimestamp |
| --- | --- | --- | --- | --- | --- | --- |
| 123456789012 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/123456789012 | master@example.com | master | ACTIVE | CREATED | 2022-05-20 09:19:00.449350+00:00 |
| 603903114667 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/603903114667 | account+audit@example.com | cloudtrail | ACTIVE | CREATED | 2022-05-20 09:19:00.455824+00:00 |
| 285409087291 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/285409087291 | account+cloudwatch@example.com | cloudwatch | ACTIVE | CREATED | 2022-05-20 09:19:00.457859+00:00 |
| 012647750333 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/012647750333 | account+resources@example.com | resources | ACTIVE | CREATED | 2022-05-20 09:19:00.459381+00:00 |

```
</details>


<details><summary>Markdown Rendered:</summary>

### customers

| Id | Arn | Email | Name | Status | JoinedMethod | JoinedTimestamp |
| --- | --- | --- | --- | --- | --- | --- |
| 052305242565 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/052305242565 | account+customer1@example.com | customer1 | ACTIVE | CREATED | 2022-05-20 09:19:00.463806+00:00 |
| 564734818981 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/564734818981 | account+customer2@example.com | customer2 | ACTIVE | CREATED | 2022-05-20 09:19:00.467967+00:00 |
| 687880000825 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/687880000825 | account+customer3@example.com | customer3 | ACTIVE | CREATED | 2022-05-20 09:19:00.470816+00:00 |

### root

| Id | Arn | Email | Name | Status | JoinedMethod | JoinedTimestamp |
| --- | --- | --- | --- | --- | --- | --- |
| 123456789012 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/123456789012 | master@example.com | master | ACTIVE | CREATED | 2022-05-20 09:19:00.449350+00:00 |
| 603903114667 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/603903114667 | account+audit@example.com | cloudtrail | ACTIVE | CREATED | 2022-05-20 09:19:00.455824+00:00 |
| 285409087291 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/285409087291 | account+cloudwatch@example.com | cloudwatch | ACTIVE | CREATED | 2022-05-20 09:19:00.457859+00:00 |
| 012647750333 | arn:aws:organizations::123456789012:account/o-thh2xor2bj/012647750333 | account+resources@example.com | resources | ACTIVE | CREATED | 2022-05-20 09:19:00.459381+00:00 |

</details>


----

### [`examples/example_headings.py`](examples/example_headings.py)

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

<details><summary>Markdown Output:</summary>

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
</details>


<details><summary>Markdown Rendered:</summary>

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

</details>


----

### [`examples/example_lists.py`](examples/example_lists.py)

```python
from markdown_toolkit import MarkdownDocument, bold, italic, link

doc = MarkdownDocument()
doc.list("Example Item")
with doc.list("List Item that has children"):
    for item in ["First Item", "Second Item", "Third Item"]:
        doc.list(item)

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

<details><summary>Markdown Output:</summary>

```markdown
*   Example Item
*   List Item that has children
    *   First Item
    *   Second Item
    *   Third Item
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
</details>


<details><summary>Markdown Rendered:</summary>

*   Example Item
*   List Item that has children
    *   First Item
    *   Second Item
    *   Third Item
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
</details>


----

### [`examples/example_tables.py`](examples/example_tables.py)

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

<details><summary>Markdown Output:</summary>

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
</details>


<details><summary>Markdown Rendered:</summary>

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

</details>


----
