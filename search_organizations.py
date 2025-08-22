#!/usr/bin/env python3
"""
Search for organizations by keyword and check if they have networks.

This script:
1. Lists all organizations
2. Filters organizations by keyword in their name (case-insensitive)
3. Gets details for each matching organization
4. Checks if they have any networks
5. Reports the results
"""

from meraki_client import MerakiClient
import sys
import json

def has_keyword_in_name(org, keyword):
    """
    Check if an organization has the keyword in its name.
    
    Args:
        org: Organization object from Meraki API
        keyword: Keyword to search for
        
    Returns:
        bool: True if keyword is in the organization name (case-insensitive)
    """
    name = org.get('name', '').lower()
    return keyword.lower() in name

def main(keyword=None):
    """Main function to search organizations and check their networks."""
    if keyword:
        print(f"🔍 Searching for organizations with '{keyword}' in the name...\n")
    else:
        print("🔍 Listing all organizations and their network status...\n")
    
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
    
    # Filter organizations by keyword if provided
    if keyword:
        matching_orgs = []
        for org in organizations:
            if has_keyword_in_name(org, keyword):
                matching_orgs.append(org)
        
        if not matching_orgs:
            print(f"ℹ️  No organizations with '{keyword}' in the name found.")
            print("\n📋 All available organizations:")
            print("-" * 40)
            for org in organizations:
                print(f"• {org['name']} (ID: {org['id']})")
            return
        
        print(f"🔎 Found {len(matching_orgs)} organizations with '{keyword}' in the name:\n")
        orgs_to_check = matching_orgs
    else:
        orgs_to_check = organizations
    
    # Check each organization for details and networks
    results = []
    
    for org in orgs_to_check:
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
                print(f"   • API Enabled: {org_details.get('api', {}).get('enabled', 'N/A')}")
            if 'licensing' in org_details:
                licensing = org_details.get('licensing', {})
                print(f"   • Licensing Model: {licensing.get('model', 'N/A')}")
            if 'cloud' in org_details:
                cloud = org_details.get('cloud', {})
                region = cloud.get('region', {})
                print(f"   • Cloud Region: {region.get('name', 'N/A')}")
            
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
    if keyword:
        print(f"📊 SUMMARY REPORT - Organizations with '{keyword}' in name")
    else:
        print("📊 SUMMARY REPORT - All Organizations")
    print("="*60 + "\n")
    
    empty_orgs = [r for r in results if r['has_networks'] is False]
    non_empty_orgs = [r for r in results if r['has_networks'] is True]
    error_orgs = [r for r in results if r['has_networks'] is None]
    
    if empty_orgs:
        print(f"🗑️  Empty Organizations ({len(empty_orgs)}):")
        print("-" * 40)
        for result in empty_orgs:
            org = result['org']
            print(f"• {org['name']}")
            print(f"  ID: {org['id']}")
            print()
    else:
        print("✅ No empty organizations found!")
    
    if non_empty_orgs:
        print(f"\n📦 Organizations with Networks ({len(non_empty_orgs)}):")
        print("-" * 40)
        for result in non_empty_orgs:
            org = result['org']
            print(f"• {org['name']} - {result['network_count']} network(s)")
            print(f"  ID: {org['id']}")
            print()
    
    if error_orgs:
        print(f"\n⚠️  Organizations with Errors ({len(error_orgs)}):")
        print("-" * 40)
        for result in error_orgs:
            org = result['org']
            print(f"• {org['name']}")
            print(f"  ID: {org['id']}")
            print(f"  Error: {result.get('error', 'Unknown error')}")
            print()
    
    print("\n" + "="*60)
    print(f"Total organizations checked: {len(orgs_to_check)}")
    print(f"Empty organizations: {len(empty_orgs)}")
    print(f"Organizations with networks: {len(non_empty_orgs)}")
    print(f"Organizations with errors: {len(error_orgs)}")
    print("="*60)

if __name__ == "__main__":
    # Get keyword from command line if provided
    keyword = sys.argv[1] if len(sys.argv) > 1 else None
    main(keyword)