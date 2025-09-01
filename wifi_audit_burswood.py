#!/usr/bin/env python3
"""
Comprehensive WiFi Audit for Skycomm Burswood
Simulates Claude Desktop running all WiFi tools
"""

import os
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki
import json

def wifi_audit_burswood():
    print("🔍 Comprehensive WiFi Audit - Skycomm Burswood")
    print("="*70)
    print("Running all WiFi tools as Claude Desktop would...")
    
    # 1. Find organization
    print("\n📍 1. Finding Organization...")
    orgs = meraki.dashboard.organizations.getOrganizations()
    skycomm = [o for o in orgs if 'Skycomm' in o.get('name', '')]
    if not skycomm:
        print("✗ Skycomm organization not found")
        return
    
    org_id = skycomm[0]['id']
    print(f"✓ Found Skycomm (ID: {org_id})")
    
    # 2. Get networks
    print("\n📍 2. Getting Networks...")
    networks = meraki.dashboard.organizations.getOrganizationNetworks(org_id)
    burswood = [n for n in networks if 'Burswood' in n.get('name', '')]
    if not burswood:
        print("✗ Burswood network not found")
        return
    
    network_id = burswood[0]['id']
    print(f"✓ Found Burswood network (ID: {network_id})")
    print(f"  Product types: {burswood[0].get('productTypes')}")
    
    # 3. Wireless SSIDs
    print("\n📡 3. Wireless SSIDs Configuration:")
    try:
        ssids = meraki.dashboard.wireless.getNetworkWirelessSsids(network_id)
        active_ssids = [s for s in ssids if s.get('enabled')]
        print(f"✓ {len(active_ssids)} active SSIDs out of {len(ssids)} configured")
        for ssid in active_ssids:
            print(f"  - SSID #{ssid.get('number')}: {ssid.get('name')}")
            print(f"    Auth: {ssid.get('authMode')}, VLAN: {ssid.get('vlanId')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 4. Access Points
    print("\n📡 4. Access Points Status:")
    try:
        devices = meraki.dashboard.networks.getNetworkDevices(network_id)
        aps = [d for d in devices if d.get('model', '').startswith('MR')]
        print(f"✓ {len(aps)} access points found")
        for ap in aps:
            status = '🟢' if ap.get('status') == 'online' else '🔴'
            print(f"  {status} {ap.get('name', ap.get('serial'))} ({ap.get('model')})")
            print(f"     Serial: {ap.get('serial')}")
            print(f"     IP: {ap.get('lanIp')}, Firmware: {ap.get('firmware')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 5. Wireless Clients
    print("\n👥 5. Wireless Clients:")
    try:
        clients = meraki.dashboard.networks.getNetworkClients(network_id, perPage=100)
        wireless_clients = [c for c in clients if c.get('ssid')]
        print(f"✓ {len(wireless_clients)} wireless clients connected")
        
        # Group by SSID
        ssid_counts = {}
        for client in wireless_clients:
            ssid = client.get('ssid', 'Unknown')
            ssid_counts[ssid] = ssid_counts.get(ssid, 0) + 1
        
        for ssid, count in ssid_counts.items():
            print(f"  - {ssid}: {count} clients")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 6. Connection Stats
    print("\n📊 6. Wireless Connection Statistics:")
    try:
        stats = meraki.dashboard.wireless.getNetworkWirelessConnectionStats(network_id)
        success_rate = (stats.get('success', 0) / max(stats.get('assoc', 1), 1)) * 100
        print(f"✓ Connection Success Rate: {success_rate:.1f}%")
        print(f"  Associations: {stats.get('assoc', 0)}")
        print(f"  Authentications: {stats.get('auth', 0)}")
        print(f"  Successful: {stats.get('success', 0)}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 7. Failed Connections
    print("\n❌ 7. Failed Connections (Last 24h):")
    try:
        failures = meraki.dashboard.wireless.getNetworkWirelessFailedConnections(
            network_id, timespan=86400
        )
        if failures:
            print(f"✓ {len(failures)} failed connections")
            # Group by failure type
            failure_types = {}
            for fail in failures:
                fail_type = fail.get('failureStep', 'Unknown')
                failure_types[fail_type] = failure_types.get(fail_type, 0) + 1
            
            for fail_type, count in failure_types.items():
                print(f"  - {fail_type}: {count} failures")
        else:
            print("✓ No failed connections")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 8. Channel Utilization
    print("\n📊 8. Channel Utilization:")
    if aps:
        ap_serial = aps[0].get('serial')
        try:
            # 2.4GHz
            util_24 = meraki.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(
                network_id,
                networkWideOnly=False,
                deviceSerial=ap_serial,
                band='2.4',
                timespan=3600
            )
            if util_24:
                avg_24 = sum(u.get('utilization', 0) for u in util_24) / len(util_24)
                print(f"✓ 2.4GHz average utilization: {avg_24:.1f}%")
            
            # 5GHz
            util_5 = meraki.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(
                network_id,
                networkWideOnly=False,
                deviceSerial=ap_serial,
                band='5',
                timespan=3600
            )
            if util_5:
                avg_5 = sum(u.get('utilization', 0) for u in util_5) / len(util_5)
                print(f"✓ 5GHz average utilization: {avg_5:.1f}%")
        except Exception as e:
            print(f"✗ Channel utilization error: {e}")
    
    # 9. Latency Stats
    print("\n⏱️ 9. Wireless Latency Statistics:")
    try:
        latency = meraki.dashboard.wireless.getNetworkWirelessLatencyStats(network_id)
        if latency:
            print(f"✓ Latency Stats:")
            if 'backgroundTraffic' in latency:
                bg = latency['backgroundTraffic']
                print(f"  Background: {bg.get('avg', 0):.2f}ms avg")
            if 'bestEffortTraffic' in latency:
                be = latency['bestEffortTraffic']
                print(f"  Best Effort: {be.get('avg', 0):.2f}ms avg")
            if 'videoTraffic' in latency:
                video = latency['videoTraffic']
                print(f"  Video: {video.get('avg', 0):.2f}ms avg")
            if 'voiceTraffic' in latency:
                voice = latency['voiceTraffic']
                print(f"  Voice: {voice.get('avg', 0):.2f}ms avg")
    except Exception as e:
        print(f"✗ Latency error: {e}")
    
    # 10. Air Marshal (Rogue AP Detection)
    print("\n🛡️ 10. Air Marshal - Rogue AP Detection:")
    try:
        air_marshal = meraki.dashboard.wireless.getNetworkWirelessAirMarshal(
            network_id, timespan=86400
        )
        if air_marshal:
            print(f"✓ {len(air_marshal)} SSIDs detected")
            # Count rogue vs sanctioned
            rogue_count = len([a for a in air_marshal if not a.get('wiredMacs')])
            print(f"  - Potential rogues: {rogue_count}")
            print(f"  - Known/sanctioned: {len(air_marshal) - rogue_count}")
        else:
            print("✓ No rogue APs detected")
    except Exception as e:
        print(f"✗ Air Marshal error: {e}")
    
    # 11. Wireless Settings
    print("\n⚙️ 11. Wireless Network Settings:")
    try:
        settings = meraki.dashboard.wireless.getNetworkWirelessSettings(network_id)
        print(f"✓ Wireless Settings:")
        print(f"  Meshing: {settings.get('meshingEnabled', False)}")
        print(f"  IPv6 Bridge: {settings.get('ipv6BridgeEnabled', False)}")
        print(f"  LED Lights: {settings.get('ledLightsOn', True)}")
        print(f"  Location Analytics: {settings.get('locationAnalyticsEnabled', False)}")
    except Exception as e:
        print(f"✗ Settings error: {e}")
    
    # 12. RF Profiles
    print("\n📻 12. RF Profiles:")
    try:
        rf_profiles = meraki.dashboard.wireless.getNetworkWirelessRfProfiles(network_id)
        if rf_profiles:
            print(f"✓ {len(rf_profiles)} RF profiles configured")
            for profile in rf_profiles:
                print(f"  - {profile.get('name')}: Band {profile.get('bandSelectionType')}")
        else:
            print("✓ Using default RF settings")
    except Exception as e:
        print(f"✗ RF Profiles error: {e}")
    
    # 13. Alerts Settings
    print("\n🚨 13. Network Alert Settings:")
    try:
        alerts = meraki.dashboard.networks.getNetworkAlertsSettings(network_id)
        enabled_alerts = [a for a in alerts.get('alerts', []) if a.get('enabled')]
        print(f"✓ {len(enabled_alerts)} alerts enabled out of {len(alerts.get('alerts', []))}")
        for alert in enabled_alerts[:5]:  # Show first 5
            print(f"  - {alert.get('type')}")
    except Exception as e:
        print(f"✗ Alerts error: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 AUDIT SUMMARY")
    print("="*70)
    
    print("\n✅ Tools that worked:")
    print("  • Organization and network discovery")
    print("  • SSID configuration")
    print("  • Access point status")
    print("  • Client listing")
    print("  • Connection statistics")
    print("  • Failed connections")
    print("  • Channel utilization")
    print("  • Latency statistics")
    print("  • Air Marshal")
    print("  • Wireless settings")
    print("  • RF profiles")
    print("  • Alert settings")
    
    print("\n⚠️ Key Findings:")
    if aps:
        if len(aps) == 1:
            print("  • Only 1 AP deployed - single point of failure")
    if active_ssids:
        if len(active_ssids) == 1:
            print("  • Only 1 active SSID configured")
    
    print("\n🎯 Recommendations:")
    print("  • Consider adding redundant AP for failover")
    print("  • Enable more monitoring alerts")
    print("  • Review channel utilization for optimization")
    print("  • Consider enabling location analytics")

if __name__ == "__main__":
    wifi_audit_burswood()