#!/usr/bin/env python3
"""
Script to list all networks in the Western ENT organization with detailed information.
"""

from meraki_client import MerakiClient
import json

def list_western_ent_networks():
    """List all networks in Western ENT organization with details."""
    # Initialize the Meraki client
    client = MerakiClient()
    
    # Organization ID for Western ENT
    org_id = "686470"
    
    print(f"Fetching all networks in Western ENT organization (ID: {org_id})...\n")
    
    try:
        # Get all networks in the organization
        networks = client.get_organization_networks(org_id)
        
        if not networks:
            print(f"No networks found in organization {org_id}")
            return
        
        print(f"Found {len(networks)} networks in Western ENT:\n")
        print("=" * 80)
        
        # Display each network with details
        for i, network in enumerate(networks, 1):
            print(f"\n{i}. Network: {network['name']}")
            print(f"   ID: {network['id']}")
            print(f"   Type: {network.get('type', 'Not specified')}")
            
            # Product types if available
            if 'productTypes' in network:
                print(f"   Product Types: {', '.join(network['productTypes'])}")
            
            # Tags
            tags = network.get('tags', [])
            if tags:
                print(f"   Tags: {', '.join(tags)}")
            else:
                print(f"   Tags: None")
            
            # Time zone if available
            if 'timeZone' in network:
                print(f"   Time Zone: {network['timeZone']}")
            
            # Notes if available
            if 'notes' in network and network['notes']:
                print(f"   Notes: {network['notes']}")
            
            print("-" * 80)
        
        # Save to JSON file for reference
        with open('western_ent_networks.json', 'w') as f:
            json.dump(networks, f, indent=2)
        print(f"\n✅ Network data saved to western_ent_networks.json")
        
    except Exception as e:
        print(f"\n❌ Error fetching networks: {str(e)}")

if __name__ == "__main__":
    list_western_ent_networks()