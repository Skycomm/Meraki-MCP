#!/usr/bin/env python3
"""
Create Sam Middlemas organization with Home network and configure wireless APs.
THIS WILL CREATE REAL INFRASTRUCTURE - PLEASE CONFIRM BEFORE RUNNING!
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from meraki_client import MerakiClient
import time
from datetime import datetime

# Initialize client
meraki = MerakiClient()

def create_sam_middlemas_setup():
    """Create organization, network, and configure APs for Sam Middlemas."""
    
    print("="*80)
    print("CREATE SAM MIDDLEMAS ORGANIZATION & NETWORK")
    print("="*80)
    print("⚠️  WARNING: This will create REAL infrastructure in Meraki Dashboard")
    print("="*80)
    
    # Get confirmation
    print("\nThis will:")
    print("1. Create organization: Sam Middlemas")
    print("2. Create network: Home")
    print("3. Claim devices: Q2PD-JL52-H3B2 and Q2PD-UYKB-3LSU")
    print("4. Configure standard WiFi")
    
    confirmation = input("\nType 'CREATE' to proceed or anything else to cancel: ")
    if confirmation != 'CREATE':
        print("❌ Cancelled - no changes made")
        return False
    
    print("\n" + "="*80)
    print(f"Starting creation at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    org_id = None
    network_id = None
    
    try:
        # Step 1: Create Organization
        print("\n📋 STEP 1: CREATE ORGANIZATION")
        print("-"*40)
        
        try:
            new_org = meraki.dashboard.organizations.createOrganization(
                name="Sam Middlemas"
            )
            org_id = new_org['id']
            print(f"✅ Organization created: Sam Middlemas")
            print(f"   Organization ID: {org_id}")
            
        except Exception as e:
            if "already exists" in str(e).lower():
                # Organization might already exist, try to find it
                orgs = meraki.dashboard.organizations.getOrganizations()
                for org in orgs:
                    if org.get('name') == 'Sam Middlemas':
                        org_id = org['id']
                        print(f"✅ Organization already exists: Sam Middlemas")
                        print(f"   Organization ID: {org_id}")
                        break
                
                if not org_id:
                    print(f"❌ Error creating organization: {e}")
                    return False
            else:
                print(f"❌ Error creating organization: {e}")
                return False
        
        # Step 2: Create Network
        print("\n📋 STEP 2: CREATE NETWORK")
        print("-"*40)
        
        try:
            new_network = meraki.dashboard.organizations.createOrganizationNetwork(
                organizationId=org_id,
                name="Home",
                productTypes=["wireless"],  # Wireless network for the APs
                timeZone="America/Los_Angeles"  # Default timezone, can be changed
            )
            network_id = new_network['id']
            print(f"✅ Network created: Home")
            print(f"   Network ID: {network_id}")
            print(f"   Product Types: wireless")
            
        except Exception as e:
            if "already exists" in str(e).lower():
                # Network might already exist
                networks = meraki.dashboard.organizations.getOrganizationNetworks(org_id)
                for net in networks:
                    if net.get('name') == 'Home':
                        network_id = net['id']
                        print(f"✅ Network already exists: Home")
                        print(f"   Network ID: {network_id}")
                        break
                
                if not network_id:
                    print(f"❌ Error creating network: {e}")
                    return False
            else:
                print(f"❌ Error creating network: {e}")
                return False
        
        # Step 3: Claim Devices
        print("\n📋 STEP 3: CLAIM WIRELESS ACCESS POINTS")
        print("-"*40)
        
        serials = ["Q2PD-JL52-H3B2", "Q2PD-UYKB-3LSU"]
        
        try:
            # Claim devices to network
            claim_result = meraki.dashboard.networks.claimNetworkDevices(
                networkId=network_id,
                serials=serials
            )
            print(f"✅ Devices claimed successfully:")
            for serial in serials:
                print(f"   - {serial}")
            
        except Exception as e:
            error_msg = str(e).lower()
            if "already claimed" in error_msg or "already in" in error_msg:
                print(f"⚠️ Devices may already be claimed: {e}")
                print("   Attempting to continue with configuration...")
            else:
                print(f"❌ Error claiming devices: {e}")
                print("\n⚠️ Note: These devices might be:")
                print("   - Already claimed by another organization")
                print("   - Invalid serial numbers")
                print("   - Not in your inventory")
                return False
        
        # Step 4: Configure Devices
        print("\n📋 STEP 4: CONFIGURE ACCESS POINTS")
        print("-"*40)
        
        # Get the devices to configure them
        try:
            devices = meraki.dashboard.networks.getNetworkDevices(network_id)
            
            ap_names = {
                "Q2PD-JL52-H3B2": "Living Room AP",
                "Q2PD-UYKB-3LSU": "Bedroom AP"
            }
            
            for device in devices:
                serial = device.get('serial')
                if serial in ap_names:
                    # Update device name and settings
                    try:
                        updated = meraki.dashboard.devices.updateDevice(
                            serial=serial,
                            name=ap_names[serial],
                            address="Home Network",
                            tags=["home", "wireless"]
                        )
                        print(f"✅ Configured: {ap_names[serial]} ({serial})")
                    except Exception as e:
                        print(f"⚠️ Could not update {serial}: {e}")
            
        except Exception as e:
            print(f"⚠️ Could not configure devices: {e}")
        
        # Step 5: Configure WiFi SSID
        print("\n📋 STEP 5: CONFIGURE WIFI SSID")
        print("-"*40)
        
        try:
            # Configure SSID 0 as the main home network
            ssid_config = meraki.dashboard.wireless.updateNetworkWirelessSsid(
                networkId=network_id,
                number=0,
                name="Middlemas Home",
                enabled=True,
                authMode="psk",
                encryptionMode="wpa",
                psk="Welcome2024!",  # Default password - SHOULD BE CHANGED
                ipAssignmentMode="NAT mode",
                minBitrate=11,
                bandSelection="Dual band operation",
                perClientBandwidthLimitDown=0,
                perClientBandwidthLimitUp=0,
                visible=True,
                availableOnAllAps=True,
                lanIsolationEnabled=False  # Not isolated for home use
            )
            
            print("✅ WiFi configured successfully:")
            print("   SSID Name: Middlemas Home")
            print("   Security: WPA2-PSK")
            print("   Password: Welcome2024!")
            print("   Mode: NAT mode")
            print("   Band: Dual band (2.4 + 5 GHz)")
            print("   Isolation: 🔓 Disabled (home network)")
            
            print("\n⚠️ IMPORTANT: Please change the WiFi password!")
            print("   Current password is a default and should be updated")
            
        except Exception as e:
            print(f"❌ Error configuring WiFi: {e}")
            return False
        
        # Step 6: Configure Guest Network (Optional)
        print("\n📋 STEP 6: CONFIGURE GUEST NETWORK")
        print("-"*40)
        
        try:
            guest_config = meraki.dashboard.wireless.updateNetworkWirelessSsid(
                networkId=network_id,
                number=1,
                name="Middlemas Guest",
                enabled=True,
                authMode="psk",
                encryptionMode="wpa",
                psk="GuestAccess2024",  # Guest password
                ipAssignmentMode="NAT mode",
                minBitrate=5.5,
                bandSelection="Dual band operation",
                visible=True,
                availableOnAllAps=True,
                lanIsolationEnabled=True  # Isolated for guest security
            )
            
            print("✅ Guest WiFi configured:")
            print("   SSID Name: Middlemas Guest")
            print("   Security: WPA2-PSK")
            print("   Password: GuestAccess2024")
            print("   Isolation: 🔒 Enabled (guest isolation)")
            
        except Exception as e:
            print(f"⚠️ Could not configure guest network: {e}")
        
        # Step 7: Summary
        print("\n" + "="*80)
        print("SETUP COMPLETE")
        print("="*80)
        
        print("\n✅ Successfully Created:")
        print(f"   Organization: Sam Middlemas (ID: {org_id})")
        print(f"   Network: Home (ID: {network_id})")
        print("   Access Points: 2 devices")
        print("   Main WiFi: Middlemas Home")
        print("   Guest WiFi: Middlemas Guest")
        
        print("\n📝 Next Steps:")
        print("   1. Log into Meraki Dashboard")
        print("   2. Change WiFi passwords")
        print("   3. Verify AP placement")
        print("   4. Test connectivity")
        
        print("\n🔗 Dashboard URL:")
        print("   https://dashboard.meraki.com")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        
        # Cleanup attempt if partially created
        if network_id and org_id:
            print("\n⚠️ Attempting cleanup...")
            try:
                # Don't actually delete - just inform
                print("   Network and organization created but not fully configured")
                print("   Please check Meraki Dashboard for partial setup")
            except:
                pass
        
        return False

if __name__ == "__main__":
    try:
        success = create_sam_middlemas_setup()
        if success:
            print("\n✅ Sam Middlemas organization setup completed successfully!")
        else:
            print("\n❌ Setup was not completed")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)