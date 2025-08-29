"""
Wireless Firewall and Traffic Shaping tools for the Cisco Meraki MCP Server.
These tools manage L3/L7 firewall rules and traffic shaping for wireless SSIDs.
"""

from typing import Optional, List, Dict, Any

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_wireless_firewall_tools(mcp_app, meraki):
    """
    Register wireless firewall and traffic shaping tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all wireless firewall tools
    register_wireless_firewall_handlers()

def register_wireless_firewall_handlers():
    """Register all wireless firewall and traffic shaping tool handlers."""
    
    # ==================== L3 FIREWALL RULES ====================
    
    @app.tool(
        name="get_network_wireless_ssid_l3_firewall_rules",
        description="📡🔥 Get L3 firewall rules for a wireless SSID"
    )
    def get_network_wireless_ssid_l3_firewall_rules(
        network_id: str,
        number: str
    ):
        """
        Get L3 firewall rules for a wireless SSID.
        
        Args:
            network_id: Network ID
            number: SSID number (0-14)
            
        Returns:
            L3 firewall rules for the SSID
        """
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL3FirewallRules(
                network_id,
                number
            )
            
            rules = result.get('rules', [])
            
            response = f"# 📡 Wireless SSID {number} - L3 Firewall Rules\n\n"
            
            if not rules:
                response += "No L3 firewall rules configured (default: allow all)\n"
            else:
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    policy = rule.get('policy', 'allow')
                    icon = "✅" if policy == 'allow' else "🚫"
                    
                    response += f"## Rule {i}: {icon} {policy.upper()}\n"
                    
                    comment = rule.get('comment')
                    if comment:
                        response += f"**Comment**: {comment}\n"
                    
                    response += f"- **Protocol**: {rule.get('protocol', 'any')}\n"
                    response += f"- **Source**: {rule.get('srcCidr', 'any')}\n"
                    response += f"- **Source Port**: {rule.get('srcPort', 'any')}\n"
                    response += f"- **Destination**: {rule.get('destCidr', 'any')}\n"
                    response += f"- **Dest Port**: {rule.get('destPort', 'any')}\n\n"
            
            response += "\n💡 **Note**: Rules are evaluated top to bottom. First match wins."
            
            return response
            
        except Exception as e:
            return f"❌ Error getting L3 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_l3_firewall_rules",
        description="📡🔥 Update L3 firewall rules for a wireless SSID (controls WiFi client traffic)"
    )
    def update_network_wireless_ssid_l3_firewall_rules(
        network_id: str,
        number: str,
        rules: str,
        allow_lan_access: Optional[bool] = True
    ):
        """
        Update L3 firewall rules for a wireless SSID.
        THIS controls what WiFi clients can access, including VPN destinations!
        
        Args:
            network_id: Network ID
            number: SSID number (0-14)
            rules: JSON string of firewall rules, e.g.:
                '[{"policy": "allow", "protocol": "any", "destCidr": "192.168.51.0/24", "comment": "Allow to Burswood"}]'
            allow_lan_access: Allow wireless clients to access LAN (default: True)
            
        Returns:
            Updated L3 firewall rules
        """
        try:
            import json
            
            # Parse rules if provided
            rule_list = []
            if rules:
                try:
                    rule_list = json.loads(rules)
                except json.JSONDecodeError:
                    return "❌ Invalid rules format. Must be valid JSON array."
            
            # Update rules
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidFirewallL3FirewallRules(
                network_id,
                number,
                rules=rule_list,
                allowLanAccess=allow_lan_access
            )
            
            response = f"# ✅ Updated SSID {number} L3 Firewall Rules\n\n"
            response += f"**Allow LAN Access**: {result.get('allowLanAccess', True)}\n\n"
            
            updated_rules = result.get('rules', [])
            if updated_rules:
                response += f"## Configured Rules ({len(updated_rules)} total)\n"
                for i, rule in enumerate(updated_rules, 1):
                    policy = rule.get('policy', 'allow')
                    icon = "✅" if policy == 'allow' else "🚫"
                    response += f"{i}. {icon} {policy.upper()}: {rule.get('comment', 'No comment')}\n"
            else:
                response += "No specific rules configured (default allow all)\n"
            
            response += "\n⚠️ **Important**: These rules apply to WiFi clients on this SSID!"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating L3 firewall rules: {str(e)}"
    
    # ==================== L7 FIREWALL RULES ====================
    
    @app.tool(
        name="get_network_wireless_ssid_l7_firewall_rules",
        description="📡🔥 Get L7 (application) firewall rules for a wireless SSID"
    )
    def get_network_wireless_ssid_l7_firewall_rules(
        network_id: str,
        number: str
    ):
        """
        Get L7 (application layer) firewall rules for a wireless SSID.
        
        Args:
            network_id: Network ID
            number: SSID number (0-14)
            
        Returns:
            L7 firewall rules for the SSID
        """
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL7FirewallRules(
                network_id,
                number
            )
            
            rules = result.get('rules', [])
            
            response = f"# 📡 Wireless SSID {number} - L7 Firewall Rules\n\n"
            
            if not rules:
                response += "No L7 firewall rules configured (all applications allowed)\n"
            else:
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    rule_type = rule.get('type', 'unknown')
                    value = rule.get('value', '')
                    
                    response += f"## Rule {i}: 🚫 DENY\n"
                    response += f"- **Type**: {rule_type}\n"
                    response += f"- **Value**: {value}\n"
                    
                    # Explain what's blocked
                    if rule_type == 'application':
                        response += f"  Blocks specific application: {value}\n"
                    elif rule_type == 'applicationCategory':
                        response += f"  Blocks application category: {value}\n"
                    elif rule_type == 'host':
                        response += f"  Blocks hostname: {value}\n"
                    elif rule_type == 'ipRange':
                        response += f"  Blocks IP range: {value}\n"
                    elif rule_type == 'port':
                        response += f"  Blocks port: {value}\n"
                    
                    response += "\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_l7_firewall_rules",
        description="📡🔥 Update L7 (application) firewall rules for a wireless SSID"
    )
    def update_network_wireless_ssid_l7_firewall_rules(
        network_id: str,
        number: str,
        rules: str
    ):
        """
        Update L7 (application layer) firewall rules for a wireless SSID.
        
        Args:
            network_id: Network ID
            number: SSID number (0-14)
            rules: JSON string of L7 firewall rules (all are deny), e.g.:
                '[{"type": "applicationCategory", "value": "Social web & photo sharing"}]'
                '[{"type": "host", "value": "facebook.com"}]'
                '[{"type": "port", "value": "8080"}]'
            
        Returns:
            Updated L7 firewall rules
        """
        try:
            import json
            
            # Parse rules
            rule_list = []
            if rules:
                try:
                    rule_list = json.loads(rules)
                    # All L7 rules are deny
                    for rule in rule_list:
                        rule['policy'] = 'deny'
                except json.JSONDecodeError:
                    return "❌ Invalid rules format. Must be valid JSON array."
            
            # Update rules
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidFirewallL7FirewallRules(
                network_id,
                number,
                rules=rule_list
            )
            
            response = f"# ✅ Updated SSID {number} L7 Firewall Rules\n\n"
            
            updated_rules = result.get('rules', [])
            if updated_rules:
                response += f"## Blocked Applications/Services ({len(updated_rules)} total)\n"
                for i, rule in enumerate(updated_rules, 1):
                    response += f"{i}. 🚫 {rule.get('type')}: {rule.get('value')}\n"
            else:
                response += "No L7 rules configured (all applications allowed)\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating L7 firewall rules: {str(e)}"
    
    # ==================== TRAFFIC SHAPING ====================
    
    @app.tool(
        name="get_network_wireless_ssid_traffic_shaping",
        description="📡🚦 Get traffic shaping rules for a wireless SSID"
    )
    def get_network_wireless_ssid_traffic_shaping(
        network_id: str,
        number: str
    ):
        """
        Get traffic shaping configuration for a wireless SSID.
        
        Args:
            network_id: Network ID
            number: SSID number (0-14)
            
        Returns:
            Traffic shaping configuration
        """
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidTrafficShapingRules(
                network_id,
                number
            )
            
            response = f"# 📡 Wireless SSID {number} - Traffic Shaping\n\n"
            
            # Overall settings
            enabled = result.get('trafficShapingEnabled', False)
            response += f"**Traffic Shaping**: {'Enabled ✅' if enabled else 'Disabled ❌'}\n"
            
            if enabled:
                # Default per-client limits
                default_limits = result.get('defaultRulesEnabled', False)
                if default_limits:
                    response += f"\n## Default Per-Client Limits\n"
                    response += f"- **Upload**: {result.get('perClientBandwidthLimits', {}).get('limitUp', 'Unlimited')} Mbps\n"
                    response += f"- **Download**: {result.get('perClientBandwidthLimits', {}).get('limitDown', 'Unlimited')} Mbps\n"
                
                # SSID bandwidth limits
                ssid_limits = result.get('bandwidthLimits', {})
                if ssid_limits:
                    response += f"\n## SSID Total Bandwidth Limits\n"
                    response += f"- **Upload**: {ssid_limits.get('limitUp', 'Unlimited')} Mbps\n"
                    response += f"- **Download**: {ssid_limits.get('limitDown', 'Unlimited')} Mbps\n"
                
                # Traffic shaping rules
                rules = result.get('rules', [])
                if rules:
                    response += f"\n## Traffic Shaping Rules ({len(rules)} total)\n"
                    for i, rule in enumerate(rules, 1):
                        response += f"\n### Rule {i}\n"
                        
                        # Definition
                        definitions = rule.get('definitions', [])
                        if definitions:
                            response += "**Matches**:\n"
                            for definition in definitions:
                                def_type = definition.get('type')
                                value = definition.get('value')
                                response += f"  - {def_type}: {value}\n"
                        
                        # Limits
                        per_client = rule.get('perClientBandwidthLimits', {})
                        if per_client:
                            response += f"**Per-Client Limits**:\n"
                            response += f"  - Upload: {per_client.get('limitUp', 'Unlimited')} Mbps\n"
                            response += f"  - Download: {per_client.get('limitDown', 'Unlimited')} Mbps\n"
                        
                        # DSCP tagging
                        dscp = rule.get('dscpTagValue')
                        if dscp is not None:
                            response += f"**DSCP Tag**: {dscp}\n"
                        
                        # PCP tagging
                        pcp = rule.get('pcpTagValue')
                        if pcp is not None:
                            response += f"**PCP Tag**: {pcp}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting traffic shaping rules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_traffic_shaping",
        description="📡🚦 Update traffic shaping rules for a wireless SSID"
    )
    def update_network_wireless_ssid_traffic_shaping(
        network_id: str,
        number: str,
        enabled: Optional[bool] = None,
        per_client_bandwidth_up: Optional[int] = None,
        per_client_bandwidth_down: Optional[int] = None,
        ssid_bandwidth_up: Optional[int] = None,
        ssid_bandwidth_down: Optional[int] = None
    ):
        """
        Update traffic shaping configuration for a wireless SSID.
        
        Args:
            network_id: Network ID
            number: SSID number (0-14)
            enabled: Enable/disable traffic shaping
            per_client_bandwidth_up: Per-client upload limit in Mbps
            per_client_bandwidth_down: Per-client download limit in Mbps
            ssid_bandwidth_up: Total SSID upload limit in Mbps
            ssid_bandwidth_down: Total SSID download limit in Mbps
            
        Returns:
            Updated traffic shaping configuration
        """
        try:
            kwargs = {}
            
            if enabled is not None:
                kwargs['trafficShapingEnabled'] = enabled
            
            # Per-client limits
            if per_client_bandwidth_up is not None or per_client_bandwidth_down is not None:
                kwargs['defaultRulesEnabled'] = True
                kwargs['perClientBandwidthLimits'] = {}
                if per_client_bandwidth_up is not None:
                    kwargs['perClientBandwidthLimits']['limitUp'] = per_client_bandwidth_up
                if per_client_bandwidth_down is not None:
                    kwargs['perClientBandwidthLimits']['limitDown'] = per_client_bandwidth_down
            
            # SSID total limits
            if ssid_bandwidth_up is not None or ssid_bandwidth_down is not None:
                kwargs['bandwidthLimits'] = {}
                if ssid_bandwidth_up is not None:
                    kwargs['bandwidthLimits']['limitUp'] = ssid_bandwidth_up
                if ssid_bandwidth_down is not None:
                    kwargs['bandwidthLimits']['limitDown'] = ssid_bandwidth_down
            
            # Update traffic shaping
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidTrafficShapingRules(
                network_id,
                number,
                **kwargs
            )
            
            response = f"# ✅ Updated SSID {number} Traffic Shaping\n\n"
            
            if result.get('trafficShapingEnabled'):
                response += "**Status**: Enabled ✅\n\n"
                
                if result.get('defaultRulesEnabled'):
                    limits = result.get('perClientBandwidthLimits', {})
                    response += "## Per-Client Limits\n"
                    response += f"- Upload: {limits.get('limitUp', 'Unlimited')} Mbps\n"
                    response += f"- Download: {limits.get('limitDown', 'Unlimited')} Mbps\n"
                
                ssid_limits = result.get('bandwidthLimits', {})
                if ssid_limits:
                    response += "\n## SSID Total Limits\n"
                    response += f"- Upload: {ssid_limits.get('limitUp', 'Unlimited')} Mbps\n"
                    response += f"- Download: {ssid_limits.get('limitDown', 'Unlimited')} Mbps\n"
            else:
                response += "**Status**: Disabled ❌\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating traffic shaping: {str(e)}"