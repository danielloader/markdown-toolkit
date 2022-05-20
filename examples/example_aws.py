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
    collated_accounts[name].append(account)

doc = MarkdownDocument()
for org_unit, table in collated_accounts.items():
    with doc.heading(level=3, heading=org_unit):
        doc.table(table)

with open("examples/example_aws.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())

mock.stop()
