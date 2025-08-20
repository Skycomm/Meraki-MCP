#!/usr/bin/env python3
"""
Comprehensive test suite for all Meraki MCP Server tools
Tests tools with natural language questions and validates API responses
"""

import sys
import os
import json
import traceback
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from meraki_client import MerakiClient
from mcp.server import FastMCP

# Import all tool modules
from server.tools_organizations import register_organization_tools
from server.tools_networks import register_network_tools  
from server.tools_devices import register_device_tools
from server.tools_wireless import register_wireless_tools
from server.tools_switch import register_switch_tools
from server.tools_analytics import register_analytics_tools
from server.tools_alerts import register_alert_tools
from server.tools_appliance import register_appliance_tools
from server.tools_camera import register_camera_tools
from server.tools_sm import register_sm_tools
from server.tools_licensing import register_licensing_tools
from server.tools_policy import register_policy_tools
from server.tools_monitoring import register_monitoring_tools
from server.tools_beta import register_beta_tools
from server.tools_live import register_live_tools
from server.tools_dhcp import register_dhcp_tools
from server.tools_dhcp_singlelan import register_single_lan_dhcp_tools
from server.tools_dhcp_helper import register_dhcp_helper_tools
from server.tools_traffic_shaping import register_traffic_shaping_tools
from server.tools_firewall import register_firewall_tools
from server.tools_monitoring_dashboard import register_monitoring_dashboard_tools

# Natural language test scenarios
TEST_SCENARIOS = {
    "organizations": [
        ("Show me all my organizations", "list_organizations"),
        ("What organizations do I have access to?", "list_organizations"),
        ("Get details about my first organization", "get_organization"),
    ],
    "networks": [
        ("List all networks in my organization", "get_organization_networks"),
        ("Show me network details", "get_network"),
        ("What devices are in this network?", "get_network_devices"),
        ("Who's connected to my network?", "get_network_clients"),
    ],
    "devices": [
        ("Show device status", "get_device_status"),
        ("Get device details", "get_device"),
        ("Who's connected to this device?", "get_device_clients"),
        ("Reboot this device", "reboot_device"),
    ],
    "wireless": [
        ("What are my WiFi passwords?", "get_network_wireless_passwords"),
        ("Show me all wireless networks", "get_network_wireless_ssids"),
        ("List wireless clients", "get_network_wireless_clients"),
        ("How's my WiFi channel utilization?", "get_network_wireless_channel_utilization"),
        ("Show wireless usage stats", "get_network_wireless_usage"),
    ],
    "switch": [
        ("Show switch port status", "get_device_switch_port_statuses"),
        ("List all VLANs", "get_device_switch_vlans"),
        ("What's connected to my switch ports?", "get_device_switch_ports"),
    ],
    "dhcp": [
        ("What type of DHCP network is this?", "check_dhcp_network_type"),
        ("Show DHCP settings for VLAN 5", "get_vlan_dhcp_settings"),
        ("Add a DHCP reservation", "add_dhcp_fixed_assignment"),
        ("List DHCP subnets", "get_appliance_dhcp_subnets"),
    ],
    "firewall": [
        ("Can I use firewall features?", "check_firewall_prerequisites"),
        ("Show L3 firewall rules", "get_firewall_l3_rules"),
        ("What ports are forwarded?", "get_firewall_port_forwarding_rules"),
        ("List application categories", "get_layer7_application_categories"),
    ],
    "monitoring": [
        ("Show network health", "get_network_health_summary"),
        ("What's my bandwidth usage?", "get_uplink_bandwidth_history"),
        ("Are there any critical alerts?", "get_critical_alerts"),
        ("How's my VPN performance?", "get_vpn_performance_stats"),
    ],
    "traffic_shaping": [
        ("Can I use traffic shaping?", "check_traffic_shaping_prerequisites"),
        ("Show QoS rules", "get_network_traffic_shaping_rules"),
        ("What apps can I shape?", "get_traffic_shaping_application_categories"),
    ],
    "live": [
        ("Ping test from device", "create_device_ping_test"),
        ("Run cable test on switch port", "create_switch_cable_test"),
        ("Blink device LEDs", "blink_device_leds"),
    ],
}

class ComprehensiveToolTester:
    def __init__(self):
        self.meraki = MerakiClient()
        self.app = FastMCP("test")
        self.results = {
            "total_tools": 0,
            "tested_tools": 0,
            "passed_tools": 0,
            "failed_tools": 0,
            "categories": {},
            "errors": []
        }
        
        # Register all tools
        self.register_all_tools()
        
        # Get test network
        self.setup_test_environment()
    
    def register_all_tools(self):
        """Register all tool modules."""
        print("📝 Registering all tools...")
        
        register_organization_tools(self.app, self.meraki)
        register_network_tools(self.app, self.meraki)
        register_device_tools(self.app, self.meraki)
        register_wireless_tools(self.app, self.meraki)
        register_switch_tools(self.app, self.meraki)
        register_analytics_tools(self.app, self.meraki)
        register_alert_tools(self.app, self.meraki)
        register_appliance_tools(self.app, self.meraki)
        register_camera_tools(self.app, self.meraki)
        register_sm_tools(self.app, self.meraki)
        register_licensing_tools(self.app, self.meraki)
        register_policy_tools(self.app, self.meraki)
        register_monitoring_tools(self.app, self.meraki)
        register_beta_tools(self.app, self.meraki)
        register_live_tools(self.app, self.meraki)
        register_dhcp_helper_tools(self.app, self.meraki)
        register_dhcp_tools(self.app, self.meraki)
        register_single_lan_dhcp_tools(self.app, self.meraki)
        register_traffic_shaping_tools(self.app, self.meraki)
        register_firewall_tools(self.app, self.meraki)
        register_monitoring_dashboard_tools(self.app, self.meraki)
        
        print("✅ All tools registered")
    
    def setup_test_environment(self):
        """Get test organization and network."""
        try:
            orgs = self.meraki.get_organizations()
            self.org_id = orgs[0]['id']
            self.org_name = orgs[0]['name']
            
            networks = self.meraki.get_organization_networks(self.org_id)
            # Find a network with MX device
            for net in networks:
                if 'appliance' in net.get('productTypes', []):
                    self.network_id = net['id']
                    self.network_name = net['name']
                    break
            else:
                # Use first network if no MX found
                self.network_id = networks[0]['id']
                self.network_name = networks[0]['name']
            
            # Get a device for testing
            devices = self.meraki.get_network_devices(self.network_id)
            if devices:
                self.device_serial = devices[0]['serial']
                self.device_name = devices[0].get('name', 'Unknown')
            else:
                self.device_serial = None
                self.device_name = None
            
            print(f"\n🌐 Test Environment:")
            print(f"   Organization: {self.org_name} ({self.org_id})")
            print(f"   Network: {self.network_name} ({self.network_id})")
            print(f"   Device: {self.device_name} ({self.device_serial})")
            print()
            
        except Exception as e:
            print(f"❌ Failed to setup test environment: {e}")
            sys.exit(1)
    
    def test_tool(self, tool_name: str, category: str, **kwargs) -> Tuple[bool, str]:
        """Test a single tool."""
        try:
            # Get the tool function
            tool_func = None
            for tool in self.app._tools:
                if tool.name == tool_name:
                    tool_func = tool.fn
                    break
            
            if not tool_func:
                # Try direct function import
                module = f"server.tools_{category}"
                try:
                    mod = __import__(module, fromlist=[tool_name])
                    tool_func = getattr(mod, tool_name, None)
                except:
                    pass
            
            if not tool_func:
                return False, f"Tool not found: {tool_name}"
            
            # Call the tool with appropriate parameters
            result = tool_func(**kwargs)
            
            # Check if result is valid
            if result and not result.startswith("❌"):
                return True, "Success"
            else:
                return False, result or "No result"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def test_natural_language_scenario(self, question: str, expected_tool: str, category: str):
        """Test a natural language scenario."""
        print(f"\n💬 Question: \"{question}\"")
        print(f"   Expected tool: {expected_tool}")
        
        # Prepare parameters based on tool requirements
        params = {}
        if 'organization' in expected_tool:
            params['org_id'] = self.org_id
        if 'network' in expected_tool and 'organization' not in expected_tool:
            params['network_id'] = self.network_id
        if 'device' in expected_tool:
            if self.device_serial:
                params['serial'] = self.device_serial
            else:
                print("   ⚠️ No device available for testing")
                return False
        if 'vlan' in expected_tool:
            params['vlan_id'] = '1'  # Default VLAN
        
        success, message = self.test_tool(expected_tool, category, **params)
        
        if success:
            print(f"   ✅ Tool responded successfully")
        else:
            print(f"   ❌ Tool failed: {message}")
        
        return success
    
    def test_category(self, category: str, scenarios: List[Tuple[str, str]]):
        """Test all scenarios in a category."""
        print(f"\n{'='*60}")
        print(f"📂 Testing {category.upper()} tools")
        print(f"{'='*60}")
        
        self.results["categories"][category] = {
            "total": len(scenarios),
            "passed": 0,
            "failed": 0
        }
        
        for question, tool_name in scenarios:
            try:
                if self.test_natural_language_scenario(question, tool_name, category):
                    self.results["categories"][category]["passed"] += 1
                    self.results["passed_tools"] += 1
                else:
                    self.results["categories"][category]["failed"] += 1
                    self.results["failed_tools"] += 1
            except Exception as e:
                print(f"   💥 Unexpected error: {e}")
                self.results["categories"][category]["failed"] += 1
                self.results["failed_tools"] += 1
                self.results["errors"].append({
                    "category": category,
                    "tool": tool_name,
                    "error": str(e)
                })
            
            self.results["tested_tools"] += 1
    
    def run_comprehensive_test(self):
        """Run all tests."""
        print("\n🚀 Starting Comprehensive Tool Test")
        print("=" * 60)
        
        # Count total tools from inventory
        with open('tool_inventory.json', 'r') as f:
            inventory = json.load(f)
            self.results["total_tools"] = inventory["total_tools"]
        
        # Test each category
        for category, scenarios in TEST_SCENARIOS.items():
            self.test_category(category, scenarios)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate test report."""
        print("\n" + "="*60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("="*60)
        
        print(f"\n📈 Overall Statistics:")
        print(f"   Total Tools: {self.results['total_tools']}")
        print(f"   Tested Tools: {self.results['tested_tools']}")
        print(f"   Passed: {self.results['passed_tools']}")
        print(f"   Failed: {self.results['failed_tools']}")
        
        if self.results['tested_tools'] > 0:
            success_rate = (self.results['passed_tools'] / self.results['tested_tools']) * 100
            print(f"   Success Rate: {success_rate:.1f}%")
        
        print(f"\n📁 Category Results:")
        for category, stats in self.results['categories'].items():
            print(f"   {category}:")
            print(f"      Tested: {stats['total']}")
            print(f"      Passed: {stats['passed']}")
            print(f"      Failed: {stats['failed']}")
        
        if self.results['errors']:
            print(f"\n❌ Errors ({len(self.results['errors'])}):")
            for error in self.results['errors'][:5]:  # Show first 5
                print(f"   - {error['category']}/{error['tool']}: {error['error']}")
        
        # Save detailed report
        with open('test_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("\n✅ Detailed report saved to test_report.json")
        
        # Recommendations
        print("\n💡 Recommendations:")
        print("   1. Tools with API errors may need updated endpoints")
        print("   2. Tools requiring specific device types need conditional testing")
        print("   3. Some tools require specific license levels")
        print("   4. Natural language mappings can be improved with more scenarios")

def main():
    """Run the comprehensive test."""
    tester = ComprehensiveToolTester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()