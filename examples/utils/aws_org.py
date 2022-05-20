from collections import defaultdict
from typing import List

import boto3
import moto

from markdown_toolkit import MarkdownDocument

mock = moto.mock_organizations()
mock.start()


def setup_accounts(org_client):
    """Create a test AWS Org to poll for markdown tests."""
    root_accounts = [
        ("account+audit@example.com", "cloudtrail"),
        ("account+cloudwatch@example.com", "cloudwatch"),
        ("account+resources@example.com", "resources"),
    ]
    customer_accounts = [
        ("account+customer1@example.com", "customer1"),
        ("account+customer2@example.com", "customer2"),
        ("account+customer3@example.com", "customer3"),
    ]
    org_client.create_organization(FeatureSet="ALL")
    root = org_client.list_roots()["Roots"][0]
    for email, account_name in root_accounts:
        org_client.create_account(
            Email=email,
            AccountName=account_name,
        )

    customers_ou = org_client.create_organizational_unit(
        ParentId=root["Id"],
        Name="customers",
        Tags=[
            {"Key": "string", "Value": "string"},
        ],
    )

    for email, account_name in customer_accounts:
        cust_account = org_client.create_account(
            Email=email,
            AccountName=account_name,
        )
        org_client.move_account(
            AccountId=cust_account["CreateAccountStatus"]["AccountId"],
            SourceParentId=root["Id"],
            DestinationParentId=customers_ou["OrganizationalUnit"]["Id"],
        )
