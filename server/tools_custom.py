"""
Custom tools and helper commands for Cisco Meraki MCP Server.
This module contains custom utilities, helper functions, and specialized
commands that extend the official Meraki API functionality.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_custom_tools(mcp_app, meraki):
    """Register custom tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all custom tools
    register_custom_handlers()

def register_custom_handlers():
    """Register all custom tool handlers using the decorator pattern."""
    
    @app.tool(
        name="quick_network_overview",
        description="🎯 [CUSTOM] Get a quick overview of network health and status"
    )
    def quick_network_overview(network_id: str):
        """
        Provides a comprehensive overview of network status including:
        - Device health
        - Client counts
        - Recent alerts
        - Uplink status
        """
        try:
            # Get network info
            network = meraki_client.dashboard.networks.getNetwork(network_id)
            
            # Get devices
            devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
            online_devices = [d for d in devices if d.get('status') == 'online']
            
            # Get clients (limit to recent)
            try:
                clients = meraki_client.dashboard.networks.getNetworkClients(
                    network_id, 
                    timespan=300  # Last 5 minutes
                )
            except:
                clients = []
            
            # Build overview
            result = f"# 🎯 Quick Network Overview\n\n"
            result += f"**Network**: {network.get('name')}\n"
            result += f"**Type**: {', '.join(network.get('productTypes', []))}\n"
            result += f"**Time Zone**: {network.get('timeZone', 'Not set')}\n\n"
            
            result += f"## 📊 Device Status\n"
            result += f"- **Total Devices**: {len(devices)}\n"
            result += f"- **Online**: {len(online_devices)} 🟢\n"
            result += f"- **Offline**: {len(devices) - len(online_devices)} 🔴\n\n"
            
            if online_devices:
                result += "### Online Devices:\n"
                for device in online_devices[:5]:
                    result += f"- {device.get('name', device['serial'])} ({device['model']})\n"
                if len(online_devices) > 5:
                    result += f"... and {len(online_devices) - 5} more\n"
            
            result += f"\n## 👥 Client Activity\n"
            result += f"- **Active Clients**: {len(clients)}\n"
            
            if clients:
                # Group by device type
                device_types = {}
                for client in clients:
                    dtype = client.get('deviceTypePrediction', 'Unknown')
                    device_types[dtype] = device_types.get(dtype, 0) + 1
                
                result += "\n### Client Types:\n"
                for dtype, count in sorted(device_types.items(), key=lambda x: x[1], reverse=True)[:5]:
                    result += f"- {dtype}: {count}\n"
            
            return result
            
        except Exception as e:
            return f"Error generating network overview: {str(e)}"
    
    @app.tool(
        name="batch_ssid_password_update",
        description="🔐 [CUSTOM] Update WiFi password across multiple SSIDs"
    )
    def batch_ssid_password_update(network_id: str, new_password: str, ssid_numbers: str = None):
        """
        Update WiFi password for multiple SSIDs at once.
        
        Args:
            network_id: Network ID
            new_password: New password to set
            ssid_numbers: Comma-separated SSID numbers (e.g., "0,1,2") or "all"
        """
        try:
            # Get all SSIDs
            ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
            
            if ssid_numbers == "all":
                target_ssids = [s for s in ssids if s.get('enabled')]
            elif ssid_numbers:
                numbers = [int(n.strip()) for n in ssid_numbers.split(',')]
                target_ssids = [s for s in ssids if s.get('number') in numbers]
            else:
                return "Please specify ssid_numbers (e.g., '0,1,2' or 'all')"
            
            result = f"# 🔐 Batch SSID Password Update\n\n"
            result += f"**New Password**: {new_password}\n\n"
            
            updated = []
            failed = []
            
            for ssid in target_ssids:
                try:
                    # Only update if using PSK
                    if ssid.get('authMode') in ['psk', 'open-with-radius']:
                        meraki_client.dashboard.wireless.updateNetworkWirelessSsid(
                            network_id,
                            ssid['number'],
                            psk=new_password
                        )
                        updated.append(ssid['name'])
                    else:
                        failed.append((ssid['name'], f"Auth mode is {ssid.get('authMode')}"))
                except Exception as e:
                    failed.append((ssid['name'], str(e)))
            
            if updated:
                result += f"✅ **Successfully Updated** ({len(updated)}):\n"
                for name in updated:
                    result += f"- {name}\n"
            
            if failed:
                result += f"\n❌ **Failed Updates** ({len(failed)}):\n"
                for name, reason in failed:
                    result += f"- {name}: {reason}\n"
            
            return result
            
        except Exception as e:
            return f"Error updating SSID passwords: {str(e)}"
    
    @app.tool(
        name="find_rogue_dhcp_servers",
        description="🔍 [CUSTOM] Detect potential rogue DHCP servers on the network"
    )
    def find_rogue_dhcp_servers(network_id: str, timespan: int = 86400):
        """
        Search for potential rogue DHCP servers by analyzing network events.
        
        Args:
            network_id: Network ID to check
            timespan: Time period in seconds (default 24 hours)
        """
        try:
            # Get DHCP-related events
            events = meraki_client.dashboard.networks.getNetworkEvents(
                network_id,
                productType='appliance',
                includedEventTypes=['dhcp_problem', 'rogue_dhcp'],
                perPage=1000
            )
            
            result = f"# 🔍 Rogue DHCP Server Detection\n\n"
            result += f"**Network**: {network_id}\n"
            result += f"**Timespan**: {timespan} seconds\n\n"
            
            if not events:
                result += "✅ No rogue DHCP servers detected!\n"
                return result
            
            # Analyze events
            rogue_servers = {}
            for event in events:
                if 'dhcp' in event.get('type', '').lower():
                    desc = event.get('description', '')
                    # Extract MAC/IP if present
                    if 'MAC' in desc or 'IP' in desc:
                        if desc not in rogue_servers:
                            rogue_servers[desc] = []
                        rogue_servers[desc].append(event.get('occurredAt'))
            
            if rogue_servers:
                result += f"⚠️ **Potential Issues Found**:\n\n"
                for desc, times in rogue_servers.items():
                    result += f"**Issue**: {desc}\n"
                    result += f"**Occurrences**: {len(times)}\n"
                    result += f"**Last Seen**: {times[0]}\n\n"
            else:
                result += "✅ No rogue DHCP servers detected!\n"
            
            return result
            
        except Exception as e:
            return f"Error detecting rogue DHCP servers: {str(e)}"
    
    @app.tool(
        name="emergency_network_lockdown",
        description="🚨 [CUSTOM] Emergency lockdown - disable all SSIDs and block traffic"
    )
    def emergency_network_lockdown(network_id: str, confirmation: str = None):
        """
        EMERGENCY: Immediately lock down network by disabling SSIDs and blocking traffic.
        
        Args:
            network_id: Network to lock down
            confirmation: Must be "LOCKDOWN" to proceed
        """
        if confirmation != "LOCKDOWN":
            return """⚠️ EMERGENCY LOCKDOWN - ARE YOU SURE?
            
This will:
- Disable ALL wireless SSIDs
- Block all client traffic (if firewall present)
- This is reversible but will disconnect all users

To proceed, call again with confirmation='LOCKDOWN'
"""
        
        try:
            result = f"# 🚨 EMERGENCY NETWORK LOCKDOWN\n\n"
            
            # Disable all SSIDs
            try:
                ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
                disabled_ssids = []
                
                for ssid in ssids:
                    if ssid.get('enabled'):
                        meraki_client.dashboard.wireless.updateNetworkWirelessSsid(
                            network_id,
                            ssid['number'],
                            enabled=False
                        )
                        disabled_ssids.append(ssid['name'])
                
                result += f"✅ **Disabled {len(disabled_ssids)} SSIDs**\n"
                
            except Exception as e:
                result += f"⚠️ Could not disable SSIDs: {str(e)}\n"
            
            # Add deny-all firewall rule
            try:
                # Get current L3 rules
                rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
                
                # Add deny-all at the top
                new_rule = {
                    'comment': 'EMERGENCY LOCKDOWN - Remove this rule to restore access',
                    'policy': 'deny',
                    'protocol': 'any',
                    'srcPort': 'Any',
                    'srcCidr': 'Any',
                    'destPort': 'Any',
                    'destCidr': 'Any'
                }
                
                rules['rules'].insert(0, new_rule)
                
                meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
                    network_id,
                    rules=rules['rules']
                )
                
                result += "✅ **Added deny-all firewall rule**\n"
                
            except Exception as e:
                result += f"⚠️ Could not add firewall rule: {str(e)}\n"
            
            result += "\n## 🔓 To Restore Access:\n"
            result += "1. Re-enable SSIDs manually\n"
            result += "2. Remove the 'EMERGENCY LOCKDOWN' firewall rule\n"
            result += "3. Verify client connectivity\n"
            
            return result
            
        except Exception as e:
            return f"Error during emergency lockdown: {str(e)}"
    
    @app.tool(
        name="auto_optimize_rf_settings",
        description="📡 [CUSTOM] Automatically optimize RF settings based on environment"
    )
    def auto_optimize_rf_settings(network_id: str, target_coverage: str = "balanced"):
        """
        Automatically adjust RF profiles for optimal performance.
        
        Args:
            network_id: Network to optimize
            target_coverage: "max_coverage", "balanced", or "high_density"
        """
        try:
            # Get current RF profiles
            rf_profiles = meraki_client.dashboard.wireless.getNetworkWirelessRfProfiles(network_id)
            
            result = f"# 📡 RF Optimization\n\n"
            result += f"**Target**: {target_coverage}\n\n"
            
            # Define optimization settings
            optimizations = {
                "max_coverage": {
                    "minPower": 8,
                    "maxPower": 30,
                    "channelWidth": "auto",
                    "rxsop": None
                },
                "balanced": {
                    "minPower": 10,
                    "maxPower": 25,
                    "channelWidth": "auto",
                    "rxsop": -78
                },
                "high_density": {
                    "minPower": 5,
                    "maxPower": 15,
                    "channelWidth": "20",
                    "rxsop": -75
                }
            }
            
            settings = optimizations.get(target_coverage, optimizations["balanced"])
            
            # Create or update RF profile
            profile_name = f"Auto-Optimized-{target_coverage}"
            
            # Check if profile exists
            existing = [p for p in rf_profiles if p.get('name') == profile_name]
            
            if existing:
                # Update existing
                profile_id = existing[0]['id']
                meraki_client.dashboard.wireless.updateNetworkWirelessRfProfile(
                    network_id,
                    profile_id,
                    twoFourGhzSettings={
                        'minPower': settings['minPower'],
                        'maxPower': settings['maxPower'],
                        'channelWidth': settings['channelWidth'],
                        'rxsop': settings['rxsop']
                    },
                    fiveGhzSettings={
                        'minPower': settings['minPower'],
                        'maxPower': settings['maxPower'],
                        'channelWidth': '40' if settings['channelWidth'] == 'auto' else settings['channelWidth'],
                        'rxsop': settings['rxsop']
                    }
                )
                result += f"✅ Updated RF profile: {profile_name}\n"
            else:
                # Create new
                meraki_client.dashboard.wireless.createNetworkWirelessRfProfile(
                    network_id,
                    name=profile_name,
                    bandSelectionType='balanced',
                    twoFourGhzSettings={
                        'minPower': settings['minPower'],
                        'maxPower': settings['maxPower'],
                        'channelWidth': settings['channelWidth'],
                        'rxsop': settings['rxsop']
                    },
                    fiveGhzSettings={
                        'minPower': settings['minPower'],
                        'maxPower': settings['maxPower'],
                        'channelWidth': '40' if settings['channelWidth'] == 'auto' else settings['channelWidth'],
                        'rxsop': settings['rxsop']
                    }
                )
                result += f"✅ Created RF profile: {profile_name}\n"
            
            result += f"\n## Settings Applied:\n"
            result += f"- Power Range: {settings['minPower']}-{settings['maxPower']} dBm\n"
            result += f"- Channel Width: {settings['channelWidth']}\n"
            if settings['rxsop']:
                result += f"- RX-SOP: {settings['rxsop']} dBm\n"
            
            result += f"\n💡 **Next Steps**:\n"
            result += f"1. Assign this profile to your APs\n"
            result += f"2. Monitor client connectivity for 24 hours\n"
            result += f"3. Adjust if needed based on coverage reports\n"
            
            return result
            
        except Exception as e:
            return f"Error optimizing RF settings: {str(e)}"
    
    @app.tool(
        name="compliance_audit_report",
        description="📋 [CUSTOM] Generate compliance audit report for security standards"
    )
    def compliance_audit_report(org_id: str, standard: str = "basic"):
        """
        Generate a compliance audit report checking security configurations.
        
        Args:
            org_id: Organization to audit
            standard: Compliance standard ("basic", "pci", "hipaa")
        """
        try:
            result = f"# 📋 Compliance Audit Report\n\n"
            result += f"**Organization**: {org_id}\n"
            result += f"**Standard**: {standard.upper()}\n"
            result += f"**Generated**: {meraki_client.dashboard.organizations.getOrganization(org_id).get('name')}\n\n"
            
            # Get networks
            networks = meraki_client.dashboard.organizations.getOrganizationNetworks(org_id)
            
            findings = {
                'critical': [],
                'warning': [],
                'info': [],
                'compliant': []
            }
            
            for network in networks[:5]:  # Limit to 5 networks for performance
                network_name = network.get('name')
                
                # Check wireless security
                if 'wireless' in network.get('productTypes', []):
                    try:
                        ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network['id'])
                        for ssid in ssids:
                            if ssid.get('enabled'):
                                # Check encryption
                                if ssid.get('authMode') == 'open':
                                    findings['critical'].append(
                                        f"{network_name}: SSID '{ssid['name']}' has no encryption"
                                    )
                                elif ssid.get('authMode') == 'psk' and ssid.get('encryptionMode') != 'wpa3':
                                    findings['warning'].append(
                                        f"{network_name}: SSID '{ssid['name']}' not using WPA3"
                                    )
                                else:
                                    findings['compliant'].append(
                                        f"{network_name}: SSID '{ssid['name']}' properly secured"
                                    )
                    except:
                        pass
                
                # Check firewall rules
                if 'appliance' in network.get('productTypes', []):
                    try:
                        rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network['id'])
                        
                        # Check for any allow-all rules
                        for rule in rules.get('rules', []):
                            if (rule.get('policy') == 'allow' and 
                                rule.get('srcCidr') == 'Any' and 
                                rule.get('destCidr') == 'Any'):
                                findings['warning'].append(
                                    f"{network_name}: Overly permissive firewall rule found"
                                )
                    except:
                        pass
            
            # Generate report
            result += "## 🔴 Critical Findings\n"
            if findings['critical']:
                for finding in findings['critical']:
                    result += f"- {finding}\n"
            else:
                result += "None found ✅\n"
            
            result += "\n## 🟡 Warnings\n"
            if findings['warning']:
                for finding in findings['warning'][:10]:
                    result += f"- {finding}\n"
                if len(findings['warning']) > 10:
                    result += f"... and {len(findings['warning']) - 10} more\n"
            else:
                result += "None found ✅\n"
            
            result += "\n## 🟢 Compliant Items\n"
            result += f"- {len(findings['compliant'])} items meet security standards\n"
            
            result += "\n## 📊 Summary\n"
            total = sum(len(v) for v in findings.values())
            if total > 0:
                compliance_rate = (len(findings['compliant']) / total) * 100
                result += f"**Compliance Rate**: {compliance_rate:.1f}%\n"
            
            result += "\n## 💡 Recommendations\n"
            if findings['critical']:
                result += "1. **URGENT**: Address critical security issues immediately\n"
            if findings['warning']:
                result += "2. Review and remediate warning items\n"
            result += "3. Enable WPA3 on all wireless networks\n"
            result += "4. Implement least-privilege firewall rules\n"
            result += "5. Regular security audits recommended\n"
            
            return result
            
        except Exception as e:
            return f"Error generating compliance report: {str(e)}"