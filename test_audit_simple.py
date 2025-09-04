#!/usr/bin/env python3
"""
Simple test of the fixed audit tools.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

# Initialize the client
meraki_client = MerakiClient()

def test_basic_audit():
    """Test basic audit functionality."""
    
    print("🧪 TESTING BASIC AUDIT FUNCTIONALITY")
    print("=" * 50)
    
    network_id = 'L_669347494617957322'  # Mercy Bariatrics
    
    # Test we can get network info
    try:
        network = meraki_client.dashboard.networks.getNetwork(network_id)
        print(f"✅ Network: {network.get('name')}")
        print(f"   Products: {network.get('productTypes')}")
    except Exception as e:
        print(f"❌ Error getting network: {e}")
        return
    
    # Test IDS/IPS check
    try:
        ids = meraki_client.dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)
        print(f"✅ IDS/IPS: {ids.get('mode', 'Unknown')}")
    except Exception as e:
        print(f"❌ IDS/IPS error: {e}")
    
    # Test malware protection
    try:
        amp = meraki_client.dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)
        print(f"✅ Malware Protection: {amp.get('mode', 'Unknown')}")
    except Exception as e:
        print(f"❌ Malware error: {e}")
    
    # Test content filtering
    try:
        cf = meraki_client.dashboard.appliance.getNetworkApplianceContentFiltering(network_id)
        blocked = cf.get('blockedUrlCategories', [])
        print(f"✅ Content Filtering: {len(blocked)} categories blocked")
    except Exception as e:
        print(f"❌ Content filtering error: {e}")
    
    # Test WiFi SSIDs
    try:
        ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
        enabled_count = len([s for s in ssids if s.get('enabled')])
        
        print(f"✅ WiFi SSIDs: {enabled_count} enabled")
        
        # Check for open networks
        for ssid in ssids:
            if ssid.get('enabled') and ssid.get('authMode') == 'open':
                print(f"   ⚠️ OPEN SSID: {ssid.get('name')} (SSID {ssid.get('number')})")
    except Exception as e:
        print(f"❌ WiFi error: {e}")
    
    # Test VLANs
    try:
        vlans = meraki_client.dashboard.appliance.getNetworkApplianceVlans(network_id)
        print(f"✅ VLANs: {len(vlans) if vlans else 0} configured")
    except Exception as e:
        # VLANs might not be enabled
        print(f"ℹ️ VLANs: Not enabled or error - {e}")
    
    # Test L7 rules
    try:
        l7 = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
        rules = l7 if isinstance(l7, list) else l7.get('rules', [])
        print(f"✅ Layer 7 Rules: {len(rules)} configured")
    except Exception as e:
        print(f"❌ L7 rules error: {e}")
    
    # Test clients
    try:
        clients = meraki_client.dashboard.networks.getNetworkClients(network_id, timespan=86400)
        print(f"✅ Clients (24h): {len(clients)} unique devices")
    except Exception as e:
        print(f"❌ Clients error: {e}")
    
    print("\n📊 Summary: Basic audit checks completed")

if __name__ == "__main__":
    test_basic_audit()