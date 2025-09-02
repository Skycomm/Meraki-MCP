#!/usr/bin/env python3
"""
Test file for all Appliance GET commands in the Cisco Meraki MCP Server.
Tests only GET operations (read-only) as per user instructions: "i want all but only test get".

This file tests all GET commands from the appliance module to ensure they work correctly
with the MCP server implementation.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the MCP server
from server.main import app, meraki_client

# Test configuration
TEST_ORG_ID = "686470"  # Skycomm organization
TEST_NETWORK_ID = "L_726205439913500692"  # Reserve St network
TEST_DEVICE_SERIAL = "Q2PD-ABCD-EFGH"  # Replace with actual appliance serial if available

def test_appliance_get_commands():
    """Test all appliance GET commands."""
    
    print("# 🧪 Testing Appliance GET Commands\n")
    print(f"**Organization ID**: {TEST_ORG_ID}")
    print(f"**Network ID**: {TEST_NETWORK_ID}")
    print(f"**Test Device Serial**: {TEST_DEVICE_SERIAL}\n")
    
    # List of all GET commands to test
    get_commands = [
        # Organization-level GET commands
        {
            "name": "get_organization_appliance_security_events",
            "params": {"organization_id": TEST_ORG_ID, "per_page": 10},
            "description": "Organization appliance security events"
        },
        {
            "name": "get_organization_appliance_security_intrusion",
            "params": {"organization_id": TEST_ORG_ID},
            "description": "Organization appliance security intrusion settings"
        },
        {
            "name": "get_organization_appliance_uplink_statuses", 
            "params": {"organization_id": TEST_ORG_ID, "per_page": 10},
            "description": "Organization appliance uplink statuses"
        },
        {
            "name": "get_organization_appliance_vpn_stats",
            "params": {"organization_id": TEST_ORG_ID, "per_page": 10},
            "description": "Organization appliance VPN statistics"
        },
        {
            "name": "get_organization_appliance_vpn_statuses",
            "params": {"organization_id": TEST_ORG_ID, "per_page": 10},
            "description": "Organization appliance VPN statuses"
        },
        {
            "name": "get_organization_appliance_vpn_third_party_vpn_peers",
            "params": {"organization_id": TEST_ORG_ID},
            "description": "Organization third-party VPN peers"
        },
        {
            "name": "get_organization_appliance_vpn_vpn_firewall_rules",
            "params": {"organization_id": TEST_ORG_ID},
            "description": "Organization VPN firewall rules"
        },
        
        # Network-level GET commands
        {
            "name": "get_network_appliance_client_security_events",
            "params": {"network_id": TEST_NETWORK_ID, "per_page": 10},
            "description": "Network appliance client security events"
        },
        {
            "name": "get_network_appliance_connectivity_monitoring_destinations",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance connectivity monitoring destinations"
        },
        {
            "name": "get_network_appliance_content_filtering",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance content filtering settings"
        },
        {
            "name": "get_network_appliance_content_filtering_categories",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance content filtering categories"
        },
        {
            "name": "get_network_appliance_dhcp_subnets",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance DHCP subnets"
        },
        {
            "name": "get_network_appliance_firewall_cellular_firewall_rules",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance cellular firewall rules"
        },
        {
            "name": "get_network_appliance_firewall_firewalled_services",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance firewalled services"
        },
        {
            "name": "get_network_appliance_firewall_inbound_cellular_firewall_rules",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance inbound cellular firewall rules"
        },
        {
            "name": "get_network_appliance_firewall_inbound_firewall_rules",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance inbound firewall rules"
        },
        {
            "name": "get_network_appliance_firewall_l3_firewall_rules",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance L3 firewall rules"
        },
        {
            "name": "get_network_appliance_firewall_l7_firewall_rules",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance L7 firewall rules"
        },
        {
            "name": "get_network_appliance_firewall_one_to_many_nat_rules",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance one-to-many NAT rules"
        },
        {
            "name": "get_network_appliance_firewall_one_to_one_nat_rules",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance one-to-one NAT rules"
        },
        {
            "name": "get_network_appliance_firewall_port_forwarding_rules",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance port forwarding rules"
        },
        {
            "name": "get_network_appliance_ports",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance ports"
        },
        {
            "name": "get_network_appliance_prefixes_delegated_statics",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance delegated static prefixes"
        },
        {
            "name": "get_network_appliance_rf_profiles",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance RF profiles"
        },
        {
            "name": "get_network_appliance_security_events",
            "params": {"network_id": TEST_NETWORK_ID, "per_page": 10},
            "description": "Network appliance security events"
        },
        {
            "name": "get_network_appliance_security_intrusion",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance security intrusion settings"
        },
        {
            "name": "get_network_appliance_security_malware",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance security malware settings"
        },
        {
            "name": "get_network_appliance_settings",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance general settings"
        },
        {
            "name": "get_network_appliance_single_lan",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance single LAN configuration"
        },
        {
            "name": "get_network_appliance_ssid",
            "params": {"network_id": TEST_NETWORK_ID, "number": "0"},
            "description": "Network appliance SSID configuration"
        },
        {
            "name": "get_network_appliance_ssids",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance SSIDs"
        },
        {
            "name": "get_network_appliance_static_routes",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance static routes"
        },
        {
            "name": "get_network_appliance_traffic_shaping",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance traffic shaping settings"
        },
        {
            "name": "get_network_appliance_traffic_shaping_custom_performance_classes",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance traffic shaping custom performance classes"
        },
        {
            "name": "get_network_appliance_traffic_shaping_rules",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance traffic shaping rules"
        },
        {
            "name": "get_network_appliance_traffic_shaping_uplink_bandwidth",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance traffic shaping uplink bandwidth"
        },
        {
            "name": "get_network_appliance_traffic_shaping_uplink_selection",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance traffic shaping uplink selection"
        },
        {
            "name": "get_network_appliance_uplinks_usage_history",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance uplinks usage history"
        },
        {
            "name": "get_network_appliance_vlans",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance VLANs"
        },
        {
            "name": "get_network_appliance_vlans_settings",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance VLAN settings"
        },
        {
            "name": "get_network_appliance_vpn_bgp",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance VPN BGP settings"
        },
        {
            "name": "get_network_appliance_vpn_site_to_site_vpn",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance site-to-site VPN settings"
        },
        {
            "name": "get_network_appliance_warm_spare",
            "params": {"network_id": TEST_NETWORK_ID},
            "description": "Network appliance warm spare configuration"
        }
    ]
    
    # Track results
    successful_tests = 0
    failed_tests = 0
    test_results = []
    
    print("## 🚀 Starting Tests\n")
    
    for test_case in get_commands:
        test_name = test_case["name"]
        test_params = test_case["params"]
        test_description = test_case["description"]
        
        print(f"### Testing: {test_name}")
        print(f"**Description**: {test_description}")
        print(f"**Parameters**: {json.dumps(test_params, indent=2)}")
        
        try:
            # Get the tool function from the MCP server
            if hasattr(app, '_tools') and test_name in app._tools:
                tool_func = app._tools[test_name]
                result = tool_func(**test_params)
                
                # Check if result indicates success
                if result and not result.startswith("❌"):
                    print("✅ **Status**: PASSED")
                    successful_tests += 1
                    test_results.append({
                        "name": test_name,
                        "status": "PASSED",
                        "description": test_description
                    })
                else:
                    print("⚠️ **Status**: WARNING - No data or error returned")
                    print(f"**Result**: {result[:200]}...")
                    failed_tests += 1
                    test_results.append({
                        "name": test_name, 
                        "status": "WARNING",
                        "description": test_description,
                        "result": result[:200]
                    })
            else:
                print("❌ **Status**: FAILED - Tool not found in MCP server")
                failed_tests += 1
                test_results.append({
                    "name": test_name,
                    "status": "FAILED",
                    "description": test_description,
                    "error": "Tool not found in MCP server"
                })
                
        except Exception as e:
            print(f"❌ **Status**: ERROR - {str(e)}")
            failed_tests += 1
            test_results.append({
                "name": test_name,
                "status": "ERROR", 
                "description": test_description,
                "error": str(e)
            })
        
        print()  # Empty line for separation
    
    # Summary
    total_tests = len(get_commands)
    print(f"## 📊 Test Summary")
    print(f"**Total Tests**: {total_tests}")
    print(f"**Passed**: {successful_tests}")
    print(f"**Failed/Warnings**: {failed_tests}")
    print(f"**Success Rate**: {(successful_tests/total_tests)*100:.1f}%")
    
    # Save results to JSON file for further analysis
    results_file = "tests/appliance_get_test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests/total_tests)*100
            },
            "test_results": test_results,
            "test_config": {
                "organization_id": TEST_ORG_ID,
                "network_id": TEST_NETWORK_ID,
                "device_serial": TEST_DEVICE_SERIAL
            }
        }, indent=2)
    
    print(f"\n**Results saved to**: {results_file}")
    
    return successful_tests, failed_tests

if __name__ == "__main__":
    try:
        passed, failed = test_appliance_get_commands()
        print(f"\n🎯 **Final Result**: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All appliance GET commands are working perfectly!")
        else:
            print("⚠️ Some tests failed - check the results above for details")
            
    except Exception as e:
        print(f"💥 **Critical Error**: {str(e)}")
        sys.exit(1)