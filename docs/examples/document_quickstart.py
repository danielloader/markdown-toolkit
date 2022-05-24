from datetime import datetime

import requests

from markdown_toolkit import MarkdownDocument, image

QUOTES_COUNT = 10


def calculate_age() -> int:
    year = 365 * 24 * 60 * 60
    rons_birthday = datetime(year=1967, month=4, day=30)
    now = datetime.now()
    return int(divmod((now - rons_birthday).total_seconds(), year)[0])


quotes = requests.get(
    f"http://ron-swanson-quotes.herokuapp.com/v2/quotes/{QUOTES_COUNT}"
)

doc = MarkdownDocument()
with doc.heading("Ron Swanson"):
    with doc.heading("Biography"):
        doc.paragraph(image(uri="img/ron_swanson.jpg"))
        doc.list(f'Name: Ronald Ulysses "Ron" Swanson')
        doc.list(f"Age: {calculate_age()}")
    with doc.heading(f"Top {QUOTES_COUNT} Greatest Quotes"):
        doc.paragraph(
            "Ron is known for some insightful quotes, here's some of the best:"
        )
        for quote in quotes.json():
            doc.list(quote)

print(doc.render())
