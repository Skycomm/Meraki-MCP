#!/usr/bin/env python3
"""
Test script to get organization details and networks for organization ID: Q_EopcIe
"""

import os
import sys

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)

from meraki_client import MerakiClient

def test_organization():
    """Test get_organization and get_organization_networks with org ID Q_EopcIe"""
    
    # Initialize client
    client = MerakiClient()
    
    # Organization ID to test
    # Note: Q_EopcIe is the URL segment, the actual org ID is 726205439913493748
    org_id = "726205439913493748"
    
    print(f"Testing organization ID: {org_id}")
    print("=" * 60)
    
    # Test 1: Get organization details
    print("\n1. Getting organization details...")
    try:
        org_details = client.get_organization(org_id)
        print("\nOrganization Details:")
        print(f"- Name: {org_details.get('name', 'N/A')}")
        print(f"- ID: {org_details.get('id', 'N/A')}")
        print(f"- URL: {org_details.get('url', 'N/A')}")
        print(f"- API: {org_details.get('api', {})}")
        print(f"- Licensing: {org_details.get('licensing', {})}")
        print(f"- Cloud: {org_details.get('cloud', {})}")
        print("\nFull response:")
        import json
        print(json.dumps(org_details, indent=2))
    except Exception as e:
        print(f"Error getting organization details: {str(e)}")
        print(f"Error type: {type(e).__name__}")
    
    # Test 2: Get organization networks
    print("\n" + "=" * 60)
    print("\n2. Getting organization networks...")
    try:
        networks = client.get_organization_networks(org_id)
        
        if not networks:
            print("No networks found in this organization.")
        else:
            print(f"\nFound {len(networks)} network(s):")
            for i, network in enumerate(networks, 1):
                print(f"\nNetwork {i}:")
                print(f"- Name: {network.get('name', 'N/A')}")
                print(f"- ID: {network.get('id', 'N/A')}")
                print(f"- Type: {network.get('type', 'N/A')}")
                print(f"- Tags: {', '.join(network.get('tags', []) or ['None'])}")
                print(f"- Time Zone: {network.get('timeZone', 'N/A')}")
                print(f"- Product Types: {', '.join(network.get('productTypes', []) or ['None'])}")
                
    except Exception as e:
        print(f"Error getting organization networks: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    # Make sure we have API key
    if not os.environ.get('MERAKI_API_KEY'):
        print("ERROR: Please set MERAKI_API_KEY environment variable")
        sys.exit(1)
    
    test_organization()