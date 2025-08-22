#!/usr/bin/env python3
"""
Test script to get administrators for Clone organizations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

def test_organization_admins():
    """Test getting organization administrators."""
    client = MerakiClient()
    
    # Clone organization IDs
    clone_org_ids = [
        "726205439913493748",  # Clone org 1
        "726205439913493749"   # Clone org 2
    ]
    
    for org_id in clone_org_ids:
        print(f"\n{'='*60}")
        print(f"Getting administrators for organization: {org_id}")
        print('='*60)
        
        try:
            # Get organization details first
            org = client.get_organization(org_id)
            print(f"Organization Name: {org.get('name', 'Unknown')}")
            print(f"Organization ID: {org.get('id', 'Unknown')}")
            print()
            
            # Get administrators
            admins = client.get_organization_admins(org_id)
            
            if not admins:
                print("No administrators found.")
                continue
                
            print(f"Found {len(admins)} administrator(s):\n")
            
            for i, admin in enumerate(admins, 1):
                print(f"Administrator {i}:")
                print(f"  - Name: {admin.get('name', 'Unknown')}")
                print(f"  - Email: {admin.get('email', 'Unknown')}")
                print(f"  - ID: {admin.get('id', 'Unknown')}")
                print(f"  - Auth Method: {admin.get('authenticationMethod', 'Unknown')}")
                print(f"  - Two Factor Auth: {admin.get('twoFactorAuthEnabled', False)}")
                print(f"  - Account Status: {admin.get('accountStatus', 'Unknown')}")
                print(f"  - Has API Key: {admin.get('hasApiKey', False)}")
                print(f"  - Last Active: {admin.get('lastActive', 'Unknown')}")
                
                # Organization access
                if 'orgAccess' in admin:
                    print(f"  - Organization Access: {admin['orgAccess']}")
                
                # Network privileges
                if 'networks' in admin and admin['networks']:
                    print("  - Network Privileges:")
                    for network in admin['networks']:
                        print(f"    - Network {network.get('id', 'Unknown')}: {network.get('access', 'Unknown')}")
                
                # Tags
                if 'tags' in admin and admin['tags']:
                    print("  - Tags:")
                    for tag in admin['tags']:
                        print(f"    - Tag {tag.get('tag', 'Unknown')}: {tag.get('access', 'Unknown')}")
                
                print()
                
        except Exception as e:
            print(f"Error getting administrators: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_organization_admins()