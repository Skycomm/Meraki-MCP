#!/usr/bin/env python3
"""Test all VPN GET commands - MCP tool testing"""

import asyncio
import json
import sys
from server.main import app
from datetime import datetime

def extract_result(result):
    """Extract actual data from MCP tool result."""
    # Handle tuple response (content, raw_result)
    if isinstance(result, tuple) and len(result) == 2:
        content, raw_result = result
        if isinstance(content, list) and len(content) > 0:
            if hasattr(content[0], 'text'):
                text = content[0].text
                if 'error' in text.lower() or 'failed' in text.lower() or '❌' in text:
                    try:
                        return json.loads(text)
                    except:
                        return {"error": text}
                try:
                    return json.loads(text)
                except:
                    return {"message": text}
        # Fall back to raw_result if available
        if isinstance(raw_result, dict) and 'result' in raw_result:
            return raw_result['result']
    # Handle list of TextContent
    elif isinstance(result, list) and len(result) > 0:
        if hasattr(result[0], 'text'):
            text = result[0].text
            if text.startswith('Error') or text.startswith('Failed') or '❌' in text:
                return {"error": text}
            try:
                return json.loads(text)
            except:
                return {"message": text}
    elif hasattr(result, 'text'):
        text = result.text
        if text.startswith('Error') or text.startswith('Failed') or '❌' in text:
            return {"error": text}
        try:
            return json.loads(text)
        except:
            return {"message": result.text}
    else:
        return result

async def test_all_vpn_get_commands():
    """Test ALL VPN GET commands comprehensively"""
    
    print("=" * 80)
    print("COMPREHENSIVE VPN GET COMMANDS TEST - MCP TOOLS")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)
    
    # Test configurations
    org_ids = [
        "686470",  # Skycomm production org
    ]
    
    network_ids = [
        "L_726205439913500692",  # Reserve St
        "L_726205439913492992",  # Attadale
    ]
    
    # Track results
    results = {
        "total": 0,
        "success": 0,
        "error": 0,
        "details": []
    }
    
    # ========================================================================
    # 1. ORGANIZATION-LEVEL VPN GET COMMANDS
    # ========================================================================
    print("\n" + "=" * 80)
    print("1. ORGANIZATION-LEVEL VPN GET COMMANDS")
    print("=" * 80)
    
    for org_id in org_ids:
        print(f"\nTesting with Organization ID: {org_id}")
        print("-" * 60)
        
        # 1.1 get_organization_appliance_vpn_statuses
        print("\n1.1. get_organization_appliance_vpn_statuses")
        results["total"] += 1
        try:
            result = await app.call_tool("get_organization_appliance_vpn_statuses", {
                "organization_id": org_id
            })
            data = extract_result(result)
            
            if "error" not in data:
                results["success"] += 1
                print(f"  ✅ SUCCESS - Retrieved VPN statuses")
                if isinstance(data, list):
                    print(f"     - Networks with VPN: {len(data)}")
                    if len(data) > 0:
                        print(f"     - Sample network: {data[0].get('networkId', 'N/A')}")
                        print(f"     - VPN mode: {data[0].get('vpnMode', 'N/A')}")
                else:
                    print(f"     - Response type: {type(data).__name__}")
                results["details"].append({
                    "tool": "get_organization_appliance_vpn_statuses",
                    "org_id": org_id,
                    "status": "success",
                    "data_type": type(data).__name__
                })
            else:
                results["error"] += 1
                error_msg = data['error'][:150]
                print(f"  ❌ ERROR: {error_msg}")
                results["details"].append({
                    "tool": "get_organization_appliance_vpn_statuses",
                    "org_id": org_id,
                    "status": "error",
                    "error": error_msg
                })
        except Exception as e:
            results["error"] += 1
            print(f"  ❌ EXCEPTION: {str(e)[:150]}")
            results["details"].append({
                "tool": "get_organization_appliance_vpn_statuses",
                "org_id": org_id,
                "status": "exception",
                "error": str(e)
            })
        
        # 1.2 get_organization_appliance_vpn_third_party_vpn_peers
        print("\n1.2. get_organization_appliance_vpn_third_party_vpn_peers")
        results["total"] += 1
        try:
            result = await app.call_tool("get_organization_appliance_vpn_third_party_vpn_peers", {
                "organization_id": org_id
            })
            data = extract_result(result)
            
            if "error" not in data:
                results["success"] += 1
                print(f"  ✅ SUCCESS - Retrieved third-party VPN peers")
                if isinstance(data, list):
                    print(f"     - Number of peers: {len(data)}")
                    if len(data) > 0:
                        print(f"     - Sample peer: {data[0].get('name', 'N/A')}")
                else:
                    print(f"     - Response type: {type(data).__name__}")
                results["details"].append({
                    "tool": "get_organization_appliance_vpn_third_party_vpn_peers",
                    "org_id": org_id,
                    "status": "success",
                    "peers_count": len(data) if isinstance(data, list) else 0
                })
            else:
                results["error"] += 1
                error_msg = data['error'][:150]
                print(f"  ❌ ERROR: {error_msg}")
                results["details"].append({
                    "tool": "get_organization_appliance_vpn_third_party_vpn_peers",
                    "org_id": org_id,
                    "status": "error",
                    "error": error_msg
                })
        except Exception as e:
            results["error"] += 1
            print(f"  ❌ EXCEPTION: {str(e)[:150]}")
            results["details"].append({
                "tool": "get_organization_appliance_vpn_third_party_vpn_peers",
                "org_id": org_id,
                "status": "exception",
                "error": str(e)
            })
        
        # 1.3 get_organization_appliance_vpn_vpn_firewall_rules
        print("\n1.3. get_organization_appliance_vpn_vpn_firewall_rules")
        results["total"] += 1
        try:
            result = await app.call_tool("get_organization_appliance_vpn_vpn_firewall_rules", {
                "organization_id": org_id
            })
            data = extract_result(result)
            
            if "error" not in data:
                results["success"] += 1
                print(f"  ✅ SUCCESS - Retrieved VPN firewall rules")
                if isinstance(data, dict):
                    rules = data.get('rules', [])
                    print(f"     - Number of rules: {len(rules)}")
                    print(f"     - Syslog default rule: {data.get('syslogDefaultRule', False)}")
                    if len(rules) > 0:
                        print(f"     - Sample rule: {rules[0].get('comment', 'N/A')}")
                else:
                    print(f"     - Response type: {type(data).__name__}")
                results["details"].append({
                    "tool": "get_organization_appliance_vpn_vpn_firewall_rules",
                    "org_id": org_id,
                    "status": "success",
                    "rules_count": len(data.get('rules', [])) if isinstance(data, dict) else 0
                })
            else:
                results["error"] += 1
                error_msg = data['error'][:150]
                print(f"  ❌ ERROR: {error_msg}")
                results["details"].append({
                    "tool": "get_organization_appliance_vpn_vpn_firewall_rules",
                    "org_id": org_id,
                    "status": "error",
                    "error": error_msg
                })
        except Exception as e:
            results["error"] += 1
            print(f"  ❌ EXCEPTION: {str(e)[:150]}")
            results["details"].append({
                "tool": "get_organization_appliance_vpn_vpn_firewall_rules",
                "org_id": org_id,
                "status": "exception",
                "error": str(e)
            })
        
        # Only test first working org
        if results["success"] > 0:
            break
    
    # ========================================================================
    # 2. NETWORK-LEVEL VPN GET COMMANDS
    # ========================================================================
    print("\n" + "=" * 80)
    print("2. NETWORK-LEVEL VPN GET COMMANDS")
    print("=" * 80)
    
    for network_id in network_ids:
        print(f"\nTesting with Network ID: {network_id}")
        print("-" * 60)
        
        # 2.1 get_network_appliance_vpn_site_to_site
        print("\n2.1. get_network_appliance_vpn_site_to_site")
        results["total"] += 1
        try:
            result = await app.call_tool("get_network_appliance_vpn_site_to_site", {
                "network_id": network_id
            })
            data = extract_result(result)
            
            if "error" not in data:
                results["success"] += 1
                print(f"  ✅ SUCCESS - Retrieved site-to-site VPN config")
                if isinstance(data, dict):
                    print(f"     - Mode: {data.get('mode', 'none')}")
                    print(f"     - Subnets: {len(data.get('subnets', []))}")
                    hubs = data.get('hubs', [])
                    print(f"     - Hubs: {len(hubs)}")
                    if len(hubs) > 0:
                        print(f"     - Sample hub: {hubs[0].get('hubId', 'N/A')}")
                else:
                    print(f"     - Response type: {type(data).__name__}")
                results["details"].append({
                    "tool": "get_network_appliance_vpn_site_to_site",
                    "network_id": network_id,
                    "status": "success",
                    "mode": data.get('mode', 'unknown') if isinstance(data, dict) else 'N/A'
                })
            else:
                results["error"] += 1
                error_msg = data['error'][:150]
                print(f"  ❌ ERROR: {error_msg}")
                results["details"].append({
                    "tool": "get_network_appliance_vpn_site_to_site",
                    "network_id": network_id,
                    "status": "error",
                    "error": error_msg
                })
        except Exception as e:
            results["error"] += 1
            print(f"  ❌ EXCEPTION: {str(e)[:150]}")
            results["details"].append({
                "tool": "get_network_appliance_vpn_site_to_site",
                "network_id": network_id,
                "status": "exception",
                "error": str(e)
            })
        
        # 2.2 get_network_appliance_vpn_bgp
        print("\n2.2. get_network_appliance_vpn_bgp")
        results["total"] += 1
        try:
            result = await app.call_tool("get_network_appliance_vpn_bgp", {
                "network_id": network_id
            })
            data = extract_result(result)
            
            if "error" not in data:
                results["success"] += 1
                print(f"  ✅ SUCCESS - Retrieved BGP configuration")
                if isinstance(data, dict):
                    print(f"     - Enabled: {data.get('enabled', False)}")
                    print(f"     - AS Number: {data.get('asNumber', 'N/A')}")
                    print(f"     - IBGP Hold Timer: {data.get('ibgpHoldTimer', 'N/A')}")
                    neighbors = data.get('neighbors', [])
                    print(f"     - Neighbors: {len(neighbors)}")
                else:
                    print(f"     - Response type: {type(data).__name__}")
                results["details"].append({
                    "tool": "get_network_appliance_vpn_bgp",
                    "network_id": network_id,
                    "status": "success",
                    "bgp_enabled": data.get('enabled', False) if isinstance(data, dict) else False
                })
            else:
                results["error"] += 1
                error_msg = data['error'][:150]
                print(f"  ❌ ERROR: {error_msg}")
                results["details"].append({
                    "tool": "get_network_appliance_vpn_bgp",
                    "network_id": network_id,
                    "status": "error",
                    "error": error_msg
                })
        except Exception as e:
            results["error"] += 1
            print(f"  ❌ EXCEPTION: {str(e)[:150]}")
            results["details"].append({
                "tool": "get_network_appliance_vpn_bgp",
                "network_id": network_id,
                "status": "exception",
                "error": str(e)
            })
    
    # ========================================================================
    # 3. DEVICE-LEVEL VPN GET COMMANDS
    # ========================================================================
    print("\n" + "=" * 80)
    print("3. DEVICE-LEVEL VPN GET COMMANDS")
    print("=" * 80)
    
    # First, try to find an MX device
    print("\nFinding MX devices...")
    mx_serials = []
    
    try:
        # Try to get devices from networks
        for network_id in network_ids:
            try:
                devices_result = await app.call_tool("get_network_devices", {
                    "network_id": network_id
                })
                devices_data = extract_result(devices_result)
                
                if isinstance(devices_data, list):
                    for device in devices_data:
                        if device.get('model', '').startswith('MX'):
                            mx_serials.append(device['serial'])
                            print(f"  Found MX: {device['model']} (Serial: {device['serial']})")
                    
                if mx_serials:
                    break
            except Exception as e:
                print(f"  Could not retrieve devices for network {network_id}: {str(e)[:100]}")
    except Exception as e:
        print(f"  Error finding devices: {str(e)[:100]}")
    
    # If no MX found via org, try known serials from Skycomm
    if not mx_serials:
        mx_serials = [
            "Q2MN-LXDL-EQWE",  # Attadale MX64W
            "Q2RN-B467-RKEW",  # Midland MX65W
        ]
        print("  Using known MX serials from Skycomm")
    
    for serial in mx_serials[:1]:  # Test just the first one
        print(f"\nTesting with Device Serial: {serial}")
        print("-" * 60)
        
        # 3.1 get_device_appliance_uplinks_settings
        print("\n3.1. get_device_appliance_uplinks_settings")
        results["total"] += 1
        try:
            result = await app.call_tool("get_device_appliance_uplinks_settings", {
                "serial": serial
            })
            data = extract_result(result)
            
            if "error" not in data:
                results["success"] += 1
                print(f"  ✅ SUCCESS - Retrieved uplink settings")
                if isinstance(data, dict):
                    interfaces = data.get('interfaces', {})
                    print(f"     - Interfaces configured: {len(interfaces)}")
                    for iface_name in ['wan1', 'wan2', 'cellular']:
                        if iface_name in interfaces:
                            iface = interfaces[iface_name]
                            print(f"     - {iface_name}: enabled={iface.get('enabled', False)}, vlanTagging={iface.get('vlanTagging', {}).get('enabled', False)}")
                else:
                    print(f"     - Response type: {type(data).__name__}")
                results["details"].append({
                    "tool": "get_device_appliance_uplinks_settings",
                    "serial": serial,
                    "status": "success",
                    "interfaces_count": len(data.get('interfaces', {})) if isinstance(data, dict) else 0
                })
            else:
                results["error"] += 1
                error_msg = data['error'][:150]
                print(f"  ❌ ERROR: {error_msg}")
                results["details"].append({
                    "tool": "get_device_appliance_uplinks_settings",
                    "serial": serial,
                    "status": "error",
                    "error": error_msg
                })
        except Exception as e:
            results["error"] += 1
            print(f"  ❌ EXCEPTION: {str(e)[:150]}")
            results["details"].append({
                "tool": "get_device_appliance_uplinks_settings",
                "serial": serial,
                "status": "exception",
                "error": str(e)
            })
    
    # ========================================================================
    # 4. SUMMARY REPORT
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST SUMMARY REPORT")
    print("=" * 80)
    
    print(f"\nTotal Tests Run: {results['total']}")
    print(f"Successful: {results['success']} ({results['success']/results['total']*100:.1f}%)")
    print(f"Errors: {results['error']} ({results['error']/results['total']*100:.1f}%)")
    
    print("\nBreakdown by Tool:")
    print("-" * 60)
    
    tool_stats = {}
    for detail in results["details"]:
        tool = detail["tool"]
        if tool not in tool_stats:
            tool_stats[tool] = {"success": 0, "error": 0, "exception": 0}
        tool_stats[tool][detail["status"]] += 1
    
    for tool, stats in tool_stats.items():
        total = sum(stats.values())
        success_rate = (stats["success"] / total * 100) if total > 0 else 0
        print(f"{tool}:")
        print(f"  Success: {stats['success']}/{total} ({success_rate:.1f}%)")
        if stats["error"] > 0:
            print(f"  Errors: {stats['error']}")
        if stats["exception"] > 0:
            print(f"  Exceptions: {stats['exception']}")
    
    print("\n" + "=" * 80)
    print("VPN GET COMMANDS TEST COMPLETE")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    results = asyncio.run(test_all_vpn_get_commands())
    
    # Exit with error code if any tests failed
    if results["error"] > 0:
        sys.exit(1)