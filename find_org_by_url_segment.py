#!/usr/bin/env python3
"""
Find organization by URL segment.

This script searches through all organizations to find one that might have
a specific URL segment in its URL or as its ID.
"""

import os
import sys

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)

from meraki_client import MerakiClient
import json

def find_org_by_url_segment(url_segment):
    """
    Find organization that matches the given URL segment.
    
    Args:
        url_segment: The URL segment to search for (e.g., "CCxOPdIe")
    
    Returns:
        Organization details if found, None otherwise
    """
    # Initialize client
    client = MerakiClient()
    
    print(f"🔍 Searching for organization with URL segment: {url_segment}")
    print("=" * 60)
    
    try:
        # Get all organizations
        print("\n📋 Fetching all organizations...")
        organizations = client.get_organizations()
        print(f"✅ Found {len(organizations)} total organizations\n")
        
        # First, check if the URL segment is an organization ID
        print(f"🔎 Checking if '{url_segment}' is an organization ID...")
        for org in organizations:
            if org.get('id') == url_segment:
                print(f"✅ Found organization with ID matching URL segment!")
                return org
        
        print(f"❌ No organization found with ID '{url_segment}'\n")
        
        # Check each organization's details for URL containing the segment
        print("🔎 Checking organization URLs for the segment...")
        matches = []
        
        for org in organizations:
            org_id = org.get('id', 'N/A')
            org_name = org.get('name', 'N/A')
            
            try:
                # Get detailed organization information
                org_details = client.get_organization(org_id)
                
                # Check if URL contains the segment
                org_url = org_details.get('url', '')
                if url_segment in org_url:
                    print(f"✅ Found match in URL!")
                    print(f"   Organization: {org_name}")
                    print(f"   ID: {org_id}")
                    print(f"   URL: {org_url}")
                    matches.append(org_details)
                
                # Also check if the URL segment appears anywhere in the org details
                org_str = json.dumps(org_details).lower()
                if url_segment.lower() in org_str and org_details not in matches:
                    print(f"🔍 Found potential match in organization data!")
                    print(f"   Organization: {org_name}")
                    print(f"   ID: {org_id}")
                    if 'url' in org_details:
                        print(f"   URL: {org_details['url']}")
                    matches.append(org_details)
                    
            except Exception as e:
                print(f"⚠️  Error checking organization {org_name}: {str(e)}")
        
        if matches:
            print(f"\n✅ Found {len(matches)} matching organization(s)")
            return matches
        else:
            print(f"\n❌ No organizations found containing URL segment '{url_segment}'")
            
            # Show all organizations for reference
            print("\n📋 All available organizations:")
            print("-" * 60)
            for org in organizations:
                org_id = org.get('id', 'N/A')
                org_name = org.get('name', 'N/A')
                print(f"• {org_name} (ID: {org_id})")
                
                # Try to get URL for each org
                try:
                    org_details = client.get_organization(org_id)
                    if 'url' in org_details:
                        print(f"  URL: {org_details['url']}")
                except:
                    pass
            
            return None
            
    except Exception as e:
        print(f"❌ Error searching organizations: {str(e)}")
        return None

def main():
    """Main function."""
    # Get URL segment from command line or use default
    url_segment = sys.argv[1] if len(sys.argv) > 1 else "CCxOPdIe"
    
    # Make sure we have API key
    if not os.environ.get('MERAKI_API_KEY'):
        print("ERROR: Please set MERAKI_API_KEY environment variable")
        sys.exit(1)
    
    # Find organization
    result = find_org_by_url_segment(url_segment)
    
    if result:
        print("\n" + "="*60)
        print("📊 ORGANIZATION DETAILS")
        print("="*60)
        
        if isinstance(result, list):
            # Multiple matches
            for i, org in enumerate(result):
                print(f"\nMatch {i+1}:")
                print(json.dumps(org, indent=2))
        else:
            # Single match
            print(json.dumps(result, indent=2))
        
        # If we found the organization, let's also check its networks
        if isinstance(result, list):
            org_to_check = result[0]
        else:
            org_to_check = result
            
        print("\n" + "="*60)
        print("🌐 CHECKING NETWORKS")
        print("="*60)
        
        try:
            client = MerakiClient()
            networks = client.get_organization_networks(org_to_check['id'])
            
            if networks:
                print(f"\n✅ Found {len(networks)} network(s):")
                for net in networks:
                    print(f"\n• {net['name']} (ID: {net['id']})")
                    print(f"  Type: {net.get('type', 'Unknown')}")
                    if net.get('tags'):
                        print(f"  Tags: {', '.join(net.get('tags', []))}")
            else:
                print("\n❌ No networks found in this organization")
                
        except Exception as e:
            print(f"\n⚠️  Error checking networks: {str(e)}")

if __name__ == "__main__":
    main()