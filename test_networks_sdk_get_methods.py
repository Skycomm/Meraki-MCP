#!/usr/bin/env python3
"""
Test all Networks SDK GET methods against live Meraki API.
Only tests read operations, no write/update/delete operations.
"""

import sys
sys.path.append('.')
from meraki_client import MerakiClient
import traceback

def test_get_methods():
    """Test all GET methods for Networks SDK."""
    
    meraki = MerakiClient()
    
    # Test parameters
    test_org_id = "686470"  # Skycomm
    test_network_id = "L_726205439913500692"  # Reserve St network
    test_client_mac = "38:f9:d3:7e:b7:aa"  # A sample client
    
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }
    
    print("🧪 TESTING NETWORKS SDK GET METHODS")
    print("=" * 60)
    print(f"Organization: {test_org_id}")
    print(f"Network: {test_network_id}")
    print()
    
    # Test 1: getNetwork
    print("1. Testing getNetwork...")
    try:
        network = meraki.dashboard.networks.getNetwork(test_network_id)
        print(f"   ✅ Success: {network.get('name')}")
        results['success'].append('getNetwork')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetwork')
    
    # Test 2: getNetworkDevices
    print("2. Testing getNetworkDevices...")
    try:
        devices = meraki.dashboard.networks.getNetworkDevices(test_network_id)
        print(f"   ✅ Success: Found {len(devices)} devices")
        results['success'].append('getNetworkDevices')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkDevices')
    
    # Test 3: getNetworkClients
    print("3. Testing getNetworkClients...")
    try:
        clients = meraki.dashboard.networks.getNetworkClients(
            test_network_id, timespan=86400, perPage=10
        )
        print(f"   ✅ Success: Found {len(clients)} clients")
        results['success'].append('getNetworkClients')
        
        # Get first client for other tests
        if clients:
            test_client_id = clients[0].get('id')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkClients')
    
    # Test 4: getNetworkEvents
    print("4. Testing getNetworkEvents...")
    try:
        events = meraki.dashboard.networks.getNetworkEvents(
            test_network_id, 
            productType='wireless',  # Required for multi-product networks
            perPage=10
        )
        print(f"   ✅ Success: Found {len(events)} events")
        results['success'].append('getNetworkEvents')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkEvents')
    
    # Test 5: getNetworkEventsEventTypes
    print("5. Testing getNetworkEventsEventTypes...")
    try:
        event_types = meraki.dashboard.networks.getNetworkEventsEventTypes(test_network_id)
        print(f"   ✅ Success: Found {len(event_types)} event types")
        results['success'].append('getNetworkEventsEventTypes')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkEventsEventTypes')
    
    # Test 6: getNetworkAlertsHistory
    print("6. Testing getNetworkAlertsHistory...")
    try:
        alerts = meraki.dashboard.networks.getNetworkAlertsHistory(
            test_network_id, perPage=10
        )
        print(f"   ✅ Success: Found {len(alerts)} alerts")
        results['success'].append('getNetworkAlertsHistory')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkAlertsHistory')
    
    # Test 7: getNetworkAlertsSettings
    print("7. Testing getNetworkAlertsSettings...")
    try:
        settings = meraki.dashboard.networks.getNetworkAlertsSettings(test_network_id)
        print(f"   ✅ Success: Got alert settings")
        results['success'].append('getNetworkAlertsSettings')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkAlertsSettings')
    
    # Test 8: getNetworkSettings
    print("8. Testing getNetworkSettings...")
    try:
        settings = meraki.dashboard.networks.getNetworkSettings(test_network_id)
        print(f"   ✅ Success: Got network settings")
        results['success'].append('getNetworkSettings')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkSettings')
    
    # Test 9: getNetworkFirmwareUpgrades
    print("9. Testing getNetworkFirmwareUpgrades...")
    try:
        upgrades = meraki.dashboard.networks.getNetworkFirmwareUpgrades(test_network_id)
        print(f"   ✅ Success: Got firmware upgrade settings")
        results['success'].append('getNetworkFirmwareUpgrades')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkFirmwareUpgrades')
    
    # Test 10: getNetworkFloorPlans
    print("10. Testing getNetworkFloorPlans...")
    try:
        floor_plans = meraki.dashboard.networks.getNetworkFloorPlans(test_network_id)
        print(f"   ✅ Success: Found {len(floor_plans)} floor plans")
        results['success'].append('getNetworkFloorPlans')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkFloorPlans')
    
    # Test 11: getNetworkGroupPolicies
    print("11. Testing getNetworkGroupPolicies...")
    try:
        policies = meraki.dashboard.networks.getNetworkGroupPolicies(test_network_id)
        print(f"   ✅ Success: Found {len(policies)} group policies")
        results['success'].append('getNetworkGroupPolicies')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkGroupPolicies')
    
    # Test 12: getNetworkBluetoothClients
    print("12. Testing getNetworkBluetoothClients...")
    try:
        bt_clients = meraki.dashboard.networks.getNetworkBluetoothClients(
            test_network_id, timespan=86400, perPage=10
        )
        print(f"   ✅ Success: Found {len(bt_clients)} Bluetooth clients")
        results['success'].append('getNetworkBluetoothClients')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkBluetoothClients')
    
    # Test 13: getNetworkHealthAlerts
    print("13. Testing getNetworkHealthAlerts...")
    try:
        health_alerts = meraki.dashboard.networks.getNetworkHealthAlerts(test_network_id)
        print(f"   ✅ Success: Found {len(health_alerts)} health alerts")
        results['success'].append('getNetworkHealthAlerts')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkHealthAlerts')
    
    # Test 14: getNetworkNetworkHealthChannelUtilization
    print("14. Testing getNetworkNetworkHealthChannelUtilization...")
    try:
        channel_util = meraki.dashboard.networks.getNetworkNetworkHealthChannelUtilization(
            test_network_id
        )
        print(f"   ✅ Success: Got channel utilization data")
        results['success'].append('getNetworkNetworkHealthChannelUtilization')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkNetworkHealthChannelUtilization')
    
    # Test 15: getNetworkMerakiAuthUsers
    print("15. Testing getNetworkMerakiAuthUsers...")
    try:
        auth_users = meraki.dashboard.networks.getNetworkMerakiAuthUsers(test_network_id)
        print(f"   ✅ Success: Found {len(auth_users)} auth users")
        results['success'].append('getNetworkMerakiAuthUsers')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkMerakiAuthUsers')
    
    # Test 16: getNetworkMqttBrokers
    print("16. Testing getNetworkMqttBrokers...")
    try:
        brokers = meraki.dashboard.networks.getNetworkMqttBrokers(test_network_id)
        print(f"   ✅ Success: Found {len(brokers)} MQTT brokers")
        results['success'].append('getNetworkMqttBrokers')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkMqttBrokers')
    
    # Test 17: getNetworkPiiRequests
    print("17. Testing getNetworkPiiRequests...")
    try:
        pii_requests = meraki.dashboard.networks.getNetworkPiiRequests(test_network_id)
        print(f"   ✅ Success: Found {len(pii_requests)} PII requests")
        results['success'].append('getNetworkPiiRequests')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkPiiRequests')
    
    # Test 18: getNetworkPiiPiiKeys
    print("18. Testing getNetworkPiiPiiKeys...")
    try:
        pii_keys = meraki.dashboard.networks.getNetworkPiiPiiKeys(
            test_network_id, username="test"  # Only ONE search parameter
        )
        print(f"   ✅ Success: Got PII keys")
        results['success'].append('getNetworkPiiPiiKeys')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkPiiPiiKeys')
    
    # Test 19: getNetworkSnmp
    print("19. Testing getNetworkSnmp...")
    try:
        snmp = meraki.dashboard.networks.getNetworkSnmp(test_network_id)
        print(f"   ✅ Success: Got SNMP settings")
        results['success'].append('getNetworkSnmp')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkSnmp')
    
    # Test 20: getNetworkSyslogServers
    print("20. Testing getNetworkSyslogServers...")
    try:
        syslog = meraki.dashboard.networks.getNetworkSyslogServers(test_network_id)
        print(f"   ✅ Success: Got syslog servers")
        results['success'].append('getNetworkSyslogServers')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkSyslogServers')
    
    # Test 21: getNetworkTopologyLinkLayer
    print("21. Testing getNetworkTopologyLinkLayer...")
    try:
        topology = meraki.dashboard.networks.getNetworkTopologyLinkLayer(test_network_id)
        print(f"   ✅ Success: Got topology data")
        results['success'].append('getNetworkTopologyLinkLayer')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkTopologyLinkLayer')
    
    # Test 22: getNetworkTraffic
    print("22. Testing getNetworkTraffic...")
    try:
        traffic = meraki.dashboard.networks.getNetworkTraffic(
            test_network_id, timespan=7200  # Minimum 2 hours required
        )
        print(f"   ✅ Success: Found {len(traffic)} traffic entries")
        results['success'].append('getNetworkTraffic')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkTraffic')
    
    # Test 23: getNetworkTrafficAnalysis
    print("23. Testing getNetworkTrafficAnalysis...")
    try:
        analysis = meraki.dashboard.networks.getNetworkTrafficAnalysis(test_network_id)
        print(f"   ✅ Success: Got traffic analysis settings")
        results['success'].append('getNetworkTrafficAnalysis')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkTrafficAnalysis')
    
    # Test 24: getNetworkTrafficShapingApplicationCategories
    print("24. Testing getNetworkTrafficShapingApplicationCategories...")
    try:
        categories = meraki.dashboard.networks.getNetworkTrafficShapingApplicationCategories(
            test_network_id
        )
        print(f"   ✅ Success: Found {len(categories.get('applicationCategories', []))} categories")
        results['success'].append('getNetworkTrafficShapingApplicationCategories')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkTrafficShapingApplicationCategories')
    
    # Test 25: getNetworkTrafficShapingDscpTaggingOptions
    print("25. Testing getNetworkTrafficShapingDscpTaggingOptions...")
    try:
        dscp = meraki.dashboard.networks.getNetworkTrafficShapingDscpTaggingOptions(
            test_network_id
        )
        print(f"   ✅ Success: Got DSCP tagging options")
        results['success'].append('getNetworkTrafficShapingDscpTaggingOptions')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkTrafficShapingDscpTaggingOptions')
    
    # Test 26: getNetworkWebhooksHttpServers
    print("26. Testing getNetworkWebhooksHttpServers...")
    try:
        servers = meraki.dashboard.networks.getNetworkWebhooksHttpServers(test_network_id)
        print(f"   ✅ Success: Found {len(servers)} webhook servers")
        results['success'].append('getNetworkWebhooksHttpServers')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkWebhooksHttpServers')
    
    # Test 27: getNetworkWebhooksPayloadTemplates
    print("27. Testing getNetworkWebhooksPayloadTemplates...")
    try:
        templates = meraki.dashboard.networks.getNetworkWebhooksPayloadTemplates(test_network_id)
        print(f"   ✅ Success: Found {len(templates)} payload templates")
        results['success'].append('getNetworkWebhooksPayloadTemplates')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkWebhooksPayloadTemplates')
    
    # Test 28: getNetworkVlanProfiles
    print("28. Testing getNetworkVlanProfiles...")
    try:
        profiles = meraki.dashboard.networks.getNetworkVlanProfiles(test_network_id)
        print(f"   ✅ Success: Found {len(profiles)} VLAN profiles")
        results['success'].append('getNetworkVlanProfiles')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkVlanProfiles')
    
    # Test 29: getNetworkNetflow
    print("29. Testing getNetworkNetflow...")
    try:
        netflow = meraki.dashboard.networks.getNetworkNetflow(test_network_id)
        print(f"   ✅ Success: Got NetFlow settings")
        results['success'].append('getNetworkNetflow')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkNetflow')
    
    # Test 30: getNetworkSplashLoginAttempts
    print("30. Testing getNetworkSplashLoginAttempts...")
    try:
        attempts = meraki.dashboard.networks.getNetworkSplashLoginAttempts(
            test_network_id, timespan=3600
        )
        print(f"   ✅ Success: Found {len(attempts)} splash login attempts")
        results['success'].append('getNetworkSplashLoginAttempts')
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        results['failed'].append('getNetworkSplashLoginAttempts')
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print(f"✅ Successful: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⏭️  Skipped: {len(results['skipped'])}")
    
    if results['failed']:
        print("\n❌ Failed methods:")
        for method in results['failed']:
            print(f"   - {method}")
    
    success_rate = len(results['success']) / (len(results['success']) + len(results['failed'])) * 100
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    return results

if __name__ == '__main__':
    test_get_methods()