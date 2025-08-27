#!/usr/bin/env python3
"""
Test that our parameter improvements are working correctly.
This tests that APIs now use perPage=1000 by default.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import Mock, patch, call
from server.main import app

def test_parameter_defaults():
    """Test that our APIs now use correct default parameters."""
    
    # Create a mock Meraki client
    mock_client = Mock()
    
    # Test cases for APIs we fixed
    test_cases = [
        {
            'module': 'server.tools_networks',
            'function': 'get_network_events',
            'api_path': 'dashboard.networks.getNetworkEvents',
            'args': ['test-network-id'],
            'expected_kwargs': {'perPage': 1000}
        },
        {
            'module': 'server.tools_networks',
            'function': 'get_network_clients',
            'api_path': 'dashboard.networks.getNetworkClients',
            'args': ['test-network-id'],
            'expected_kwargs': {'perPage': 1000, 'total_pages': 'all'}
        },
        {
            'module': 'server.tools_networks_additional',
            'function': 'get_network_alerts_history',
            'api_path': 'dashboard.networks.getNetworkAlertsHistory',
            'args': ['test-network-id'],
            'expected_kwargs': {'perPage': 1000}
        },
        {
            'module': 'server.tools_appliance_additional',
            'function': 'get_network_appliance_security_events',
            'api_path': 'dashboard.appliance.getNetworkApplianceSecurityEvents',
            'args': ['test-network-id'],
            'expected_kwargs': {'perPage': 1000, 'timespan': 2678400}
        },
        {
            'module': 'server.tools_wireless',
            'function': 'get_network_wireless_clients',
            'api_path': 'dashboard.wireless.getNetworkWirelessClients',
            'args': ['test-network-id'],
            'expected_kwargs': {'perPage': 1000}
        },
        {
            'module': 'server.tools_organizations_additional',
            'function': 'get_organization_devices_availabilities',
            'api_path': 'dashboard.organizations.getOrganizationDevicesAvailabilities',
            'args': ['test-org-id'],
            'expected_kwargs': {'perPage': 1000}
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        try:
            # Import the module
            module = __import__(test_case['module'], fromlist=[test_case['function']])
            
            # Set the global meraki_client in the module
            module.meraki_client = mock_client
            
            # Get the function
            func = getattr(module, test_case['function'])
            
            # Set up mock for this specific API call
            api_parts = test_case['api_path'].split('.')
            mock_api = mock_client
            for part in api_parts[:-1]:
                mock_api = getattr(mock_api, part)
            
            # Set the final method to return empty list/dict
            setattr(mock_api, api_parts[-1], Mock(return_value=[]))
            
            # Call the function
            func(*test_case['args'])
            
            # Get the actual call
            actual_call = getattr(mock_api, api_parts[-1]).call_args
            
            # Check if the expected kwargs are present
            success = True
            for key, value in test_case['expected_kwargs'].items():
                if key not in actual_call.kwargs or actual_call.kwargs[key] != value:
                    success = False
                    break
            
            results.append({
                'function': f"{test_case['module']}.{test_case['function']}",
                'success': success,
                'expected': test_case['expected_kwargs'],
                'actual': actual_call.kwargs if actual_call else {}
            })
            
        except Exception as e:
            results.append({
                'function': f"{test_case['module']}.{test_case['function']}",
                'success': False,
                'error': str(e)
            })
    
    # Print results
    print("=" * 60)
    print("PARAMETER IMPROVEMENT TEST RESULTS")
    print("=" * 60)
    
    for result in results:
        if result['success']:
            print(f"✅ {result['function']}")
            print(f"   Correctly uses: {result.get('expected', {})}")
        else:
            print(f"❌ {result['function']}")
            if 'error' in result:
                print(f"   Error: {result['error']}")
            else:
                print(f"   Expected: {result.get('expected', {})}")
                print(f"   Actual: {result.get('actual', {})}")
        print()
    
    # Summary
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    print("=" * 60)
    print(f"SUMMARY: {success_count}/{total_count} tests passed")
    print("=" * 60)
    
    if success_count == total_count:
        print("✅ All parameter improvements working correctly!")
    else:
        print("⚠️ Some APIs may need additional fixes")
    
    return success_count == total_count

if __name__ == "__main__":
    success = test_parameter_defaults()
    sys.exit(0 if success else 1)