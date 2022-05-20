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
