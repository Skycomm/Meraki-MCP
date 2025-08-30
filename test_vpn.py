#!/usr/bin/env python3
"""Test VPN configuration tools"""

import asyncio
import json
import sys
from server.main import app

def extract_result(result):
    """Extract actual data from MCP tool result."""
    if isinstance(result, list) and len(result) > 0:
        # Handle list of TextContent
        if hasattr(result[0], 'text'):
            text = result[0].text
            # Check if it's an error message
            if text.startswith('Error'):
                return {"error": text}
            try:
                return json.loads(text)
            except:
                return {"message": text}
    elif hasattr(result, 'text'):
        # Handle single TextContent
        try:
            return json.loads(result.text)
        except:
            return {"message": result.text}
    else:
        # Already a dict/list
        return result

async def test_vpn_config():
    """Test VPN hub configuration and VLAN sharing"""
    network_id = "L_828099381482775084"
    
    # Step 1: Get current VPN configuration
    print("Step 1: Getting current VPN configuration...", file=sys.stderr)
    try:
        result = await app.call_tool("get_network_appliance_vpn_site_to_site", {
            "network_id": network_id
        })
        result_data = extract_result(result)
        
        if "error" in result_data:
            print(f"VPN not configured yet: {result_data['error']}", file=sys.stderr)
            # Initialize with default config
            result_data = {"mode": "none", "subnets": []}
        else:
            print(f"Current VPN config: {json.dumps(result_data, indent=2)}", file=sys.stderr)
            
        current_mode = result_data.get('mode', 'none')
        print(f"Current mode: {current_mode}", file=sys.stderr)
    except Exception as e:
        print(f"Error getting VPN config: {e}", file=sys.stderr)
        # Initialize with default config
        result_data = {"mode": "none", "subnets": []}

    # Step 2: Configure MX as VPN hub and share VLAN 101
    print("\nStep 2: Configuring MX as VPN hub and sharing VLAN 101...", file=sys.stderr)
    
    # First, get current VLANs to properly configure subnets
    try:
        vlans = await app.call_tool("get_network_appliance_vlans", {
            "network_id": network_id
        })
        vlans_data = extract_result(vlans)
        
        if isinstance(vlans_data, list):
            print(f"Found {len(vlans_data)} VLANs", file=sys.stderr)
        else:
            print(f"VLANs response: {vlans_data}", file=sys.stderr)
            vlans_data = []
        
        # Find VLAN 101
        vlan_101 = None
        for vlan in vlans_data:
            if vlan.get('id') == 101:
                vlan_101 = vlan
                break
        
        if vlan_101:
            print(f"VLAN 101 found: {vlan_101.get('subnet')}", file=sys.stderr)
        else:
            print("VLAN 101 not found!", file=sys.stderr)
            return
            
    except Exception as e:
        print(f"Error getting VLANs: {e}", file=sys.stderr)
        return

    # Step 3: Update VPN configuration to hub mode with VLAN 101 shared
    print("\nStep 3: Updating VPN configuration...", file=sys.stderr)
    
    # Prepare subnets list with VLAN 101
    subnets = []
    
    # Add VLAN 101 to VPN
    if vlan_101:
        subnets.append({
            "localSubnet": vlan_101.get('subnet'),
            "useVpn": True
        })
    
    # Keep existing subnets if any
    if 'subnets' in result_data:
        for subnet in result_data['subnets']:
            # Don't duplicate VLAN 101
            if subnet.get('localSubnet') != vlan_101.get('subnet'):
                subnets.append(subnet)
    
    update_params = {
        "network_id": network_id,
        "mode": "hub",
        "subnets": subnets
    }
    
    print(f"Update params: {json.dumps(update_params, indent=2)}", file=sys.stderr)
    
    try:
        update_result = await app.call_tool("update_network_appliance_vpn_site_to_site", update_params)
        update_data = extract_result(update_result)
        
        if "error" in update_data:
            print(f"Error updating VPN: {update_data['error']}", file=sys.stderr)
        else:
            print(f"VPN updated successfully: {json.dumps(update_data, indent=2)}", file=sys.stderr)
    except Exception as e:
        print(f"Error updating VPN: {e}", file=sys.stderr)
        return

    # Step 4: Verify configuration
    print("\nStep 4: Verifying configuration...", file=sys.stderr)
    try:
        final_config = await app.call_tool("get_network_appliance_vpn_site_to_site", {
            "network_id": network_id
        })
        final_data = extract_result(final_config)
        
        if "error" not in final_data:
            print(f"Final VPN config: {json.dumps(final_data, indent=2)}", file=sys.stderr)
            
            # Check if hub mode is set
            if final_data.get('mode') == 'hub':
                print("✓ MX is configured as VPN hub", file=sys.stderr)
            else:
                print(f"✗ MX mode is {final_data.get('mode')}, not hub", file=sys.stderr)
            
            # Check if VLAN 101 is shared
            vlan_101_shared = False
            for subnet in final_data.get('subnets', []):
                if subnet.get('localSubnet') == vlan_101.get('subnet') and subnet.get('useVpn'):
                    vlan_101_shared = True
                    break
            
            if vlan_101_shared:
                print(f"✓ VLAN 101 ({vlan_101.get('subnet')}) is shared on VPN", file=sys.stderr)
            else:
                print(f"✗ VLAN 101 is not shared on VPN", file=sys.stderr)
        else:
            print(f"Could not verify: {final_data['error']}", file=sys.stderr)
            
    except Exception as e:
        print(f"Error verifying config: {e}", file=sys.stderr)

    # Step 5: Test other VPN tools
    print("\nStep 5: Testing other VPN tools...", file=sys.stderr)
    
    # Test VPN statuses
    try:
        org_id = "828099381482771185"
        vpn_statuses = await app.call_tool("get_organization_appliance_vpn_statuses", {
            "organization_id": org_id
        })
        status_data = extract_result(vpn_statuses)
        if "error" not in status_data:
            print(f"✓ VPN statuses retrieved: {len(status_data) if isinstance(status_data, list) else 'N/A'} networks", file=sys.stderr)
        else:
            print(f"✗ VPN statuses error: {status_data['error']}", file=sys.stderr)
    except Exception as e:
        print(f"✗ Error getting VPN statuses: {e}", file=sys.stderr)
    
    # Test third party VPN peers
    try:
        peers = await app.call_tool("get_organization_appliance_vpn_third_party_vpn_peers", {
            "organization_id": org_id
        })
        peers_data = extract_result(peers)
        if "error" not in peers_data:
            print(f"✓ Third party VPN peers retrieved: {len(peers_data) if isinstance(peers_data, list) else 'N/A'} peers", file=sys.stderr)
        else:
            print(f"✗ Third party VPN peers error: {peers_data['error']}", file=sys.stderr)
    except Exception as e:
        print(f"✗ Error getting third party VPN peers: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(test_vpn_config())