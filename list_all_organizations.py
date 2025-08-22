#!/usr/bin/env python3
"""
List all organizations accessible with the current API key
"""

import os
import sys

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)

from meraki_client import MerakiClient

def list_all_organizations():
    """List all organizations accessible with the current API key"""
    
    # Initialize client
    client = MerakiClient()
    
    print("Listing all accessible organizations...")
    print("=" * 60)
    
    try:
        organizations = client.get_organizations()
        
        if not organizations:
            print("No organizations found for this API key.")
        else:
            print(f"\nFound {len(organizations)} organization(s):\n")
            
            # Check if Q_EopcIe is in the list
            target_org_found = False
            
            for org in organizations:
                org_id = org.get('id', 'N/A')
                org_name = org.get('name', 'N/A')
                
                # Highlight if this is our target organization
                if org_id == "Q_EopcIe":
                    print(f">>> FOUND TARGET: {org_name} (ID: {org_id}) <<<")
                    target_org_found = True
                else:
                    print(f"- {org_name} (ID: {org_id})")
                
                # Show additional details
                if org.get('url'):
                    print(f"  URL: {org['url']}")
                if org.get('api', {}).get('enabled') is not None:
                    print(f"  API Enabled: {org['api']['enabled']}")
                print()
            
            if not target_org_found:
                print("\n⚠️  Organization ID 'Q_EopcIe' was NOT found in the accessible organizations list.")
                print("This means either:")
                print("1. The organization ID is incorrect")
                print("2. The API key doesn't have access to this organization")
                
    except Exception as e:
        print(f"Error listing organizations: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    # Make sure we have API key
    if not os.environ.get('MERAKI_API_KEY'):
        print("ERROR: Please set MERAKI_API_KEY environment variable")
        sys.exit(1)
    
    list_all_organizations()