#!/usr/bin/env python3
"""
Test get_organization with the organization ID that corresponds to URL segment CCxOPdIe.
"""

import os
import sys

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)

from meraki_client import MerakiClient
import json

def test_get_organization():
    """Test get_organization with the found organization ID."""
    
    # The organization ID that corresponds to URL segment "CCxOPdIe"
    org_id = "726205439913493749"
    url_segment = "CCxOPdIe"
    
    print(f"🔍 Testing get_organization for URL segment: {url_segment}")
    print(f"📋 Using Organization ID: {org_id}")
    print("=" * 60)
    
    # Initialize client
    try:
        client = MerakiClient()
    except Exception as e:
        print(f"❌ Failed to initialize Meraki client: {str(e)}")
        return
    
    # Get organization details
    print("\n📊 Getting organization details...")
    try:
        org_details = client.get_organization(org_id)
        
        print("✅ Successfully retrieved organization!")
        print("\n📄 Organization Details:")
        print(json.dumps(org_details, indent=2))
        
        # Verify the URL contains our segment
        if 'url' in org_details and url_segment in org_details['url']:
            print(f"\n✅ Confirmed: URL contains segment '{url_segment}'")
            print(f"   Full URL: {org_details['url']}")
        else:
            print(f"\n⚠️  Warning: URL segment '{url_segment}' not found in organization URL")
        
        # Check networks in this organization
        print("\n🌐 Checking networks in this organization...")
        try:
            networks = client.get_organization_networks(org_id)
            
            if networks:
                print(f"✅ Found {len(networks)} network(s):")
                for net in networks:
                    print(f"\n   • {net['name']} (ID: {net['id']})")
                    print(f"     Type: {net.get('type', 'Unknown')}")
                    if net.get('tags'):
                        print(f"     Tags: {', '.join(net.get('tags', []))}")
            else:
                print("❌ No networks found in this organization")
                
        except Exception as e:
            print(f"⚠️  Error checking networks: {str(e)}")
        
        # Check alerts configuration
        print("\n🔔 Checking alert configuration...")
        try:
            alerts = client.get_organization_alerts(org_id)
            if alerts:
                print("✅ Alert configuration retrieved")
            else:
                print("ℹ️  No alert configuration found")
        except Exception as e:
            print(f"⚠️  Error checking alerts: {str(e)}")
            
    except Exception as e:
        print(f"❌ Failed to get organization: {str(e)}")
        print(f"   Error type: {type(e).__name__}")

def main():
    """Main function."""
    # Make sure we have API key
    if not os.environ.get('MERAKI_API_KEY'):
        print("ERROR: Please set MERAKI_API_KEY environment variable")
        sys.exit(1)
    
    test_get_organization()

if __name__ == "__main__":
    main()