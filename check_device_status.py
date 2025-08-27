#!/usr/bin/env python3
"""
Check if a device serial number exists in any organization.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from meraki_client import MerakiClient
from datetime import datetime

# Initialize client
meraki = MerakiClient()

def check_device_status(serial):
    """Check if device exists in any organization."""
    
    print("="*80)
    print(f"DEVICE SEARCH: {serial}")
    print("="*80)
    print(f"Search started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    found = False
    device_info = None
    
    # Get all organizations
    print("\n🔍 Searching all organizations...")
    print("-"*40)
    
    try:
        orgs = meraki.dashboard.organizations.getOrganizations()
        print(f"Checking {len(orgs)} organizations...")
        
        for org in orgs:
            org_name = org.get('name', 'Unknown')
            org_id = org.get('id')
            
            try:
                # Try to get the device directly
                device = meraki.dashboard.devices.getDevice(serial)
                
                print(f"\n✅ DEVICE FOUND!")
                print(f"   Organization: {org_name}")
                print(f"   Serial: {device.get('serial')}")
                print(f"   Model: {device.get('model', 'Unknown')}")
                print(f"   Name: {device.get('name', 'Unnamed')}")
                print(f"   MAC: {device.get('mac', 'Unknown')}")
                print(f"   Network ID: {device.get('networkId', 'Not assigned')}")
                print(f"   Status: {device.get('status', 'Unknown')}")
                
                # Get network name if assigned
                if device.get('networkId'):
                    try:
                        network = meraki.dashboard.networks.getNetwork(device['networkId'])
                        print(f"   Network Name: {network.get('name', 'Unknown')}")
                    except:
                        pass
                
                found = True
                device_info = device
                break
                
            except:
                # Device not found in this org, continue searching
                pass
            
            # Also try searching organization inventory
            try:
                # Get all devices in org
                org_devices = meraki.dashboard.organizations.getOrganizationDevices(
                    org_id,
                    perPage=1000
                )
                
                for dev in org_devices:
                    if dev.get('serial') == serial:
                        print(f"\n✅ DEVICE FOUND IN ORGANIZATION INVENTORY!")
                        print(f"   Organization: {org_name} (ID: {org_id})")
                        print(f"   Serial: {dev.get('serial')}")
                        print(f"   Model: {dev.get('model', 'Unknown')}")
                        print(f"   Name: {dev.get('name', 'Unnamed')}")
                        print(f"   MAC: {dev.get('mac', 'Unknown')}")
                        print(f"   Network ID: {dev.get('networkId', 'Not assigned')}")
                        print(f"   Status: {dev.get('status', 'Unknown')}")
                        
                        # Get network details if assigned
                        if dev.get('networkId'):
                            try:
                                network = meraki.dashboard.networks.getNetwork(dev['networkId'])
                                print(f"   Network Name: {network.get('name', 'Unknown')}")
                                print(f"   Network Tags: {', '.join(network.get('tags', []))}")
                            except:
                                pass
                        
                        found = True
                        device_info = dev
                        break
                
                if found:
                    break
                    
            except Exception as e:
                # Could not get org devices
                pass
        
        if not found:
            print(f"\n❌ DEVICE NOT FOUND: {serial}")
            print("\nPossible reasons:")
            print("   1. Invalid serial number")
            print("   2. Device not in your organizations")
            print("   3. Device not yet claimed")
            print("   4. Device in another admin's organization")
            
            # Try to check if it's a valid format
            if serial.startswith('Q'):
                print("\n📝 Serial Format Check:")
                print("   ✅ Starts with Q (typical for Meraki devices)")
                if '-' in serial and len(serial.split('-')) == 3:
                    print("   ✅ Has correct dash format")
                if len(serial) == 14:
                    print("   ✅ Has correct length")
            
    except Exception as e:
        print(f"\n❌ Error searching for device: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("SEARCH COMPLETE")
    print("="*80)
    
    if found and device_info:
        print(f"\n📍 Device Location:")
        if device_info.get('networkId'):
            print(f"   Status: CLAIMED AND ASSIGNED")
            print(f"   Network: {device_info.get('networkId')}")
        else:
            print(f"   Status: IN INVENTORY BUT NOT ASSIGNED")
        
        print(f"\n🔧 Next Steps:")
        if device_info.get('networkId'):
            print("   1. Device is already in use")
            print("   2. Must be removed from current network first")
            print("   3. Then can be claimed to new network")
        else:
            print("   1. Device is available in inventory")
            print("   2. Can be assigned to a network")
    else:
        print(f"\n❓ Device Status: NOT FOUND IN ANY ACCESSIBLE ORGANIZATION")
        print("\n🔧 Next Steps:")
        print("   1. Verify the serial number is correct")
        print("   2. Check if device is in order/purchase history")
        print("   3. Contact Meraki support if device should be accessible")
    
    return found

if __name__ == "__main__":
    # Check the specific serial
    serial = "Q2PD-UYKB-3LSU"
    
    print(f"Searching for device: {serial}")
    found = check_device_status(serial)
    
    # Also check the other serial
    print("\n" + "="*80)
    serial2 = "Q2PD-JL52-H3B2"
    print(f"Also checking: {serial2}")
    found2 = check_device_status(serial2)
    
    sys.exit(0 if (found or found2) else 1)