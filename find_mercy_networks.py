#!/usr/bin/env python3
"""
Search for all Mercy Bariatrics related networks to find the one in the screenshot.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

def find_mercy_networks():
    """Find all networks related to Mercy Bariatrics."""
    
    print("🔍 SEARCHING FOR ALL MERCY BARIATRICS NETWORKS")
    print("=" * 60)
    
    meraki_client = MerakiClient()
    mercy_org_id = '669347494617942320'  # Mercy Bariatrics org
    
    try:
        # Get all networks in the organization
        networks = meraki_client.dashboard.organizations.getOrganizationNetworks(mercy_org_id)
        
        print(f"Found {len(networks)} total networks in Mercy Bariatrics org")
        print()
        
        mercy_networks = []
        
        for network in networks:
            network_id = network.get('id')
            network_name = network.get('name', 'Unnamed')
            product_types = network.get('productTypes', [])
            
            print(f"📡 Network: {network_name}")
            print(f"   ID: {network_id}")
            print(f"   Products: {product_types}")
            
            # Check if it has wireless
            if 'wireless' in product_types:
                print(f"   🔎 Has wireless - checking SSIDs...")
                
                try:
                    # Check for configured SSIDs
                    ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
                    
                    for ssid in ssids:
                        if ssid.get('enabled'):
                            ssid_name = ssid.get('name', 'Unnamed')
                            ssid_num = ssid.get('number', 'Unknown')
                            auth_mode = ssid.get('authMode', 'Unknown')
                            
                            print(f"      SSID {ssid_num}: {ssid_name} ({auth_mode})")
                            
                            # Check if this matches our screenshot criteria
                            if ('mercy' in ssid_name.lower() or 
                                'bariatric' in ssid_name.lower() or
                                auth_mode == 'psk'):
                                print(f"      ⭐ POTENTIAL MATCH!")
                                mercy_networks.append({
                                    'network_id': network_id,
                                    'network_name': network_name,
                                    'ssid_number': ssid_num,
                                    'ssid_name': ssid_name,
                                    'auth_mode': auth_mode
                                })
                                
                except Exception as e:
                    print(f"      ❌ Error checking SSIDs: {e}")
            
            print()
        
        print("=" * 60)
        print("🎯 POTENTIAL MATCHES FOR SCREENSHOT")
        print("=" * 60)
        
        if mercy_networks:
            for match in mercy_networks:
                print(f"Network: {match['network_name']}")
                print(f"  ID: {match['network_id']}")
                print(f"  SSID {match['ssid_number']}: {match['ssid_name']}")
                print(f"  Security: {match['auth_mode']}")
                print()
        else:
            print("❌ No networks found with WPA2 or Mercy Bariatrics SSID names")
            print("🤔 The screenshot might be from:")
            print("   - A different organization")
            print("   - A configuration that was changed")
            print("   - A different device/network")
        
    except Exception as e:
        print(f"❌ Error searching networks: {e}")

if __name__ == "__main__":
    find_mercy_networks()