import requests
import json
from markdown_toolkit import MarkdownInjector, MarkdownBuilder


with MarkdownInjector(path="TEST.md", anchor="#example") as block, MarkdownBuilder() as doc:
    url = "https://random-data-api.com/api/users/random_user"
    random_user = json.dumps(
        requests.get(url).json(),
        indent=2
    )
    doc.info(f"Retrieved from {url}.")
    doc.code(source=random_user, language="json")
    doc.write(block)
