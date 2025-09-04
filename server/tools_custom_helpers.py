"""
Helper tools for common tasks - composite tools that combine multiple operations.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_helper_tools(mcp_app, meraki):
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    """
    Register helper tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    
    # Register all helper tools
    register_helper_tool_handlers()

def register_helper_tool_handlers():
    """Register all helper tool handlers using the decorator pattern."""
    
    @app.tool(
        name="perform_security_audit",
        description="🔍 Run comprehensive security audit - checks IDS/IPS, AMP, firewall, content filtering, threats, WiFi security"
    )
    def perform_security_audit(network_id: str):
        """
        Perform a comprehensive security audit on a network.
        
        Args:
            network_id: ID of the network to audit
            
        Returns:
            Comprehensive security audit report
        """
        try:
            # Get network details first
            network = meraki_client.dashboard.networks.getNetwork(network_id)
            network_name = network.get('name', 'Unknown')
            
            audit_results = []
            audit_results.append(f"# 🔍 Comprehensive Security Audit Report: {network_name}")
            audit_results.append(f"**Network ID**: {network_id}")
            audit_results.append(f"**Organization**: {network.get('organizationId', 'Unknown')}")
            audit_results.append(f"**Product Types**: {', '.join(network.get('productTypes', []))}")
            audit_results.append(f"**Time Zone**: {network.get('timeZone', 'Unknown')}")
            audit_results.append(f"**Audit Time**: {__import__('datetime').datetime.now().isoformat()}\n")
            
            # 1. Check IDS/IPS status
            try:
                ids_status = meraki_client.dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)
                mode = ids_status.get('mode', 'disabled')
                if mode == 'disabled':
                    audit_results.append("## ❌ IDS/IPS Status: DISABLED")
                    audit_results.append("**Risk**: Network vulnerable to known attacks")
                    audit_results.append("**Action**: Enable IDS/IPS in prevention mode\n")
                else:
                    audit_results.append(f"## ✅ IDS/IPS Status: {mode.upper()}")
                    audit_results.append(f"**Ruleset**: {ids_status.get('idsRulesets', 'Unknown')}\n")
            except:
                audit_results.append("## ⚠️ IDS/IPS Status: Unable to check\n")
            
            # 2. Check AMP status
            try:
                amp_status = meraki_client.dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)
                mode = amp_status.get('mode', 'disabled')
                if mode == 'disabled':
                    audit_results.append("## ❌ Malware Protection: DISABLED")
                    audit_results.append("**Risk**: No protection against malware")
                    audit_results.append("**Action**: Enable AMP protection\n")
                else:
                    audit_results.append(f"## ✅ Malware Protection: {mode.upper()}\n")
            except:
                audit_results.append("## ⚠️ Malware Protection: Unable to check\n")
            
            # 3. Check content filtering
            try:
                content_filter = meraki_client.dashboard.appliance.getNetworkApplianceContentFiltering(network_id)
                blocked_categories = content_filter.get('blockedUrlCategories', [])
                if not blocked_categories:
                    audit_results.append("## ❌ Content Filtering: NO CATEGORIES BLOCKED")
                    audit_results.append("**Risk**: Users can access malicious websites")
                    audit_results.append("**Action**: Block malware, phishing, and other dangerous categories\n")
                else:
                    audit_results.append(f"## ✅ Content Filtering: {len(blocked_categories)} categories blocked\n")
            except:
                audit_results.append("## ⚠️ Content Filtering: Unable to check\n")
            
            # 4. Check firewall rules
            try:
                l3_rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
                rules = l3_rules.get('rules', [])
                custom_rules = [r for r in rules if r.get('comment') != 'Default rule']
                if len(custom_rules) == 0:
                    audit_results.append("## ⚠️ Firewall Rules: Only default allow-all rule")
                    audit_results.append("**Risk**: No custom security policies")
                    audit_results.append("**Action**: Consider adding specific firewall rules\n")
                else:
                    audit_results.append(f"## ✅ Firewall Rules: {len(custom_rules)} custom rules configured\n")
            except:
                audit_results.append("## ⚠️ Firewall Rules: Unable to check\n")
            
            # 5. Check recent security events
            try:
                events = meraki_client.dashboard.appliance.getNetworkApplianceSecurityEvents(
                    network_id, 
                    timespan=86400  # Last 24 hours
                )
                if events:
                    audit_results.append(f"## 🚨 Recent Security Events: {len(events)} in last 24h")
                    # Show first few events
                    for event in events[:3]:
                        audit_results.append(f"- {event.get('message', 'Unknown event')}")
                    audit_results.append("")
                else:
                    audit_results.append("## ✅ No security events in last 24 hours\n")
            except:
                audit_results.append("## ⚠️ Security Events: Unable to check\n")
            
            # 6. Check WiFi security
            try:
                ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
                weak_ssids = []
                secure_ssids = []
                disabled_ssids = 0
                
                for ssid in ssids:
                    if ssid.get('enabled'):
                        ssid_name = ssid.get('name', f"SSID {ssid.get('number', '?')}")
                        auth = ssid.get('authMode', '')
                        
                        if auth == 'open':
                            weak_ssids.append(f"**{ssid_name}** (SSID {ssid.get('number')})")
                            weak_ssids.append(f"  - ❌ Security: Open (No password!)")
                            weak_ssids.append(f"  - Visible: {ssid.get('visible', 'Unknown')}")
                            weak_ssids.append(f"  - Splash Page: {ssid.get('splashPage', 'None')}")
                        elif auth == 'psk' and ssid.get('encryptionMode') == 'wep':
                            weak_ssids.append(f"**{ssid_name}** (SSID {ssid.get('number')})")
                            weak_ssids.append(f"  - ❌ Security: WEP (Weak encryption!)")
                        elif auth == 'psk':
                            wpa_mode = ssid.get('wpaEncryptionMode', 'Unknown')
                            if wpa_mode not in ['WPA2 only', 'WPA3 only', 'WPA3 Transition Mode']:
                                weak_ssids.append(f"**{ssid_name}** (SSID {ssid.get('number')})")
                                weak_ssids.append(f"  - ⚠️ Security: {wpa_mode} (Consider WPA2/WPA3)")
                            else:
                                secure_ssids.append(f"{ssid_name} ({wpa_mode})")
                        elif auth == '8021x-radius':
                            secure_ssids.append(f"{ssid_name} (Enterprise 802.1X)")
                        else:
                            secure_ssids.append(f"{ssid_name} ({auth})")
                    else:
                        disabled_ssids += 1
                
                audit_results.append("## 📶 WiFi Security Analysis")
                audit_results.append(f"**Total SSIDs**: 15 (standard for Meraki)")
                audit_results.append(f"**Enabled SSIDs**: {15 - disabled_ssids}")
                audit_results.append(f"**Disabled SSIDs**: {disabled_ssids}\n")
                
                if weak_ssids:
                    audit_results.append("### ❌ Security Issues Found:")
                    for line in weak_ssids:
                        audit_results.append(line)
                    audit_results.append("")
                
                if secure_ssids:
                    audit_results.append("### ✅ Properly Secured SSIDs:")
                    for ssid in secure_ssids:
                        audit_results.append(f"- {ssid}")
                    audit_results.append("")
                    
                if not weak_ssids and not secure_ssids:
                    audit_results.append("### ℹ️ No active SSIDs configured\n")
                    
            except Exception as e:
                audit_results.append(f"## ⚠️ WiFi Security: Unable to check - {str(e)}\n")
            
            # 7. Check VPN configuration
            try:
                vpn_config = meraki_client.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)
                mode = vpn_config.get('mode', 'none')
                
                audit_results.append("## 🔐 VPN Configuration")
                audit_results.append(f"**Mode**: {mode}")
                
                if mode != 'none':
                    subnets = vpn_config.get('subnets', [])
                    hubs = vpn_config.get('hubs', [])
                    audit_results.append(f"**Subnets in VPN**: {len(subnets)}")
                    audit_results.append(f"**Hub connections**: {len(hubs)}")
                    
                    # Check for local subnets
                    local_subnets = [s for s in subnets if s.get('useVpn')]
                    if local_subnets:
                        audit_results.append("### Local subnets in VPN:")
                        for subnet in local_subnets[:3]:
                            audit_results.append(f"- {subnet.get('localSubnet')} ({subnet.get('name', 'Unnamed')})")
                else:
                    audit_results.append("VPN not configured")
                audit_results.append("")
            except:
                pass
            
            # 8. Check VLAN configuration
            try:
                vlans = meraki_client.dashboard.appliance.getNetworkApplianceVlans(network_id)
                
                if vlans:
                    audit_results.append("## 🏗️ Network Segmentation (VLANs)")
                    audit_results.append(f"**Total VLANs**: {len(vlans)}")
                    
                    for vlan in vlans[:5]:  # Show first 5
                        vlan_id = vlan.get('id', 'Unknown')
                        vlan_name = vlan.get('name', 'Unnamed')
                        subnet = vlan.get('subnet', 'Unknown')
                        audit_results.append(f"- VLAN {vlan_id}: {vlan_name} ({subnet})")
                    
                    if len(vlans) > 5:
                        audit_results.append(f"  ... and {len(vlans) - 5} more VLANs")
                    audit_results.append("")
                else:
                    audit_results.append("## 🏗️ Network Segmentation")
                    audit_results.append("⚠️ **No VLANs configured** - Consider network segmentation for security\n")
            except:
                pass
            
            # 9. Check Layer 7 firewall
            try:
                l7_rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
                rules = l7_rules.get('rules', []) if isinstance(l7_rules, dict) else l7_rules
                
                if rules:
                    audit_results.append("## 🌐 Layer 7 Application Control")
                    audit_results.append(f"**Total L7 Rules**: {len(rules)}")
                    
                    blocked_countries = []
                    blocked_apps = []
                    
                    for rule in rules:
                        if rule.get('policy') == 'deny':
                            rule_type = rule.get('type', '')
                            if rule_type == 'blacklistedCountries':
                                countries = rule.get('value', {}).get('countries', [])
                                blocked_countries.extend(countries)
                            elif rule_type == 'application':
                                app_name = rule.get('value', {}).get('name', 'Unknown app')
                                blocked_apps.append(app_name)
                    
                    if blocked_countries:
                        audit_results.append(f"### 🌍 Geo-blocking Active:")
                        audit_results.append(f"Blocking {len(set(blocked_countries))} countries: {', '.join(set(blocked_countries))}")
                    
                    if blocked_apps:
                        audit_results.append(f"### 📱 Application Blocking:")
                        for app in blocked_apps[:5]:
                            audit_results.append(f"- {app}")
                    audit_results.append("")
                else:
                    audit_results.append("## 🌐 Layer 7 Application Control")
                    audit_results.append("⚠️ No L7 rules configured\n")
            except:
                pass
            
            # 10. Check client devices
            try:
                clients = meraki_client.dashboard.networks.getNetworkClients(network_id, timespan=86400)
                
                if clients:
                    audit_results.append("## 👥 Client Analysis (Last 24h)")
                    audit_results.append(f"**Total unique clients**: {len(clients)}")
                    
                    # Analyze client types
                    os_types = {}
                    manufacturers = {}
                    
                    for client in clients:
                        os = client.get('os', 'Unknown')
                        if os:
                            os_types[os] = os_types.get(os, 0) + 1
                        
                        manufacturer = client.get('manufacturer', 'Unknown')
                        if manufacturer:
                            manufacturers[manufacturer] = manufacturers.get(manufacturer, 0) + 1
                    
                    # Show top OS types
                    if os_types:
                        audit_results.append("### Operating Systems:")
                        sorted_os = sorted(os_types.items(), key=lambda x: x[1], reverse=True)
                        for os, count in sorted_os[:5]:
                            audit_results.append(f"- {os}: {count} devices")
                    
                    # Show top manufacturers
                    if manufacturers:
                        audit_results.append("### Device Manufacturers:")
                        sorted_mfg = sorted(manufacturers.items(), key=lambda x: x[1], reverse=True)
                        for mfg, count in sorted_mfg[:5]:
                            audit_results.append(f"- {mfg}: {count} devices")
                    
                    audit_results.append("")
            except:
                pass
            
            # 11. Calculate security score
            security_score = 0
            max_score = 100
            issues = []
            
            # IDS/IPS (20 points)
            try:
                if 'prevention' in str(audit_results):
                    security_score += 20
                elif 'detection' in str(audit_results):
                    security_score += 10
                else:
                    issues.append("IDS/IPS disabled")
            except:
                pass
            
            # Malware protection (20 points)
            if '✅ Malware Protection' in str(audit_results):
                security_score += 20
            else:
                issues.append("Malware protection disabled")
            
            # Content filtering (15 points)
            if '✅ Content Filtering' in str(audit_results):
                security_score += 15
            elif 'categories blocked' in str(audit_results):
                security_score += 10
            else:
                issues.append("No content filtering")
            
            # Firewall rules (15 points)
            if 'custom rules configured' in str(audit_results):
                security_score += 15
            else:
                security_score += 5
                issues.append("Only default firewall rules")
            
            # WiFi security (20 points)
            if '❌ Security: Open' in str(audit_results):
                issues.append("Open WiFi network detected")
            elif '✅ Properly Secured SSIDs' in str(audit_results):
                security_score += 20
            else:
                security_score += 10
            
            # VLANs (10 points)
            if 'Total VLANs' in str(audit_results) and 'No VLANs' not in str(audit_results):
                security_score += 10
            else:
                issues.append("No network segmentation")
            
            audit_results.append("## 🎯 Security Score")
            audit_results.append(f"**Overall Score: {security_score}/100**")
            
            if security_score >= 80:
                audit_results.append("✅ **Rating: Excellent** - Strong security posture")
            elif security_score >= 60:
                audit_results.append("⚠️ **Rating: Good** - Some improvements recommended")
            elif security_score >= 40:
                audit_results.append("⚠️ **Rating: Fair** - Significant improvements needed")
            else:
                audit_results.append("❌ **Rating: Poor** - Critical security gaps")
            
            if issues:
                audit_results.append("\n### Key Issues to Address:")
                for issue in issues:
                    audit_results.append(f"- {issue}")
            
            # 12. Summary and recommendations
            audit_results.append("\n## 📋 Detailed Recommendations")
            
            priority = 1
            if 'IDS/IPS disabled' in issues:
                audit_results.append(f"{priority}. **Enable IDS/IPS in prevention mode** - Critical for threat protection")
                priority += 1
            
            if 'Malware protection disabled' in issues:
                audit_results.append(f"{priority}. **Enable Advanced Malware Protection** - Essential for ransomware defense")
                priority += 1
            
            if 'Open WiFi network' in str(issues):
                audit_results.append(f"{priority}. **Secure WiFi with WPA2/WPA3** - Prevent unauthorized access")
                priority += 1
            
            if 'No content filtering' in issues:
                audit_results.append(f"{priority}. **Configure content filtering** - Block malicious websites")
                priority += 1
            
            if 'No network segmentation' in issues:
                audit_results.append(f"{priority}. **Implement VLANs** - Isolate critical systems")
                priority += 1
            
            if priority == 1:
                audit_results.append("✅ Security configuration looks good - maintain current settings")
            
            audit_results.append("\n**Regular Maintenance:**")
            audit_results.append("- Review security events weekly")
            audit_results.append("- Update firmware quarterly")
            audit_results.append("- Audit firewall rules monthly")
            audit_results.append("- Test backup connectivity regularly")
            
            return "\n".join(audit_results)
            
        except Exception as e:
            return f"❌ Error performing security audit: {str(e)}"
    
    @app.tool(
        name="check_network_health",
        description="🏥 Check network health - device status, recent events, wireless performance metrics"
    )
    def check_network_health(network_id: str):
        """
        Check overall network health including devices and performance.
        
        Args:
            network_id: ID of the network to check
            
        Returns:
            Network health report
        """
        try:
            # Get network details
            network = meraki_client.dashboard.networks.getNetwork(network_id)
            network_name = network.get('name', 'Unknown')
            org_id = network.get('organizationId')
            product_types = network.get('productTypes', [])
            
            health_report = []
            health_report.append(f"# 🏥 Network Health Report: {network_name}")
            health_report.append(f"**Check Time**: {__import__('datetime').datetime.now().isoformat()}")
            health_report.append(f"**Product Types**: {', '.join(product_types)}\n")
            
            # 1. For wireless networks, check connection stats
            if 'wireless' in product_types:
                try:
                    conn_stats = meraki_client.dashboard.wireless.getNetworkWirelessConnectionStats(
                        network_id, timespan=3600
                    )
                    if conn_stats:
                        health_report.append("## 📡 Wireless Performance (Last Hour)")
                        
                        # Calculate success rate from raw counts
                        success_count = conn_stats.get('success', 0)
                        auth_fails = conn_stats.get('auth', 0)
                        assoc_fails = conn_stats.get('assoc', 0)
                        dhcp_fails = conn_stats.get('dhcp', 0)
                        dns_fails = conn_stats.get('dns', 0)
                        
                        total_attempts = success_count + auth_fails + assoc_fails + dhcp_fails + dns_fails
                        
                        if total_attempts > 0:
                            success_rate = (success_count / total_attempts) * 100
                            if success_rate < 90:
                                health_report.append(f"- ⚠️ Success Rate: {success_rate:.1f}% (LOW)")
                            else:
                                health_report.append(f"- ✅ Success Rate: {success_rate:.1f}%")
                            
                            if auth_fails > 0:
                                auth_fail_rate = (auth_fails / total_attempts) * 100
                                health_report.append(f"- ❌ Auth Failures: {auth_fail_rate:.1f}% ({auth_fails} failures)")
                        health_report.append("")
                except:
                    pass
            
            # 2. For appliance networks, check uplink status
            if 'appliance' in product_types:
                try:
                    # Get organization uplink statuses
                    uplink_statuses = meraki_client.dashboard.appliance.getOrganizationApplianceUplinkStatuses(org_id)
                    network_uplinks = [u for u in uplink_statuses if u.get('networkId') == network_id]
                    
                    if network_uplinks:
                        health_report.append("## 🌐 Uplink Status")
                        for uplink in network_uplinks:
                            for interface in uplink.get('uplinks', []):
                                status = interface.get('status', 'unknown')
                                interface_name = interface.get('interface', 'Unknown')
                                if status == 'active':
                                    health_report.append(f"- ✅ {interface_name}: Active")
                                else:
                                    health_report.append(f"- ❌ {interface_name}: {status}")
                        health_report.append("")
                except:
                    pass
            
            # 3. Check device status
            try:
                devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
                offline_devices = []
                alerting_devices = []
                
                for device in devices:
                    status = device.get('status', 'unknown')
                    if status == 'offline':
                        offline_devices.append(f"{device.get('name', device.get('serial'))} ({device.get('model')})")
                    elif status == 'alerting':
                        alerting_devices.append(f"{device.get('name', device.get('serial'))} ({device.get('model')})")
                
                health_report.append("## 🖥️ Device Status")
                health_report.append(f"- Total Devices: {len(devices)}")
                health_report.append(f"- ✅ Online: {len([d for d in devices if d.get('status') == 'online'])}")
                
                if offline_devices:
                    health_report.append(f"- ❌ Offline: {len(offline_devices)}")
                    for device in offline_devices[:3]:  # Show first 3
                        health_report.append(f"  - {device}")
                
                if alerting_devices:
                    health_report.append(f"- ⚠️ Alerting: {len(alerting_devices)}")
                    for device in alerting_devices[:3]:  # Show first 3
                        health_report.append(f"  - {device}")
                health_report.append("")
            except:
                health_report.append("## ⚠️ Device Status: Unable to check\n")
            
            # 4. Check recent events
            try:
                events = meraki_client.dashboard.networks.getNetworkEvents(
                    network_id,
                    productType='appliance',  # Required for multi-product networks
                    perPage=1000
                )
                
                if events:
                    health_report.append(f"## 📋 Recent Network Events (24h)")
                    event_counts = {}
                    for event in events:
                        event_type = event.get('type', 'unknown')
                        event_counts[event_type] = event_counts.get(event_type, 0) + 1
                    
                    for event_type, count in event_counts.items():
                        if 'down' in event_type.lower():
                            health_report.append(f"- ❌ {event_type}: {count} occurrences")
                        else:
                            health_report.append(f"- ⚠️ {event_type}: {count} occurrences")
                    health_report.append("")
                else:
                    health_report.append("## ✅ No concerning network events in last 24h\n")
            except:
                health_report.append("## ⚠️ Network Events: Unable to check\n")
            
            # 5. Summary
            health_report.append("## 📊 Health Summary")
            health_report.append("Review any ❌ or ⚠️ items above for potential issues.")
            health_report.append("\n**Recommended Actions:**")
            health_report.append("1. Investigate any offline or alerting devices")
            health_report.append("2. Address high packet loss or latency if present")
            health_report.append("3. Review recent network events for patterns")
            
            return "\n".join(health_report)
            
        except Exception as e:
            return f"❌ Error checking network health: {str(e)}"
    
    @app.tool(
        name="analyze_security_posture",
        description="🛡️ Analyze security posture - comprehensive check of all security settings and recent threats"
    )
    def analyze_security_posture(organization_id: str):
        """
        Analyze the security posture across the entire organization.
        
        Args:
            organization_id: ID of the organization to analyze
            
        Returns:
            Organization-wide security posture analysis
        """
        try:
            # Get organization details
            org = meraki_client.dashboard.organizations.getOrganization(organization_id)
            org_name = org.get('name', 'Unknown')
            
            analysis = []
            analysis.append(f"# 🛡️ Security Posture Analysis: {org_name}")
            analysis.append(f"**Analysis Time**: {__import__('datetime').datetime.now().isoformat()}\n")
            
            # Get all networks
            networks = meraki_client.dashboard.organizations.getOrganizationNetworks(organization_id)
            
            # Security statistics
            networks_checked = 0
            ids_enabled_count = 0
            amp_enabled_count = 0
            content_filter_count = 0
            weak_wifi_count = 0
            total_threats = 0
            
            analysis.append(f"## 📊 Organization Overview")
            analysis.append(f"- Total Networks: {len(networks)}")
            analysis.append("")
            
            # Check each network
            for network in networks:
                network_id = network['id']
                network_name = network['name']
                networks_checked += 1
                
                # Check IDS/IPS
                try:
                    ids = meraki_client.dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)
                    if ids.get('mode') != 'disabled':
                        ids_enabled_count += 1
                except:
                    pass
                
                # Check AMP
                try:
                    amp = meraki_client.dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)
                    if amp.get('mode') != 'disabled':
                        amp_enabled_count += 1
                except:
                    pass
                
                # Check content filtering
                try:
                    cf = meraki_client.dashboard.appliance.getNetworkApplianceContentFiltering(network_id)
                    if cf.get('blockedUrlCategories'):
                        content_filter_count += 1
                except:
                    pass
                
                # Check WiFi security
                try:
                    ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
                    for ssid in ssids:
                        if ssid.get('enabled'):
                            auth = ssid.get('authMode', '')
                            if auth == 'open' or (auth == 'psk' and ssid.get('encryptionMode') == 'wep'):
                                weak_wifi_count += 1
                                break
                except:
                    pass
                
                # Count security events
                try:
                    events = meraki_client.dashboard.appliance.getNetworkApplianceSecurityEvents(
                        network_id, 
                        timespan=86400
                    )
                    total_threats += len(events)
                except:
                    pass
            
            # Calculate percentages
            ids_percent = (ids_enabled_count / networks_checked * 100) if networks_checked > 0 else 0
            amp_percent = (amp_enabled_count / networks_checked * 100) if networks_checked > 0 else 0
            cf_percent = (content_filter_count / networks_checked * 100) if networks_checked > 0 else 0
            
            # Security scores
            analysis.append("## 🔒 Security Feature Adoption")
            analysis.append(f"- IDS/IPS Enabled: {ids_enabled_count}/{networks_checked} ({ids_percent:.0f}%)")
            analysis.append(f"- Malware Protection: {amp_enabled_count}/{networks_checked} ({amp_percent:.0f}%)")
            analysis.append(f"- Content Filtering: {content_filter_count}/{networks_checked} ({cf_percent:.0f}%)")
            analysis.append("")
            
            # Risk indicators
            analysis.append("## ⚠️ Risk Indicators")
            if weak_wifi_count > 0:
                analysis.append(f"- ❌ Weak WiFi Security: {weak_wifi_count} networks with open/WEP")
            else:
                analysis.append("- ✅ WiFi Security: All networks using strong encryption")
            
            if total_threats > 0:
                analysis.append(f"- 🚨 Security Events (24h): {total_threats} threats detected")
            else:
                analysis.append("- ✅ Security Events: No threats in last 24 hours")
            analysis.append("")
            
            # Overall score
            security_score = 0
            if ids_percent >= 80: security_score += 25
            elif ids_percent >= 50: security_score += 15
            elif ids_percent > 0: security_score += 5
            
            if amp_percent >= 80: security_score += 25
            elif amp_percent >= 50: security_score += 15  
            elif amp_percent > 0: security_score += 5
            
            if cf_percent >= 80: security_score += 25
            elif cf_percent >= 50: security_score += 15
            elif cf_percent > 0: security_score += 5
            
            if weak_wifi_count == 0: security_score += 25
            elif weak_wifi_count <= 2: security_score += 10
            
            analysis.append("## 🎯 Security Score")
            analysis.append(f"**Overall Score: {security_score}/100**")
            
            if security_score >= 80:
                analysis.append("Rating: Excellent - Strong security posture")
            elif security_score >= 60:
                analysis.append("Rating: Good - Some improvements needed")
            elif security_score >= 40:
                analysis.append("Rating: Fair - Significant improvements required")
            else:
                analysis.append("Rating: Poor - Critical security gaps")
            
            analysis.append("\n## 📋 Recommendations")
            if ids_percent < 100:
                analysis.append("1. Enable IDS/IPS on all networks")
            if amp_percent < 100:
                analysis.append("2. Enable malware protection on all networks")
            if cf_percent < 100:
                analysis.append("3. Configure content filtering on all networks")
            if weak_wifi_count > 0:
                analysis.append("4. Upgrade WiFi security to WPA2/WPA3")
            
            return "\n".join(analysis)
            
        except Exception as e:
            return f"❌ Error analyzing security posture: {str(e)}"
    
    @app.tool(
        name="apply_common_security_rules",
        description="🔒 Apply common security rules - easily block malicious traffic, countries, and content"
    )
    def apply_common_security_rules(
        network_id: str,
        block_malicious_sites: bool = True,
        block_high_risk_countries: bool = False,
        block_p2p: bool = False,
        block_social_media: bool = False,
        custom_blocked_countries: str = None,
        custom_blocked_ports: str = None
    ):
        """
        Apply common security rules to a network with a single command.
        
        Args:
            network_id: Network ID to apply rules to
            block_malicious_sites: Block malware, phishing, and spam sites (default: True)
            block_high_risk_countries: Block traffic from high-risk countries (default: False)
            block_p2p: Block peer-to-peer applications (default: False)
            block_social_media: Block social media sites (default: False)
            custom_blocked_countries: Additional countries to block (e.g., "CN,RU,KP")
            custom_blocked_ports: TCP ports to block (e.g., "445,3389,22")
            
        Returns:
            Summary of applied security rules
        """
        try:
            results = []
            results.append(f"# 🔒 Applying Security Rules to Network {network_id}\n")
            
            # 1. Content Filtering for malicious sites
            if block_malicious_sites:
                try:
                    # Block dangerous content categories
                    dangerous_categories = [
                        "5",   # Malware sites
                        "6",   # Phishing and other frauds
                        "3",   # Illegal content
                        "4",   # Illegal downloads
                        "83"   # Peer to peer (if not separately handled)
                    ]
                    
                    if block_social_media:
                        dangerous_categories.extend(["70"])  # Social networking
                    
                    if block_p2p:
                        if "83" not in dangerous_categories:
                            dangerous_categories.append("83")
                    
                    meraki_client.dashboard.appliance.updateNetworkApplianceContentFiltering(
                        network_id,
                        blockedUrlCategories=[f"meraki:contentFiltering/category/{cat}" for cat in dangerous_categories],
                        urlCategoryListSize='fullList'
                    )
                    results.append("✅ **Content Filtering**: Blocked malicious site categories")
                except Exception as e:
                    results.append(f"❌ **Content Filtering**: Failed - {str(e)}")
            
            # 2. Layer 7 Firewall Rules
            l7_rules = []
            
            # Block high-risk countries
            if block_high_risk_countries or custom_blocked_countries:
                countries = []
                if block_high_risk_countries:
                    # Common high-risk countries
                    countries.extend(["CN", "RU", "KP", "IR"])
                if custom_blocked_countries:
                    countries.extend([c.strip().upper() for c in custom_blocked_countries.split(',')])
                
                # Remove duplicates
                countries = list(set(countries))
                
                if countries:
                    l7_rules.append({
                        "policy": "deny",
                        "type": "blacklistedCountries",
                        "value": {"countries": countries}
                    })
                    results.append(f"✅ **Geo-blocking**: Blocked {len(countries)} countries: {', '.join(countries)}")
            
            # Block P2P applications
            if block_p2p:
                # Common P2P applications
                p2p_apps = [
                    "meraki:layer7/application/17",   # BitTorrent
                    "meraki:layer7/application/169"   # Tor
                ]
                for app_id in p2p_apps:
                    l7_rules.append({
                        "policy": "deny",
                        "type": "application",
                        "value": {"id": app_id}
                    })
                results.append("✅ **L7 Firewall**: Blocked P2P applications")
            
            # Apply L7 rules if any
            if l7_rules:
                try:
                    meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL7FirewallRules(network_id, rules=l7_rules)
                except Exception as e:
                    results.append(f"❌ **L7 Firewall**: Failed - {str(e)}")
            
            # 3. Layer 3 Firewall Rules for specific ports
            if custom_blocked_ports:
                try:
                    # Get existing L3 rules
                    current_l3 = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
                    existing_rules = current_l3.get('rules', [])
                    
                    # Add port blocking rules
                    ports = [p.strip() for p in custom_blocked_ports.split(',')]
                    for port in ports:
                        new_rule = {
                            'comment': f'Block port {port} - Added by security helper',
                            'policy': 'deny',
                            'protocol': 'tcp',
                            'srcCidr': 'any',
                            'destCidr': 'any',
                            'destPort': port,
                            'syslogEnabled': True
                        }
                        existing_rules.insert(0, new_rule)  # Add to beginning
                    
                    # Update rules
                    meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(network_id, rules=existing_rules)
                    results.append(f"✅ **L3 Firewall**: Blocked TCP ports: {custom_blocked_ports}")
                except Exception as e:
                    results.append(f"❌ **L3 Firewall**: Failed - {str(e)}")
            
            # 4. Enable IDS/IPS if not already enabled
            try:
                ids_status = meraki_client.dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)
                if ids_status.get('mode') == 'disabled':
                    meraki_client.dashboard.appliance.updateNetworkApplianceSecurityIntrusion(
                        network_id,
                        mode='prevention',
                        idsRulesets='balanced'
                    )
                    results.append("✅ **IDS/IPS**: Enabled in prevention mode")
                else:
                    results.append(f"ℹ️ **IDS/IPS**: Already enabled ({ids_status.get('mode')})")
            except Exception as e:
                results.append(f"❌ **IDS/IPS**: Failed - {str(e)}")
            
            # 5. Enable AMP if not already enabled
            try:
                amp_status = meraki_client.dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)
                if amp_status.get('mode') == 'disabled':
                    meraki_client.dashboard.appliance.updateNetworkApplianceSecurityMalware(network_id, mode='enabled')
                    results.append("✅ **Malware Protection**: Enabled AMP")
                else:
                    results.append("ℹ️ **Malware Protection**: Already enabled")
            except Exception as e:
                results.append(f"❌ **Malware Protection**: Failed - {str(e)}")
            
            # Summary
            results.append("\n## 📋 Summary")
            results.append("Security rules have been applied. Review the results above.")
            results.append("\n💡 **Next Steps**:")
            results.append("- Review firewall logs for blocked traffic")
            results.append("- Monitor security events")
            results.append("- Consider adding custom rules for your specific needs")
            
            return "\n".join(results)
            
        except Exception as e:
            return f"❌ Error applying security rules: {str(e)}"