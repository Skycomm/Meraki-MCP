#!/usr/bin/env python3
"""
Example: Get organization administrators using the Meraki API.

This script demonstrates how to retrieve the list of dashboard administrators
for a Meraki organization.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

def main():
    # Initialize the Meraki client
    client = MerakiClient()
    
    # Example: Get administrators for a specific organization
    org_id = "726205439913493748"  # Replace with your organization ID
    
    try:
        # Get the organization details
        org = client.get_organization(org_id)
        print(f"Organization: {org['name']} (ID: {org['id']})")
        print("-" * 50)
        
        # Get all administrators
        admins = client.get_organization_admins(org_id)
        
        print(f"\nTotal administrators: {len(admins)}")
        print("\nAdministrator list:")
        
        for admin in admins:
            print(f"\n- {admin['name']} ({admin['email']})")
            print(f"  Access level: {admin['orgAccess']}")
            print(f"  Has API key: {admin['hasApiKey']}")
            print(f"  Two-factor auth: {admin['twoFactorAuthEnabled']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()