#!/usr/bin/env python3
"""
Apply security improvements to the Attadale network:
1. Add additional content filtering categories
2. Update minimum WiFi bitrate to 12 Mbps
"""

import os
import sys
from meraki_client import MerakiClient

# Initialize the Meraki client
meraki_client = MerakiClient()

# Network ID for Attadale
NETWORK_ID = "L_726205439913492992"

def update_content_filtering():
    """Add additional content filtering categories to block."""
    print("📋 Updating content filtering settings...")
    
    # Additional categories to block:
    # - Hacking (C50)
    # - Filter Avoidance (C25)
    # - Peer File Transfer (C56)
    # - Cryptomining (C112)
    # - Terrorism content (C119)
    
    # First, get current content filtering settings
    try:
        current_settings = meraki_client.dashboard.appliance.getNetworkApplianceContentFiltering(NETWORK_ID)
        print(f"Current blocked categories: {current_settings.get('blockedUrlCategories', [])}")
        
        # Get existing blocked categories and add new ones
        blocked_categories = current_settings.get('blockedUrlCategories', [])
        
        # Extract the category IDs from the current settings
        existing_ids = [cat['id'] if isinstance(cat, dict) else cat for cat in blocked_categories]
        
        # New categories to add with full IDs
        new_categories = [
            'meraki:contentFiltering/category/C50',  # Hacking
            'meraki:contentFiltering/category/C25',  # Filter Avoidance
            'meraki:contentFiltering/category/C56',  # Peer File Transfer
            'meraki:contentFiltering/category/C112', # Cryptomining
            'meraki:contentFiltering/category/C119'  # Terrorism content
        ]
        
        # Build the final list of category IDs
        final_categories = []
        for cat in blocked_categories:
            if isinstance(cat, dict):
                final_categories.append(cat['id'])
            else:
                final_categories.append(cat)
        
        # Add new categories if not already present
        for cat in new_categories:
            if cat not in final_categories:
                final_categories.append(cat)
        
        # Update content filtering
        update_params = {
            'blockedUrlCategories': final_categories,
            'urlCategoryListSize': current_settings.get('urlCategoryListSize', 'topSites')
        }
        
        result = meraki_client.update_network_appliance_content_filtering(NETWORK_ID, **update_params)
        
        print("✅ Content filtering updated successfully!")
        print(f"New blocked categories: {result.get('blockedUrlCategories', [])}")
        
        # Map category codes to names for clarity
        category_names = {
            'meraki:contentFiltering/category/C50': 'Hacking',
            'meraki:contentFiltering/category/C25': 'Filter Avoidance',
            'meraki:contentFiltering/category/C56': 'Peer File Transfer',
            'meraki:contentFiltering/category/C112': 'Cryptomining',
            'meraki:contentFiltering/category/C119': 'Terrorism content'
        }
        
        print("\n📌 Newly added categories:")
        for cat in new_categories:
            if cat in [c['id'] if isinstance(c, dict) else c for c in result.get('blockedUrlCategories', [])]:
                print(f"  - {category_names.get(cat, cat)}: Blocked ✓")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating content filtering: {str(e)}")
        return False

def update_wifi_bitrate():
    """Update minimum WiFi bitrate to 12 Mbps."""
    print("\n📡 Updating WiFi RF profiles...")
    
    try:
        # Get current RF profiles
        rf_profiles = meraki_client.get_network_wireless_rf_profiles(NETWORK_ID)
        
        # Check if we already have a custom security profile
        custom_profile = None
        for profile in rf_profiles:
            if profile['name'] == "Attadale-Security-Profile" or "Security" in profile['name']:
                custom_profile = profile
                break
        
        if custom_profile:
            # Update existing custom profile
            print(f"\nUpdating existing RF profile: {custom_profile['name']} (ID: {custom_profile['id']})")
            
            # Prepare update parameters
            update_params = {
                'minBitrate': 12.0,
                'perSsidSettings': {}
            }
            
            # Update per-SSID settings if they exist
            if 'perSsidSettings' in custom_profile:
                for ssid_num, settings in custom_profile['perSsidSettings'].items():
                    update_params['perSsidSettings'][ssid_num] = {
                        'minBitrate': 12.0,
                        'bandOperationMode': settings.get('bandOperationMode', 'dual')
                    }
            else:
                # Default per-SSID settings
                for i in range(4):  # SSIDs 0-3
                    update_params['perSsidSettings'][str(i)] = {
                        'minBitrate': 12.0,
                        'bandOperationMode': 'dual'
                    }
            
            # Update the RF profile
            updated_profile = meraki_client.dashboard.wireless.updateNetworkWirelessRfProfile(
                NETWORK_ID,
                custom_profile['id'],
                **update_params
            )
            
            print(f"✅ Updated RF profile: {updated_profile['name']}")
            print(f"   - Minimum bitrate: {updated_profile.get('minBitrate', 'N/A')} Mbps")
            
        else:
            # Create a new custom RF profile
            print("Creating new custom RF profile with 12 Mbps minimum bitrate...")
            
            # Create a new RF profile with 12 Mbps minimum bitrate
            new_profile = meraki_client.dashboard.wireless.createNetworkWirelessRfProfile(
                NETWORK_ID,
                name="Attadale-Security-Profile",
                bandSelectionType="ap",
                minBitrate=12.0,
                perSsidSettings={
                    '0': {'minBitrate': 12.0, 'bandOperationMode': 'dual'},
                    '1': {'minBitrate': 12.0, 'bandOperationMode': 'dual'},
                    '2': {'minBitrate': 12.0, 'bandOperationMode': 'dual'},
                    '3': {'minBitrate': 12.0, 'bandOperationMode': 'dual'}
                }
            )
            print(f"✅ Created new RF profile: {new_profile['name']}")
            print(f"   - Minimum bitrate: {new_profile.get('minBitrate', 'N/A')} Mbps")
            
            # Now we need to apply this profile to the APs
            print("\n🔧 Applying RF profile to access points...")
            try:
                # Get all devices in the network
                devices = meraki_client.dashboard.networks.getNetworkDevices(NETWORK_ID)
                
                # Filter for APs
                aps = [d for d in devices if d['model'].startswith('MR') or d['model'].startswith('CW')]
                
                for ap in aps:
                    print(f"  - Applying to {ap['name'] or ap['serial']} ({ap['model']})")
                    try:
                        # Update device RF profile assignment
                        meraki_client.dashboard.wireless.updateDevice(
                            ap['serial'],
                            rfProfileId=new_profile['id']
                        )
                    except Exception as e:
                        print(f"    ⚠️  Could not update AP {ap['serial']}: {str(e)}")
                
            except Exception as e:
                print(f"⚠️  Could not apply profile to APs: {str(e)}")
        
        # Also check and update wireless settings if needed
        print("\n🔧 Checking wireless network settings...")
        
        # Get all SSIDs and update their settings
        ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(NETWORK_ID)
        
        for ssid in ssids:
            if ssid['enabled']:
                print(f"\nSSID {ssid['number']}: {ssid['name']}")
                
                # Update SSID with minimum bitrate setting if supported
                try:
                    update_ssid_params = {}
                    
                    # Some SSIDs support direct minBitrate setting
                    if 'minBitrate' in ssid:
                        update_ssid_params['minBitrate'] = 12
                        
                    if update_ssid_params:
                        updated_ssid = meraki_client.update_network_wireless_ssid(
                            NETWORK_ID,
                            ssid['number'],
                            **update_ssid_params
                        )
                        print(f"   ✅ Updated SSID minimum bitrate")
                    else:
                        print(f"   ℹ️  Minimum bitrate controlled by RF profile")
                        
                except Exception as e:
                    print(f"   ⚠️  Could not update SSID directly: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating WiFi settings: {str(e)}")
        return False

def main():
    """Main function to apply all security improvements."""
    print(f"🔐 Applying security improvements to Attadale network")
    print(f"Network ID: {NETWORK_ID}")
    print("=" * 60)
    
    # Apply content filtering updates
    cf_success = update_content_filtering()
    
    # Apply WiFi bitrate updates
    wifi_success = update_wifi_bitrate()
    
    print("\n" + "=" * 60)
    print("📊 Security Update Summary:")
    print(f"  - Content Filtering: {'✅ Success' if cf_success else '❌ Failed'}")
    print(f"  - WiFi Bitrate (12 Mbps): {'✅ Success' if wifi_success else '❌ Failed'}")
    
    if cf_success and wifi_success:
        print("\n✅ All security improvements applied successfully!")
    else:
        print("\n⚠️  Some updates failed. Please check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()