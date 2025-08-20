#!/usr/bin/env python3
"""
Simple example showing how to use get_organizations to list all organizations
and find one named "Western ENT" or similar.
"""

from meraki_client import MerakiClient

# Initialize the Meraki client
client = MerakiClient()

# Get all organizations
print("Fetching all organizations...")
organizations = client.get_organizations()

# Display all organizations
print(f"\nFound {len(organizations)} organizations:")
for org in organizations:
    print(f"- {org['name']} (ID: {org['id']})")

# Search for "Western ENT" or similar
print("\nSearching for 'Western ENT' or similar...")
western_ent_orgs = [
    org for org in organizations 
    if 'western' in org['name'].lower() or 'ent' in org['name'].lower()
]

if western_ent_orgs:
    print(f"\nFound {len(western_ent_orgs)} matching organization(s):")
    for org in western_ent_orgs:
        print(f"- {org['name']} (ID: {org['id']})")
        
        # Get more details about this organization
        org_details = client.get_organization(org['id'])
        print(f"  URL: {org_details.get('url', 'N/A')}")
        
        # Get networks in this organization
        networks = client.get_organization_networks(org['id'])
        print(f"  Number of networks: {len(networks)}")
else:
    print("\nNo organizations found matching 'Western ENT' or similar.")