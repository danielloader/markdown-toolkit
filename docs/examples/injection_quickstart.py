from typing import Generator

import requests

from markdown_toolkit import MarkdownDocument, MarkdownInjector, bold, image, italic


def get_customers(count: int = 1) -> Generator[dict]:
    response = requests.get(
        f"https://randomuser.me/api/?seed=markdown-toolkit&results={count}&nat=gb"
    )
    for customer in response.json()["results"]:
        yield customer


def customer_name(customer: dict) -> str:
    title = customer["name"]["title"]
    first = customer["name"]["first"]
    last = customer["name"]["last"]
    profile_photo = customer["picture"]["thumbnail"]
    return f"{image(uri=profile_photo)}<br>{title} {first} {last}"


def customer_address(customer: dict) -> str:
    components = [
        str(customer["location"]["street"]["number"]),
        customer["location"]["street"]["name"],
        customer["location"]["city"],
        customer["location"]["country"],
        bold(customer["location"]["postcode"]),
    ]
    return "<br>".join(components)


with open("docs/examples/injection_source.md", "r", encoding="UTF-8") as file:
    source_document = MarkdownInjector(file)

doc = MarkdownDocument()
with doc.heading("Customers", level=2):
    doc.paragraph(f"List of Customers from the {italic('Database')}")
    with doc.table(titles=["Name", "Login", "Age", "Address"]) as table:
        for customer in get_customers(count=10):
            table.add_row(
                name=customer_name(customer),
                login=f'{customer["login"]["username"]} ({customer["email"]})',
                age=customer["dob"]["age"],
                address=customer_address(customer),
            )

source_document.anchors.customers.value = doc.render()
print(source_document.render())
