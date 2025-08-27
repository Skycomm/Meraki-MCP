#!/usr/bin/env python3
"""
Configure WiFi for Sam Middlemas Home network.
The org and network already exist, just need to configure SSIDs.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from meraki_client import MerakiClient
from datetime import datetime

# Initialize client
meraki = MerakiClient()

def configure_wifi():
    """Configure WiFi SSIDs for Sam Middlemas Home network."""
    
    print("="*80)
    print("CONFIGURE WIFI FOR SAM MIDDLEMAS HOME NETWORK")
    print("="*80)
    
    # Known IDs from creation
    org_id = "726205439913493783"
    network_id = "N_726205439913521314"
    
    print(f"Organization: Sam Middlemas (ID: {org_id})")
    print(f"Network: Home (ID: {network_id})")
    print("="*80)
    
    success_count = 0
    
    # Configure Main WiFi
    print("\n📋 CONFIGURING MAIN WIFI NETWORK")
    print("-"*40)
    
    try:
        ssid_config = meraki.dashboard.wireless.updateNetworkWirelessSsid(
            networkId=network_id,
            number=0,  # First SSID
            name="Middlemas Home",
            enabled=True,
            authMode="psk",
            encryptionMode="wpa",
            psk="SecureHome2024!",  # Strong default password
            ipAssignmentMode="NAT mode",
            minBitrate=11,
            bandSelection="Dual band operation",
            visible=True,
            availableOnAllAps=True,
            lanIsolationEnabled=False,  # No isolation for main network
            perClientBandwidthLimitDown=0,  # No bandwidth limits
            perClientBandwidthLimitUp=0
        )
        
        print("✅ Main WiFi configured successfully:")
        print("   SSID Name: Middlemas Home")
        print("   Security: WPA2-PSK")
        print("   Password: SecureHome2024!")
        print("   Band: Dual band (2.4 + 5 GHz)")
        print("   Mode: NAT mode")
        print("   Isolation: 🔓 Disabled (for device sharing)")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Error configuring main WiFi: {e}")
    
    # Configure Guest WiFi
    print("\n📋 CONFIGURING GUEST WIFI NETWORK")
    print("-"*40)
    
    try:
        guest_config = meraki.dashboard.wireless.updateNetworkWirelessSsid(
            networkId=network_id,
            number=1,  # Second SSID
            name="Middlemas Guest",
            enabled=True,
            authMode="psk",
            encryptionMode="wpa",
            psk="WelcomeGuest2024",
            ipAssignmentMode="NAT mode",
            minBitrate=5.5,
            bandSelection="Dual band operation",
            visible=True,
            availableOnAllAps=True,
            lanIsolationEnabled=True,  # Guest isolation enabled
            perClientBandwidthLimitDown=5000,  # 5 Mbps limit for guests
            perClientBandwidthLimitUp=2000     # 2 Mbps upload limit
        )
        
        print("✅ Guest WiFi configured successfully:")
        print("   SSID Name: Middlemas Guest")
        print("   Security: WPA2-PSK")
        print("   Password: WelcomeGuest2024")
        print("   Isolation: 🔒 Enabled (guest security)")
        print("   Bandwidth: 5 Mbps down / 2 Mbps up")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Error configuring guest WiFi: {e}")
    
    # Configure IoT Network (optional)
    print("\n📋 CONFIGURING IOT NETWORK (OPTIONAL)")
    print("-"*40)
    
    try:
        iot_config = meraki.dashboard.wireless.updateNetworkWirelessSsid(
            networkId=network_id,
            number=2,  # Third SSID
            name="Middlemas IoT",
            enabled=True,
            authMode="psk",
            encryptionMode="wpa",
            psk="IoTDevices2024",
            ipAssignmentMode="Bridge mode",
            vlanId=10,  # IoT VLAN
            minBitrate=2,  # Lower bitrate for IoT devices
            bandSelection="2.4 GHz only",  # Many IoT devices are 2.4GHz only
            visible=False,  # Hidden SSID for IoT
            availableOnAllAps=True,
            lanIsolationEnabled=True  # Isolate IoT devices
        )
        
        print("✅ IoT WiFi configured successfully:")
        print("   SSID Name: Middlemas IoT")
        print("   Security: WPA2-PSK")
        print("   Password: IoTDevices2024")
        print("   Band: 2.4 GHz only")
        print("   VLAN: 10")
        print("   Hidden: Yes")
        print("   Isolation: 🔒 Enabled (IoT security)")
        success_count += 1
        
    except Exception as e:
        print(f"⚠️ Could not configure IoT network: {e}")
        print("   (Bridge mode may require additional network configuration)")
    
    # Disable unused SSIDs
    print("\n📋 DISABLING UNUSED SSIDS")
    print("-"*40)
    
    for ssid_num in range(3, 15):  # SSIDs 3-14
        try:
            meraki.dashboard.wireless.updateNetworkWirelessSsid(
                networkId=network_id,
                number=ssid_num,
                enabled=False
            )
        except:
            pass  # Silent fail for unused SSIDs
    
    print("✅ Unused SSIDs disabled")
    
    # Summary
    print("\n" + "="*80)
    print("WIFI CONFIGURATION COMPLETE")
    print("="*80)
    
    print(f"\n✅ Successfully configured {success_count} WiFi networks:")
    
    print("\n📱 NETWORK DETAILS:")
    print("\n1. Main Network:")
    print("   SSID: Middlemas Home")
    print("   Pass: SecureHome2024!")
    print("   Use: Primary devices, streaming, work")
    
    print("\n2. Guest Network:")
    print("   SSID: Middlemas Guest")
    print("   Pass: WelcomeGuest2024")
    print("   Use: Visitor access (isolated)")
    
    if success_count > 2:
        print("\n3. IoT Network:")
        print("   SSID: Middlemas IoT (hidden)")
        print("   Pass: IoTDevices2024")
        print("   Use: Smart home devices")
    
    print("\n⚠️ IMPORTANT NOTES:")
    print("1. Change these default passwords immediately")
    print("2. You need to add access points to this network")
    print("3. Configure firewall rules as needed")
    print("4. Set up VLAN configuration if using Bridge mode")
    
    print("\n🔧 TO ADD ACCESS POINTS:")
    print("1. Purchase compatible Meraki APs")
    print("2. Add them to inventory via order/claim")
    print("3. Claim them to this network")
    print("4. They will auto-configure with these SSIDs")
    
    print("\n🔗 Manage at: https://dashboard.meraki.com")
    
    return success_count > 0

if __name__ == "__main__":
    try:
        success = configure_wifi()
        if success:
            print("\n✅ WiFi configuration completed successfully!")
        else:
            print("\n❌ WiFi configuration failed")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Configuration failed: {e}")
        sys.exit(1)