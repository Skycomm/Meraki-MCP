#!/usr/bin/env python3
"""
Check for empty test organizations in Meraki.

This script:
1. Lists all organizations
2. Identifies test organizations (with "test" in name)
3. Checks if they have any networks
4. Reports which test organizations are empty
"""

from meraki_client import MerakiClient
from datetime import datetime, timezone
import json

def is_test_organization(org):
    """
    Determine if an organization is a test organization.
    
    Args:
        org: Organization object from Meraki API
        
    Returns:
        bool: True if organization appears to be for testing
    """
    # Check if "test" is in the name (case-insensitive)
    name = org.get('name', '').lower()
    if 'test' in name:
        return True
    
    # Check if organization was created recently (if createdAt field exists)
    # Note: Meraki API might not return creation date for all organizations
    if 'createdAt' in org:
        try:
            created_date = datetime.fromisoformat(org['createdAt'].replace('Z', '+00:00'))
            days_old = (datetime.now(timezone.utc) - created_date).days
            # Consider organizations created in last 7 days as potentially test
            if days_old <= 7:
                return True
        except Exception:
            pass
    
    return False

def main():
    """Main function to check for empty test organizations."""
    print("🔍 Checking for empty test organizations in Meraki...\n")
    
    # Initialize Meraki client
    try:
        client = MerakiClient()
    except Exception as e:
        print(f"❌ Failed to initialize Meraki client: {str(e)}")
        return
    
    # Get all organizations
    print("📋 Fetching all organizations...")
    try:
        organizations = client.get_organizations()
        print(f"✅ Found {len(organizations)} total organizations\n")
    except Exception as e:
        print(f"❌ Failed to get organizations: {str(e)}")
        return
    
    # Filter for test organizations
    test_orgs = []
    for org in organizations:
        if is_test_organization(org):
            test_orgs.append(org)
    
    if not test_orgs:
        print("ℹ️  No test organizations found.")
        return
    
    print(f"🧪 Found {len(test_orgs)} test organizations:\n")
    
    # Check each test organization for networks
    empty_orgs = []
    non_empty_orgs = []
    
    for org in test_orgs:
        org_id = org['id']
        org_name = org['name']
        
        print(f"Checking organization: {org_name} (ID: {org_id})")
        
        try:
            networks = client.get_organization_networks(org_id)
            network_count = len(networks)
            
            if network_count == 0:
                empty_orgs.append(org)
                print(f"  └─ ❌ EMPTY - No networks found\n")
            else:
                non_empty_orgs.append((org, network_count))
                print(f"  └─ ✅ Has {network_count} network(s)")
                # List first few networks
                for i, net in enumerate(networks[:3]):
                    print(f"     • {net['name']} ({net.get('type', 'Unknown')})")
                if network_count > 3:
                    print(f"     • ... and {network_count - 3} more")
                print()
                
        except Exception as e:
            print(f"  └─ ⚠️  Error checking networks: {str(e)}\n")
    
    # Summary report
    print("\n" + "="*60)
    print("📊 SUMMARY REPORT")
    print("="*60 + "\n")
    
    if empty_orgs:
        print(f"🗑️  Empty Test Organizations ({len(empty_orgs)}):")
        print("-" * 40)
        for org in empty_orgs:
            print(f"• {org['name']}")
            print(f"  ID: {org['id']}")
            if 'createdAt' in org:
                print(f"  Created: {org['createdAt']}")
            print()
    else:
        print("✅ No empty test organizations found!")
    
    if non_empty_orgs:
        print(f"\n📦 Test Organizations with Networks ({len(non_empty_orgs)}):")
        print("-" * 40)
        for org, count in non_empty_orgs:
            print(f"• {org['name']} - {count} network(s)")
    
    print("\n" + "="*60)
    print(f"Total test organizations: {len(test_orgs)}")
    print(f"Empty organizations: {len(empty_orgs)}")
    print(f"Organizations with networks: {len(non_empty_orgs)}")
    print("="*60)

if __name__ == "__main__":
    main()