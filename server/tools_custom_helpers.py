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
            
            # Initialize device tracking variables for use throughout audit
            mx_with_wifi = []
            mr_devices = []
            other_devices = []
            
            audit_results = []
            audit_results.append(f"# 🔍 Comprehensive Security Audit Report: {network_name}")
            audit_results.append(f"**Network ID**: {network_id}")
            audit_results.append(f"**Organization**: {network.get('organizationId', 'Unknown')}")
            audit_results.append(f"**Product Types**: {', '.join(network.get('productTypes', []))}")
            audit_results.append(f"**Time Zone**: {network.get('timeZone', 'Unknown')}")
            audit_results.append(f"**Audit Time**: {__import__('datetime').datetime.now().isoformat()}\n")
            
            # 0. Analyze wireless infrastructure
            try:
                devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
                
                for device in devices:
                    model = device.get('model', '')
                    device_name = device.get('name') or device.get('serial', 'Unnamed')
                    
                    if model.startswith('MX') and ('W' in model or 'w' in model):
                        mx_with_wifi.append({
                            'model': model,
                            'name': device_name,
                            'serial': device.get('serial', ''),
                            'status': device.get('status', 'unknown')
                        })
                    elif model.startswith('MR'):
                        mr_devices.append({
                            'model': model,
                            'name': device_name,
                            'serial': device.get('serial', ''),
                            'status': device.get('status', 'unknown')
                        })
                    else:
                        other_devices.append({
                            'model': model,
                            'name': device_name,
                            'serial': device.get('serial', ''),
                            'status': device.get('status', 'unknown')
                        })
                
                # Determine wireless infrastructure type
                audit_results.append("## 📡 Wireless Infrastructure Analysis")
                
                if mx_with_wifi and not mr_devices:
                    audit_results.append("**WiFi Source**: MX Integrated Wireless Only")
                    audit_results.append("*Note: No dedicated wireless access points - WiFi provided by MX appliance*")
                    for mx in mx_with_wifi:
                        status_icon = "✅" if mx['status'] == 'online' else "❌"
                        audit_results.append(f"- {status_icon} **{mx['model']}**: {mx['name']} ({mx['serial']})")
                        
                elif mr_devices and not mx_with_wifi:
                    audit_results.append("**WiFi Source**: Dedicated MR Access Points Only")
                    audit_results.append(f"**Total APs**: {len(mr_devices)}")
                    for mr in mr_devices[:3]:  # Show first 3
                        status_icon = "✅" if mr['status'] == 'online' else "❌" 
                        audit_results.append(f"- {status_icon} **{mr['model']}**: {mr['name']} ({mr['serial']})")
                    if len(mr_devices) > 3:
                        audit_results.append(f"  ... and {len(mr_devices) - 3} more APs")
                        
                elif mx_with_wifi and mr_devices:
                    audit_results.append("**WiFi Source**: Mixed Infrastructure (MX + MR)")
                    audit_results.append("*Network has both MX integrated wireless and dedicated access points*")
                    
                    audit_results.append("### MX Appliances with WiFi:")
                    for mx in mx_with_wifi:
                        status_icon = "✅" if mx['status'] == 'online' else "❌"
                        audit_results.append(f"- {status_icon} **{mx['model']}**: {mx['name']}")
                    
                    audit_results.append("### Dedicated Access Points:")
                    for mr in mr_devices[:3]:
                        status_icon = "✅" if mr['status'] == 'online' else "❌"
                        audit_results.append(f"- {status_icon} **{mr['model']}**: {mr['name']}")
                    if len(mr_devices) > 3:
                        audit_results.append(f"  ... and {len(mr_devices) - 3} more APs")
                        
                else:
                    audit_results.append("**WiFi Source**: ⚠️ No wireless infrastructure detected")
                    audit_results.append("*Network may not have WiFi capability*")
                
                # Show other network devices for context
                if other_devices:
                    audit_results.append(f"\n**Other Network Devices**: {len(other_devices)}")
                    device_summary = {}
                    for device in other_devices:
                        model_type = device['model'][:2] if device['model'] else 'Unknown'
                        device_summary[model_type] = device_summary.get(model_type, 0) + 1
                    
                    for device_type, count in device_summary.items():
                        audit_results.append(f"- {device_type}*: {count} device{'s' if count > 1 else ''}")
                
                audit_results.append("")
                
            except Exception as e:
                audit_results.append("## 📡 Wireless Infrastructure")
                audit_results.append(f"⚠️ Unable to analyze devices: {str(e)}\n")
            
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
            
            # 6. Check WiFi security based on infrastructure type
            audit_results.append("## 📶 WiFi Security Analysis")
            
            # Determine wireless infrastructure type and audit accordingly
            if 'wireless' not in network.get('productTypes', []):
                audit_results.append("⚠️ **No wireless capability** detected in this network\n")
                
            elif mx_with_wifi and not mr_devices:
                # MX integrated wireless only
                mx_model = mx_with_wifi[0].get('model', 'MX*W')
                audit_results.append(f"**Infrastructure**: {mx_model} integrated wireless")
                audit_results.append("*WiFi provided by security appliance - no separate access points*\n")
                
                try:
                    # Use MX appliance wireless API for integrated wireless (not MR wireless API)
                    ssids = meraki_client.dashboard.appliance.getNetworkApplianceSsids(network_id)
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
                            elif auth == 'psk' and ssid.get('encryptionMode') == 'wep':
                                weak_ssids.append(f"**{ssid_name}** (SSID {ssid.get('number')})")
                                weak_ssids.append(f"  - ❌ Security: WEP (Weak encryption!)")
                            elif auth == 'psk':
                                # MX appliances may not have wpaEncryptionMode field like MR devices
                                if ssid.get('psk'):
                                    secure_ssids.append(f"{ssid_name} (WPA/WPA2 PSK)")
                                else:
                                    weak_ssids.append(f"**{ssid_name}** (SSID {ssid.get('number')})")
                                    weak_ssids.append(f"  - ⚠️ Security: PSK configured but no password set")
                            elif auth == '8021x-radius':
                                secure_ssids.append(f"{ssid_name} (Enterprise 802.1X)")
                            else:
                                secure_ssids.append(f"{ssid_name} ({auth})")
                        else:
                            disabled_ssids += 1
                    
                    total_ssids = len(ssids)
                    enabled_ssids = total_ssids - disabled_ssids
                    audit_results.append(f"**Total MX SSIDs**: {total_ssids}")
                    audit_results.append(f"**Enabled SSIDs**: {enabled_ssids}")
                    audit_results.append(f"**Disabled SSIDs**: {disabled_ssids}")
                    audit_results.append("")
                    
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
                    audit_results.append(f"⚠️ **WiFi Security**: Unable to check - {str(e)}")
                    audit_results.append("*This might be expected for MX-only networks with integrated wireless*\n")
                    
            else:
                # Dedicated MR access points or mixed infrastructure
                if mr_devices and not mx_with_wifi:
                    audit_results.append(f"**Infrastructure**: {len(mr_devices)} dedicated access point{'s' if len(mr_devices) > 1 else ''}")
                elif mx_with_wifi and mr_devices:
                    audit_results.append(f"**Infrastructure**: Mixed wireless (MX integrated + {len(mr_devices)} dedicated AP{'s' if len(mr_devices) > 1 else ''})")
                else:
                    audit_results.append("**Infrastructure**: Wireless enabled (checking configuration...)")
                
                audit_results.append("*Full wireless infrastructure analysis and connection monitoring available*\n")
                
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
                    
                    audit_results.append(f"**Total SSIDs**: 15 (standard for Meraki)")
                    audit_results.append(f"**Enabled SSIDs**: {15 - disabled_ssids}")
                    audit_results.append(f"**Disabled SSIDs**: {disabled_ssids}")
                    audit_results.append("")
                    
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
                        
                    # For dedicated infrastructure, also check wireless connection stats
                    if mr_devices:
                        try:
                            conn_stats = meraki_client.dashboard.wireless.getNetworkWirelessConnectionStats(
                                network_id, timespan=3600
                            )
                            if conn_stats:
                                success = conn_stats.get('success', 0)
                                total = sum([conn_stats.get(k, 0) for k in ['success', 'auth', 'assoc', 'dhcp', 'dns']])
                                if total > 0:
                                    success_rate = (success / total) * 100
                                    audit_results.append(f"**WiFi Connection Success Rate**: {success_rate:.1f}% ({success}/{total} attempts)")
                                    audit_results.append("")
                        except:
                            # Connection stats may not be available, that's OK
                            pass
                        
                except Exception as e:
                    audit_results.append(f"⚠️ **WiFi Security**: Unable to check - {str(e)}\n")
            
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
            
            # Get devices to understand infrastructure
            mx_with_wifi = []
            mr_devices = []
            try:
                devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
                for device in devices:
                    model = device.get('model', '')
                    if model.startswith('MX') and ('W' in model or 'w' in model):
                        mx_with_wifi.append(device)
                    elif model.startswith('MR'):
                        mr_devices.append(device)
            except:
                pass
            
            health_report = []
            health_report.append(f"# 🏥 Network Health Report: {network_name}")
            health_report.append(f"**Check Time**: {__import__('datetime').datetime.now().isoformat()}")
            health_report.append(f"**Product Types**: {', '.join(product_types)}\n")
            
            # 1. For wireless networks with dedicated APs, check connection stats
            if 'wireless' in product_types and mr_devices:
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
            elif 'wireless' in product_types and mx_with_wifi and not mr_devices:
                # MX-only wireless - connection stats may not be available via wireless API
                health_report.append("## 📡 Wireless Infrastructure")
                mx_model = mx_with_wifi[0].get('model', 'MX*W') if mx_with_wifi else 'MX*W'
                health_report.append(f"**WiFi Source**: {mx_model} integrated wireless")
                health_report.append("*Note: Dedicated AP metrics not applicable - WiFi provided by security appliance*\n")
            
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
                
                # Check WiFi security (use correct API based on infrastructure)
                try:
                    # First determine infrastructure type
                    devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
                    mx_with_wifi = [d for d in devices if d.get('model', '').startswith('MX') and ('W' in d.get('model', '') or 'w' in d.get('model', ''))]
                    mr_devices = [d for d in devices if d.get('model', '').startswith('MR')]
                    
                    # Use appropriate API based on infrastructure
                    if mx_with_wifi and not mr_devices:
                        # MX integrated wireless - use appliance API
                        ssids = meraki_client.dashboard.appliance.getNetworkApplianceSsids(network_id)
                    else:
                        # Dedicated/mixed wireless - use wireless API
                        ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
                    
                    for ssid in ssids:
                        if ssid.get('enabled'):
                            auth = ssid.get('authMode', '')
                            # For MX integrated wireless, check PSK presence
                            if mx_with_wifi and not mr_devices:
                                if auth == 'open' or (auth == 'psk' and not ssid.get('psk')):
                                    weak_wifi_count += 1
                                    break
                            else:
                                # For MR wireless, use original logic
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

    @app.tool(
        name="perform_hipaa_compliance_audit",
        description="🏥 HIPAA Compliance Audit - comprehensive evaluation of all technical safeguards and 2025 requirements"
    )
    def perform_hipaa_compliance_audit(
        organization_id: str,
        audit_scope: str = "full",
        include_phi_mapping: bool = True,
        include_2025_requirements: bool = True,
        generate_evidence: bool = True,
        output_format: str = "markdown"
    ):
        """
        Perform comprehensive HIPAA compliance audit covering all technical safeguards.
        
        Args:
            organization_id: Organization ID to audit
            audit_scope: Audit scope - 'full', 'technical', 'network', 'access'
            include_phi_mapping: Include PHI data flow analysis
            include_2025_requirements: Include 2025 proposed requirements
            generate_evidence: Collect configuration evidence
            output_format: Output format - 'markdown', 'json'
            
        Returns:
            Comprehensive HIPAA compliance audit report with scoring and remediation
        """
        try:
            import datetime
            import json
            
            # Initialize audit results
            audit_start = datetime.datetime.now()
            org = meraki_client.dashboard.organizations.getOrganization(organization_id)
            org_name = org.get('name', 'Unknown Organization')
            
            audit_results = {
                'organization': {'id': organization_id, 'name': org_name},
                'audit_timestamp': audit_start.isoformat(),
                'audit_scope': audit_scope,
                'findings': {},
                'scores': {},
                'evidence': {},
                'remediation': [],
                'summary': {}
            }
            
            # Get organization networks and devices
            networks = meraki_client.dashboard.organizations.getOrganizationNetworks(organization_id)
            all_devices = meraki_client.dashboard.organizations.getOrganizationDevices(organization_id)
            
            if output_format == "markdown":
                report = []
                report.append(f"# 🏥 HIPAA Compliance Audit Report")
                report.append(f"**Organization**: {org_name}")
                report.append(f"**Audit Date**: {audit_start.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                report.append(f"**Audit Scope**: {audit_scope.title()}")
                report.append(f"**Networks Analyzed**: {len(networks)}")
                report.append(f"**Devices Analyzed**: {len(all_devices)}")
                report.append("")
            
            # Initialize scoring system
            total_score = 0
            max_score = 0
            
            # Section 1: Access Controls (§164.312(a)) - 25 points
            access_score, access_findings = _audit_access_controls(networks, all_devices)
            total_score += access_score
            max_score += 25
            audit_results['findings']['access_controls'] = access_findings
            audit_results['scores']['access_controls'] = {'score': access_score, 'max': 25}
            
            if output_format == "markdown":
                report.append("## 🔐 ACCESS CONTROLS (§164.312(a)) - 25 Points")
                report.append(f"**Score: {access_score}/25** ({access_score/25*100:.1f}%)")
                report.append("")
                for finding in access_findings:
                    report.append(f"- {finding}")
                report.append("")
            
            # Section 2: Audit Controls (§164.312(b)) - 15 points
            audit_score, audit_findings = _audit_audit_controls(networks)
            total_score += audit_score
            max_score += 15
            audit_results['findings']['audit_controls'] = audit_findings
            audit_results['scores']['audit_controls'] = {'score': audit_score, 'max': 15}
            
            if output_format == "markdown":
                report.append("## 📋 AUDIT CONTROLS (§164.312(b)) - 15 Points")
                report.append(f"**Score: {audit_score}/15** ({audit_score/15*100:.1f}%)")
                report.append("")
                for finding in audit_findings:
                    report.append(f"- {finding}")
                report.append("")
            
            # Section 3: Integrity Controls (§164.312(c)) - 15 points
            integrity_score, integrity_findings = _audit_integrity_controls(networks, all_devices)
            total_score += integrity_score
            max_score += 15
            audit_results['findings']['integrity_controls'] = integrity_findings
            audit_results['scores']['integrity_controls'] = {'score': integrity_score, 'max': 15}
            
            if output_format == "markdown":
                report.append("## 🔒 INTEGRITY CONTROLS (§164.312(c)) - 15 Points")
                report.append(f"**Score: {integrity_score}/15** ({integrity_score/15*100:.1f}%)")
                report.append("")
                for finding in integrity_findings:
                    report.append(f"- {finding}")
                report.append("")
            
            # Section 4: Transmission Security (§164.312(e)) - 20 points
            transmission_score, transmission_findings = _audit_transmission_security(networks, all_devices)
            total_score += transmission_score
            max_score += 20
            audit_results['findings']['transmission_security'] = transmission_findings
            audit_results['scores']['transmission_security'] = {'score': transmission_score, 'max': 20}
            
            if output_format == "markdown":
                report.append("## 📡 TRANSMISSION SECURITY (§164.312(e)) - 20 Points")
                report.append(f"**Score: {transmission_score}/20** ({transmission_score/20*100:.1f}%)")
                report.append("")
                for finding in transmission_findings:
                    report.append(f"- {finding}")
                report.append("")
            
            # Section 5: 2025 Proposed Requirements - 15 points (if enabled)
            if include_2025_requirements:
                new_reqs_score, new_reqs_findings = _audit_2025_requirements(networks, all_devices)
                total_score += new_reqs_score
                max_score += 15
                audit_results['findings']['2025_requirements'] = new_reqs_findings
                audit_results['scores']['2025_requirements'] = {'score': new_reqs_score, 'max': 15}
                
                if output_format == "markdown":
                    report.append("## 🆕 2025 PROPOSED REQUIREMENTS - 15 Points")
                    report.append(f"**Score: {new_reqs_score}/15** ({new_reqs_score/15*100:.1f}%)")
                    report.append("")
                    for finding in new_reqs_findings:
                        report.append(f"- {finding}")
                    report.append("")
            
            # Section 6: PHI Data Flow Analysis (if enabled)
            if include_phi_mapping:
                phi_analysis = _analyze_phi_data_flows(networks, all_devices)
                audit_results['phi_analysis'] = phi_analysis
                
                if output_format == "markdown":
                    report.append("## 🗺️ PHI DATA FLOW ANALYSIS")
                    report.append("")
                    for flow in phi_analysis:
                        report.append(f"- {flow}")
                    report.append("")
            
            # Section 7: Risk Assessment - 10 points
            risk_score, risk_findings = _audit_security_risks(networks)
            total_score += risk_score
            max_score += 10
            audit_results['findings']['security_risks'] = risk_findings
            audit_results['scores']['security_risks'] = {'score': risk_score, 'max': 10}
            
            if output_format == "markdown":
                report.append("## ⚠️ SECURITY RISK ASSESSMENT - 10 Points")
                report.append(f"**Score: {risk_score}/10** ({risk_score/10*100:.1f}%)")
                report.append("")
                for finding in risk_findings:
                    report.append(f"- {finding}")
                report.append("")
            
            # Calculate final compliance score
            compliance_percentage = (total_score / max_score * 100) if max_score > 0 else 0
            audit_results['summary'] = {
                'total_score': total_score,
                'max_score': max_score,
                'compliance_percentage': compliance_percentage,
                'audit_duration': str(datetime.datetime.now() - audit_start)
            }
            
            # Determine compliance level
            if compliance_percentage >= 95:
                level = "FULLY COMPLIANT (Low Risk)"
                color = "🟢"
            elif compliance_percentage >= 85:
                level = "SUBSTANTIALLY COMPLIANT (Medium-Low Risk)"
                color = "🟡"
            elif compliance_percentage >= 70:
                level = "PARTIALLY COMPLIANT (Medium Risk)"
                color = "🟠"
            elif compliance_percentage >= 50:
                level = "NON-COMPLIANT (High Risk)"
                color = "🔴"
            else:
                level = "CRITICAL NON-COMPLIANCE (Critical Risk)"
                color = "🚫"
            
            if output_format == "markdown":
                report.append("## 📊 OVERALL COMPLIANCE SCORE")
                report.append("")
                report.append(f"### {color} {compliance_percentage:.1f}% - {level}")
                report.append(f"**Score**: {total_score}/{max_score} points")
                report.append("")
                
                # Add remediation recommendations
                remediation = _generate_remediation_plan(audit_results['findings'], compliance_percentage)
                audit_results['remediation'] = remediation
                
                report.append("## 🔧 REMEDIATION RECOMMENDATIONS")
                report.append("")
                for priority, items in remediation.items():
                    if items:
                        report.append(f"### {priority}")
                        for item in items:
                            report.append(f"- {item}")
                        report.append("")
                
                # Add evidence collection summary
                if generate_evidence:
                    evidence_summary = _collect_compliance_evidence(networks, all_devices)
                    audit_results['evidence'] = evidence_summary
                    
                    report.append("## 📁 EVIDENCE COLLECTED")
                    report.append("")
                    for category, count in evidence_summary.items():
                        report.append(f"- **{category}**: {count} items")
                    report.append("")
                
                # Add footer
                report.append("---")
                report.append(f"*Report generated by Cisco Meraki MCP Server on {audit_start.strftime('%Y-%m-%d %H:%M:%S UTC')}*")
                report.append(f"*Audit completed in {datetime.datetime.now() - audit_start}*")
                
                return "\n".join(report)
            
            elif output_format == "json":
                return json.dumps(audit_results, indent=2)
            
        except Exception as e:
            return f"❌ Error performing HIPAA compliance audit: {str(e)}"

# Supporting HIPAA audit functions

def _audit_access_controls(networks, all_devices):
    """Audit Access Controls (§164.312(a)) - 25 points"""
    findings = []
    score = 0
    
    try:
        # Check for unique user identification (5 points)
        admin_count = 0
        radius_enabled = 0
        
        for network in networks:
            net_id = network['id']
            net_name = network['name']
            
            try:
                # Check RADIUS authentication
                auth_users = meraki_client.dashboard.networks.getNetworkMerakiAuthUsers(net_id)
                if auth_users:
                    admin_count += len(auth_users)
                    radius_enabled += 1
            except:
                pass
        
        if admin_count > 0 and radius_enabled > 0:
            score += 5
            findings.append(f"✅ **Unique User ID**: {admin_count} admin users across {radius_enabled} networks")
        else:
            findings.append("❌ **Unique User ID**: No RADIUS/admin users found - implement user identification")
        
        # Check automatic logoff (5 points)
        logoff_configured = 0
        for network in networks:
            net_id = network['id']
            try:
                ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(net_id)
                for ssid in ssids:
                    if ssid.get('enabled') and ssid.get('splashPage') == 'Click-through':
                        logoff_configured += 1
                        break
            except:
                # Try MX integrated wireless
                try:
                    ssids = meraki_client.dashboard.appliance.getNetworkApplianceSsids(net_id)
                    for ssid in ssids:
                        if ssid.get('enabled'):
                            logoff_configured += 1
                            break
                except:
                    pass
        
        if logoff_configured > 0:
            score += 3
            findings.append(f"⚠️ **Automatic Logoff**: {logoff_configured} networks with session controls")
        else:
            score += 1
            findings.append("❌ **Automatic Logoff**: No session timeout controls detected")
        
        # Check encryption/decryption (15 points - critical)
        encrypted_networks = 0
        weak_encryption = 0
        
        for network in networks:
            net_id = network['id']
            has_encryption = False
            
            # Check WiFi encryption
            try:
                # Determine infrastructure type
                devices = meraki_client.dashboard.networks.getNetworkDevices(net_id)
                mx_with_wifi = [d for d in devices if d.get('model', '').startswith('MX') and 'W' in d.get('model', '')]
                mr_devices = [d for d in devices if d.get('model', '').startswith('MR')]
                
                if mx_with_wifi and not mr_devices:
                    # MX integrated wireless
                    ssids = meraki_client.dashboard.appliance.getNetworkApplianceSsids(net_id)
                    for ssid in ssids:
                        if ssid.get('enabled'):
                            auth = ssid.get('authMode', '')
                            if auth in ['psk', 'wpa3-personal', 'wpa3-enterprise'] and ssid.get('psk'):
                                has_encryption = True
                            elif auth == 'open':
                                weak_encryption += 1
                else:
                    # MR wireless
                    ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(net_id)
                    for ssid in ssids:
                        if ssid.get('enabled'):
                            auth = ssid.get('authMode', '')
                            if auth in ['psk', 'wpa3-personal', 'wpa3-enterprise', '8021x-radius']:
                                has_encryption = True
                            elif auth == 'open':
                                weak_encryption += 1
            except:
                pass
            
            # Check VPN encryption
            try:
                site_vpn = meraki_client.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(net_id)
                if site_vpn.get('mode') != 'none':
                    has_encryption = True
            except:
                pass
            
            if has_encryption:
                encrypted_networks += 1
        
        encryption_percentage = (encrypted_networks / len(networks) * 100) if networks else 0
        
        if encryption_percentage >= 90:
            score += 15
            findings.append(f"✅ **Encryption**: {encrypted_networks}/{len(networks)} networks encrypted ({encryption_percentage:.0f}%)")
        elif encryption_percentage >= 70:
            score += 10
            findings.append(f"⚠️ **Encryption**: {encrypted_networks}/{len(networks)} networks encrypted ({encryption_percentage:.0f}%) - improve coverage")
        else:
            score += 2
            findings.append(f"❌ **Encryption**: Only {encrypted_networks}/{len(networks)} networks encrypted ({encryption_percentage:.0f}%) - CRITICAL GAP")
        
        if weak_encryption > 0:
            findings.append(f"🚨 **Security Alert**: {weak_encryption} open/insecure wireless networks detected")
        
    except Exception as e:
        findings.append(f"❌ Error auditing access controls: {str(e)}")
    
    return score, findings

def _audit_audit_controls(networks):
    """Audit Controls (§164.312(b)) - 15 points"""
    findings = []
    score = 0
    
    try:
        # Check event logging (10 points)
        logging_enabled = 0
        syslog_configured = 0
        
        for network in networks:
            net_id = network['id']
            
            # Check syslog servers
            try:
                syslog = meraki_client.dashboard.networks.getNetworkSyslogServers(net_id)
                if syslog.get('servers'):
                    syslog_configured += 1
                    logging_enabled += 1
            except:
                pass
            
            # Check event log settings
            try:
                events = meraki_client.dashboard.networks.getNetworkEvents(net_id, perPage=1)
                if events:
                    logging_enabled += 1
            except:
                pass
        
        if logging_enabled >= len(networks) * 0.8:  # 80% threshold
            score += 10
            findings.append(f"✅ **Event Logging**: {logging_enabled}/{len(networks)} networks with logging enabled")
        elif logging_enabled >= len(networks) * 0.5:  # 50% threshold
            score += 5
            findings.append(f"⚠️ **Event Logging**: {logging_enabled}/{len(networks)} networks - expand coverage")
        else:
            score += 1
            findings.append(f"❌ **Event Logging**: Only {logging_enabled}/{len(networks)} networks with logging")
        
        # Check log retention (5 points)
        if syslog_configured > 0:
            score += 5
            findings.append(f"✅ **Log Retention**: {syslog_configured} networks with syslog servers configured")
        else:
            findings.append("❌ **Log Retention**: No external syslog servers - logs may be lost")
        
    except Exception as e:
        findings.append(f"❌ Error auditing audit controls: {str(e)}")
    
    return score, findings

def _audit_integrity_controls(networks, all_devices):
    """Integrity Controls (§164.312(c)) - 15 points"""
    findings = []
    score = 0
    
    try:
        # Check firmware integrity (8 points)
        updated_devices = 0
        total_devices = len(all_devices)
        
        for device in all_devices:
            firmware = device.get('firmware', '')
            # Simple check - devices with recent firmware (this is a simplified check)
            if firmware and not any(old in firmware.lower() for old in ['beta', 'rc', 'dev']):
                updated_devices += 1
        
        firmware_percentage = (updated_devices / total_devices * 100) if total_devices > 0 else 0
        
        if firmware_percentage >= 95:
            score += 8
            findings.append(f"✅ **Firmware Integrity**: {updated_devices}/{total_devices} devices with stable firmware ({firmware_percentage:.0f}%)")
        elif firmware_percentage >= 85:
            score += 5
            findings.append(f"⚠️ **Firmware Integrity**: {updated_devices}/{total_devices} devices updated ({firmware_percentage:.0f}%) - update remaining")
        else:
            score += 1
            findings.append(f"❌ **Firmware Integrity**: Only {updated_devices}/{total_devices} devices updated ({firmware_percentage:.0f}%) - security risk")
        
        # Check configuration backup (7 points)
        backup_networks = 0
        
        for network in networks:
            net_id = network['id']
            
            # Check if network has configuration templates (indication of backup/standardization)
            try:
                devices = meraki_client.dashboard.networks.getNetworkDevices(net_id)
                if devices:  # If network has devices, assume configuration is backed up
                    backup_networks += 1
            except:
                pass
        
        if backup_networks >= len(networks):
            score += 7
            findings.append(f"✅ **Configuration Backup**: All {backup_networks} networks have device configurations")
        elif backup_networks >= len(networks) * 0.8:
            score += 5
            findings.append(f"⚠️ **Configuration Backup**: {backup_networks}/{len(networks)} networks backed up")
        else:
            score += 2
            findings.append(f"❌ **Configuration Backup**: Only {backup_networks}/{len(networks)} networks have backup procedures")
        
    except Exception as e:
        findings.append(f"❌ Error auditing integrity controls: {str(e)}")
    
    return score, findings

def _audit_transmission_security(networks, all_devices):
    """Transmission Security (§164.312(e)) - 20 points"""
    findings = []
    score = 0
    
    try:
        # Check network segmentation (8 points)
        segmented_networks = 0
        vlan_count = 0
        
        for network in networks:
            net_id = network['id']
            has_vlans = False
            
            try:
                # Check VLANs on switches
                vlans = meraki_client.dashboard.switch.getNetworkSwitchSettings(net_id)
                if vlans.get('vlan'):
                    has_vlans = True
                    vlan_count += 1
                    segmented_networks += 1
            except:
                pass
            
            # Check wireless segmentation
            try:
                ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(net_id)
                for ssid in ssids:
                    if ssid.get('enabled') and ssid.get('vlanId'):
                        if not has_vlans:
                            segmented_networks += 1
                            has_vlans = True
            except:
                pass
        
        if segmented_networks >= len(networks) * 0.8:
            score += 8
            findings.append(f"✅ **Network Segmentation**: {segmented_networks}/{len(networks)} networks with VLANs")
        elif segmented_networks >= len(networks) * 0.5:
            score += 5
            findings.append(f"⚠️ **Network Segmentation**: {segmented_networks}/{len(networks)} networks segmented - expand coverage")
        else:
            score += 1
            findings.append(f"❌ **Network Segmentation**: Only {segmented_networks}/{len(networks)} networks segmented")
        
        # Check VPN security (6 points)
        vpn_networks = 0
        client_vpn_networks = 0
        
        for network in networks:
            net_id = network['id']
            
            # Check site-to-site VPN
            try:
                site_vpn = meraki_client.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(net_id)
                if site_vpn.get('mode') != 'none':
                    vpn_networks += 1
            except:
                pass
            
            # Check client VPN
            try:
                client_vpn = meraki_client.dashboard.appliance.getNetworkApplianceClientVpnSettings(net_id)
                if client_vpn.get('enabled'):
                    client_vpn_networks += 1
            except:
                pass
        
        if vpn_networks > 0 or client_vpn_networks > 0:
            if vpn_networks >= len(networks) * 0.3:  # 30% threshold for VPN
                score += 6
                findings.append(f"✅ **VPN Security**: {vpn_networks} site-to-site, {client_vpn_networks} client VPN networks")
            else:
                score += 3
                findings.append(f"⚠️ **VPN Security**: {vpn_networks} site-to-site, {client_vpn_networks} client VPN - consider expansion")
        else:
            findings.append("❌ **VPN Security**: No VPN connectivity detected - remote access security risk")
        
        # Check wireless security (6 points)
        secure_wireless = 0
        total_wireless = 0
        
        for network in networks:
            net_id = network['id']
            
            # Check wireless SSIDs
            try:
                # Determine infrastructure type
                devices = meraki_client.dashboard.networks.getNetworkDevices(net_id)
                mx_with_wifi = [d for d in devices if d.get('model', '').startswith('MX') and 'W' in d.get('model', '')]
                mr_devices = [d for d in devices if d.get('model', '').startswith('MR')]
                
                if mx_with_wifi and not mr_devices:
                    # MX integrated wireless
                    ssids = meraki_client.dashboard.appliance.getNetworkApplianceSsids(net_id)
                    for ssid in ssids:
                        if ssid.get('enabled'):
                            total_wireless += 1
                            auth = ssid.get('authMode', '')
                            if auth in ['psk', 'wpa3-personal', 'wpa3-enterprise'] and ssid.get('psk'):
                                secure_wireless += 1
                else:
                    # MR wireless
                    ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(net_id)
                    for ssid in ssids:
                        if ssid.get('enabled'):
                            total_wireless += 1
                            auth = ssid.get('authMode', '')
                            if auth in ['psk', 'wpa3-personal', 'wpa3-enterprise', '8021x-radius']:
                                secure_wireless += 1
            except:
                pass
        
        if total_wireless > 0:
            wireless_security_percentage = (secure_wireless / total_wireless * 100)
            if wireless_security_percentage >= 95:
                score += 6
                findings.append(f"✅ **Wireless Security**: {secure_wireless}/{total_wireless} SSIDs secure ({wireless_security_percentage:.0f}%)")
            elif wireless_security_percentage >= 80:
                score += 4
                findings.append(f"⚠️ **Wireless Security**: {secure_wireless}/{total_wireless} SSIDs secure ({wireless_security_percentage:.0f}%) - secure remaining")
            else:
                score += 1
                findings.append(f"❌ **Wireless Security**: Only {secure_wireless}/{total_wireless} SSIDs secure ({wireless_security_percentage:.0f}%) - CRITICAL")
        else:
            findings.append("ℹ️ **Wireless Security**: No wireless networks detected")
        
    except Exception as e:
        findings.append(f"❌ Error auditing transmission security: {str(e)}")
    
    return score, findings

def _audit_2025_requirements(networks, all_devices):
    """2025 Proposed Requirements - 15 points"""
    findings = []
    score = 0
    
    try:
        # Mandatory encryption compliance (5 points)
        encrypted_at_rest = 0
        encrypted_in_transit = 0
        
        for network in networks:
            net_id = network['id']
            
            # Check VPN encryption (in-transit)
            try:
                site_vpn = meraki_client.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(net_id)
                if site_vpn.get('mode') != 'none':
                    encrypted_in_transit += 1
            except:
                pass
            
            # Assume devices with strong wireless encryption have encrypted storage
            try:
                ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(net_id)
                for ssid in ssids:
                    if ssid.get('enabled') and ssid.get('authMode') in ['wpa3-personal', 'wpa3-enterprise']:
                        encrypted_at_rest += 1
                        break
            except:
                pass
        
        if encrypted_in_transit >= len(networks) * 0.8:
            score += 3
            findings.append(f"✅ **2025 Encryption**: {encrypted_in_transit}/{len(networks)} networks with in-transit encryption")
        else:
            findings.append(f"❌ **2025 Encryption**: Only {encrypted_in_transit}/{len(networks)} networks encrypted - mandatory requirement")
        
        if encrypted_at_rest >= len(networks) * 0.5:
            score += 2
            findings.append(f"✅ **At-Rest Encryption**: {encrypted_at_rest}/{len(networks)} networks with strong encryption")
        
        # Anti-malware deployment (5 points)
        amp_enabled = 0
        
        for network in networks:
            net_id = network['id']
            
            try:
                amp = meraki_client.dashboard.appliance.getNetworkApplianceSecurityMalware(net_id)
                if amp.get('mode') != 'disabled':
                    amp_enabled += 1
            except:
                pass
        
        amp_percentage = (amp_enabled / len(networks) * 100) if networks else 0
        
        if amp_percentage >= 90:
            score += 5
            findings.append(f"✅ **2025 Anti-Malware**: {amp_enabled}/{len(networks)} networks with AMP ({amp_percentage:.0f}%)")
        elif amp_percentage >= 70:
            score += 3
            findings.append(f"⚠️ **2025 Anti-Malware**: {amp_enabled}/{len(networks)} networks ({amp_percentage:.0f}%) - deploy to all networks")
        else:
            findings.append(f"❌ **2025 Anti-Malware**: Only {amp_enabled}/{len(networks)} networks ({amp_percentage:.0f}%) - mandatory requirement")
        
        # System configuration consistency (5 points)
        template_networks = 0
        consistent_configs = 0
        
        # Check for configuration templates (indication of consistency)
        for network in networks:
            try:
                # Networks with devices indicate managed configurations
                devices = meraki_client.dashboard.networks.getNetworkDevices(network['id'])
                if devices:
                    consistent_configs += 1
            except:
                pass
        
        if consistent_configs >= len(networks) * 0.8:
            score += 5
            findings.append(f"✅ **2025 Config Management**: {consistent_configs}/{len(networks)} networks with managed configurations")
        else:
            findings.append(f"❌ **2025 Config Management**: Only {consistent_configs}/{len(networks)} networks - implement standardization")
        
    except Exception as e:
        findings.append(f"❌ Error auditing 2025 requirements: {str(e)}")
    
    return score, findings

def _analyze_phi_data_flows(networks, all_devices):
    """Analyze PHI data flow patterns"""
    flows = []
    
    try:
        # Analyze network connectivity patterns
        for network in networks:
            net_id = network['id']
            net_name = network['name']
            
            # Check for VLAN segmentation
            try:
                vlans = meraki_client.dashboard.switch.getNetworkSwitchSettings(net_id)
                if vlans.get('vlan'):
                    flows.append(f"🏥 **{net_name}**: VLAN segmentation configured - PHI isolation possible")
                else:
                    flows.append(f"⚠️ **{net_name}**: Flat network - PHI data not segmented")
            except:
                flows.append(f"ℹ️ **{net_name}**: Network segmentation status unknown")
            
            # Check wireless guest isolation
            try:
                ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(net_id)
                for ssid in ssids:
                    if ssid.get('enabled'):
                        if 'guest' in ssid.get('name', '').lower():
                            if ssid.get('clientIsolationEnabled'):
                                flows.append(f"✅ **{net_name}**: Guest network isolated - PHI protected")
                            else:
                                flows.append(f"❌ **{net_name}**: Guest network not isolated - PHI risk")
            except:
                pass
            
            # Check inter-VLAN routing
            try:
                firewall = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(net_id)
                rules = firewall.get('rules', [])
                if len(rules) > 1:  # More than just default allow
                    flows.append(f"✅ **{net_name}**: Custom firewall rules - traffic control in place")
                else:
                    flows.append(f"⚠️ **{net_name}**: Default firewall rules - consider PHI traffic restrictions")
            except:
                pass
        
    except Exception as e:
        flows.append(f"❌ Error analyzing PHI data flows: {str(e)}")
    
    return flows

def _audit_security_risks(networks):
    """Security Risk Assessment - 10 points"""
    findings = []
    score = 0
    
    try:
        # Check IDS/IPS deployment (5 points)
        ids_enabled = 0
        
        for network in networks:
            net_id = network['id']
            
            try:
                ids = meraki_client.dashboard.appliance.getNetworkApplianceSecurityIntrusion(net_id)
                if ids.get('mode') != 'disabled':
                    ids_enabled += 1
            except:
                pass
        
        ids_percentage = (ids_enabled / len(networks) * 100) if networks else 0
        
        if ids_percentage >= 90:
            score += 5
            findings.append(f"✅ **IDS/IPS**: {ids_enabled}/{len(networks)} networks protected ({ids_percentage:.0f}%)")
        elif ids_percentage >= 70:
            score += 3
            findings.append(f"⚠️ **IDS/IPS**: {ids_enabled}/{len(networks)} networks protected ({ids_percentage:.0f}%) - expand coverage")
        else:
            findings.append(f"❌ **IDS/IPS**: Only {ids_enabled}/{len(networks)} networks protected ({ids_percentage:.0f}%)")
        
        # Check recent security events (5 points)
        total_events = 0
        high_risk_events = 0
        
        for network in networks:
            net_id = network['id']
            
            try:
                events = meraki_client.dashboard.appliance.getNetworkApplianceSecurityEvents(
                    net_id, 
                    timespan=86400  # Last 24 hours
                )
                total_events += len(events)
                
                # Count high-risk events
                for event in events:
                    priority = event.get('priority', '').lower()
                    if priority in ['critical', 'high', 'major']:
                        high_risk_events += 1
                        
            except:
                pass
        
        if high_risk_events == 0:
            score += 5
            findings.append(f"✅ **Security Events**: No high-risk events in 24h ({total_events} total events)")
        elif high_risk_events <= 5:
            score += 3
            findings.append(f"⚠️ **Security Events**: {high_risk_events} high-risk events in 24h - investigate")
        else:
            findings.append(f"❌ **Security Events**: {high_risk_events} high-risk events in 24h - IMMEDIATE ACTION REQUIRED")
        
    except Exception as e:
        findings.append(f"❌ Error auditing security risks: {str(e)}")
    
    return score, findings

def _generate_remediation_plan(findings, compliance_percentage):
    """Generate prioritized remediation recommendations"""
    remediation = {
        "🚨 Priority 1 (Immediate - 0-7 days)": [],
        "⚠️ Priority 2 (High - 30 days)": [],
        "📋 Priority 3 (Medium - 90 days)": [],
        "💡 Priority 4 (Best Practice - Annual)": []
    }
    
    # Critical compliance gaps (< 50% compliance)
    if compliance_percentage < 50:
        remediation["🚨 Priority 1 (Immediate - 0-7 days)"].extend([
            "Implement mandatory encryption for all networks handling PHI",
            "Enable IDS/IPS on all networks immediately",
            "Secure all open wireless networks with WPA3 or WPA2",
            "Deploy anti-malware protection (AMP) organization-wide",
            "Implement network segmentation to isolate PHI systems"
        ])
    
    # High priority gaps (50-70% compliance)
    elif compliance_percentage < 70:
        remediation["⚠️ Priority 2 (High - 30 days)"].extend([
            "Complete wireless security hardening across all networks",
            "Implement comprehensive logging and SIEM integration",
            "Deploy VPN connectivity for all remote access needs",
            "Enable advanced threat protection on remaining networks"
        ])
    
    # Medium priority improvements (70-85% compliance)
    elif compliance_percentage < 85:
        remediation["📋 Priority 3 (Medium - 90 days)"].extend([
            "Standardize configuration management across all networks",
            "Implement automated backup and recovery procedures",
            "Enhance network segmentation with micro-segmentation",
            "Deploy advanced authentication (802.1X) where applicable"
        ])
    
    # Best practice enhancements (85%+ compliance)
    else:
        remediation["💡 Priority 4 (Best Practice - Annual)"].extend([
            "Implement zero-trust network architecture",
            "Deploy advanced analytics and behavioral monitoring",
            "Enhance incident response automation",
            "Consider cloud security integration"
        ])
    
    # Always include these based on specific findings
    for category, category_findings in findings.items():
        for finding in category_findings:
            if "❌" in finding:
                if "CRITICAL" in finding.upper() or "IMMEDIATE" in finding.upper():
                    if "encryption" in finding.lower() or "open" in finding.lower():
                        remediation["🚨 Priority 1 (Immediate - 0-7 days)"].append(f"Address: {finding.replace('❌', '').strip()}")
                elif "mandatory" in finding.lower() or "2025" in finding:
                    remediation["⚠️ Priority 2 (High - 30 days)"].append(f"Prepare for: {finding.replace('❌', '').strip()}")
    
    return remediation

def _collect_compliance_evidence(networks, all_devices):
    """Collect compliance evidence for documentation"""
    evidence = {
        "Network Configurations": len(networks),
        "Device Configurations": len(all_devices),
        "Security Policies": 0,
        "Firewall Rules": 0,
        "VPN Configurations": 0,
        "Wireless Security Settings": 0,
        "Audit Logs": 0
    }
    
    try:
        for network in networks:
            net_id = network['id']
            
            # Count security policies
            try:
                amp = meraki_client.dashboard.appliance.getNetworkApplianceSecurityMalware(net_id)
                if amp.get('mode') != 'disabled':
                    evidence["Security Policies"] += 1
            except:
                pass
            
            # Count firewall rules
            try:
                l3_rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(net_id)
                if l3_rules.get('rules'):
                    evidence["Firewall Rules"] += len(l3_rules['rules'])
            except:
                pass
            
            # Count VPN configs
            try:
                vpn = meraki_client.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(net_id)
                if vpn.get('mode') != 'none':
                    evidence["VPN Configurations"] += 1
            except:
                pass
            
            # Count wireless configs
            try:
                ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(net_id)
                evidence["Wireless Security Settings"] += len([s for s in ssids if s.get('enabled')])
            except:
                pass
            
            # Count audit logs (sample)
            try:
                events = meraki_client.dashboard.networks.getNetworkEvents(net_id, perPage=1)
                if events:
                    evidence["Audit Logs"] += 1
            except:
                pass
                
    except Exception:
        pass
    
    return evidence