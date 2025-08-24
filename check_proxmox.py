#!/usr/bin/env python3
"""
Quick script to find the Proxmox server at 10.0.90.2
"""

from meraki_client import MerakiClient
import json

# Initialize client
meraki = MerakiClient()

# Network ID for Reserve St
network_id = "L_726205439913500692"

print("Searching for device at 10.0.90.2...")

# Try different timespans
timespans = [
    (86400, "24 hours"),
    (604800, "7 days"),
    (2592000, "30 days")
]

found = False
for timespan, label in timespans:
    print(f"\nChecking clients from last {label}...")
    try:
        clients = meraki.get_network_clients(network_id, timespan=timespan)
        
        # Look for the device at 10.0.90.2
        for client in clients:
            if client.get('ip') == '10.0.90.2':
                found = True
                print(f"\n✅ FOUND DEVICE AT 10.0.90.2!")
                print(f"Description: {client.get('description', 'Unknown')}")
                print(f"MAC Address: {client.get('mac', 'Unknown')}")
                print(f"VLAN: {client.get('vlan', 'Unknown')}")
                print(f"Status: {client.get('status', 'Unknown')}")
                print(f"Manufacturer: {client.get('manufacturer', 'Unknown')}")
                print(f"Operating System: {client.get('os', 'Unknown')}")
                print(f"Last Seen: {client.get('lastSeen', 'Unknown')}")
                
                # Print full details
                print("\nFull client details:")
                print(json.dumps(client, indent=2))
                break
        
        if found:
            break
            
    except Exception as e:
        print(f"Error checking {label}: {str(e)}")

if not found:
    print("\n❌ Device at 10.0.90.2 not found in client list")
    print("\nChecking all clients on VLAN 90...")
    
    # List all clients on VLAN 90
    try:
        clients = meraki.get_network_clients(network_id, timespan=2592000)  # 30 days
        vlan_90_clients = [c for c in clients if str(c.get('vlan', '')) == '90']
        
        print(f"\nFound {len(vlan_90_clients)} clients on VLAN 90:")
        for client in vlan_90_clients:
            print(f"- {client.get('ip', 'No IP')} - {client.get('mac', 'Unknown')} - {client.get('description', 'Unknown')}")
    except Exception as e:
        print(f"Error listing VLAN 90 clients: {str(e)}")

print("\nDone.")