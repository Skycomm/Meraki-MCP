"""
Security Appliance management tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_appliance_tools(mcp_app, meraki):
    """
    Register security appliance tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all appliance tools
    register_appliance_tool_handlers()

def register_appliance_tool_handlers():
    """Register all security appliance tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="get_network_appliance_firewall_l3_rules",
        description="🔥 Get Layer 3 firewall rules for a network"
    )
    def get_network_appliance_firewall_l3_rules(network_id: str):
        """
        Get Layer 3 firewall rules for a network appliance.
        
        Args:
            network_id: Network ID
            
        Returns:
            Formatted L3 firewall rules
        """
        try:
            rules = meraki_client.get_network_appliance_firewall_l3_rules(network_id)
            
            if not rules or not rules.get('rules'):
                return f"No L3 firewall rules found for network {network_id}."
                
            result = f"# 🔥 Layer 3 Firewall Rules for Network {network_id}\n\n"
            
            for idx, rule in enumerate(rules.get('rules', []), 1):
                result += f"## Rule {idx}: {rule.get('comment', 'No comment')}\n"
                result += f"- **Policy**: {rule.get('policy', 'N/A')}\n"
                result += f"- **Protocol**: {rule.get('protocol', 'any')}\n"
                result += f"- **Source**: {rule.get('srcCidr', 'any')}\n"
                
                if rule.get('srcPort'):
                    result += f"- **Source Port**: {rule['srcPort']}\n"
                    
                result += f"- **Destination**: {rule.get('destCidr', 'any')}\n"
                
                if rule.get('destPort'):
                    result += f"- **Destination Port**: {rule['destPort']}\n"
                    
                result += f"- **Syslog**: {'✅ Enabled' if rule.get('syslogEnabled') else '❌ Disabled'}\n"
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving L3 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_l3_rules",
        description="🔥 Update Layer 3 firewall rules (BE CAREFUL!)"
    )
    def update_network_appliance_firewall_l3_rules(
        network_id: str, 
        comment: str,
        policy: str,
        protocol: str = "any",
        src_cidr: str = "any",
        dest_cidr: str = "any",
        dest_port: str = None,
        syslog_enabled: bool = False
    ):
        """
        Add a new L3 firewall rule to a network (existing rules are preserved).
        
        Args:
            network_id: Network ID
            comment: Description of the rule
            policy: 'allow' or 'deny'
            protocol: 'tcp', 'udp', 'icmp', or 'any'
            src_cidr: Source CIDR (e.g., '192.168.1.0/24')
            dest_cidr: Destination CIDR
            dest_port: Destination port (optional)
            syslog_enabled: Enable syslog for this rule
            
        Returns:
            Updated firewall rules
        """
        try:
            # Get existing rules first
            current = meraki_client.get_network_appliance_firewall_l3_rules(network_id)
            existing_rules = current.get('rules', [])
            
            # Create new rule
            new_rule = {
                'comment': comment,
                'policy': policy,
                'protocol': protocol,
                'srcCidr': src_cidr,
                'destCidr': dest_cidr,
                'syslogEnabled': syslog_enabled
            }
            
            if dest_port:
                new_rule['destPort'] = dest_port
                
            # Add new rule to beginning (processed first)
            updated_rules = [new_rule] + existing_rules
            
            # Update firewall rules
            result = meraki_client.update_network_appliance_firewall_l3_rules(
                network_id,
                rules=updated_rules
            )
            
            return f"✅ Firewall rule added successfully!\n\nNew rule: {comment}\nPolicy: {policy}\nTotal rules: {len(updated_rules)}"
            
        except Exception as e:
            return f"Error updating L3 firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_content_filtering",
        description="🌐 Get content filtering settings for a network"
    )
    def get_network_appliance_content_filtering(network_id: str):
        """
        Get content filtering settings for a network appliance.
        
        Args:
            network_id: Network ID
            
        Returns:
            Content filtering configuration
        """
        try:
            filtering = meraki_client.get_network_appliance_content_filtering(network_id)
            
            result = f"# 🌐 Content Filtering for Network {network_id}\n\n"
            
            # Blocked URL categories
            blocked_categories = filtering.get('blockedUrlCategories', [])
            if blocked_categories:
                result += "## Blocked Categories\n"
                for category in blocked_categories:
                    result += f"- {category}\n"
                result += "\n"
                
            # Blocked URL patterns
            blocked_patterns = filtering.get('blockedUrlPatterns', [])
            if blocked_patterns:
                result += "## Blocked URL Patterns\n"
                for pattern in blocked_patterns:
                    result += f"- {pattern}\n"
                result += "\n"
                
            # Allowed URL patterns
            allowed_patterns = filtering.get('allowedUrlPatterns', [])
            if allowed_patterns:
                result += "## Allowed URL Patterns\n"
                for pattern in allowed_patterns:
                    result += f"- {pattern}\n"
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving content filtering settings: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_vpn_site_to_site",
        description="🔐 Get site-to-site VPN settings for a network"
    )
    def get_network_appliance_vpn_site_to_site(network_id: str):
        """
        Get site-to-site VPN settings for a network appliance.
        
        Args:
            network_id: Network ID
            
        Returns:
            Site-to-site VPN configuration
        """
        try:
            vpn = meraki_client.get_network_appliance_vpn_site_to_site(network_id)
            
            result = f"# 🔐 Site-to-Site VPN for Network {network_id}\n\n"
            
            mode = vpn.get('mode', 'none')
            result += f"**Mode**: {mode}\n\n"
            
            if mode != 'none':
                # Hubs (for spoke mode)
                hubs = vpn.get('hubs', [])
                if hubs:
                    result += "## VPN Hubs\n"
                    for hub in hubs:
                        result += f"- Hub ID: {hub.get('hubId')}\n"
                        result += f"  Default route: {'✅' if hub.get('useDefaultRoute') else '❌'}\n"
                    result += "\n"
                    
                # Subnets
                subnets = vpn.get('subnets', [])
                if subnets:
                    result += "## Local Subnets in VPN\n"
                    for subnet in subnets:
                        result += f"- {subnet.get('localSubnet')}"
                        if subnet.get('useVpn'):
                            result += " ✅ In VPN"
                        else:
                            result += " ❌ Not in VPN"
                        result += "\n"
                    result += "\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving site-to-site VPN settings: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_security_malware",
        description="🛡️ Get malware protection settings for a network"
    )
    def get_network_appliance_security_malware(network_id: str):
        """
        Get malware protection settings for a network appliance.
        
        Args:
            network_id: Network ID
            
        Returns:
            Malware protection configuration
        """
        try:
            malware = meraki_client.get_network_appliance_security_malware(network_id)
            
            result = f"# 🛡️ Malware Protection for Network {network_id}\n\n"
            
            mode = malware.get('mode', 'disabled')
            result += f"**Mode**: {mode}\n"
            
            if mode == 'enabled':
                result += "✅ Malware protection is ACTIVE\n"
                
                # Allowed URLs
                allowed_urls = malware.get('allowedUrls', [])
                if allowed_urls:
                    result += "\n## Allowed URLs (Whitelist)\n"
                    for url in allowed_urls:
                        result += f"- {url.get('url')} - {url.get('comment', 'No comment')}\n"
                        
                # Allowed files
                allowed_files = malware.get('allowedFiles', [])
                if allowed_files:
                    result += "\n## Allowed Files (by SHA256)\n"
                    for file in allowed_files:
                        result += f"- {file.get('sha256')[:16]}... - {file.get('comment', 'No comment')}\n"
            else:
                result += "❌ Malware protection is DISABLED\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving malware protection settings: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_security_intrusion",
        description="🚨 Get intrusion detection/prevention settings"
    )
    def get_network_appliance_security_intrusion(network_id: str):
        """
        Get intrusion detection and prevention settings for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            IDS/IPS configuration
        """
        try:
            intrusion = meraki_client.get_network_appliance_security_intrusion(network_id)
            
            result = f"# 🚨 Intrusion Detection/Prevention for Network {network_id}\n\n"
            
            mode = intrusion.get('mode', 'disabled')
            result += f"**Mode**: {mode}\n"
            
            if mode != 'disabled':
                result += f"✅ IDS/IPS is ACTIVE in {mode.upper()} mode\n"
                
                # IDS rulesets
                ids_rulesets = intrusion.get('idsRulesets', 'balanced')
                result += f"\n**Ruleset**: {ids_rulesets}\n"
                
                # Protected networks
                protected = intrusion.get('protectedNetworks', {})
                use_default = protected.get('useDefault', True)
                
                if use_default:
                    result += "\n**Protected Networks**: Using default (all local networks)\n"
                else:
                    included = protected.get('includedCidr', [])
                    excluded = protected.get('excludedCidr', [])
                    
                    if included:
                        result += "\n**Protected Networks**:\n"
                        for cidr in included:
                            result += f"- ✅ {cidr}\n"
                            
                    if excluded:
                        result += "\n**Excluded Networks**:\n"
                        for cidr in excluded:
                            result += f"- ❌ {cidr}\n"
            else:
                result += "❌ IDS/IPS is DISABLED\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving intrusion detection settings: {str(e)}"