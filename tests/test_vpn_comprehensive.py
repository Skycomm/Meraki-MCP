#!/usr/bin/env python3
"""Comprehensive VPN tools test - testing as MCP client would"""

import asyncio
import json
import sys
from server.main import app

def extract_result(result):
    """Extract actual data from MCP tool result."""
    if isinstance(result, list) and len(result) > 0:
        if hasattr(result[0], 'text'):
            text = result[0].text
            if text.startswith('Error') or text.startswith('Failed'):
                return {"error": text}
            try:
                return json.loads(text)
            except:
                return {"message": text}
    elif hasattr(result, 'text'):
        try:
            return json.loads(result.text)
        except:
            return {"message": result.text}
    else:
        return result

async def test_all_vpn_tools():
    """Test all VPN tools comprehensively"""
    
    # Test network IDs to try
    test_networks = [
        ("L_828099381482775084", "Reserve St"),  # Main network
        ("L_828099381482775075", "Network 2"),    # Alternative
    ]
    
    org_id = "828099381482775075"  # Organization ID
    
    print("=" * 60)
    print("COMPREHENSIVE VPN TOOLS TEST - AS MCP CLIENT")
    print("=" * 60)
    
    # Test 1: Organization VPN tools
    print("\n1. TESTING ORGANIZATION VPN TOOLS")
    print("-" * 40)
    
    # Test get_organization_appliance_vpn_statuses
    print("\n1.1. Testing get_organization_appliance_vpn_statuses...")
    try:
        result = await app.call_tool("get_organization_appliance_vpn_statuses", {
            "organization_id": org_id
        })
        data = extract_result(result)
        if "error" not in data:
            print(f"✓ VPN statuses retrieved: {len(data) if isinstance(data, list) else 1} networks")
            if isinstance(data, list) and len(data) > 0:
                print(f"  Sample: {json.dumps(data[0], indent=2)[:200]}...")
        else:
            print(f"✗ Error: {data['error'][:100]}")
    except Exception as e:
        print(f"✗ Tool error: {e}")
    
    # Test get_organization_appliance_vpn_third_party_vpn_peers
    print("\n1.2. Testing get_organization_appliance_vpn_third_party_vpn_peers...")
    try:
        result = await app.call_tool("get_organization_appliance_vpn_third_party_vpn_peers", {
            "organization_id": org_id
        })
        data = extract_result(result)
        if "error" not in data:
            print(f"✓ Third party VPN peers: {len(data) if isinstance(data, list) else 0} peers")
        else:
            print(f"✗ Error: {data['error'][:100]}")
    except Exception as e:
        print(f"✗ Tool error: {e}")
    
    # Test get_organization_appliance_vpn_vpn_firewall_rules
    print("\n1.3. Testing get_organization_appliance_vpn_vpn_firewall_rules...")
    try:
        result = await app.call_tool("get_organization_appliance_vpn_vpn_firewall_rules", {
            "organization_id": org_id
        })
        data = extract_result(result)
        if "error" not in data:
            rules = data.get('rules', [])
            print(f"✓ VPN firewall rules: {len(rules)} rules")
        else:
            print(f"✗ Error: {data['error'][:100]}")
    except Exception as e:
        print(f"✗ Tool error: {e}")
    
    # Test 2: Network VPN tools
    print("\n2. TESTING NETWORK VPN TOOLS")
    print("-" * 40)
    
    working_network_id = None
    
    for network_id, network_name in test_networks:
        print(f"\n2.1. Testing network: {network_name} ({network_id})")
        
        # Test get_network_appliance_vpn_site_to_site
        print(f"  Testing get_network_appliance_vpn_site_to_site...")
        try:
            result = await app.call_tool("get_network_appliance_vpn_site_to_site", {
                "network_id": network_id
            })
            data = extract_result(result)
            if "error" not in data:
                print(f"  ✓ VPN config retrieved")
                print(f"    Mode: {data.get('mode', 'none')}")
                print(f"    Subnets: {len(data.get('subnets', []))}")
                working_network_id = network_id
                
                # If VPN is configured, test BGP
                print(f"  Testing get_network_appliance_vpn_bgp...")
                try:
                    bgp_result = await app.call_tool("get_network_appliance_vpn_bgp", {
                        "network_id": network_id
                    })
                    bgp_data = extract_result(bgp_result)
                    if "error" not in bgp_data:
                        print(f"  ✓ BGP config retrieved")
                        print(f"    Enabled: {bgp_data.get('enabled', False)}")
                    else:
                        print(f"  ℹ BGP not configured: {bgp_data['error'][:50]}")
                except Exception as e:
                    print(f"  ℹ BGP tool error: {e}")
                    
                break  # Found working network
            else:
                print(f"  ℹ VPN not available: {data['error'][:50]}")
        except Exception as e:
            print(f"  ✗ Tool error: {e}")
    
    # Test 3: Device uplink tools
    print("\n3. TESTING DEVICE UPLINK TOOLS")
    print("-" * 40)
    
    # Get a device serial
    print("\n3.1. Finding MX device...")
    try:
        devices_result = await app.call_tool("get_organization_devices", {
            "organization_id": org_id,
            "per_page": 100
        })
        devices_data = extract_result(devices_result)
        
        mx_serial = None
        if isinstance(devices_data, list):
            for device in devices_data:
                if device.get('model', '').startswith('MX'):
                    mx_serial = device['serial']
                    print(f"  Found MX device: {device['model']} (Serial: {mx_serial})")
                    break
        
        if mx_serial:
            print(f"\n3.2. Testing get_device_appliance_uplinks_settings...")
            try:
                uplinks_result = await app.call_tool("get_device_appliance_uplinks_settings", {
                    "serial": mx_serial
                })
                uplinks_data = extract_result(uplinks_result)
                if "error" not in uplinks_data:
                    print(f"  ✓ Uplink settings retrieved")
                    interfaces = uplinks_data.get('interfaces', {})
                    for iface in ['wan1', 'wan2', 'cellular']:
                        if iface in interfaces:
                            print(f"    {iface}: {interfaces[iface].get('enabled', False)}")
                else:
                    print(f"  ✗ Error: {uplinks_data['error'][:100]}")
            except Exception as e:
                print(f"  ✗ Tool error: {e}")
        else:
            print("  ℹ No MX device found")
    except Exception as e:
        print(f"  ✗ Error getting devices: {e}")
    
    # Test 4: VPN Configuration attempt
    if working_network_id:
        print("\n4. TESTING VPN CONFIGURATION UPDATE")
        print("-" * 40)
        print(f"Using network ID: {working_network_id}")
        
        # Try to set as hub with a test subnet
        print("\n4.1. Attempting to configure as VPN hub...")
        try:
            update_result = await app.call_tool("update_network_appliance_vpn_site_to_site", {
                "network_id": working_network_id,
                "mode": "hub",
                "subnets": [
                    {
                        "localSubnet": "10.0.101.0/24",
                        "useVpn": True
                    }
                ]
            })
            update_data = extract_result(update_result)
            if "error" not in update_data:
                print(f"  ✓ VPN configuration updated successfully")
                print(f"    New mode: {update_data.get('mode')}")
                print(f"    Subnets shared: {len(update_data.get('subnets', []))}")
            else:
                print(f"  ✗ Update error: {update_data['error'][:100]}")
        except Exception as e:
            print(f"  ✗ Tool error: {e}")
    
    print("\n" + "=" * 60)
    print("VPN TOOLS TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_all_vpn_tools())