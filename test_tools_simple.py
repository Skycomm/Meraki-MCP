#!/usr/bin/env python3
"""Simple test for tools"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from meraki_client import MerakiClient

# Initialize
meraki = MerakiClient()

# Get networks
orgs = meraki.get_organizations()
print(f"Found {len(orgs)} organizations")

for org in orgs:
    print(f"\nOrganization: {org['name']} ({org['id']})")
    networks = meraki.get_organization_networks(org['id'])
    print(f"Networks ({len(networks)}):")
    for net in networks:
        print(f"  - {net['name']} ({net['id']})")
        print(f"    Types: {', '.join(net.get('productTypes', []))}")