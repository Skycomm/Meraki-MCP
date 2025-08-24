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
        name="get_network_appliance_content_filtering_categories",
        description="📋 Get all available content filtering categories with IDs"
    )
    def get_network_appliance_content_filtering_categories(network_id: str):
        """
        Get all available content filtering categories for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of all available content filtering categories with their IDs
        """
        try:
            categories = meraki_client.get_network_appliance_content_filtering_categories(network_id)
            
            result = f"# 📋 Content Filtering Categories for Network {network_id}\n\n"
            
            # Group categories by type if available
            if 'categories' in categories:
                cat_list = categories['categories']
                result += f"**Total Categories**: {len(cat_list)}\n\n"
                
                # Separate security-related categories
                security_keywords = ['malware', 'phishing', 'spam', 'threat', 'illegal', 'fraud', 
                                   'exploit', 'virus', 'trojan', 'spyware', 'adware', 'botnet',
                                   'proxy', 'tor', 'crypto', 'hack']
                
                security_cats = []
                other_cats = []
                
                for cat in cat_list:
                    cat_name = cat.get('name', '').lower()
                    if any(keyword in cat_name for keyword in security_keywords):
                        security_cats.append(cat)
                    else:
                        other_cats.append(cat)
                
                # Show security categories first
                if security_cats:
                    result += "## 🔒 Security Categories\n"
                    for cat in security_cats:
                        result += f"- **{cat.get('name')}**: `{cat.get('id')}`\n"
                    result += "\n"
                
                # Show other categories
                if other_cats:
                    result += "## 📂 Other Categories\n"
                    for cat in other_cats:
                        result += f"- **{cat.get('name')}**: `{cat.get('id')}`\n"
            else:
                # Fallback format
                result += str(categories)
            
            return result
            
        except Exception as e:
            return f"❌ Error getting content filtering categories: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_ports",
        description="🔌 Get MX appliance port VLAN configuration with enhanced details"
    )
    def get_network_appliance_ports(network_id: str):
        """
        Get per-port VLAN settings for all ports of a MX appliance with enhanced information.
        Now includes VLAN details and client counts.
        
        Args:
            network_id: Network ID
            
        Returns:
            Enhanced port VLAN configuration with additional context
        """
        try:
            ports = meraki_client.get_network_appliance_ports(network_id)
            
            result = f"# 🔌 MX Appliance Port Configuration\n"
            result += f"**Network**: {network_id}\n\n"
            
            if not ports:
                result += "No port configuration found.\n"
                return result
            
            # Get VLANs for additional context
            vlans_dict = {}
            try:
                vlans = meraki_client.get_network_vlans(network_id)
                for vlan in vlans:
                    vlans_dict[str(vlan.get('id', ''))] = vlan
            except:
                pass
            
            # Get client count per VLAN
            vlan_client_counts = {}
            try:
                clients = meraki_client.get_network_clients(network_id, timespan=86400)
                for client in clients:
                    vlan_id = str(client.get('vlan', ''))
                    vlan_client_counts[vlan_id] = vlan_client_counts.get(vlan_id, 0) + 1
            except:
                pass
            
            # Summary section
            enabled_ports = sum(1 for p in ports if p.get('enabled', False))
            trunk_ports = sum(1 for p in ports if p.get('type') == 'trunk')
            access_ports = sum(1 for p in ports if p.get('type') == 'access')
            
            result += "## 📊 Summary\n"
            result += f"- **Total Ports**: {len(ports)}\n"
            result += f"- **Enabled**: {enabled_ports} ports\n"
            result += f"- **Trunk Ports**: {trunk_ports}\n"
            result += f"- **Access Ports**: {access_ports}\n\n"
            
            # Port details with enhanced information
            result += "## 🔧 Port Details\n\n"
            
            for port in ports:
                port_num = port.get('number', 'Unknown')
                vlan_id = str(port.get('vlan', ''))
                port_type = port.get('type', '')
                
                # Port header with status
                result += f"### Port {port_num}"
                if not port.get('enabled', False):
                    result += " ⚠️ **DISABLED**"
                result += "\n"
                
                # Configuration
                result += f"- **Status**: {'✅ Enabled' if port.get('enabled', False) else '❌ Disabled'}\n"
                result += f"- **Type**: {port_type}\n"
                
                # VLAN configuration
                if port_type == 'access':
                    result += f"- **Access VLAN**: {vlan_id}"
                    # Add VLAN name if available
                    if vlan_id in vlans_dict:
                        result += f" ({vlans_dict[vlan_id].get('name', 'Unknown')})"
                    # Add client count
                    client_count = vlan_client_counts.get(vlan_id, 0)
                    result += f" - **{client_count} devices**"
                    result += "\n"
                elif port_type == 'trunk':
                    result += f"- **Native VLAN**: {vlan_id}"
                    if vlan_id in vlans_dict:
                        result += f" ({vlans_dict[vlan_id].get('name', 'Unknown')})"
                    result += "\n"
                    
                    allowed_vlans = port.get('allowedVlans', 'all')
                    result += f"- **Allowed VLANs**: {allowed_vlans}\n"
                    
                    # Show client count for trunk ports
                    if allowed_vlans == 'all':
                        total_clients = sum(vlan_client_counts.values())
                        result += f"- **Total Devices**: {total_clients} across all VLANs\n"
                    else:
                        # Count clients on allowed VLANs
                        allowed_list = [vlan_id] + allowed_vlans.split(',') if allowed_vlans else [vlan_id]
                        trunk_clients = sum(vlan_client_counts.get(v, 0) for v in allowed_list)
                        result += f"- **Total Devices**: {trunk_clients} on allowed VLANs\n"
                
                # Additional settings
                if port.get('dropUntaggedTraffic'):
                    result += f"- **Drop Untagged**: ✅ Yes\n"
                
                # Add VLAN subnet info if available
                if vlan_id in vlans_dict:
                    vlan = vlans_dict[vlan_id]
                    if vlan.get('subnet'):
                        result += f"- **Subnet**: {vlan['subnet']}\n"
                
                result += "\n"
            
            # VLAN summary section
            if vlans_dict:
                result += "## 🏷️ VLAN Summary\n"
                for vlan_id, vlan in sorted(vlans_dict.items()):
                    client_count = vlan_client_counts.get(vlan_id, 0)
                    result += f"- **VLAN {vlan_id}** - {vlan.get('name', 'Unknown')}: "
                    result += f"{vlan.get('subnet', 'No subnet')} "
                    result += f"({client_count} devices)\n"
                result += "\n"
            
            # Helpful tips
            result += "## 💡 Helpful Commands\n"
            result += "- **See all details for a port**: `get_port_comprehensive_status` - Shows connected devices, IPs, and activity\n"
            result += "- **Check specific port**: `get_port_comprehensive_status network_id: \"..\" port_number: \"4\"`\n"
            result += "- **Modify port**: `update_network_appliance_port`\n"
            result += "- **View all clients**: `get_network_clients`\n"
            result += "- **Check events**: `get_network_events` - Look for 'carrier change' events\n"
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg:
                return f"❌ This network does not have an MX appliance or does not support port configuration."
            else:
                return f"❌ Error getting appliance ports: {error_msg}"
    
    @app.tool(
        name="update_network_appliance_port",
        description="🔌 Update MX appliance port VLAN configuration"
    )
    def update_network_appliance_port(
        network_id: str, 
        port_id: str,
        enabled: bool = None,
        vlan: int = None,
        type: str = None,
        allowed_vlans: str = None,
        drop_untagged_traffic: bool = None
    ):
        """
        Update per-port VLAN settings for a single MX port.
        
        ⚠️ WARNING: Due to Meraki API behavior, when only updating 'enabled' state,
        other settings may be reset to defaults. Use 'toggle_network_appliance_port' 
        instead for safely enabling/disabling ports without losing VLAN configuration.
        
        Args:
            network_id: Network ID
            port_id: Port ID (e.g., '1', '2', etc.)
            enabled: Whether port is enabled
            vlan: VLAN number for access port or native VLAN for trunk
            type: Port type ('access' or 'trunk')
            allowed_vlans: Comma-separated VLAN IDs or 'all' (trunk only)
            drop_untagged_traffic: Drop untagged traffic (trunk only)
            
        Returns:
            Updated port configuration
        """
        try:
            kwargs = {}
            
            if enabled is not None:
                kwargs['enabled'] = enabled
                
            if vlan is not None:
                kwargs['vlan'] = vlan
                
            if type is not None:
                if type not in ['access', 'trunk']:
                    return f"❌ Invalid port type '{type}'. Must be 'access' or 'trunk'"
                kwargs['type'] = type
                
            if allowed_vlans is not None:
                kwargs['allowedVlans'] = allowed_vlans
                
            if drop_untagged_traffic is not None:
                kwargs['dropUntaggedTraffic'] = drop_untagged_traffic
            
            # Update the port
            result = meraki_client.update_network_appliance_port(network_id, port_id, **kwargs)
            
            # Format response
            response = f"# ✅ Updated MX Port Configuration\n\n"
            response += f"**Network**: {network_id}\n"
            response += f"**Port**: {port_id}\n\n"
            
            response += "## New Configuration\n"
            response += f"- **Enabled**: {'✅' if result.get('enabled', False) else '❌'}\n"
            response += f"- **Type**: {result.get('type', 'Unknown')}\n"
            
            port_type = result.get('type', '')
            if port_type == 'access':
                response += f"- **Access VLAN**: {result.get('vlan', 'Unknown')}\n"
            elif port_type == 'trunk':
                response += f"- **Native VLAN**: {result.get('vlan', 'Unknown')}\n"
                response += f"- **Allowed VLANs**: {result.get('allowedVlans', 'all')}\n"
                if result.get('dropUntaggedTraffic'):
                    response += f"- **Drop Untagged Traffic**: ✅\n"
            
            response += "\n💡 **Note**: Port status (up/down) changes will appear in the network event log.\n"
            
            # Add warning if only enabled was changed
            if len(kwargs) == 1 and 'enabled' in kwargs:
                response += "\n⚠️ **Warning**: Only 'enabled' was updated. If VLAN settings were lost, "
                response += "use 'toggle_network_appliance_port' instead to preserve configuration.\n"
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg:
                return f"❌ Invalid configuration or this network does not have an MX appliance."
            elif "404" in error_msg:
                return f"❌ Port {port_id} not found on this MX appliance."
            else:
                return f"❌ Error updating appliance port: {error_msg}"
    
    @app.tool(
        name="get_network_appliance_port",
        description="🔌 Get configuration for a single MX appliance port"
    )
    def get_network_appliance_port(network_id: str, port_id: str):
        """
        Get configuration for a specific MX appliance port.
        
        Args:
            network_id: Network ID
            port_id: Port ID (e.g., '1', '2', etc.)
            
        Returns:
            Port configuration details
        """
        try:
            # Get all ports
            ports = meraki_client.get_network_appliance_ports(network_id)
            
            # Find the specific port
            port = None
            for p in ports:
                if str(p.get('number', '')) == str(port_id):
                    port = p
                    break
            
            if not port:
                return f"❌ Port {port_id} not found on this MX appliance."
            
            # Format the response
            result = f"# 🔌 MX Port {port_id} Configuration\n\n"
            result += f"**Network**: {network_id}\n\n"
            
            result += "## Current Settings\n"
            result += f"- **Enabled**: {'✅' if port.get('enabled', False) else '❌'}\n"
            result += f"- **Type**: {port.get('type', 'Unknown')}\n"
            
            port_type = port.get('type', '')
            if port_type == 'access':
                result += f"- **Access VLAN**: {port.get('vlan', 'Unknown')}\n"
            elif port_type == 'trunk':
                result += f"- **Native VLAN**: {port.get('vlan', 'Unknown')}\n"
                result += f"- **Allowed VLANs**: {port.get('allowedVlans', 'all')}\n"
                if port.get('dropUntaggedTraffic'):
                    result += f"- **Drop Untagged Traffic**: ✅\n"
                else:
                    result += f"- **Drop Untagged Traffic**: ❌\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error getting appliance port: {str(e)}"
    
    @app.tool(
        name="toggle_network_appliance_port",
        description="🔄 Safely enable/disable MX port without losing VLAN configuration"
    )
    def toggle_network_appliance_port(network_id: str, port_id: str, enabled: bool):
        """
        Safely toggle MX port enable/disable state while preserving all VLAN settings.
        This function prevents the known issue where VLAN configuration is lost when
        toggling port states.
        
        Args:
            network_id: Network ID
            port_id: Port ID (e.g., '1', '2', etc.)
            enabled: True to enable, False to disable
            
        Returns:
            Updated port configuration with preserved settings
        """
        try:
            # Step 1: Get current port configuration
            ports = meraki_client.get_network_appliance_ports(network_id)
            
            # Find the specific port
            current_port = None
            for p in ports:
                if str(p.get('number', '')) == str(port_id):
                    current_port = p
                    break
            
            if not current_port:
                return f"❌ Port {port_id} not found on this MX appliance."
            
            # Step 2: Build update parameters with ALL current settings
            kwargs = {
                'enabled': enabled,
                'type': current_port.get('type', 'access'),
                'vlan': current_port.get('vlan', 1)
            }
            
            # Add trunk-specific settings if applicable
            if current_port.get('type') == 'trunk':
                if 'allowedVlans' in current_port:
                    kwargs['allowedVlans'] = current_port['allowedVlans']
                if 'dropUntaggedTraffic' in current_port:
                    kwargs['dropUntaggedTraffic'] = current_port['dropUntaggedTraffic']
            
            # Step 3: Update the port with all settings preserved
            result = meraki_client.update_network_appliance_port(network_id, port_id, **kwargs)
            
            # Format response
            action = "enabled" if enabled else "disabled"
            response = f"# ✅ Port {port_id} safely {action}\n\n"
            response += f"**Network**: {network_id}\n\n"
            
            response += "## Configuration Status\n"
            response += f"- **Port State**: {'✅ Enabled' if result.get('enabled', False) else '❌ Disabled'}\n"
            response += f"- **Type**: {result.get('type', 'Unknown')}\n"
            
            port_type = result.get('type', '')
            if port_type == 'access':
                response += f"- **Access VLAN**: {result.get('vlan', 'Unknown')} ✅ Preserved\n"
            elif port_type == 'trunk':
                response += f"- **Native VLAN**: {result.get('vlan', 'Unknown')} ✅ Preserved\n"
                response += f"- **Allowed VLANs**: {result.get('allowedVlans', 'all')} ✅ Preserved\n"
                if result.get('dropUntaggedTraffic'):
                    response += f"- **Drop Untagged Traffic**: ✅ Preserved\n"
            
            response += f"\n💡 **All VLAN settings have been preserved during the {action} operation.**\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error toggling appliance port: {str(e)}"
    
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
        description="🚨 Get security threats detected - IDS/IPS blocks, malware detections, intrusion attempts, blocked attacks"
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
    
    @app.tool(
        name="get_network_appliance_vlans",
        description="🏷️ Get VLANs configured on the MX appliance with client details"
    )
    def get_network_appliance_vlans(network_id: str):
        """
        Get all VLANs configured on the MX appliance with enhanced client information.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of VLANs with configuration and connected devices
        """
        try:
            vlans = meraki_client.get_network_vlans(network_id)
            
            result = f"# 🏷️ VLANs for Network {network_id}\n\n"
            
            if not vlans:
                result += "**No VLANs configured**\n"
                result += "\n💡 **Tip**: By default, all traffic uses VLAN 1. Create additional VLANs to segment your network.\n"
                return result
            
            # Get client information
            clients_by_vlan = {}
            total_clients = 0
            try:
                clients = meraki_client.get_network_clients(network_id, timespan=86400)
                for client in clients:
                    vlan_id = str(client.get('vlan', ''))
                    if vlan_id not in clients_by_vlan:
                        clients_by_vlan[vlan_id] = []
                    clients_by_vlan[vlan_id].append(client)
                    total_clients += 1
            except:
                pass
            
            result += f"**Total VLANs**: {len(vlans)}\n"
            result += f"**Total Connected Devices**: {total_clients}\n\n"
            
            for vlan in vlans:
                vlan_id = str(vlan.get('id', 'Unknown'))
                vlan_name = vlan.get('name', f'VLAN {vlan_id}')
                vlan_clients = clients_by_vlan.get(vlan_id, [])
                
                result += f"## VLAN {vlan_id}: {vlan_name} ({len(vlan_clients)} devices)\n"
                
                # Network configuration
                subnet = vlan.get('subnet', 'Not configured')
                result += f"- **Subnet**: {subnet}\n"
                result += f"- **MX IP**: {vlan.get('applianceIp', 'Not configured')}\n"
                
                # Calculate and show IP range
                if subnet and subnet != 'Not configured':
                    try:
                        import ipaddress
                        network = ipaddress.ip_network(subnet)
                        hosts = list(network.hosts())
                        if hosts:
                            result += f"- **Usable IPs**: {hosts[0]} - {hosts[-1]} ({len(hosts)} total)\n"
                    except:
                        pass
                
                # DHCP settings
                dhcp_handling = vlan.get('dhcpHandling', 'Run a DHCP server')
                result += f"- **DHCP**: {dhcp_handling}\n"
                
                if dhcp_handling == 'Run a DHCP server':
                    result += f"  - **Lease Time**: {vlan.get('dhcpLeaseTime', '1 day')}\n"
                    result += f"  - **Boot Options**: {'✅' if vlan.get('dhcpBootOptionsEnabled') else '❌'}\n"
                    
                    # DHCP options
                    dhcp_options = vlan.get('dhcpOptions', [])
                    if dhcp_options:
                        result += "  - **DHCP Options**:\n"
                        for opt in dhcp_options:
                            result += f"    - Code {opt.get('code')}: {opt.get('type')} = {opt.get('value')}\n"
                
                # DNS servers
                dns_servers = vlan.get('dnsNameservers', '')
                if dns_servers and dns_servers != 'upstream_dns':
                    result += f"- **DNS Servers**: {dns_servers}\n"
                
                # Reserved IP ranges
                reserved = vlan.get('reservedIpRanges', [])
                if reserved:
                    result += "- **Reserved IP Ranges**:\n"
                    for r in reserved:
                        result += f"  - {r.get('start')} - {r.get('end')}: {r.get('comment', 'No comment')}\n"
                
                # Fixed IP assignments
                fixed = vlan.get('fixedIpAssignments', {})
                if fixed:
                    result += f"- **Fixed IP Assignments**: {len(fixed)} devices\n"
                    # Show first few fixed assignments
                    for mac, ip_info in list(fixed.items())[:3]:
                        result += f"  - {mac}: {ip_info.get('ip', 'Unknown')}"
                        if ip_info.get('name'):
                            result += f" ({ip_info['name']})"
                        result += "\n"
                    if len(fixed) > 3:
                        result += f"  - ... and {len(fixed) - 3} more\n"
                
                # Show connected devices
                if vlan_clients:
                    result += f"\n### 📱 Active Devices on VLAN {vlan_id}\n"
                    # Show top devices by usage
                    vlan_clients_sorted = sorted(vlan_clients, 
                                               key=lambda c: c.get('usage', {}).get('recv', 0) + c.get('usage', {}).get('sent', 0), 
                                               reverse=True)
                    
                    for client in vlan_clients_sorted[:5]:
                        result += f"- **{client.get('description', 'Unknown Device')}**\n"
                        result += f"  - IP: `{client.get('ip', 'No IP')}`\n"
                        result += f"  - MAC: `{client.get('mac', 'Unknown')}`\n"
                        if client.get('usage'):
                            sent_mb = client['usage'].get('sent', 0) / 1024 / 1024
                            recv_mb = client['usage'].get('recv', 0) / 1024 / 1024
                            result += f"  - Usage: ↑ {sent_mb:.1f} MB / ↓ {recv_mb:.1f} MB\n"
                    
                    if len(vlan_clients) > 5:
                        result += f"\n... and {len(vlan_clients) - 5} more devices\n"
                else:
                    result += "\n*No active devices on this VLAN*\n"
                
                result += "\n"
            
            # Summary section
            result += "## 💡 Quick Actions\n"
            result += "- **Create VLAN**: `create_network_appliance_vlan`\n"
            result += "- **Update VLAN**: `update_network_appliance_vlan`\n"
            result += "- **Check port assignments**: `get_network_appliance_ports`\n"
            result += "- **View detailed port status**: `get_port_comprehensive_status`\n"
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg:
                return f"❌ This network does not have VLANs enabled. VLANs are only available on MX appliances."
            else:
                return f"❌ Error getting VLANs: {error_msg}"
    
    @app.tool(
        name="create_network_appliance_vlan",
        description="🏷️ Create a new VLAN on the MX appliance"
    )
    def create_network_appliance_vlan(
        network_id: str,
        vlan_id: int,
        name: str,
        subnet: str,
        appliance_ip: str = None
    ):
        """
        Create a new VLAN on the MX appliance.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID (1-4094)
            name: VLAN name
            subnet: Subnet in CIDR format (e.g., '192.168.10.0/24')
            appliance_ip: MX IP address in this VLAN (defaults to first usable IP)
            
        Returns:
            Created VLAN configuration
        """
        try:
            # Validate VLAN ID
            if not 1 <= vlan_id <= 4094:
                return f"❌ Invalid VLAN ID {vlan_id}. Must be between 1 and 4094."
            
            kwargs = {
                'id': str(vlan_id),
                'name': name,
                'subnet': subnet
            }
            
            if appliance_ip:
                kwargs['applianceIp'] = appliance_ip
            else:
                # Default to first usable IP in subnet
                import ipaddress
                network = ipaddress.ip_network(subnet)
                kwargs['applianceIp'] = str(list(network.hosts())[0])
            
            # Create VLAN
            result = meraki_client.dashboard.appliance.createNetworkApplianceVlan(network_id, **kwargs)
            
            # Format response
            response = f"# ✅ Created VLAN {vlan_id}\n\n"
            response += f"**Name**: {result.get('name')}\n"
            response += f"**Subnet**: {result.get('subnet')}\n"
            response += f"**MX IP**: {result.get('applianceIp')}\n"
            response += f"**DHCP**: {result.get('dhcpHandling', 'Run a DHCP server')}\n"
            
            response += "\n💡 **Next Steps**:\n"
            response += "- Configure DHCP options if needed\n"
            response += "- Assign ports to this VLAN\n"
            response += "- Configure firewall rules between VLANs\n"
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            if "already exists" in error_msg.lower():
                return f"❌ VLAN {vlan_id} already exists in this network."
            elif "400" in error_msg:
                return f"❌ Invalid configuration: {error_msg}"
            else:
                return f"❌ Error creating VLAN: {error_msg}"
    
    @app.tool(
        name="update_network_appliance_vlan",
        description="🏷️ Update VLAN configuration on the MX appliance"
    )
    def update_network_appliance_vlan(
        network_id: str,
        vlan_id: int,
        name: str = None,
        subnet: str = None,
        appliance_ip: str = None,
        dhcp_handling: str = None,
        dhcp_lease_time: str = None,
        dns_nameservers: str = None,
        fixed_ip_assignments: str = None
    ):
        """
        Update VLAN configuration on the MX appliance.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID to update
            name: New VLAN name
            subnet: New subnet in CIDR format
            appliance_ip: New MX IP address
            dhcp_handling: 'Run a DHCP server', 'Relay DHCP to another server', or 'Do not respond to DHCP requests'
            dhcp_lease_time: DHCP lease time (e.g., '1 day', '12 hours')
            dns_nameservers: Custom DNS servers (comma-separated) or 'upstream_dns'
            fixed_ip_assignments: JSON string of DHCP reservations, e.g.:
                '{"aa:bb:cc:dd:ee:ff": {"ip": "192.168.1.100", "name": "Server"}}'
            
        Returns:
            Updated VLAN configuration
        """
        try:
            kwargs = {}
            
            if name is not None:
                kwargs['name'] = name
            if subnet is not None:
                kwargs['subnet'] = subnet
            if appliance_ip is not None:
                kwargs['applianceIp'] = appliance_ip
            if dhcp_handling is not None:
                kwargs['dhcpHandling'] = dhcp_handling
            if dhcp_lease_time is not None:
                kwargs['dhcpLeaseTime'] = dhcp_lease_time
            if dns_nameservers is not None:
                kwargs['dnsNameservers'] = dns_nameservers
            
            if fixed_ip_assignments is not None:
                try:
                    import json
                    # Parse the JSON string
                    fixed_ips = json.loads(fixed_ip_assignments)
                    kwargs['fixedIpAssignments'] = fixed_ips
                except json.JSONDecodeError:
                    return "❌ Invalid fixed_ip_assignments format. Must be valid JSON."
            
            # Update VLAN
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVlan(
                network_id, 
                str(vlan_id), 
                **kwargs
            )
            
            # Format response
            response = f"# ✅ Updated VLAN {vlan_id}\n\n"
            response += "## New Configuration\n"
            response += f"- **Name**: {result.get('name')}\n"
            response += f"- **Subnet**: {result.get('subnet')}\n"
            response += f"- **MX IP**: {result.get('applianceIp')}\n"
            response += f"- **DHCP**: {result.get('dhcpHandling')}\n"
            
            if result.get('dhcpHandling') == 'Run a DHCP server':
                response += f"- **DHCP Lease Time**: {result.get('dhcpLeaseTime', '1 day')}\n"
            
            dns = result.get('dnsNameservers')
            if dns and dns != 'upstream_dns':
                response += f"- **DNS Servers**: {dns}\n"
            
            # Show fixed IP assignments if any
            fixed = result.get('fixedIpAssignments', {})
            if fixed:
                response += f"\n## Fixed IP Assignments ({len(fixed)} total)\n"
                for mac, ip_info in fixed.items():
                    response += f"- **{mac}**: {ip_info.get('ip')} - {ip_info.get('name', 'No name')}\n"
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                return f"❌ VLAN {vlan_id} not found in this network."
            else:
                return f"❌ Error updating VLAN: {error_msg}"
    
    @app.tool(
        name="delete_network_appliance_vlan",
        description="🏷️ Delete a VLAN from the MX appliance"
    )
    def delete_network_appliance_vlan(network_id: str, vlan_id: int):
        """
        Delete a VLAN from the MX appliance.
        WARNING: This will remove all devices from this VLAN!
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID to delete
            
        Returns:
            Deletion confirmation
        """
        try:
            # Cannot delete VLAN 1
            if vlan_id == 1:
                return "❌ Cannot delete VLAN 1 (default VLAN)"
            
            # Delete VLAN
            meraki_client.dashboard.appliance.deleteNetworkApplianceVlan(
                network_id,
                str(vlan_id)
            )
            
            return f"""✅ VLAN {vlan_id} deleted successfully!

⚠️ **Impact**:
- All devices on this VLAN have been moved to the default VLAN
- Any port assignments to this VLAN have been reset
- Related firewall rules may need to be updated"""
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                return f"❌ VLAN {vlan_id} not found in this network."
            elif "400" in error_msg:
                return f"❌ Cannot delete VLAN: {error_msg}"
            else:
                return f"❌ Error deleting VLAN: {error_msg}"
    
    @app.tool(
        name="add_dhcp_reservation",
        description="📌 Add a DHCP reservation (fixed IP assignment) to a VLAN"
    )
    def add_dhcp_reservation(
        network_id: str,
        vlan_id: int,
        mac_address: str,
        ip_address: str,
        name: str = None
    ):
        """
        Add a DHCP reservation to assign a fixed IP to a specific MAC address.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID where the reservation should be added
            mac_address: MAC address of the device (format: aa:bb:cc:dd:ee:ff)
            ip_address: IP address to reserve
            name: Optional name for the reservation
            
        Returns:
            Success message with updated DHCP reservations
        """
        try:
            # Normalize MAC address format
            mac_address = mac_address.lower().replace('-', ':')
            
            # Validate MAC address format
            import re
            if not re.match(r'^([0-9a-f]{2}:){5}[0-9a-f]{2}$', mac_address):
                return f"❌ Invalid MAC address format: {mac_address}. Use format: aa:bb:cc:dd:ee:ff"
            
            # Get current VLAN configuration
            current_vlan = None
            vlans = meraki_client.get_network_vlans(network_id)
            for vlan in vlans:
                if str(vlan.get('id')) == str(vlan_id):
                    current_vlan = vlan
                    break
            
            if not current_vlan:
                return f"❌ VLAN {vlan_id} not found in network {network_id}"
            
            # Get current fixed IP assignments
            current_fixed = current_vlan.get('fixedIpAssignments', {})
            
            # Check if this MAC already has a reservation
            if mac_address in current_fixed:
                existing = current_fixed[mac_address]
                return f"⚠️ MAC {mac_address} already has a reservation: {existing.get('ip')} ({existing.get('name', 'No name')})"
            
            # Validate IP is within VLAN subnet
            import ipaddress
            try:
                subnet = current_vlan.get('subnet')
                if subnet:
                    network = ipaddress.ip_network(subnet)
                    ip = ipaddress.ip_address(ip_address)
                    if ip not in network:
                        return f"❌ IP {ip_address} is not within VLAN {vlan_id} subnet ({subnet})"
            except:
                pass  # Skip validation if there's an issue
            
            # Add the new reservation
            current_fixed[mac_address] = {
                'ip': ip_address,
                'name': name or f'Reserved for {mac_address}'
            }
            
            # Update the VLAN with new fixed IP assignments
            import json
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVlan(
                network_id,
                str(vlan_id),
                fixedIpAssignments=current_fixed
            )
            
            # Format response
            response = f"# ✅ DHCP Reservation Added Successfully!\n\n"
            response += f"**VLAN**: {vlan_id} ({current_vlan.get('name', 'Unknown')})\n"
            response += f"**MAC Address**: {mac_address}\n"
            response += f"**Reserved IP**: {ip_address}\n"
            response += f"**Name**: {name or 'Not specified'}\n\n"
            
            # Show all reservations
            all_fixed = result.get('fixedIpAssignments', {})
            if len(all_fixed) > 1:
                response += f"## All DHCP Reservations ({len(all_fixed)} total)\n"
                for mac, info in sorted(all_fixed.items()):
                    response += f"- **{mac}**: {info.get('ip')} - {info.get('name', 'No name')}\n"
            
            response += "\n💡 **Note**: The device will get the reserved IP on its next DHCP renewal.\n"
            response += "You may need to release/renew the lease or reboot the device.\n"
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg:
                return f"❌ Bad request: {error_msg}\nCheck that the IP address is valid and not already in use."
            else:
                return f"❌ Error adding DHCP reservation: {error_msg}"
    
    @app.tool(
        name="remove_dhcp_reservation",
        description="🗑️ Remove a DHCP reservation from a VLAN"
    )
    def remove_dhcp_reservation(
        network_id: str,
        vlan_id: int,
        mac_address: str
    ):
        """
        Remove a DHCP reservation for a specific MAC address.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID where the reservation exists
            mac_address: MAC address to remove reservation for
            
        Returns:
            Success message
        """
        try:
            # Normalize MAC address format
            mac_address = mac_address.lower().replace('-', ':')
            
            # Get current VLAN configuration
            current_vlan = None
            vlans = meraki_client.get_network_vlans(network_id)
            for vlan in vlans:
                if str(vlan.get('id')) == str(vlan_id):
                    current_vlan = vlan
                    break
            
            if not current_vlan:
                return f"❌ VLAN {vlan_id} not found in network {network_id}"
            
            # Get current fixed IP assignments
            current_fixed = current_vlan.get('fixedIpAssignments', {})
            
            # Check if this MAC has a reservation
            if mac_address not in current_fixed:
                return f"❌ No DHCP reservation found for MAC {mac_address} on VLAN {vlan_id}"
            
            # Store the old reservation info
            old_reservation = current_fixed[mac_address]
            
            # Remove the reservation
            del current_fixed[mac_address]
            
            # Update the VLAN
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVlan(
                network_id,
                str(vlan_id),
                fixedIpAssignments=current_fixed
            )
            
            # Format response
            response = f"# ✅ DHCP Reservation Removed\n\n"
            response += f"**VLAN**: {vlan_id} ({current_vlan.get('name', 'Unknown')})\n"
            response += f"**MAC Address**: {mac_address}\n"
            response += f"**Released IP**: {old_reservation.get('ip')}\n"
            response += f"**Name**: {old_reservation.get('name', 'No name')}\n\n"
            
            # Show remaining reservations
            remaining = result.get('fixedIpAssignments', {})
            if remaining:
                response += f"## Remaining Reservations ({len(remaining)} total)\n"
                for mac, info in sorted(remaining.items()):
                    response += f"- **{mac}**: {info.get('ip')} - {info.get('name', 'No name')}\n"
            else:
                response += "No DHCP reservations remaining on this VLAN.\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error removing DHCP reservation: {str(e)}"
    
    @app.tool(
        name="list_dhcp_reservations",
        description="📋 List all DHCP reservations for a VLAN"
    )
    def list_dhcp_reservations(network_id: str, vlan_id: int = None):
        """
        List all DHCP reservations (fixed IP assignments) for a VLAN or all VLANs.
        
        Args:
            network_id: Network ID
            vlan_id: Specific VLAN ID (optional, shows all if not specified)
            
        Returns:
            List of all DHCP reservations
        """
        try:
            vlans = meraki_client.get_network_vlans(network_id)
            
            if not vlans:
                return "No VLANs configured on this network."
            
            result = f"# 📋 DHCP Reservations\n"
            result += f"**Network**: {network_id}\n\n"
            
            total_reservations = 0
            
            for vlan in vlans:
                current_vlan_id = str(vlan.get('id'))
                
                # Skip if specific VLAN requested and this isn't it
                if vlan_id is not None and current_vlan_id != str(vlan_id):
                    continue
                
                fixed_ips = vlan.get('fixedIpAssignments', {})
                
                if fixed_ips:
                    result += f"## VLAN {current_vlan_id}: {vlan.get('name', 'Unknown')} ({len(fixed_ips)} reservations)\n"
                    result += f"**Subnet**: {vlan.get('subnet', 'Not configured')}\n\n"
                    
                    # Sort by IP address for easier reading
                    sorted_macs = sorted(fixed_ips.items(), key=lambda x: x[1].get('ip', ''))
                    
                    for mac, info in sorted_macs:
                        result += f"- **{mac}**\n"
                        result += f"  - IP: `{info.get('ip')}`\n"
                        result += f"  - Name: {info.get('name', 'No name')}\n"
                        total_reservations += 1
                    
                    result += "\n"
                elif vlan_id is not None:
                    result += f"## VLAN {current_vlan_id}: {vlan.get('name', 'Unknown')}\n"
                    result += "No DHCP reservations configured.\n\n"
            
            if vlan_id is not None and total_reservations == 0:
                result += "No DHCP reservations found for the specified VLAN.\n"
            elif vlan_id is None and total_reservations == 0:
                result += "No DHCP reservations configured on any VLAN.\n"
            else:
                result += f"**Total Reservations**: {total_reservations}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error listing DHCP reservations: {str(e)}"
    
    @app.tool(
        name="get_port_comprehensive_status",
        description="🔍 Get comprehensive status for an MX port including connected devices, VLANs, and activity"
    )
    def get_port_comprehensive_status(network_id: str, port_number: str = None):
        """
        Get comprehensive port status including configuration, connected clients, and VLAN details.
        This provides a complete picture of what's happening on a port.
        
        Args:
            network_id: Network ID
            port_number: Specific port number (optional, shows all if not specified)
            
        Returns:
            Comprehensive port status with clients, VLANs, and activity
        """
        try:
            result = f"# 🔍 Comprehensive MX Port Status\n"
            result += f"**Network**: {network_id}\n\n"
            
            # Get port configuration
            try:
                ports = meraki_client.get_network_appliance_ports(network_id)
            except Exception as e:
                return f"❌ This network does not have an MX appliance or port access is not available.\n\nError: {str(e)}"
            
            # Get all VLANs for reference
            vlans_dict = {}
            try:
                vlans = meraki_client.get_network_vlans(network_id)
                for vlan in vlans:
                    vlans_dict[str(vlan.get('id', ''))] = vlan
            except:
                vlans_dict = {}
            
            # Get all clients in the network
            all_clients = []
            try:
                all_clients = meraki_client.get_network_clients(network_id, timespan=86400)
            except:
                pass
            
            # Get recent events
            recent_events = []
            try:
                events = meraki_client.get_network_events(network_id, 
                                                         productType='appliance',
                                                         perPage=1000,
                                                         timespan=86400)
                # Filter for port-related events
                port_events = [e for e in events if 'port' in str(e).lower() or 'carrier' in str(e).lower()]
                recent_events = port_events[:10]  # Last 10 port events
            except:
                pass
            
            # Process each port
            port_found = False
            for port in ports:
                port_num = str(port.get('number', 'Unknown'))
                
                # If specific port requested, skip others
                if port_number and port_num != str(port_number):
                    continue
                    
                port_found = True
                
                result += f"## 🔌 Port {port_num}"
                if not port.get('enabled', False):
                    result += " (❌ DISABLED)"
                result += "\n\n"
                
                # Basic configuration
                result += "### Configuration\n"
                result += f"- **Status**: {'✅ Enabled' if port.get('enabled', False) else '❌ Disabled'}\n"
                result += f"- **Type**: {port.get('type', 'Unknown')}\n"
                
                port_type = port.get('type', '')
                vlan_id = str(port.get('vlan', ''))
                
                if port_type == 'access':
                    result += f"- **Access VLAN**: {vlan_id}\n"
                elif port_type == 'trunk':
                    result += f"- **Native VLAN**: {vlan_id}\n"
                    result += f"- **Allowed VLANs**: {port.get('allowedVlans', 'all')}\n"
                    if port.get('dropUntaggedTraffic'):
                        result += f"- **Drop Untagged**: ✅\n"
                
                # VLAN details
                if vlan_id in vlans_dict:
                    vlan = vlans_dict[vlan_id]
                    result += f"\n### VLAN {vlan_id} Details\n"
                    result += f"- **Name**: {vlan.get('name', 'Unknown')}\n"
                    result += f"- **Subnet**: {vlan.get('subnet', 'Not configured')}\n"
                    result += f"- **MX IP**: {vlan.get('applianceIp', 'Not configured')}\n"
                    result += f"- **DHCP**: {vlan.get('dhcpHandling', 'Unknown')}\n"
                    
                    # Calculate DHCP pool if subnet exists
                    if vlan.get('subnet'):
                        try:
                            import ipaddress
                            network = ipaddress.ip_network(vlan['subnet'])
                            first_ip = list(network.hosts())[0]
                            last_ip = list(network.hosts())[-1]
                            result += f"- **DHCP Pool**: {first_ip} - {last_ip}\n"
                        except:
                            pass
                
                # Find clients on this VLAN
                vlan_clients = []
                if port_type == 'access':
                    # For access ports, clients must be on the specific VLAN
                    vlan_clients = [c for c in all_clients if str(c.get('vlan', '')) == vlan_id]
                elif port_type == 'trunk':
                    # For trunk ports, show clients on native VLAN and any allowed VLANs
                    if port.get('allowedVlans') == 'all':
                        # All VLANs allowed - just show native VLAN clients
                        vlan_clients = [c for c in all_clients if str(c.get('vlan', '')) == vlan_id]
                    else:
                        # Specific VLANs allowed
                        allowed_vlans = [vlan_id]  # Include native VLAN
                        if port.get('allowedVlans'):
                            allowed_vlans.extend(port['allowedVlans'].split(','))
                        vlan_clients = [c for c in all_clients if str(c.get('vlan', '')) in allowed_vlans]
                
                # Display connected clients
                result += f"\n### 📱 Connected Devices ({len(vlan_clients)} found)\n"
                if vlan_clients:
                    # Group by VLAN for trunk ports
                    if port_type == 'trunk' and len(set(c.get('vlan', '') for c in vlan_clients)) > 1:
                        vlan_groups = {}
                        for client in vlan_clients:
                            client_vlan = str(client.get('vlan', 'Unknown'))
                            if client_vlan not in vlan_groups:
                                vlan_groups[client_vlan] = []
                            vlan_groups[client_vlan].append(client)
                        
                        for vlan_num, clients in sorted(vlan_groups.items()):
                            vlan_name = vlans_dict.get(vlan_num, {}).get('name', f'VLAN {vlan_num}')
                            result += f"\n#### VLAN {vlan_num} - {vlan_name} ({len(clients)} devices)\n"
                            for client in clients[:5]:  # Show first 5 per VLAN
                                result += f"- **{client.get('description', 'Unknown Device')}**\n"
                                result += f"  - IP: `{client.get('ip', 'No IP')}`\n"
                                result += f"  - MAC: `{client.get('mac', 'Unknown')}`\n"
                                result += f"  - Manufacturer: {client.get('manufacturer', 'Unknown')}\n"
                                if client.get('usage'):
                                    sent_mb = client['usage'].get('sent', 0) / 1024 / 1024
                                    recv_mb = client['usage'].get('recv', 0) / 1024 / 1024
                                    result += f"  - Usage: ↑ {sent_mb:.1f} MB / ↓ {recv_mb:.1f} MB\n"
                            if len(clients) > 5:
                                result += f"\n... and {len(clients) - 5} more devices on VLAN {vlan_num}\n"
                    else:
                        # Single VLAN or access port
                        for client in vlan_clients[:10]:  # Show first 10
                            result += f"- **{client.get('description', 'Unknown Device')}**\n"
                            result += f"  - IP: `{client.get('ip', 'No IP')}`\n"
                            result += f"  - MAC: `{client.get('mac', 'Unknown')}`\n"
                            result += f"  - VLAN: {client.get('vlan', 'Unknown')}\n"
                            result += f"  - Manufacturer: {client.get('manufacturer', 'Unknown')}\n"
                            if client.get('usage'):
                                sent_mb = client['usage'].get('sent', 0) / 1024 / 1024
                                recv_mb = client['usage'].get('recv', 0) / 1024 / 1024
                                result += f"  - Usage: ↑ {sent_mb:.1f} MB / ↓ {recv_mb:.1f} MB\n"
                        
                        if len(vlan_clients) > 10:
                            result += f"\n... and {len(vlan_clients) - 10} more devices\n"
                else:
                    result += "No active clients found on this port/VLAN.\n"
                    result += "\nPossible reasons:\n"
                    result += "- No devices currently connected\n"
                    result += "- Devices may be on a different VLAN\n"
                    result += "- Port may be physically disconnected\n"
                
                # Show recent port events
                port_specific_events = [e for e in recent_events if f'port{port_num}' in str(e).lower() or f'lan{port_num}' in str(e).lower()]
                if port_specific_events:
                    result += f"\n### 📊 Recent Port Events\n"
                    for event in port_specific_events[:5]:
                        result += f"- {event.get('occurredAt', 'Unknown time')}: {event.get('type', 'Unknown event')}\n"
                        if event.get('details'):
                            result += f"  Details: {event['details']}\n"
                
                result += "\n" + "="*60 + "\n\n"
            
            if port_number and not port_found:
                result += f"❌ Port {port_number} not found on this MX appliance.\n"
            
            # Add summary
            result += "### 💡 Quick Actions\n"
            result += "- To see port link status: Check dashboard or event logs for 'carrier change' events\n"
            result += "- To modify port: Use `update_network_appliance_port`\n"
            result += "- To check specific client: Use `get_network_clients` with MAC filter\n"
            result += "- To view DHCP leases: Check dashboard under Security & SD-WAN > DHCP\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error getting comprehensive port status: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_warm_spare",
        description="🔥 Get MX warm spare (high availability) configuration"
    )
    def get_network_appliance_warm_spare(network_id: str):
        """
        Get warm spare configuration for MX high availability.
        
        Args:
            network_id: Network ID
            
        Returns:
            Warm spare configuration details
        """
        try:
            warm_spare = meraki_client.dashboard.appliance.getNetworkApplianceWarmSpare(network_id)
            
            result = f"# 🔥 MX Warm Spare Configuration\n"
            result += f"**Network**: {network_id}\n\n"
            
            if not warm_spare.get('enabled'):
                result += "❌ **Warm Spare**: Disabled\n\n"
                result += "💡 **Note**: Enable warm spare for high availability failover.\n"
                return result
            
            result += "✅ **Warm Spare**: Enabled\n\n"
            
            # Primary MX
            primary_serial = warm_spare.get('primarySerial', 'Unknown')
            result += f"## Primary MX\n"
            result += f"- **Serial**: {primary_serial}\n"
            
            # Spare MX
            spare_serial = warm_spare.get('spareSerial', 'Not configured')
            result += f"\n## Spare MX\n"
            result += f"- **Serial**: {spare_serial}\n"
            
            # Uplink mode
            uplink_mode = warm_spare.get('uplinkMode', 'virtual')
            result += f"\n## Configuration\n"
            result += f"- **Uplink Mode**: {uplink_mode}\n"
            
            if uplink_mode == 'virtual':
                result += f"- **Virtual IP 1**: {warm_spare.get('virtualIp1', 'Not set')}\n"
                result += f"- **Virtual IP 2**: {warm_spare.get('virtualIp2', 'Not set')}\n"
            
            result += "\n## How It Works\n"
            result += "- Primary and spare share health info via VRRP\n"
            result += "- DHCP leases sync between units on UDP port 3483\n"
            result += "- Automatic failover when primary loses all uplinks\n"
            result += "- Stateful failover preserves client connections\n"
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg:
                return "❌ This network does not support warm spare (MX required)"
            else:
                return f"❌ Error getting warm spare config: {error_msg}"
    
    @app.tool(
        name="update_network_appliance_warm_spare",
        description="🔥 Update MX warm spare configuration"
    )
    def update_network_appliance_warm_spare(
        network_id: str,
        enabled: bool,
        spare_serial: str = None,
        uplink_mode: str = None,
        virtual_ip1: str = None,
        virtual_ip2: str = None
    ):
        """
        Update warm spare configuration for MX high availability.
        
        Args:
            network_id: Network ID
            enabled: Enable/disable warm spare
            spare_serial: Serial number of spare MX
            uplink_mode: 'virtual' or 'public'
            virtual_ip1: Virtual IP for WAN 1 (if using virtual mode)
            virtual_ip2: Virtual IP for WAN 2 (if using virtual mode)
            
        Returns:
            Updated warm spare configuration
        """
        try:
            kwargs = {'enabled': enabled}
            
            if spare_serial:
                kwargs['spareSerial'] = spare_serial
            if uplink_mode:
                if uplink_mode not in ['virtual', 'public']:
                    return "❌ Invalid uplink mode. Must be 'virtual' or 'public'"
                kwargs['uplinkMode'] = uplink_mode
            if virtual_ip1:
                kwargs['virtualIp1'] = virtual_ip1
            if virtual_ip2:
                kwargs['virtualIp2'] = virtual_ip2
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceWarmSpare(
                network_id, **kwargs
            )
            
            response = f"# ✅ Updated Warm Spare Configuration\n\n"
            response += f"**Status**: {'Enabled' if result.get('enabled') else 'Disabled'}\n"
            
            if result.get('enabled'):
                response += f"**Spare Serial**: {result.get('spareSerial', 'Not set')}\n"
                response += f"**Uplink Mode**: {result.get('uplinkMode', 'virtual')}\n"
                
                if result.get('uplinkMode') == 'virtual':
                    response += f"**Virtual IP 1**: {result.get('virtualIp1', 'Not set')}\n"
                    response += f"**Virtual IP 2**: {result.get('virtualIp2', 'Not set')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating warm spare: {str(e)}"
    
    @app.tool(
        name="swap_network_appliance_warm_spare",
        description="🔄 Swap primary and spare MX appliances"
    )
    def swap_network_appliance_warm_spare(network_id: str):
        """
        Swap the primary and warm spare MX appliances.
        This makes the current spare become the primary.
        
        Args:
            network_id: Network ID
            
        Returns:
            Swap confirmation
        """
        try:
            result = meraki_client.dashboard.appliance.swapNetworkApplianceWarmSpare(network_id)
            
            response = f"# ✅ MX Appliances Swapped!\n\n"
            response += f"**New Primary**: {result.get('primarySerial', 'Unknown')}\n"
            response += f"**New Spare**: {result.get('spareSerial', 'Unknown')}\n\n"
            response += "⚠️ **Note**: The swap may take a few minutes to complete.\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error swapping warm spare: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_vpn_site_to_site",
        description="🔐 Update site-to-site VPN configuration"
    )
    def update_network_appliance_vpn_site_to_site(
        network_id: str,
        mode: str,
        hubs: str = None,
        subnets: str = None
    ):
        """
        Update site-to-site VPN settings for the network.
        
        Args:
            network_id: Network ID
            mode: VPN mode - 'none', 'spoke', or 'hub'
            hubs: JSON array of hub networks (for spoke mode)
            subnets: JSON array of local subnets to advertise
            
        Returns:
            Updated VPN configuration
        """
        try:
            kwargs = {'mode': mode}
            
            if mode not in ['none', 'spoke', 'hub']:
                return "❌ Invalid mode. Must be 'none', 'spoke', or 'hub'"
            
            if hubs:
                import json
                try:
                    kwargs['hubs'] = json.loads(hubs)
                except:
                    return "❌ Invalid hubs format. Must be JSON array"
            
            if subnets:
                import json
                try:
                    kwargs['subnets'] = json.loads(subnets)
                except:
                    return "❌ Invalid subnets format. Must be JSON array"
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
                network_id, **kwargs
            )
            
            response = f"# ✅ Updated Site-to-Site VPN\n\n"
            response += f"**Mode**: {result.get('mode', 'none')}\n"
            
            if result.get('mode') == 'spoke':
                hubs_list = result.get('hubs', [])
                response += f"\n## Connected Hubs ({len(hubs_list)})\n"
                for hub in hubs_list:
                    response += f"- Hub ID: {hub.get('hubId', 'Unknown')}\n"
            
            subnets_list = result.get('subnets', [])
            if subnets_list:
                response += f"\n## Local Subnets ({len(subnets_list)})\n"
                for subnet in subnets_list:
                    response += f"- {subnet.get('localSubnet', 'Unknown')}"
                    if subnet.get('useVpn'):
                        response += " ✅ In VPN"
                    response += "\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating site-to-site VPN: {str(e)}"
    
    @app.tool(
        name="get_device_appliance_dhcp_subnets",
        description="📊 Get DHCP subnet information for an MX"
    )
    def get_device_appliance_dhcp_subnets(serial: str):
        """
        Get DHCP subnet information for a specific MX appliance.
        Shows DHCP pools and usage statistics.
        
        Args:
            serial: Device serial number
            
        Returns:
            DHCP subnet details and statistics
        """
        try:
            subnets = meraki_client.dashboard.appliance.getDeviceApplianceDhcpSubnets(serial)
            
            result = f"# 📊 DHCP Subnets for MX {serial}\n\n"
            
            if not subnets:
                result += "No DHCP subnet information available.\n"
                return result
            
            for subnet in subnets:
                vlan_id = subnet.get('vlanId', 'Unknown')
                result += f"## VLAN {vlan_id}\n"
                result += f"- **Subnet**: {subnet.get('subnet', 'Unknown')}\n"
                result += f"- **Mask**: {subnet.get('mask', 'Unknown')}\n"
                
                # Usage statistics
                used_count = subnet.get('usedCount', 0)
                free_count = subnet.get('freeCount', 0)
                total = used_count + free_count
                
                if total > 0:
                    usage_percent = (used_count / total) * 100
                    result += f"- **DHCP Usage**: {used_count}/{total} ({usage_percent:.1f}%)\n"
                    result += f"- **Free IPs**: {free_count}\n"
                
                # Status indicator
                if usage_percent >= 90:
                    result += "- **Status**: 🔴 Critical - Pool nearly exhausted!\n"
                elif usage_percent >= 75:
                    result += "- **Status**: 🟡 Warning - High usage\n"
                else:
                    result += "- **Status**: 🟢 Healthy\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg:
                return f"❌ Device {serial} is not an MX appliance"
            else:
                return f"❌ Error getting DHCP subnets: {error_msg}"
    
    @app.tool(
        name="get_network_appliance_static_routes",
        description="🛤️ Get static routes configured on the MX"
    )
    def get_network_appliance_static_routes(network_id: str):
        """
        Get static routes configured on the MX appliance.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of static routes
        """
        try:
            routes = meraki_client.dashboard.appliance.getNetworkApplianceStaticRoutes(network_id)
            
            result = f"# 🛤️ Static Routes for Network {network_id}\n\n"
            
            if not routes:
                result += "No static routes configured.\n"
                result += "\n💡 **Tip**: Static routes are used to direct traffic to specific subnets via custom gateways.\n"
                return result
            
            result += f"**Total Routes**: {len(routes)}\n\n"
            
            for i, route in enumerate(routes, 1):
                result += f"## Route {i}: {route.get('name', 'Unnamed')}\n"
                result += f"- **ID**: {route.get('id', 'Unknown')}\n"
                result += f"- **Subnet**: {route.get('subnet', 'Unknown')}\n"
                result += f"- **Gateway IP**: {route.get('gatewayIp', 'Unknown')}\n"
                
                # Gateway VLAN
                gateway_vlan = route.get('gatewayVlanId')
                if gateway_vlan:
                    result += f"- **Gateway VLAN**: {gateway_vlan}\n"
                
                result += f"- **Enabled**: {'✅' if route.get('enabled', True) else '❌'}\n"
                
                # Fixed IP assignments for this route
                fixed_ips = route.get('fixedIpAssignments', {})
                if fixed_ips:
                    result += f"- **Reserved IPs**: {len(fixed_ips)}\n"
                
                # Reserved IP ranges
                reserved = route.get('reservedIpRanges', [])
                if reserved:
                    result += "- **Reserved Ranges**:\n"
                    for r in reserved:
                        result += f"  - {r.get('start')} - {r.get('end')}: {r.get('comment', '')}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error getting static routes: {str(e)}"
    
    @app.tool(
        name="create_network_appliance_static_route",
        description="🛤️ Create a new static route on the MX"
    )
    def create_network_appliance_static_route(
        network_id: str,
        name: str,
        subnet: str,
        gateway_ip: str
    ):
        """
        Create a new static route on the MX appliance.
        
        Args:
            network_id: Network ID
            name: Name for the route
            subnet: Destination subnet in CIDR format
            gateway_ip: Next hop IP address
            
        Returns:
            Created route details
        """
        try:
            result = meraki_client.dashboard.appliance.createNetworkApplianceStaticRoute(
                network_id,
                name=name,
                subnet=subnet,
                gatewayIp=gateway_ip
            )
            
            response = f"# ✅ Static Route Created\n\n"
            response += f"**Name**: {result.get('name')}\n"
            response += f"**ID**: {result.get('id')}\n"
            response += f"**Subnet**: {result.get('subnet')}\n"
            response += f"**Gateway**: {result.get('gatewayIp')}\n"
            response += f"**Enabled**: {'✅' if result.get('enabled', True) else '❌'}\n"
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg:
                return f"❌ Invalid route configuration: {error_msg}"
            else:
                return f"❌ Error creating static route: {error_msg}"