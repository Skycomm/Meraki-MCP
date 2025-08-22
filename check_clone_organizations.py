#!/usr/bin/env python3
"""
Search for organizations with 'clone' in the name and check if they have networks.

This script:
1. Lists all organizations
2. Filters organizations with 'clone' in their name (case-insensitive)
3. Gets details for each clone organization
4. Checks if they have any networks
5. Reports the results
"""

from meraki_client import MerakiClient
import json

def has_clone_in_name(org):
    """
    Check if an organization has 'clone' in its name.
    
    Args:
        org: Organization object from Meraki API
        
    Returns:
        bool: True if 'clone' is in the organization name (case-insensitive)
    """
    name = org.get('name', '').lower()
    return 'clone' in name

def main():
    """Main function to check for clone organizations and their networks."""
    print("🔍 Searching for organizations with 'clone' in the name...\n")
    
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
    
    # Filter organizations with 'clone' in the name
    clone_orgs = []
    for org in organizations:
        if has_clone_in_name(org):
            clone_orgs.append(org)
    
    if not clone_orgs:
        print("ℹ️  No organizations with 'clone' in the name found.")
        print("\n📋 All available organizations:")
        print("-" * 40)
        for org in organizations:
            print(f"• {org['name']} (ID: {org['id']})")
        return
    
    print(f"🧬 Found {len(clone_orgs)} organizations with 'clone' in the name:\n")
    
    # Check each clone organization for details and networks
    results = []
    
    for org in clone_orgs:
        org_id = org['id']
        org_name = org['name']
        
        print(f"=" * 60)
        print(f"📁 Organization: {org_name}")
        print(f"   ID: {org_id}")
        
        # Get detailed organization information
        try:
            org_details = client.get_organization(org_id)
            print(f"\n   📊 Organization Details:")
            print(f"   • Name: {org_details.get('name', 'N/A')}")
            print(f"   • ID: {org_details.get('id', 'N/A')}")
            if 'url' in org_details:
                print(f"   • URL: {org_details.get('url', 'N/A')}")
            if 'api' in org_details:
                print(f"   • API: {org_details.get('api', {}).get('enabled', 'N/A')}")
            if 'licensing' in org_details:
                licensing = org_details.get('licensing', {})
                print(f"   • Licensing Model: {licensing.get('model', 'N/A')}")
            if 'cloud' in org_details:
                cloud = org_details.get('cloud', {})
                print(f"   • Cloud Region: {cloud.get('region', {}).get('name', 'N/A')}")
            
        except Exception as e:
            print(f"   ⚠️  Error getting organization details: {str(e)}")
            org_details = org
        
        # Check for networks
        print(f"\n   🌐 Checking networks...")
        try:
            networks = client.get_organization_networks(org_id)
            network_count = len(networks)
            
            if network_count == 0:
                print(f"   └─ ❌ EMPTY - No networks found")
                results.append({
                    'org': org_details,
                    'has_networks': False,
                    'network_count': 0,
                    'networks': []
                })
            else:
                print(f"   └─ ✅ Has {network_count} network(s):")
                # List all networks
                for i, net in enumerate(networks):
                    print(f"      {i+1}. {net['name']} (ID: {net['id']})")
                    print(f"         • Type: {net.get('type', 'Unknown')}")
                    if net.get('tags'):
                        print(f"         • Tags: {', '.join(net.get('tags', []))}")
                    if net.get('timeZone'):
                        print(f"         • Time Zone: {net.get('timeZone')}")
                
                results.append({
                    'org': org_details,
                    'has_networks': True,
                    'network_count': network_count,
                    'networks': networks
                })
                
        except Exception as e:
            print(f"   └─ ⚠️  Error checking networks: {str(e)}")
            results.append({
                'org': org_details,
                'has_networks': None,
                'network_count': None,
                'networks': None,
                'error': str(e)
            })
        
        print()
    
    # Summary report
    print("\n" + "="*60)
    print("📊 SUMMARY REPORT - Organizations with 'clone' in name")
    print("="*60 + "\n")
    
    empty_clone_orgs = [r for r in results if r['has_networks'] is False]
    non_empty_clone_orgs = [r for r in results if r['has_networks'] is True]
    error_clone_orgs = [r for r in results if r['has_networks'] is None]
    
    if empty_clone_orgs:
        print(f"🗑️  Empty Clone Organizations ({len(empty_clone_orgs)}):")
        print("-" * 40)
        for result in empty_clone_orgs:
            org = result['org']
            print(f"• {org['name']}")
            print(f"  ID: {org['id']}")
            print()
    else:
        print("✅ No empty clone organizations found!")
    
    if non_empty_clone_orgs:
        print(f"\n📦 Clone Organizations with Networks ({len(non_empty_clone_orgs)}):")
        print("-" * 40)
        for result in non_empty_clone_orgs:
            org = result['org']
            print(f"• {org['name']} - {result['network_count']} network(s)")
            print(f"  ID: {org['id']}")
            print()
    
    if error_clone_orgs:
        print(f"\n⚠️  Organizations with Errors ({len(error_clone_orgs)}):")
        print("-" * 40)
        for result in error_clone_orgs:
            org = result['org']
            print(f"• {org['name']}")
            print(f"  ID: {org['id']}")
            print(f"  Error: {result.get('error', 'Unknown error')}")
            print()
    
    print("\n" + "="*60)
    print(f"Total organizations with 'clone' in name: {len(clone_orgs)}")
    print(f"Empty organizations: {len(empty_clone_orgs)}")
    print(f"Organizations with networks: {len(non_empty_clone_orgs)}")
    print(f"Organizations with errors: {len(error_clone_orgs)}")
    print("="*60)

if __name__ == "__main__":
    main()