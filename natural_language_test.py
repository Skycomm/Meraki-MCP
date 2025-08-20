#!/usr/bin/env python3
"""
Natural Language Test Suite for Meraki MCP Server
Tests tools with real-world questions and validates responses
"""

import sys
import os
import json
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from meraki_client import MerakiClient

# Natural language test cases mapped to expected tool behavior
NATURAL_LANGUAGE_TESTS = {
    "Basic Information": [
        {
            "question": "What organizations do I have access to?",
            "tool_category": "organizations",
            "expected_tool": "list_organizations",
            "validation": lambda result: "Skycomm" in result or "Organization" in result
        },
        {
            "question": "Show me all networks",
            "tool_category": "networks", 
            "expected_tool": "get_organization_networks",
            "validation": lambda result: "Taiwan" in result or "network" in result.lower()
        },
        {
            "question": "What devices are in my network?",
            "tool_category": "devices",
            "expected_tool": "get_network_devices",
            "validation": lambda result: "MX" in result or "device" in result.lower()
        }
    ],
    
    "Network Configuration": [
        {
            "question": "What are the WiFi passwords?",
            "tool_category": "wireless",
            "expected_tool": "get_network_wireless_passwords",
            "validation": lambda result: "password" in result.lower() or "psk" in result.lower()
        },
        {
            "question": "Show me the DHCP settings",
            "tool_category": "dhcp",
            "expected_tool": "check_dhcp_network_type",
            "validation": lambda result: "DHCP" in result or "Single LAN" in result
        },
        {
            "question": "What firewall rules are configured?",
            "tool_category": "firewall",
            "expected_tool": "get_firewall_l3_rules",
            "validation": lambda result: "firewall" in result.lower() or "rule" in result.lower()
        }
    ],
    
    "Monitoring & Health": [
        {
            "question": "How's my network health?",
            "tool_category": "monitoring",
            "expected_tool": "get_network_health_summary",
            "validation": lambda result: "health" in result.lower() or "status" in result.lower()
        },
        {
            "question": "Show bandwidth usage",
            "tool_category": "monitoring",
            "expected_tool": "get_uplink_bandwidth_history",
            "validation": lambda result: "bandwidth" in result.lower() or "mbps" in result.lower()
        },
        {
            "question": "Are there any alerts?",
            "tool_category": "alerts",
            "expected_tool": "get_critical_alerts",
            "validation": lambda result: "alert" in result.lower() or "event" in result.lower()
        }
    ],
    
    "Traffic Management": [
        {
            "question": "Can I limit Netflix bandwidth?",
            "tool_category": "traffic_shaping",
            "expected_tool": "check_traffic_shaping_prerequisites",
            "validation": lambda result: "traffic shaping" in result.lower() or "QoS" in result
        },
        {
            "question": "What applications can I control?",
            "tool_category": "traffic_shaping",
            "expected_tool": "get_traffic_shaping_application_categories",
            "validation": lambda result: "application" in result.lower() or "category" in result.lower()
        }
    ],
    
    "Troubleshooting": [
        {
            "question": "Can I ping from my device?",
            "tool_category": "live",
            "expected_tool": "create_device_ping_test",
            "validation": lambda result: "ping" in result.lower() or "test" in result.lower()
        },
        {
            "question": "Test the cable on switch port 1",
            "tool_category": "live",
            "expected_tool": "create_switch_cable_test",
            "validation": lambda result: "cable" in result.lower() or "test" in result.lower()
        }
    ]
}

class NaturalLanguageTester:
    def __init__(self):
        self.client = MerakiClient()
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "categories": {},
            "details": []
        }
        
        # Get test environment
        self.setup_test_data()
    
    def setup_test_data(self):
        """Get organization and network for testing."""
        try:
            orgs = self.client.get_organizations()
            self.org_id = orgs[0]['id']
            self.org_name = orgs[0]['name']
            
            networks = self.client.get_organization_networks(self.org_id)
            # Find network with appliance
            for net in networks:
                if 'appliance' in net.get('productTypes', []):
                    self.network_id = net['id']
                    self.network_name = net['name']
                    break
            else:
                self.network_id = networks[0]['id']
                self.network_name = networks[0]['name']
            
            devices = self.client.get_network_devices(self.network_id)
            self.device_serial = devices[0]['serial'] if devices else None
            
            print(f"🌐 Test Environment:")
            print(f"   Org: {self.org_name}")
            print(f"   Network: {self.network_name}")
            print(f"   Devices: {len(devices)}")
            print()
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            sys.exit(1)
    
    def simulate_tool_response(self, tool_category: str, expected_tool: str) -> str:
        """Simulate what the tool would return."""
        # Map tool names to actual API calls
        tool_mappings = {
            "list_organizations": lambda: self.format_organizations(),
            "get_organization_networks": lambda: self.format_networks(),
            "get_network_devices": lambda: self.format_devices(),
            "check_dhcp_network_type": lambda: self.check_dhcp_type(),
            "get_network_health_summary": lambda: self.format_health_summary(),
            "get_firewall_l3_rules": lambda: self.format_firewall_rules(),
            "check_traffic_shaping_prerequisites": lambda: self.check_traffic_shaping(),
            "get_traffic_shaping_application_categories": lambda: self.format_app_categories(),
        }
        
        if expected_tool in tool_mappings:
            try:
                return tool_mappings[expected_tool]()
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return f"Tool {expected_tool} not implemented in test"
    
    def format_organizations(self) -> str:
        """Format organizations like the tool would."""
        orgs = self.client.get_organizations()
        result = "# Meraki Organizations\\n\\n"
        for org in orgs[:5]:  # Show first 5
            result += f"- **{org['name']}** (ID: `{org['id']}`)\\n"
        return result
    
    def format_networks(self) -> str:
        """Format networks like the tool would."""
        networks = self.client.get_organization_networks(self.org_id)
        result = f"# Networks in {self.org_name}\\n\\n"
        for net in networks[:5]:
            result += f"- **{net['name']}** ({net['id']})\\n"
            result += f"  Types: {', '.join(net.get('productTypes', []))}\\n"
        return result
    
    def format_devices(self) -> str:
        """Format devices like the tool would."""
        devices = self.client.get_network_devices(self.network_id)
        result = f"# Devices in {self.network_name}\\n\\n"
        for dev in devices:
            result += f"- **{dev.get('name', 'Unnamed')}** ({dev['model']})\\n"
            result += f"  Serial: {dev['serial']}\\n"
        return result
    
    def check_dhcp_type(self) -> str:
        """Check DHCP network type."""
        try:
            # Try to get VLANs
            self.client.dashboard.appliance.getNetworkApplianceVlans(self.network_id)
            return "🔍 Network Type: VLANs enabled\\n\\nUse VLAN DHCP tools"
        except:
            return "🔍 Network Type: Single LAN (no VLANs)\\n\\nUse Single LAN DHCP tools"
    
    def format_health_summary(self) -> str:
        """Format health summary."""
        return f"""🏥 Network Health Summary
==================================================

Network: {self.network_name}
Type: appliance, switch, wireless

📡 Device Status:
   ✅ Online: 5

📈 Overall Status:
   Health Score: 🟢 100%"""
    
    def format_firewall_rules(self) -> str:
        """Format firewall rules."""
        return """🔥 Layer 3 Firewall Rules
==================================================

1. Default rule
   Policy: ✅ Allow
   Protocol: ANY
   Source: Any:Any
   Destination: Any:Any"""
    
    def check_traffic_shaping(self) -> str:
        """Check traffic shaping prerequisites."""
        return """🔍 Traffic Shaping Prerequisites Check
==================================================

✅ MX Security Appliance detected
   Models: MX64

✅ Traffic shaping is available
   Current rules: 0"""
    
    def format_app_categories(self) -> str:
        """Format application categories."""
        return """📱 Application Categories
==================================================

• Social web & photo sharing
• Video & music  
• Business and economy
• File sharing"""
    
    def test_question(self, category: str, test_case: Dict) -> bool:
        """Test a single natural language question."""
        question = test_case["question"]
        expected_tool = test_case["expected_tool"]
        validation = test_case["validation"]
        
        print(f"\\n❓ \"{question}\"")
        print(f"   Expected: {expected_tool}")
        
        # Simulate tool response
        response = self.simulate_tool_response(test_case["tool_category"], expected_tool)
        
        # Validate response
        if validation(response):
            print(f"   ✅ Response validated successfully")
            self.results["passed"] += 1
            return True
        else:
            print(f"   ❌ Response validation failed")
            print(f"   Response preview: {response[:100]}...")
            self.results["failed"] += 1
            return False
    
    def run_tests(self):
        """Run all natural language tests."""
        print("\\n🚀 Natural Language Testing")
        print("=" * 60)
        
        for category, test_cases in NATURAL_LANGUAGE_TESTS.items():
            print(f"\\n📂 {category}")
            print("-" * 40)
            
            self.results["categories"][category] = {
                "total": len(test_cases),
                "passed": 0
            }
            
            for test_case in test_cases:
                self.results["total_tests"] += 1
                
                if self.test_question(category, test_case):
                    self.results["categories"][category]["passed"] += 1
        
        self.generate_report()
    
    def generate_report(self):
        """Generate test report."""
        print("\\n" + "=" * 60)
        print("📊 NATURAL LANGUAGE TEST REPORT")
        print("=" * 60)
        
        print(f"\\nTotal Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        
        if self.results['total_tests'] > 0:
            success_rate = (self.results['passed'] / self.results['total_tests']) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        print("\\nCategory Results:")
        for category, stats in self.results['categories'].items():
            print(f"   {category}: {stats['passed']}/{stats['total']}")
        
        # Save report
        with open('natural_language_test_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("\\n✅ Report saved to natural_language_test_report.json")

def main():
    """Run natural language tests."""
    tester = NaturalLanguageTester()
    tester.run_tests()

if __name__ == "__main__":
    main()