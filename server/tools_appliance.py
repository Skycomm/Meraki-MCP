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
    
    @app.tool(
        name="update_network_appliance_security_intrusion",
        description="🚨 Update intrusion detection/prevention settings - Enable or configure IDS/IPS"
    )
    def update_network_appliance_security_intrusion(
        network_id: str,
        mode: str = None,
        ids_rulesets: str = None,
        use_default_protected_networks: bool = None,
        included_cidr: str = None,
        excluded_cidr: str = None
    ):
        """
        Update intrusion detection and prevention settings for a network.
        
        Args:
            network_id: Network ID
            mode: Set to 'disabled', 'detection', or 'prevention'
            ids_rulesets: Set to 'connectivity', 'balanced', or 'security'
            use_default_protected_networks: Use default protected networks (all local networks)
            included_cidr: Comma-separated list of CIDR ranges to protect (e.g., "10.0.0.0/8,192.168.0.0/16")
            excluded_cidr: Comma-separated list of CIDR ranges to exclude from protection
            
        Returns:
            Updated IDS/IPS configuration
        """
        try:
            # Build kwargs for the update
            kwargs = {}
            
            # Add mode if specified
            if mode:
                if mode not in ['disabled', 'detection', 'prevention']:
                    return f"❌ Invalid mode '{mode}'. Must be 'disabled', 'detection', or 'prevention'"
                kwargs['mode'] = mode
            
            # Add ruleset if specified
            if ids_rulesets:
                if ids_rulesets not in ['connectivity', 'balanced', 'security']:
                    return f"❌ Invalid ruleset '{ids_rulesets}'. Must be 'connectivity', 'balanced', or 'security'"
                kwargs['idsRulesets'] = ids_rulesets
            
            # Handle protected networks configuration
            if use_default_protected_networks is not None or included_cidr or excluded_cidr:
                protected_networks = {}
                
                if use_default_protected_networks is not None:
                    protected_networks['useDefault'] = use_default_protected_networks
                
                if included_cidr:
                    protected_networks['includedCidr'] = [cidr.strip() for cidr in included_cidr.split(',')]
                
                if excluded_cidr:
                    protected_networks['excludedCidr'] = [cidr.strip() for cidr in excluded_cidr.split(',')]
                
                kwargs['protectedNetworks'] = protected_networks
            
            # Get current settings first for comparison
            current = meraki_client.get_network_appliance_security_intrusion(network_id)
            current_mode = current.get('mode', 'disabled')
            
            # Update the settings
            result = meraki_client.update_network_appliance_security_intrusion(network_id, **kwargs)
            
            # Format response
            response = f"# ✅ Updated IDS/IPS Settings for Network {network_id}\n\n"
            
            new_mode = result.get('mode', 'disabled')
            response += f"**Mode**: {current_mode} → {new_mode}\n"
            
            if new_mode == 'detection':
                response += "🔍 **Detection Mode**: Monitoring traffic for threats (not blocking)\n"
            elif new_mode == 'prevention':
                response += "🛡️ **Prevention Mode**: Actively blocking detected threats\n"
            else:
                response += "❌ **Disabled**: No intrusion detection/prevention active\n"
            
            # Show ruleset if IDS/IPS is enabled
            if new_mode != 'disabled':
                ruleset = result.get('idsRulesets', 'balanced')
                response += f"\n**Ruleset**: {ruleset}\n"
                
                if ruleset == 'connectivity':
                    response += "- Minimal rules (CVSS 10 only) - for critical connectivity\n"
                elif ruleset == 'balanced':
                    response += "- Balanced protection (CVSS 9+) - includes malware C&C, SQL injection\n"
                elif ruleset == 'security':
                    response += "- Maximum protection (CVSS 8+) - includes app detection rules\n"
                
                # Show protected networks
                protected = result.get('protectedNetworks', {})
                if protected.get('useDefault'):
                    response += "\n**Protected Networks**: Using default (all local networks)\n"
                else:
                    included = protected.get('includedCidr', [])
                    excluded = protected.get('excludedCidr', [])
                    
                    if included:
                        response += "\n**Protected Networks**:\n"
                        for cidr in included:
                            response += f"- ✅ {cidr}\n"
                    
                    if excluded:
                        response += "\n**Excluded Networks**:\n"
                        for cidr in excluded:
                            response += f"- ❌ {cidr}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating intrusion detection settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_security_malware",
        description="🦠 Update Advanced Malware Protection (AMP) settings - Enable/disable malware blocking"
    )
    def update_network_appliance_security_malware(
        network_id: str,
        mode: str,
        allowed_urls: str = None,
        allowed_files: str = None
    ):
        """
        Update malware protection settings for a network.
        
        Args:
            network_id: Network ID
            mode: 'enabled' or 'disabled'
            allowed_urls: Comma-separated list of URLs to whitelist (e.g., "example.com,test.com")
            allowed_files: Comma-separated list of file SHA256 hashes to whitelist
            
        Returns:
            Updated malware protection configuration
        """
        try:
            # Validate mode
            if mode not in ['enabled', 'disabled']:
                return f"❌ Invalid mode '{mode}'. Must be 'enabled' or 'disabled'"
            
            # Build kwargs
            kwargs = {'mode': mode}
            
            # Handle allowed URLs
            if allowed_urls:
                urls_list = []
                for url in allowed_urls.split(','):
                    urls_list.append({
                        'url': url.strip(),
                        'comment': f'Added via MCP'
                    })
                kwargs['allowedUrls'] = urls_list
            
            # Handle allowed files
            if allowed_files:
                files_list = []
                for file_hash in allowed_files.split(','):
                    files_list.append({
                        'sha256': file_hash.strip(),
                        'comment': f'Added via MCP'
                    })
                kwargs['allowedFiles'] = files_list
            
            # Get current settings
            current = meraki_client.get_network_appliance_security_malware(network_id)
            current_mode = current.get('mode', 'disabled')
            
            # Update settings
            result = meraki_client.update_network_appliance_security_malware(network_id, **kwargs)
            
            # Format response
            response = f"# ✅ Updated Malware Protection for Network {network_id}\n\n"
            response += f"**Mode**: {current_mode} → {result.get('mode', 'disabled')}\n"
            
            if result.get('mode') == 'enabled':
                response += "🛡️ **Advanced Malware Protection (AMP)** is now ACTIVE\n"
                response += "- Blocking malicious file downloads\n"
                response += "- Using Cisco Talos threat intelligence\n"
                
                # Show whitelisted URLs
                allowed_urls = result.get('allowedUrls', [])
                if allowed_urls:
                    response += "\n**Whitelisted URLs**:\n"
                    for url in allowed_urls:
                        response += f"- {url.get('url')} - {url.get('comment', '')}\n"
                
                # Show whitelisted files
                allowed_files = result.get('allowedFiles', [])
                if allowed_files:
                    response += "\n**Whitelisted Files** (by SHA256):\n"
                    for file in allowed_files:
                        response += f"- {file.get('sha256')[:16]}... - {file.get('comment', '')}\n"
            else:
                response += "❌ **Malware Protection is DISABLED**\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating malware protection: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_content_filtering",
        description="🌐 Update web content filtering - Block categories of websites"
    )
    def update_network_appliance_content_filtering(
        network_id: str,
        allowed_url_patterns: str = None,
        blocked_url_patterns: str = None,
        blocked_categories: str = None,
        url_category_list_size: str = None
    ):
        """
        Update content filtering settings for a network.
        
        Args:
            network_id: Network ID
            allowed_url_patterns: Comma-separated list of allowed URL patterns
            blocked_url_patterns: Comma-separated list of blocked URL patterns
            blocked_categories: Comma-separated list of categories to block (e.g., "meraki:contentFiltering/category/1,meraki:contentFiltering/category/2")
            url_category_list_size: Size of URL category list ('topSites' or 'fullList')
            
        Returns:
            Updated content filtering configuration
        """
        try:
            # Build kwargs
            kwargs = {}
            
            # Handle allowed URL patterns
            if allowed_url_patterns:
                kwargs['allowedUrlPatterns'] = [pattern.strip() for pattern in allowed_url_patterns.split(',')]
            
            # Handle blocked URL patterns
            if blocked_url_patterns:
                kwargs['blockedUrlPatterns'] = [pattern.strip() for pattern in blocked_url_patterns.split(',')]
            
            # Handle blocked categories
            if blocked_categories:
                kwargs['blockedUrlCategories'] = [cat.strip() for cat in blocked_categories.split(',')]
            
            # Handle URL category list size
            if url_category_list_size:
                if url_category_list_size not in ['topSites', 'fullList']:
                    return f"❌ Invalid list size '{url_category_list_size}'. Must be 'topSites' or 'fullList'"
                kwargs['urlCategoryListSize'] = url_category_list_size
            
            # Update settings
            result = meraki_client.update_network_appliance_content_filtering(network_id, **kwargs)
            
            # Format response
            response = f"# ✅ Updated Content Filtering for Network {network_id}\n\n"
            
            # Show allowed patterns
            allowed = result.get('allowedUrlPatterns', [])
            if allowed:
                response += "**Allowed URL Patterns**:\n"
                for pattern in allowed:
                    response += f"- ✅ {pattern}\n"
                response += "\n"
            
            # Show blocked patterns
            blocked = result.get('blockedUrlPatterns', [])
            if blocked:
                response += "**Blocked URL Patterns**:\n"
                for pattern in blocked:
                    response += f"- ❌ {pattern}\n"
                response += "\n"
            
            # Show blocked categories
            categories = result.get('blockedUrlCategories', [])
            if categories:
                response += f"**Blocked Categories**: {len(categories)} categories\n"
                # Note: Category IDs would need to be mapped to names
                response += "Use get_network_appliance_content_filtering_categories to see category details\n"
            
            # Show list size
            list_size = result.get('urlCategoryListSize', 'topSites')
            response += f"\n**Category List Size**: {list_size}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating content filtering: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_l7_rules",
        description="🔥 Get Layer 7 (application) firewall rules - Including geo-blocking"
    )
    def get_network_appliance_firewall_l7_rules(network_id: str):
        """
        Get Layer 7 firewall rules for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            L7 firewall rules configuration
        """
        try:
            rules = meraki_client.get_network_appliance_firewall_l7_rules(network_id)
            
            result = f"# 🔥 Layer 7 Firewall Rules for Network {network_id}\n\n"
            
            # Get rules list
            rules_list = rules.get('rules', [])
            if not rules_list:
                result += "**No L7 firewall rules configured**\n"
                return result
            
            result += f"**Total Rules**: {len(rules_list)}\n\n"
            
            for i, rule in enumerate(rules_list, 1):
                result += f"## Rule {i}: {rule.get('policy', 'Unknown')}\n"
                
                # Rule type and value
                rule_type = rule.get('type', 'Unknown')
                value = rule.get('value', {})
                
                if rule_type == 'application':
                    result += f"- **Application**: {value.get('name', 'Unknown')}\n"
                elif rule_type == 'applicationCategory':
                    result += f"- **Category**: {value.get('name', 'Unknown')}\n"
                elif rule_type == 'ipRange':
                    result += f"- **IP Range**: {value}\n"
                elif rule_type == 'blacklistedCountries':
                    countries = value.get('countries', [])
                    result += f"- **Blocked Countries**: {', '.join(countries)}\n"
                elif rule_type == 'whitelistedCountries':
                    countries = value.get('countries', [])
                    result += f"- **Allowed Countries Only**: {', '.join(countries)}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_l7_rules",
        description="🔥 Update Layer 7 firewall rules - Block applications, categories, or countries"
    )
    def update_network_appliance_firewall_l7_rules(
        network_id: str,
        rules: str
    ):
        """
        Update Layer 7 firewall rules for a network.
        
        Args:
            network_id: Network ID
            rules: JSON string of rules array. Each rule needs: policy (deny), type, and value.
                   Example: '[{"policy":"deny","type":"blacklistedCountries","value":{"countries":["CN","RU"]}}]'
            
        Returns:
            Updated L7 firewall rules
        """
        try:
            import json
            
            # Parse rules
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid rules format. Must be valid JSON array"
            
            # Update rules
            result = meraki_client.update_network_appliance_firewall_l7_rules(
                network_id,
                rules=rules_list
            )
            
            # Format response
            response = f"# ✅ Updated L7 Firewall Rules for Network {network_id}\n\n"
            
            updated_rules = result.get('rules', [])
            response += f"**Total Rules**: {len(updated_rules)}\n\n"
            
            for i, rule in enumerate(updated_rules, 1):
                response += f"## Rule {i}: {rule.get('policy', 'Unknown').upper()}\n"
                
                rule_type = rule.get('type', 'Unknown')
                value = rule.get('value', {})
                
                if rule_type == 'blacklistedCountries':
                    countries = value.get('countries', [])
                    response += f"- 🌍 **Blocked Countries**: {', '.join(countries)}\n"
                elif rule_type == 'whitelistedCountries':
                    countries = value.get('countries', [])
                    response += f"- 🌍 **Allowed Countries Only**: {', '.join(countries)}\n"
                elif rule_type == 'application':
                    response += f"- 📱 **Application**: {value.get('name', 'Unknown')}\n"
                elif rule_type == 'applicationCategory':
                    response += f"- 📂 **Category**: {value.get('name', 'Unknown')}\n"
                
                response += "\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_settings", 
        description="⚙️ Get general firewall settings"
    )
    def get_network_appliance_firewall_settings(network_id: str):
        """
        Get firewall settings for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            Firewall settings configuration
        """
        try:
            settings = meraki_client.get_network_appliance_firewall_settings(network_id)
            
            result = f"# ⚙️ Firewall Settings for Network {network_id}\n\n"
            
            # Spoofing protection
            spoofing = settings.get('spoofingProtection', {})
            result += f"**Spoofing Protection**:\n"
            result += f"- IP Source Guard: {'✅ Enabled' if spoofing.get('ipSourceGuard', {}).get('mode') == 'block' else '❌ Disabled'}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving firewall settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_settings",
        description="⚙️ Update general firewall settings"
    )
    def update_network_appliance_firewall_settings(
        network_id: str,
        spoofing_protection_mode: str = None
    ):
        """
        Update firewall settings for a network.
        
        Args:
            network_id: Network ID
            spoofing_protection_mode: 'block' to enable IP source guard, 'log' to log only
            
        Returns:
            Updated firewall settings
        """
        try:
            kwargs = {}
            
            if spoofing_protection_mode:
                if spoofing_protection_mode not in ['block', 'log']:
                    return f"❌ Invalid mode '{spoofing_protection_mode}'. Must be 'block' or 'log'"
                kwargs['spoofingProtection'] = {
                    'ipSourceGuard': {
                        'mode': spoofing_protection_mode
                    }
                }
            
            # Update settings
            result = meraki_client.update_network_appliance_firewall_settings(network_id, **kwargs)
            
            # Format response
            response = f"# ✅ Updated Firewall Settings for Network {network_id}\n\n"
            
            spoofing = result.get('spoofingProtection', {})
            mode = spoofing.get('ipSourceGuard', {}).get('mode', 'disabled')
            
            if mode == 'block':
                response += "🛡️ **IP Source Guard**: ✅ Blocking spoofed traffic\n"
            elif mode == 'log':
                response += "📝 **IP Source Guard**: Logging spoofed traffic only\n"
            else:
                response += "❌ **IP Source Guard**: Disabled\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating firewall settings: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_security_events",
        description="🚨 Get security events/threats detected on the network"
    )
    def get_network_appliance_security_events(
        network_id: str,
        timespan: int = 86400,
        per_page: int = 100
    ):
        """
        Get security events for a network.
        
        Args:
            network_id: Network ID
            timespan: Timespan in seconds (default 24 hours)
            per_page: Number of events per page (default 100)
            
        Returns:
            List of security events
        """
        try:
            events = meraki_client.get_network_appliance_security_events(
                network_id,
                timespan=timespan,
                perPage=per_page
            )
            
            result = f"# 🚨 Security Events for Network {network_id}\n"
            result += f"*Last {timespan//3600} hours*\n\n"
            
            if not events:
                result += "✅ No security events detected\n"
                return result
            
            result += f"**Total Events**: {len(events)}\n\n"
            
            # Group events by type
            event_types = {}
            for event in events:
                event_type = event.get('eventType', 'Unknown')
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            result += "**Event Summary**:\n"
            for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
                result += f"- {event_type}: {count} events\n"
            
            result += "\n**Recent Events**:\n"
            for event in events[:10]:  # Show first 10
                result += f"\n🔸 **{event.get('eventType', 'Unknown')}**\n"
                result += f"- Time: {event.get('ts', 'Unknown')}\n"
                result += f"- Client: {event.get('clientMac', 'Unknown')}\n"
                result += f"- Source IP: {event.get('srcIp', 'Unknown')}\n"
                result += f"- Destination: {event.get('destIp', 'Unknown')}\n"
                
                if event.get('message'):
                    result += f"- Message: {event['message']}\n"
                if event.get('signature'):
                    result += f"- Signature: {event['signature']}\n"
                if event.get('priority'):
                    result += f"- Priority: {event['priority']}\n"
            
            if len(events) > 10:
                result += f"\n... and {len(events) - 10} more events\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving security events: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_one_to_one_nat_rules",
        description="🔄 Get 1:1 NAT mapping rules"
    )
    def get_network_appliance_firewall_one_to_one_nat_rules(network_id: str):
        """
        Get 1:1 NAT rules for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            1:1 NAT rules configuration
        """
        try:
            rules = meraki_client.get_network_appliance_firewall_one_to_one_nat_rules(network_id)
            
            result = f"# 🔄 1:1 NAT Rules for Network {network_id}\n\n"
            
            rules_list = rules.get('rules', [])
            if not rules_list:
                result += "**No 1:1 NAT rules configured**\n"
                return result
            
            result += f"**Total Rules**: {len(rules_list)}\n\n"
            
            for i, rule in enumerate(rules_list, 1):
                result += f"## Rule {i}: {rule.get('name', 'Unnamed')}\n"
                result += f"- **Public IP**: {rule.get('publicIp', 'Unknown')}\n"
                result += f"- **LAN IP**: {rule.get('lanIp', 'Unknown')}\n"
                result += f"- **Uplink**: {rule.get('uplink', 'both')}\n"
                
                # Allowed inbound connections
                allowed = rule.get('allowedInbound', [])
                if allowed:
                    result += "- **Allowed Inbound**:\n"
                    for conn in allowed:
                        result += f"  - {conn.get('protocol', 'any')} ports {conn.get('destinationPorts', 'any')}"
                        if conn.get('allowedIps'):
                            result += f" from {conn['allowedIps']}"
                        result += "\n"
                else:
                    result += "- **Allowed Inbound**: All traffic\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving 1:1 NAT rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_one_to_one_nat_rules",
        description="🔄 Update 1:1 NAT mapping rules - Map public IPs to internal servers"
    )
    def update_network_appliance_firewall_one_to_one_nat_rules(
        network_id: str,
        rules: str
    ):
        """
        Update 1:1 NAT rules for a network.
        
        Args:
            network_id: Network ID
            rules: JSON string of rules array. Example:
                   '[{"name":"Web Server","publicIp":"1.2.3.4","lanIp":"192.168.1.10","uplink":"internet1","allowedInbound":[{"protocol":"tcp","destinationPorts":["80","443"]}]}]'
            
        Returns:
            Updated 1:1 NAT rules
        """
        try:
            import json
            
            # Parse rules
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid rules format. Must be valid JSON array"
            
            # Update rules
            result = meraki_client.update_network_appliance_firewall_one_to_one_nat_rules(
                network_id,
                rules=rules_list
            )
            
            # Format response
            response = f"# ✅ Updated 1:1 NAT Rules for Network {network_id}\n\n"
            
            updated_rules = result.get('rules', [])
            response += f"**Total Rules**: {len(updated_rules)}\n\n"
            
            for i, rule in enumerate(updated_rules, 1):
                response += f"## Rule {i}: {rule.get('name', 'Unnamed')}\n"
                response += f"- 🌐 **Public IP**: {rule.get('publicIp')} → **LAN IP**: {rule.get('lanIp')}\n"
                response += f"- **Uplink**: {rule.get('uplink', 'both')}\n"
                
                allowed = rule.get('allowedInbound', [])
                if allowed:
                    response += "- **Security**:\n"
                    for conn in allowed:
                        response += f"  - ✅ {conn.get('protocol', 'any').upper()} ports {conn.get('destinationPorts', 'any')}\n"
                else:
                    response += "- **Security**: ⚠️ All traffic allowed\n"
                
                response += "\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating 1:1 NAT rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_port_forwarding_rules",
        description="↪️ Get port forwarding rules"
    )
    def get_network_appliance_firewall_port_forwarding_rules(network_id: str):
        """
        Get port forwarding rules for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            Port forwarding rules configuration
        """
        try:
            rules = meraki_client.get_network_appliance_firewall_port_forwarding_rules(network_id)
            
            result = f"# ↪️ Port Forwarding Rules for Network {network_id}\n\n"
            
            rules_list = rules.get('rules', [])
            if not rules_list:
                result += "**No port forwarding rules configured**\n"
                return result
            
            result += f"**Total Rules**: {len(rules_list)}\n\n"
            
            for i, rule in enumerate(rules_list, 1):
                result += f"## Rule {i}: {rule.get('name', 'Unnamed')}\n"
                result += f"- **Protocol**: {rule.get('protocol', 'Unknown')}\n"
                result += f"- **Public Port**: {rule.get('publicPort', 'Unknown')}\n"
                result += f"- **LAN IP**: {rule.get('lanIp', 'Unknown')}\n"
                result += f"- **Local Port**: {rule.get('localPort', 'Unknown')}\n"
                result += f"- **Uplink**: {rule.get('uplink', 'both')}\n"
                
                if rule.get('allowedIps'):
                    result += f"- **Allowed IPs**: {', '.join(rule['allowedIps'])}\n"
                else:
                    result += "- **Allowed IPs**: Any\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving port forwarding rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_port_forwarding_rules",
        description="↪️ Update port forwarding rules - Forward ports to internal servers"
    )
    def update_network_appliance_firewall_port_forwarding_rules(
        network_id: str,
        rules: str
    ):
        """
        Update port forwarding rules for a network.
        
        Args:
            network_id: Network ID
            rules: JSON string of rules array. Example:
                   '[{"name":"RDP Server","protocol":"tcp","publicPort":"3389","lanIp":"192.168.1.10","localPort":"3389","uplink":"both","allowedIps":["1.2.3.4"]}]'
            
        Returns:
            Updated port forwarding rules
        """
        try:
            import json
            
            # Parse rules
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid rules format. Must be valid JSON array"
            
            # Update rules
            result = meraki_client.update_network_appliance_firewall_port_forwarding_rules(
                network_id,
                rules=rules_list
            )
            
            # Format response
            response = f"# ✅ Updated Port Forwarding Rules for Network {network_id}\n\n"
            
            updated_rules = result.get('rules', [])
            response += f"**Total Rules**: {len(updated_rules)}\n\n"
            
            for i, rule in enumerate(updated_rules, 1):
                response += f"## Rule {i}: {rule.get('name', 'Unnamed')}\n"
                response += f"- 📥 **{rule.get('protocol', '').upper()}** Port {rule.get('publicPort')} → {rule.get('lanIp')}:{rule.get('localPort')}\n"
                response += f"- **Uplink**: {rule.get('uplink', 'both')}\n"
                
                if rule.get('allowedIps'):
                    response += f"- **Security**: Only from {', '.join(rule['allowedIps'])}\n"
                else:
                    response += "- **Security**: ⚠️ Open to all IPs\n"
                
                response += "\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating port forwarding rules: {str(e)}"