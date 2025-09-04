#!/usr/bin/env python3
"""
Comprehensive network audit for Skycomm Attadale.
Handles both MX integrated WiFi and dedicated MR access points.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

def find_attadale_network():
    """Find the Skycomm Attadale network."""
    
    print("🔍 FINDING SKYCOMM ATTADALE NETWORK")
    print("=" * 50)
    
    meraki_client = MerakiClient()
    skycomm_org_id = '686470'  # Skycomm organization
    
    try:
        networks = meraki_client.dashboard.organizations.getOrganizationNetworks(skycomm_org_id)
        
        attadale_networks = []
        for network in networks:
            name = network.get('name', '').lower()
            if 'attadale' in name:
                attadale_networks.append(network)
                print(f"✅ Found: {network.get('name')} ({network.get('id')})")
        
        return attadale_networks
        
    except Exception as e:
        print(f"❌ Error finding networks: {e}")
        return []

def identify_devices(network_id):
    """Identify MX and MR devices in the network."""
    
    print(f"\n🔍 IDENTIFYING DEVICES IN NETWORK")
    print("=" * 50)
    
    meraki_client = MerakiClient()
    
    try:
        devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
        
        mx_devices = []
        mr_devices = []
        other_devices = []
        
        for device in devices:
            model = device.get('model', '')
            serial = device.get('serial', '')
            name = device.get('name', 'Unnamed')
            
            if model.startswith('MX'):
                mx_devices.append(device)
                print(f"🛡️  MX Device: {name} ({model}) - {serial}")
            elif model.startswith('MR'):
                mr_devices.append(device)
                print(f"📡 MR Device: {name} ({model}) - {serial}")
            else:
                other_devices.append(device)
                print(f"⚙️  Other: {name} ({model}) - {serial}")
        
        return mx_devices, mr_devices, other_devices
        
    except Exception as e:
        print(f"❌ Error getting devices: {e}")
        return [], [], []

def audit_wireless_security(network_id, mx_devices, mr_devices):
    """Audit wireless security for both MX and MR devices."""
    
    print(f"\n🔐 WIRELESS SECURITY AUDIT")
    print("=" * 50)
    
    meraki_client = MerakiClient()
    security_issues = []
    secure_ssids = []
    
    try:
        # Get all wireless SSIDs
        ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
        
        print(f"Found {len(ssids)} total SSIDs")
        print()
        
        for ssid in ssids:
            if ssid.get('enabled'):
                ssid_num = ssid.get('number')
                ssid_name = ssid.get('name', 'Unnamed')
                auth_mode = ssid.get('authMode', 'Unknown')
                visible = ssid.get('visible', True)
                
                print(f"📶 SSID {ssid_num}: {ssid_name}")
                print(f"   Status: {'🟢 Enabled' if ssid.get('enabled') else '🔴 Disabled'}")
                print(f"   Visibility: {'👁️  Visible' if visible else '🫥 Hidden'}")
                
                # Security Analysis
                if auth_mode == 'psk':
                    wpa_mode = ssid.get('wpaEncryptionMode', 'Unknown')
                    print(f"   Security: ✅ WPA/WPA2 PSK ({wpa_mode})")
                    secure_ssids.append(ssid_name)
                elif auth_mode == 'open':
                    print(f"   Security: ❌ OPEN (No Password)")
                    security_issues.append(f"SSID '{ssid_name}' is open/unsecured")
                elif auth_mode == '8021x-radius':
                    print(f"   Security: ✅ WPA2 Enterprise (802.1X)")
                    secure_ssids.append(ssid_name)
                else:
                    print(f"   Security: ⚠️  {auth_mode.upper()}")
                
                # Bandwidth limits
                up_limit = ssid.get('perClientBandwidthLimitUp', 0)
                down_limit = ssid.get('perClientBandwidthLimitDown', 0)
                if up_limit > 0 or down_limit > 0:
                    print(f"   Bandwidth: ↑{up_limit} ↓{down_limit} Kbps per client")
                
                print()
        
        return security_issues, secure_ssids
        
    except Exception as e:
        print(f"❌ Error auditing wireless: {e}")
        return [], []

def audit_firewall_rules(network_id):
    """Audit firewall configuration."""
    
    print(f"\n🔥 FIREWALL AUDIT")
    print("=" * 50)
    
    meraki_client = MerakiClient()
    firewall_issues = []
    
    try:
        # Layer 3 firewall rules
        l3_rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
        
        print(f"Layer 3 Firewall Rules: {len(l3_rules)} rules")
        
        allow_any_found = False
        for rule in l3_rules:
            policy = rule.get('policy', 'unknown')
            protocol = rule.get('protocol', 'any')
            dest_port = rule.get('destPort', 'any')
            dest_cidr = rule.get('destCidr', 'any')
            
            if policy == 'allow' and dest_cidr == 'any' and dest_port == 'any':
                allow_any_found = True
                print(f"   ⚠️  Rule: Allow ANY to ANY ({protocol})")
        
        if allow_any_found:
            firewall_issues.append("Default allow-all rule found - consider more restrictive policies")
        else:
            print(f"   ✅ No obvious allow-all rules found")
        
        # Layer 7 firewall rules  
        try:
            l7_rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
            print(f"Layer 7 Firewall Rules: {len(l7_rules)} rules")
            
            blocked_apps = [rule for rule in l7_rules if rule.get('policy') == 'deny']
            print(f"   Blocked applications: {len(blocked_apps)}")
            
        except Exception as e:
            print(f"   L7 rules: {e}")
        
        return firewall_issues
        
    except Exception as e:
        print(f"❌ Error auditing firewall: {e}")
        return []

def audit_content_filtering(network_id):
    """Audit content filtering settings."""
    
    print(f"\n🛡️  CONTENT FILTERING AUDIT")
    print("=" * 50)
    
    meraki_client = MerakiClient()
    content_issues = []
    
    try:
        content_filter = meraki_client.dashboard.appliance.getNetworkApplianceContentFiltering(network_id)
        
        allowed_patterns = content_filter.get('allowedUrlPatterns', [])
        blocked_patterns = content_filter.get('blockedUrlPatterns', [])
        
        print(f"Allowed URL patterns: {len(allowed_patterns)}")
        print(f"Blocked URL patterns: {len(blocked_patterns)}")
        
        # Check blocked categories
        try:
            categories = meraki_client.dashboard.appliance.getNetworkApplianceContentFilteringCategories(network_id)
            blocked_categories = [cat['name'] for cat in categories if cat.get('blocked', False)]
            
            print(f"Blocked categories: {len(blocked_categories)}")
            if blocked_categories:
                print(f"   {', '.join(blocked_categories[:5])}{'...' if len(blocked_categories) > 5 else ''}")
            else:
                content_issues.append("No content categories are blocked")
                
        except Exception as e:
            print(f"   Categories error: {e}")
        
        return content_issues
        
    except Exception as e:
        print(f"❌ Error auditing content filtering: {e}")
        return []

def audit_threat_protection(network_id):
    """Audit intrusion detection and malware protection."""
    
    print(f"\n🛡️  THREAT PROTECTION AUDIT")
    print("=" * 50)
    
    meraki_client = MerakiClient()
    threat_issues = []
    
    try:
        # IDS/IPS
        intrusion = meraki_client.dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)
        
        ids_enabled = intrusion.get('mode', 'disabled') != 'disabled'
        ids_mode = intrusion.get('mode', 'disabled')
        
        print(f"IDS/IPS: {'✅ Enabled' if ids_enabled else '❌ Disabled'} ({ids_mode})")
        
        if not ids_enabled:
            threat_issues.append("Intrusion Detection/Prevention is disabled")
        
        # Malware protection
        malware = meraki_client.dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)
        
        malware_enabled = malware.get('mode', 'disabled') != 'disabled'
        malware_mode = malware.get('mode', 'disabled')
        
        print(f"Malware Protection: {'✅ Enabled' if malware_enabled else '❌ Disabled'} ({malware_mode})")
        
        if not malware_enabled:
            threat_issues.append("Malware protection is disabled")
        
        return threat_issues
        
    except Exception as e:
        print(f"❌ Error auditing threat protection: {e}")
        return []

def generate_audit_report(network_name, network_id, mx_devices, mr_devices, security_issues, firewall_issues, content_issues, threat_issues, secure_ssids):
    """Generate comprehensive audit report."""
    
    print(f"\n📊 COMPREHENSIVE AUDIT REPORT")
    print("=" * 60)
    
    print(f"🏢 **Network**: {network_name}")
    print(f"🆔 **Network ID**: {network_id}")
    print(f"📅 **Audit Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n🔧 **Infrastructure Summary**:")
    print(f"   MX Devices: {len(mx_devices)}")
    for mx in mx_devices:
        print(f"      - {mx.get('name', 'Unnamed')} ({mx.get('model')})")
    print(f"   MR Devices: {len(mr_devices)}")
    for mr in mr_devices:
        print(f"      - {mr.get('name', 'Unnamed')} ({mr.get('model')})")
    
    print(f"\n✅ **Secure SSIDs**: {len(secure_ssids)}")
    for ssid in secure_ssids:
        print(f"      - {ssid}")
    
    # Critical Issues
    all_issues = security_issues + firewall_issues + content_issues + threat_issues
    
    print(f"\n⚠️  **Security Issues Found**: {len(all_issues)}")
    
    if all_issues:
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")
    else:
        print(f"   🎉 No critical security issues found!")
    
    # Risk Assessment
    risk_level = "LOW"
    if len(all_issues) > 5:
        risk_level = "HIGH"
    elif len(all_issues) > 2:
        risk_level = "MEDIUM"
    
    print(f"\n🎯 **Overall Risk Level**: {risk_level}")
    
    # Recommendations
    print(f"\n💡 **Recommendations**:")
    if security_issues:
        print(f"   - Secure all open WiFi networks with WPA2/WPA3")
    if firewall_issues:
        print(f"   - Review and tighten firewall rules")
    if content_issues:
        print(f"   - Enable content filtering for malicious categories")
    if threat_issues:
        print(f"   - Enable IDS/IPS and malware protection")
    
    if not all_issues:
        print(f"   ✅ Network security posture is good - maintain current settings")

def main():
    """Run comprehensive Skycomm Attadale audit."""
    
    print("🏢 SKYCOMM ATTADALE COMPREHENSIVE NETWORK AUDIT")
    print("=" * 60)
    
    # Find Attadale network
    attadale_networks = find_attadale_network()
    
    if not attadale_networks:
        print("❌ No Attadale networks found")
        return
    
    for network in attadale_networks:
        network_id = network.get('id')
        network_name = network.get('name')
        
        print(f"\n📡 Auditing: {network_name}")
        
        # Identify devices
        mx_devices, mr_devices, other_devices = identify_devices(network_id)
        
        # Run security audits
        security_issues, secure_ssids = audit_wireless_security(network_id, mx_devices, mr_devices)
        firewall_issues = audit_firewall_rules(network_id)
        content_issues = audit_content_filtering(network_id)
        threat_issues = audit_threat_protection(network_id)
        
        # Generate report
        generate_audit_report(
            network_name, network_id, mx_devices, mr_devices,
            security_issues, firewall_issues, content_issues, 
            threat_issues, secure_ssids
        )

if __name__ == "__main__":
    main()