#!/usr/bin/env python3
"""
Test MCP prompts to verify parameter improvements.
This simulates what would happen when Claude uses the MCP tools.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.main import app
from meraki_client import MerakiClient
import json

# Initialize client
meraki = MerakiClient()

def test_prompt_1():
    """Test: List organizations - Simple connectivity test"""
    print("\n" + "="*60)
    print("TEST 1: List Organizations")
    print("Prompt: 'Show me all Meraki organizations'")
    print("-"*60)
    
    try:
        # Find the list_organizations tool
        orgs = meraki.dashboard.organizations.getOrganizations()
        print(f"✅ Found {len(orgs)} organizations")
        for org in orgs[:3]:  # Show first 3
            print(f"  - {org.get('name')} (ID: {org.get('id')})")
        return True, orgs[0]['id'] if orgs else None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def test_prompt_2(org_id):
    """Test: Get networks - Tests basic pagination"""
    print("\n" + "="*60)
    print("TEST 2: Get Networks in Organization")
    print("Prompt: 'List all networks in the organization'")
    print("-"*60)
    
    try:
        networks = meraki.dashboard.organizations.getOrganizationNetworks(org_id)
        print(f"✅ Found {len(networks)} networks")
        
        # Find Reserve St or any network
        target_network = None
        for net in networks:
            print(f"  - {net.get('name')} (ID: {net.get('id')})")
            if 'Reserve' in net.get('name', '') or not target_network:
                target_network = net
        
        return True, target_network['id'] if target_network else None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def test_prompt_3(network_id):
    """Test: Network Events - Should use perPage=1000"""
    print("\n" + "="*60)
    print("TEST 3: Network Events (Testing perPage=1000)")
    print("Prompt: 'Show me recent network events'")
    print("-"*60)
    
    try:
        # This should internally use perPage=1000
        from server.tools_networks import meraki_client as tools_meraki
        tools_meraki.dashboard = meraki.dashboard
        
        # Import the function to test
        from server.tools_networks import register_network_tool_handlers
        from server.tools_networks import app as tools_app
        
        # Mock the response to check parameters
        original_method = meraki.dashboard.networks.getNetworkEvents
        called_params = {}
        
        def mock_get_events(net_id, **kwargs):
            called_params.update(kwargs)
            # Return empty response to avoid errors
            return {'events': [], 'pageInfo': {}}
        
        meraki.dashboard.networks.getNetworkEvents = mock_get_events
        
        # Call through the tool
        from server.tools_networks import get_network_events
        result = get_network_events(network_id)
        
        # Restore original method
        meraki.dashboard.networks.getNetworkEvents = original_method
        
        # Check if perPage was set correctly
        if called_params.get('perPage') == 1000:
            print(f"✅ Network Events using perPage=1000")
            print(f"   Parameters used: {called_params}")
        else:
            print(f"❌ Network Events NOT using correct perPage")
            print(f"   Expected perPage=1000, got: {called_params.get('perPage')}")
            return False, None
            
        return True, None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def test_prompt_4(network_id):
    """Test: Network Clients - Should use perPage=1000"""
    print("\n" + "="*60)
    print("TEST 4: Network Clients (Testing perPage=1000)")
    print("Prompt: 'List all clients in the network'")
    print("-"*60)
    
    try:
        from server.tools_networks import meraki_client as tools_meraki
        tools_meraki.dashboard = meraki.dashboard
        
        # Mock to check parameters
        called_params = {}
        original_method = meraki.dashboard.networks.getNetworkClients
        
        def mock_get_clients(net_id, **kwargs):
            called_params.update(kwargs)
            return []  # Return empty list
        
        meraki.dashboard.networks.getNetworkClients = mock_get_clients
        
        # Call the tool
        from server.tools_networks import get_network_clients
        result = get_network_clients(network_id)
        
        # Restore
        meraki.dashboard.networks.getNetworkClients = original_method
        
        # Check parameters
        if called_params.get('perPage') == 1000:
            print(f"✅ Network Clients using perPage=1000")
            print(f"   Parameters: {called_params}")
        else:
            print(f"❌ Network Clients NOT using correct perPage")
            print(f"   Expected perPage=1000, got: {called_params.get('perPage')}")
            return False, None
            
        return True, None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def test_prompt_5(network_id):
    """Test: Security Events - Should use perPage=1000 and timespan"""
    print("\n" + "="*60)
    print("TEST 5: Security Events (Testing perPage=1000 + timespan)")
    print("Prompt: 'Show security events for the network'")
    print("-"*60)
    
    try:
        from server.tools_appliance_additional import meraki_client as tools_meraki
        tools_meraki.dashboard = meraki.dashboard
        
        # Mock to check parameters
        called_params = {}
        original_method = meraki.dashboard.appliance.getNetworkApplianceSecurityEvents
        
        def mock_get_security_events(net_id, **kwargs):
            called_params.update(kwargs)
            return []
        
        meraki.dashboard.appliance.getNetworkApplianceSecurityEvents = mock_get_security_events
        
        # Call the tool
        from server.tools_appliance_additional import get_network_appliance_security_events
        result = get_network_appliance_security_events(network_id)
        
        # Restore
        meraki.dashboard.appliance.getNetworkApplianceSecurityEvents = original_method
        
        # Check parameters
        success = True
        if called_params.get('perPage') != 1000:
            print(f"❌ Security Events NOT using perPage=1000 (got {called_params.get('perPage')})")
            success = False
        else:
            print(f"✅ Security Events using perPage=1000")
            
        if called_params.get('timespan') != 2678400:
            print(f"❌ Security Events NOT using timespan=2678400 (got {called_params.get('timespan')})")
            success = False
        else:
            print(f"✅ Security Events using timespan=2678400 (31 days)")
            
        print(f"   Full parameters: {called_params}")
        return success, None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def test_prompt_6(org_id):
    """Test: Organization Device Availability - Should use perPage=1000"""
    print("\n" + "="*60)
    print("TEST 6: Organization Device Availability (Testing perPage=1000)")
    print("Prompt: 'Show device availability for the organization'")
    print("-"*60)
    
    try:
        from server.tools_organizations_additional import meraki_client as tools_meraki
        tools_meraki.dashboard = meraki.dashboard
        
        # Mock to check parameters
        called_params = {}
        original_method = meraki.dashboard.organizations.getOrganizationDevicesAvailabilities
        
        def mock_get_availabilities(org_id, **kwargs):
            called_params.update(kwargs)
            return []
        
        meraki.dashboard.organizations.getOrganizationDevicesAvailabilities = mock_get_availabilities
        
        # Call the tool
        from server.tools_organizations_additional import get_organization_devices_availabilities
        result = get_organization_devices_availabilities(org_id)
        
        # Restore
        meraki.dashboard.organizations.getOrganizationDevicesAvailabilities = original_method
        
        # Check parameters
        if called_params.get('perPage') == 1000:
            print(f"✅ Device Availabilities using perPage=1000")
            print(f"   Parameters: {called_params}")
        else:
            print(f"❌ Device Availabilities NOT using correct perPage")
            print(f"   Expected perPage=1000, got: {called_params.get('perPage')}")
            return False, None
            
        return True, None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def test_prompt_7(network_id):
    """Test: Wireless Clients - Should use perPage=1000"""
    print("\n" + "="*60)
    print("TEST 7: Wireless Clients (Testing perPage=1000)")
    print("Prompt: 'List all wireless clients'")
    print("-"*60)
    
    try:
        from server.tools_wireless import meraki_client as tools_meraki
        tools_meraki.dashboard = meraki.dashboard
        
        # Mock to check parameters
        called_params = {}
        original_method = meraki.dashboard.wireless.getNetworkWirelessClients
        
        def mock_get_wireless_clients(net_id, **kwargs):
            called_params.update(kwargs)
            return []
        
        meraki.dashboard.wireless.getNetworkWirelessClients = mock_get_wireless_clients
        
        # Call the tool
        from server.tools_wireless import get_network_wireless_clients
        result = get_network_wireless_clients(network_id)
        
        # Restore
        meraki.dashboard.wireless.getNetworkWirelessClients = original_method
        
        # Check parameters
        if called_params.get('perPage') == 1000:
            print(f"✅ Wireless Clients using perPage=1000")
            print(f"   Parameters: {called_params}")
        else:
            print(f"❌ Wireless Clients NOT using correct perPage")
            print(f"   Expected perPage=1000, got: {called_params.get('perPage')}")
            return False, None
            
        return True, None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def test_prompt_8(network_id):
    """Test: Alert History - Should use perPage=1000"""
    print("\n" + "="*60)
    print("TEST 8: Alert History (Testing perPage=1000)")
    print("Prompt: 'Show network alert history'")
    print("-"*60)
    
    try:
        from server.tools_networks_additional import meraki_client as tools_meraki
        tools_meraki.dashboard = meraki.dashboard
        
        # Mock to check parameters
        called_params = {}
        original_method = meraki.dashboard.networks.getNetworkAlertsHistory
        
        def mock_get_alerts(net_id, **kwargs):
            called_params.update(kwargs)
            return []
        
        meraki.dashboard.networks.getNetworkAlertsHistory = mock_get_alerts
        
        # Call the tool
        from server.tools_networks_additional import get_network_alerts_history
        result = get_network_alerts_history(network_id)
        
        # Restore
        meraki.dashboard.networks.getNetworkAlertsHistory = original_method
        
        # Check parameters
        if called_params.get('perPage') == 1000:
            print(f"✅ Alert History using perPage=1000 (was 100 before)")
            print(f"   Parameters: {called_params}")
        else:
            print(f"❌ Alert History NOT using correct perPage")
            print(f"   Expected perPage=1000, got: {called_params.get('perPage')}")
            return False, None
            
        return True, None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def main():
    """Run all tests"""
    print("="*60)
    print("MCP PARAMETER IMPROVEMENT TESTS")
    print("Testing that all APIs use perPage=1000 and proper defaults")
    print("="*60)
    
    # Track results
    results = []
    
    # Test 1: Get organizations
    success, org_id = test_prompt_1()
    results.append(("List Organizations", success))
    
    if not org_id:
        print("\n⚠️ No organization found, using fallback")
        org_id = "test-org"
    
    # Test 2: Get networks
    success, network_id = test_prompt_2(org_id)
    results.append(("Get Networks", success))
    
    if not network_id:
        print("\n⚠️ No network found, using fallback")
        network_id = "test-network"
    
    # Test 3: Network Events
    success, _ = test_prompt_3(network_id)
    results.append(("Network Events (perPage=1000)", success))
    
    # Test 4: Network Clients
    success, _ = test_prompt_4(network_id)
    results.append(("Network Clients (perPage=1000)", success))
    
    # Test 5: Security Events
    success, _ = test_prompt_5(network_id)
    results.append(("Security Events (perPage + timespan)", success))
    
    # Test 6: Device Availability
    success, _ = test_prompt_6(org_id)
    results.append(("Device Availability (perPage=1000)", success))
    
    # Test 7: Wireless Clients
    success, _ = test_prompt_7(network_id)
    results.append(("Wireless Clients (perPage=1000)", success))
    
    # Test 8: Alert History
    success, _ = test_prompt_8(network_id)
    results.append(("Alert History (perPage=1000)", success))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL PARAMETER IMPROVEMENTS WORKING CORRECTLY!")
    else:
        print("⚠️ Some tests failed - check parameter handling")
    
    print("\n" + "="*60)
    print("SAMPLE MCP PROMPTS FOR MANUAL TESTING:")
    print("="*60)
    print("""
1. "List all organizations I have access to"
2. "Show me all networks in the Skycomm organization"
3. "Get the last 100 events for Reserve St network"
4. "List all clients connected to Reserve St"
5. "Show security events for Reserve St network"
6. "Check device availability across the organization"
7. "List wireless clients in Reserve St"
8. "Show alert history for Reserve St"
9. "Display SSID configuration with isolation settings"
10. "Get comprehensive network health for Reserve St"
    """)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)