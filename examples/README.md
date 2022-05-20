# Examples

> **INFO:** Examples here are automatically taken from the `examples` directory and shown below.

## [`examples/example_aws.py`](examples/example_aws.py)

```python
"""Example to generate tables of AWS Org Units in Markdown."""
from collections import defaultdict
from typing import List, Tuple

import boto3
import moto
from markdown_toolkit import MarkdownDocument

from examples.utils.aws_org import setup_accounts

mock = moto.mock_organizations()
mock.start()
org = boto3.client("organizations")
setup_accounts(org)


def get_all_accounts(parentid: str, org_client: str) -> Tuple[str, dict]:
    """Organisation Account Generator.

    Args:
        parentid (str): Id of Org unit to start at.
        org_client (boto3.client): Client to iterate with.

    Yields:
        tuple(str,dict): Organisation Unit Name, Account Information
    """
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
    collated_accounts[name.title()].append(account)

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
### Customers

| Id | Arn | Email | Name | Status | JoinedMethod | JoinedTimestamp |
| --- | --- | --- | --- | --- | --- | --- |
| 519271310306 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/519271310306 | account+customer1@example.com | customer1 | ACTIVE | CREATED | 2022-05-20 09:29:26.043531+00:00 |
| 481835384758 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/481835384758 | account+customer2@example.com | customer2 | ACTIVE | CREATED | 2022-05-20 09:29:26.047826+00:00 |
| 121421799398 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/121421799398 | account+customer3@example.com | customer3 | ACTIVE | CREATED | 2022-05-20 09:29:26.050721+00:00 |

### Root

| Id | Arn | Email | Name | Status | JoinedMethod | JoinedTimestamp |
| --- | --- | --- | --- | --- | --- | --- |
| 123456789012 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/123456789012 | master@example.com | master | ACTIVE | CREATED | 2022-05-20 09:29:26.028908+00:00 |
| 321432293313 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/321432293313 | account+audit@example.com | cloudtrail | ACTIVE | CREATED | 2022-05-20 09:29:26.035425+00:00 |
| 956167072858 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/956167072858 | account+cloudwatch@example.com | cloudwatch | ACTIVE | CREATED | 2022-05-20 09:29:26.037498+00:00 |
| 568840745363 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/568840745363 | account+resources@example.com | resources | ACTIVE | CREATED | 2022-05-20 09:29:26.039073+00:00 |

```
</details>


<details><summary>Markdown Rendered:</summary>

### Customers

| Id | Arn | Email | Name | Status | JoinedMethod | JoinedTimestamp |
| --- | --- | --- | --- | --- | --- | --- |
| 519271310306 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/519271310306 | account+customer1@example.com | customer1 | ACTIVE | CREATED | 2022-05-20 09:29:26.043531+00:00 |
| 481835384758 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/481835384758 | account+customer2@example.com | customer2 | ACTIVE | CREATED | 2022-05-20 09:29:26.047826+00:00 |
| 121421799398 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/121421799398 | account+customer3@example.com | customer3 | ACTIVE | CREATED | 2022-05-20 09:29:26.050721+00:00 |

### Root

| Id | Arn | Email | Name | Status | JoinedMethod | JoinedTimestamp |
| --- | --- | --- | --- | --- | --- | --- |
| 123456789012 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/123456789012 | master@example.com | master | ACTIVE | CREATED | 2022-05-20 09:29:26.028908+00:00 |
| 321432293313 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/321432293313 | account+audit@example.com | cloudtrail | ACTIVE | CREATED | 2022-05-20 09:29:26.035425+00:00 |
| 956167072858 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/956167072858 | account+cloudwatch@example.com | cloudwatch | ACTIVE | CREATED | 2022-05-20 09:29:26.037498+00:00 |
| 568840745363 | arn:aws:organizations::123456789012:account/o-kztcujnp4v/568840745363 | account+resources@example.com | resources | ACTIVE | CREATED | 2022-05-20 09:29:26.039073+00:00 |

</details>


----

## [`examples/example_headings.py`](examples/example_headings.py)

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

## [`examples/example_lists.py`](examples/example_lists.py)

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

## [`examples/example_tables.py`](examples/example_tables.py)

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
