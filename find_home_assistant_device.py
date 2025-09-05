#!/usr/bin/env python3
"""
Find Home Assistant device by IP address 10.0.5.146 and get MAC address for DHCP reservation.
"""

import os
os.environ['MCP_PROFILE'] = 'FULL'

from server.main import app, meraki

def find_home_assistant_device():
    """Find Home Assistant device and prepare DHCP reservation info."""
    
    print("🔍 Searching for Home Assistant device at IP 10.0.5.146")
    print("=" * 60)
    
    try:
        # Get Skycomm organization
        orgs = meraki.dashboard.organizations.getOrganizations()
        skycomm_org = next((org for org in orgs if 'skycomm' in org['name'].lower()), None)
        
        if not skycomm_org:
            print("❌ Skycomm organization not found")
            return
        
        print(f"✅ Found organization: {skycomm_org['name']} ({skycomm_org['id']})")
        
        # Get Reserve St network
        networks = meraki.dashboard.organizations.getOrganizationNetworks(skycomm_org['id'])
        reserve_st = next((net for net in networks if 'reserve st' in net['name'].lower()), None)
        
        if not reserve_st:
            print("❌ Reserve St network not found")
            return
            
        print(f"✅ Found network: {reserve_st['name']} ({reserve_st['id']})")
        
        # Search for device at 10.0.5.146
        print(f"\n🔍 Searching for device at IP 10.0.5.146...")
        
        # Get all clients (extended timespan to catch recent connections)
        clients = meraki.dashboard.networks.getNetworkClients(
            reserve_st['id'], 
            timespan=86400 * 7,  # 7 days
            perPage=1000,
            total_pages='all'
        )
        
        print(f"📊 Found {len(clients)} total clients")
        
        # Search for the specific IP
        target_device = None
        home_assistant_candidates = []
        
        for client in clients:
            client_ip = client.get('ip', '')
            client_description = client.get('description') or client.get('dhcpHostname') or 'Unknown'
            client_mac = client.get('mac', '')
            client_usage = client.get('usage', {})
            
            # Check if this is the target IP
            if client_ip == '10.0.5.146':
                target_device = client
                print(f"🎯 FOUND TARGET DEVICE!")
                print(f"   IP: {client_ip}")
                print(f"   MAC: {client_mac}")
                print(f"   Description: {client_description}")
                print(f"   Manufacturer: {client.get('manufacturer', 'Unknown')}")
                print(f"   OS: {client.get('os', 'Unknown')}")
                print(f"   VLAN: {client.get('vlan', 'Unknown')}")
                print(f"   Status: {client.get('status', 'Unknown')}")
                break
            
            # Also collect potential Home Assistant devices (safe string handling)
            desc_lower = str(client_description).lower() if client_description else ''
            if any(term in desc_lower for term in ['home', 'assistant', 'ha']):
                home_assistant_candidates.append({
                    'ip': client_ip,
                    'mac': client_mac,
                    'description': client_description,
                    'manufacturer': client.get('manufacturer', 'Unknown'),
                    'vlan': client.get('vlan', 'Unknown')
                })
            
            # Debug: Show clients on VLAN 5 or with IP starting with 10.0.5
            if client_ip.startswith('10.0.5.') or client.get('vlan') == '5':
                print(f"🔍 VLAN 5 device: IP={client_ip}, MAC={client_mac}, Desc={client_description}")
        
        if target_device:
            print(f"\n✅ SUCCESS! Found device at 10.0.5.146")
            print(f"MAC Address: {target_device.get('mac')}")
            
            # Generate the MCP command for DHCP reservation
            mac_address = target_device.get('mac')
            print(f"\n🎯 DHCP Reservation Command:")
            print(f"Use this with your N8N MCP client:")
            print(f"""
"Create a DHCP reservation for MAC address {mac_address} 
to use IP address 10.0.5.5 on VLAN 5 in the Skycomm Reserve St network.
The device name should be 'Home-Assistant'."
            """)
            
            return target_device
            
        else:
            print(f"❌ No device found at IP 10.0.5.146")
            
            if home_assistant_candidates:
                print(f"\n🤔 Found {len(home_assistant_candidates)} potential Home Assistant devices:")
                for i, candidate in enumerate(home_assistant_candidates, 1):
                    print(f"   {i}. IP: {candidate['ip']} | MAC: {candidate['mac']} | Desc: {candidate['description']}")
                    
            print(f"\n💡 Next steps (Option 2):")
            print(f"1. SSH into your Home Assistant device")
            print(f"2. Run: ip addr show")
            print(f"3. Find the MAC address of the network interface")
            print(f"4. Use that MAC address to create the DHCP reservation")
            
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    find_home_assistant_device()