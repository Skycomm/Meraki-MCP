"""
Security Appliance management tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

from typing import Optional
import json

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
    
    # Register additional appliance tools from backup
    register_additional_appliance_tools()

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
        description="🔥 Update Layer 3 firewall rules - Block/allow traffic by IP, port, protocol"
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
            src_cidr: Source CIDR (e.g., '192.168.1.0/24') or 'any'
            dest_cidr: Destination CIDR (e.g., '10.0.0.0/8') or 'any'
            dest_port: Destination port - Examples: '80', '443', '80-443', 'any' (optional)
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
            
            # Handle destination port - IMPORTANT: only add if not 'any' and protocol supports ports
            if dest_port and dest_port.lower() != 'any' and protocol.lower() in ['tcp', 'udp']:
                new_rule['destPort'] = dest_port
            elif protocol.lower() not in ['tcp', 'udp', 'any'] and dest_port:
                return f"❌ Cannot specify port for protocol '{protocol}'. Ports only work with TCP/UDP."
                
            # Add new rule to beginning (processed first)
            updated_rules = [new_rule] + existing_rules
            
            # Update firewall rules
            result = meraki_client.update_network_appliance_firewall_l3_rules(
                network_id,
                rules=updated_rules
            )
            
            # Build detailed response
            response = f"✅ Firewall rule added successfully!\n\n"
            response += f"**New Rule**: {comment}\n"
            response += f"**Policy**: {policy.upper()}\n"
            response += f"**Protocol**: {protocol}\n"
            response += f"**Source**: {src_cidr}\n"
            response += f"**Destination**: {dest_cidr}\n"
            if dest_port and dest_port.lower() != 'any' and protocol.lower() in ['tcp', 'udp']:
                response += f"**Port**: {dest_port}\n"
            response += f"\n**Total rules**: {len(updated_rules)}"
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            if "destPort" in error_msg:
                return f"❌ Port format error. Use: '80', '443', '80-443', or omit for any port\n{error_msg}"
            return f"❌ Error updating L3 firewall rules: {error_msg}"
    
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
            allowed_url_patterns: Comma-separated list of allowed URL patterns (e.g., "*.example.com,*.education.gov")
            blocked_url_patterns: Comma-separated list of blocked URL patterns (e.g., "*.gambling.com,*.adult.com")
            blocked_categories: Comma-separated list of categories to block. Can use:
                - Category IDs: "meraki:contentFiltering/category/1,meraki:contentFiltering/category/2"
                - Category numbers: "1,2,3"
                - Category names: "Adult and Pornography,Illegal Content"
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
                # Category name to ID mapping
                category_mapping = {
                    "adult and pornography": "meraki:contentFiltering/category/1",
                    "abortion": "meraki:contentFiltering/category/2",
                    "illegal content": "meraki:contentFiltering/category/3",
                    "illegal downloads": "meraki:contentFiltering/category/4",
                    "malware sites": "meraki:contentFiltering/category/5",
                    "phishing and other frauds": "meraki:contentFiltering/category/6",
                    "violence": "meraki:contentFiltering/category/7",
                    "gambling": "meraki:contentFiltering/category/8",
                    "hate and intolerance": "meraki:contentFiltering/category/9",
                    "recreational drugs": "meraki:contentFiltering/category/10",
                    "alcohol and tobacco": "meraki:contentFiltering/category/11",
                    "web advertisements": "meraki:contentFiltering/category/67",
                    "swimsuits and intimate apparel": "meraki:contentFiltering/category/68",
                    "sex education": "meraki:contentFiltering/category/69",
                    "social networking": "meraki:contentFiltering/category/70",
                    "file sharing": "meraki:contentFiltering/category/71",
                    "shopping": "meraki:contentFiltering/category/72",
                    "weapons": "meraki:contentFiltering/category/73",
                    "games": "meraki:contentFiltering/category/74",
                    "music": "meraki:contentFiltering/category/75",
                    "video and movies": "meraki:contentFiltering/category/76",
                    "reference and research": "meraki:contentFiltering/category/77",
                    "health and medicine": "meraki:contentFiltering/category/78",
                    "peer to peer": "meraki:contentFiltering/category/83"
                }
                
                category_ids = []
                for cat in blocked_categories.split(','):
                    cat = cat.strip()
                    
                    # If it's already a full ID, use it
                    if cat.startswith("meraki:contentFiltering/category/"):
                        category_ids.append(cat)
                    # If it's just a number, format it
                    elif cat.isdigit():
                        category_ids.append(f"meraki:contentFiltering/category/{cat}")
                    # Otherwise try to map the name
                    else:
                        cat_lower = cat.lower()
                        if cat_lower in category_mapping:
                            category_ids.append(category_mapping[cat_lower])
                        else:
                            # Try partial match
                            matched = False
                            for name, id in category_mapping.items():
                                if cat_lower in name or name in cat_lower:
                                    category_ids.append(id)
                                    matched = True
                                    break
                            if not matched:
                                return f"❌ Unknown category: '{cat}'. Use get_network_appliance_content_filtering_categories to see valid categories."
                
                kwargs['blockedUrlCategories'] = category_ids
            
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
        rules: str = None,
        block_countries: str = None,
        block_applications: str = None,
        block_categories: str = None
    ):
        """
        Update Layer 7 firewall rules for a network.
        
        Args:
            network_id: Network ID
            rules: (Optional) JSON string of custom rules array
            block_countries: (Optional) Comma-separated country codes to block (e.g., "CN,RU,KP")
            block_applications: (Optional) Comma-separated applications to block (e.g., "FACEBOOK,YOUTUBE")
            block_categories: (Optional) Comma-separated app categories to block (e.g., "SOCIAL_WEB_AND_PHOTO_SHARING")
            
        Returns:
            Updated L7 firewall rules
        """
        try:
            import json
            
            # If rules provided directly, use them
            if rules:
                try:
                    rules_list = json.loads(rules)
                except:
                    return "❌ Invalid rules format. Must be valid JSON array"
            else:
                # Build rules from simplified parameters
                rules_list = []
                
                # Add country blocking rules
                if block_countries:
                    countries = [c.strip().upper() for c in block_countries.split(',')]
                    rules_list.append({
                        "policy": "deny",
                        "type": "blacklistedCountries",
                        "value": {"countries": countries}
                    })
                
                # Add application blocking rules
                if block_applications:
                    for app in block_applications.split(','):
                        app_name = app.strip()
                        # Map common names to Meraki application IDs
                        app_mapping = {
                            "FACEBOOK": "meraki:layer7/application/68",
                            "YOUTUBE": "meraki:layer7/application/142",
                            "TWITTER": "meraki:layer7/application/141",
                            "INSTAGRAM": "meraki:layer7/application/189",
                            "NETFLIX": "meraki:layer7/application/209",
                            "BITTORRENT": "meraki:layer7/application/17",
                            "TOR": "meraki:layer7/application/169"
                        }
                        
                        # Use mapping or assume it's already an ID
                        app_id = app_mapping.get(app_name.upper(), app_name)
                        
                        rules_list.append({
                            "policy": "deny",
                            "type": "application",
                            "value": {"id": app_id}
                        })
                
                # Add category blocking rules
                if block_categories:
                    for cat in block_categories.split(','):
                        cat_name = cat.strip()
                        # Map common names to Meraki category IDs
                        cat_mapping = {
                            "SOCIAL_WEB_AND_PHOTO_SHARING": "meraki:layer7/category/7",
                            "PEER_TO_PEER": "meraki:layer7/category/14",
                            "ONLINE_GAMING": "meraki:layer7/category/8",
                            "ADULT_AND_PORNOGRAPHY": "meraki:layer7/category/1",
                            "ILLEGAL_CONTENT": "meraki:layer7/category/3"
                        }
                        
                        # Use mapping or assume it's already an ID
                        cat_id = cat_mapping.get(cat_name.upper(), cat_name)
                        
                        rules_list.append({
                            "policy": "deny",
                            "type": "applicationCategory",
                            "value": {"id": cat_id}
                        })
            
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
        per_page: int = 1000
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
    
    # @app.tool(
    # name="create_network_appliance_vlan",
    # description="🏷️ Create a NEW VLAN that doesn't exist yet (use update_network_appliance_vlan to modify existing VLANs)"
    # )
    # def create_network_appliance_vlan(
    # network_id: str,
    # vlan_id: int,
    # name: str,
    # subnet: str,
    # appliance_ip: str = None
    # ):
        # """
        # Create a new VLAN on the MX appliance.
        
        # Args:
            # network_id: Network ID
            # vlan_id: VLAN ID (1-4094)
            # name: VLAN name
            # subnet: Subnet in CIDR format (e.g., '192.168.10.0/24')
            # appliance_ip: MX IP address in this VLAN (defaults to first usable IP)
            
        # Returns:
            # Created VLAN configuration
        # """
    # try:
            # Validate VLAN ID
    # if not 1 <= vlan_id <= 4094:
    # return f"❌ Invalid VLAN ID {vlan_id}. Must be between 1 and 4094."
            
            # Check if VLAN already exists
    # try:
    # existing_vlans = meraki_client.dashboard.appliance.getNetworkApplianceVlans(network_id)
    # for vlan in existing_vlans:
    # if int(vlan.get('id', 0)) == vlan_id:
    # return f"""⚠️ VLAN {vlan_id} already exists!

# **Existing VLAN Details:**
# - Name: {vlan.get('name')}
# - Subnet: {vlan.get('subnet')}
# - MX IP: {vlan.get('applianceIp')}

# **To modify this VLAN, use:** `update_network_appliance_vlan` instead
# **To update DHCP ranges:** Include `reserved_ip_ranges` parameter

# Example to exclude IPs from DHCP:
# ```
# update_network_appliance_vlan(
#     network_id="{network_id}",
#     vlan_id={vlan_id},
#     reserved_ip_ranges='[{{"start": "X.X.X.1", "end": "X.X.X.99", "comment": "Reserved"}}]'
# )
# ```"""
    #         except:
    #             # If we can't check, proceed with creation
    #             pass
    #         
    #         kwargs = {
    #             'id': str(vlan_id),
    #             'name': name,
    #             'subnet': subnet
    # }
            
    # if appliance_ip:
    # kwargs['applianceIp'] = appliance_ip
    # else:
                # Default to first usable IP in subnet
    # import ipaddress
    # network = ipaddress.ip_network(subnet)
    # kwargs['applianceIp'] = str(list(network.hosts())[0])
            
            # Create VLAN
    # result = meraki_client.dashboard.appliance.createNetworkApplianceVlan(network_id, **kwargs)
            
            # Format response
    # response = f"# ✅ Created VLAN {vlan_id}\n\n"
    # response += f"**Name**: {result.get('name')}\n"
    # response += f"**Subnet**: {result.get('subnet')}\n"
    # response += f"**MX IP**: {result.get('applianceIp')}\n"
    # response += f"**DHCP**: {result.get('dhcpHandling', 'Run a DHCP server')}\n"
            
    # response += "\n💡 **Next Steps**:\n"
    # response += "- Configure DHCP options if needed\n"
    # response += "- Assign ports to this VLAN\n"
    # response += "- Configure firewall rules between VLANs\n"
            
    # return response
            
    # except Exception as e:
    # error_msg = str(e)
    # if "already exists" in error_msg.lower():
    # return f"❌ VLAN {vlan_id} already exists in this network."
    # elif "400" in error_msg:
    # return f"❌ Invalid configuration: {error_msg}"
    # else:
    # return f"❌ Error creating VLAN: {error_msg}"
    
    @app.tool(
        name="update_network_appliance_vlan",
        description="🏷️ Update/modify an EXISTING VLAN (including DHCP ranges, reserved IPs, etc). Use this for any changes to existing VLANs"
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
        fixed_ip_assignments: str = None,
        reserved_ip_ranges: str = None
    ):
        """
        Update VLAN configuration on the MX appliance.
        USE THIS to modify any existing VLAN including setting up DHCP exclusions.
        
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
            reserved_ip_ranges: JSON string of reserved IP ranges (excluded from DHCP), e.g.:
                '[{"start": "10.0.101.1", "end": "10.0.101.99", "comment": "Reserved"}]'
            
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
            
            if reserved_ip_ranges is not None:
                try:
                    import json
                    # Parse the JSON string
                    reserved_ranges = json.loads(reserved_ip_ranges)
                    kwargs['reservedIpRanges'] = reserved_ranges
                except json.JSONDecodeError:
                    return "❌ Invalid reserved_ip_ranges format. Must be valid JSON array."
            
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
            
            # Show reserved IP ranges if any
            reserved = result.get('reservedIpRanges', [])
            if reserved:
                response += f"\n## Reserved IP Ranges (Excluded from DHCP)\n"
                for r in reserved:
                    response += f"- **{r['start']} - {r['end']}**: {r.get('comment', 'No comment')}\n"
                
                # Calculate available DHCP range
                if result.get('subnet'):
                    response += f"\n💡 DHCP will assign IPs outside of reserved ranges\n"
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                return f"❌ VLAN {vlan_id} not found in this network."
            else:
                return f"❌ Error updating VLAN: {error_msg}"
    
    # @app.tool(
    # name="delete_network_appliance_vlan",
    # description="🏷️ Delete a VLAN from the MX appliance"
    # )
    # def delete_network_appliance_vlan(network_id: str, vlan_id: int):
    #     """
    #     Delete a VLAN from the MX appliance.
    #     WARNING: This will remove all devices from this VLAN!
    #     
    #     Args:
    #         network_id: Network ID
    #         vlan_id: VLAN ID to delete
    #         
    #     Returns:
    #         Deletion confirmation
    #     """
    def delete_network_appliance_vlan_duplicate(network_id: str, vlan_id: int):
        """Duplicate function - use tools_appliance_additional.py version"""
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
    
    # @app.tool(
    # name="update_network_appliance_warm_spare",
    # description="🔥 Update MX warm spare configuration"
    # )
    # def update_network_appliance_warm_spare(
    # network_id: str,
    # enabled: bool,
    # spare_serial: str = None,
    # uplink_mode: str = None,
    # virtual_ip1: str = None,
    # virtual_ip2: str = None
    # ):
    #     """
    #     Update warm spare configuration for MX high availability.
    #     
    #     Args:
    #         network_id: Network ID
    #         enabled: Enable/disable warm spare
    #         spare_serial: Serial number of spare MX
    #         uplink_mode: 'virtual' or 'public'
    #         virtual_ip1: Virtual IP for WAN 1 (if using virtual mode)
    #         virtual_ip2: Virtual IP for WAN 2 (if using virtual mode)
    #         
    #     Returns:
    #         Updated warm spare configuration
    #     """
    #     try:
    #         kwargs = {'enabled': enabled}
    #         
    #         if spare_serial:
    #             kwargs['spareSerial'] = spare_serial
    #         if uplink_mode:
    #             if uplink_mode not in ['virtual', 'public']:
    #                 return "❌ Invalid uplink mode. Must be 'virtual' or 'public'"
    #             kwargs['uplinkMode'] = uplink_mode
    #         if virtual_ip1:
    #             kwargs['virtualIp1'] = virtual_ip1
    #         if virtual_ip2:
    #             kwargs['virtualIp2'] = virtual_ip2
    #         
    #         result = meraki_client.dashboard.appliance.updateNetworkApplianceWarmSpare(
    #             network_id, **kwargs
    #         )
    #         
    #         response = f"# ✅ Updated Warm Spare Configuration\n\n"
    #         response += f"**Status**: {'Enabled' if result.get('enabled') else 'Disabled'}\n"
    #         
    #         if result.get('enabled'):
    #             response += f"**Spare Serial**: {result.get('spareSerial', 'Not set')}\n"
    #             response += f"**Uplink Mode**: {result.get('uplinkMode', 'virtual')}\n"
    #             
    #             if result.get('uplinkMode') == 'virtual':
    #                 response += f"**Virtual IP 1**: {result.get('virtualIp1', 'Not set')}\n"
    #                 response += f"**Virtual IP 2**: {result.get('virtualIp2', 'Not set')}\n"
    #         
    #         return response
    #         
    #     except Exception as e:
    #         return f"❌ Error updating warm spare: {str(e)}"
    
    # @app.tool(
    # name="swap_network_appliance_warm_spare",
    # description="🔄 Swap primary and spare MX appliances"
    # )
    # def swap_network_appliance_warm_spare(network_id: str):
    # """
    # Swap the primary and warm spare MX appliances.
    # This makes the current spare become the primary.
    #     # Args:
    # network_id: Network ID
    #         
    #     Returns:
    #         Swap confirmation
    #     """
    #     try:
    #         result = meraki_client.dashboard.appliance.swapNetworkApplianceWarmSpare(network_id)
    #         
    #         response = f"# ✅ MX Appliances Swapped!\n\n"
    #         response += f"**New Primary**: {result.get('primarySerial', 'Unknown')}\n"
    #         response += f"**New Spare**: {result.get('spareSerial', 'Unknown')}\n\n"
    #         response += "⚠️ **Note**: The swap may take a few minutes to complete.\n"
    #         
    #         return response
    #         
    #     except Exception as e:
    #         return f"❌ Error swapping warm spare: {str(e)}"
    
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
    
    # @app.tool(
    # name="create_network_appliance_static_route",
    # description="🛤️ Create a new static route on the MX"
    # )
    # def create_network_appliance_static_route(
    # network_id: str,
    # name: str,
    # subnet: str,
    # gateway_ip: str
    # ):
    # """
    #     Create a new static route on the MX appliance.
    #     
    #     Args:
    #         network_id: Network ID
    #         name: Name for the route
    #         subnet: Destination subnet in CIDR format
    #         gateway_ip: Next hop IP address
    #         
    #     Returns:
    #         Created route details
    #     """
    #     try:
    #         result = meraki_client.dashboard.appliance.createNetworkApplianceStaticRoute(
    #             network_id,
    #             name=name,
    #             subnet=subnet,
    #             gatewayIp=gateway_ip
    #         )
    #         
    #         response = f"# ✅ Static Route Created\n\n"
    #         response += f"**Name**: {result.get('name')}\n"
    #         response += f"**ID**: {result.get('id')}\n"
    #         response += f"**Subnet**: {result.get('subnet')}\n"
    #         response += f"**Gateway**: {result.get('gatewayIp')}\n"
    #         response += f"**Enabled**: {'✅' if result.get('enabled', True) else '❌'}\n"
    #         
    #         return response
    #         
    #     except Exception as e:
    #         error_msg = str(e)
    #         if "400" in error_msg:
    #             return f"❌ Invalid route configuration: {error_msg}"
    #         else:
    #             return f"❌ Error creating static route: {error_msg}"
    
    # ========== MISSING APPLIANCE SDK METHODS ==========
    
    @app.tool(
        name="update_network_appliance_traffic_shaping_uplink_selection",
        description="🌐 Update uplink selection settings for traffic shaping"
    )
    def update_network_appliance_traffic_shaping_uplink_selection(
        network_id: str,
        active_active_auto_vpn: Optional[bool] = None,
        default_uplink: Optional[str] = None,
        load_balancing_enabled: Optional[bool] = None
    ):
        """
        Update uplink selection settings for traffic shaping.
        
        Args:
            network_id: Network ID
            active_active_auto_vpn: Enable active-active Auto VPN
            default_uplink: Default uplink (wan1 or wan2)
            load_balancing_enabled: Enable load balancing
            
        Returns:
            Updated configuration
        """
        try:
            kwargs = {}
            
            if active_active_auto_vpn is not None:
                kwargs["activeActiveAutoVpnEnabled"] = active_active_auto_vpn
            if default_uplink:
                kwargs["defaultUplink"] = default_uplink
            if load_balancing_enabled is not None:
                kwargs["loadBalancingEnabled"] = load_balancing_enabled
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingUplinkSelection(
                network_id, **kwargs
            )
            
            return "✅ Uplink selection settings updated successfully"
            
        except Exception as e:
            return f"Error updating uplink selection: {str(e)}"

# ==================== ADDITIONAL APPLIANCE SDK TOOLS ====================
# Missing tools restored from backup to achieve complete SDK coverage

def register_additional_appliance_tools():
    """Register additional appliance tools from backup files."""
    
    @app.tool(
        name="get_network_appliance_vpn_site_to_site_vpn",
        description="🔐 Get site-to-site VPN settings for network"
    )
    def get_network_appliance_vpn_site_to_site_vpn(network_id: str):
        """Get site-to-site VPN configuration."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)
            
            response = f"# 🔐 Site-to-Site VPN Configuration\n\n"
            response += f"**Mode**: {result.get('mode', 'N/A')}\n"
            response += f"**Hub Networks**: {result.get('hubs', [])}\n\n"
            
            # Subnets
            subnets = result.get('subnets', [])
            if subnets:
                response += f"## Local Subnets ({len(subnets)})\n"
                for subnet in subnets:
                    response += f"- {subnet.get('localSubnet', 'N/A')} - {'Use VPN' if subnet.get('useVpn') else 'Local only'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting VPN settings: {str(e)}"

    @app.tool(
        name="get_organization_appliance_vpn_stats",
        description="📊 Get organization VPN statistics"
    )
    def get_organization_appliance_vpn_stats(
        organization_id: str,
        per_page: int = 1000,
        network_ids: Optional[str] = None
    ):
        """Get VPN statistics for organization."""
        try:
            kwargs = {'perPage': per_page, 'total_pages': 'all'}
            
            if network_ids:
                kwargs['networkIds'] = network_ids.split(',')
            
            result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnStats(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Organization VPN Statistics\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total VPN Connections**: {len(result)}\n\n"
                
                for vpn in result[:5]:  # Show first 5
                    response += f"## {vpn.get('networkName', 'Unknown Network')}\n"
                    response += f"- **Sent**: {vpn.get('bytesSent', 0):,} bytes\n"
                    response += f"- **Received**: {vpn.get('bytesReceived', 0):,} bytes\n\n"
                
                if len(result) > 5:
                    response += f"*...and {len(result) - 5} more VPN connections*\n"
            else:
                response += "*No VPN statistics found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting VPN stats: {str(e)}"
    
    # Additional appliance tools from consolidated backup
    @app.tool(
        name="get_network_appliance_firewall_inbound_rules",
        description="🔥 Get inbound firewall rules for network"
    )
    def get_network_appliance_firewall_inbound_rules(network_id: str):
        """Get inbound firewall rules for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallInboundFirewallRules(network_id)
            
            response = f"# 🔥 Inbound Firewall Rules - {network_id}\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n"
                response += f"**Syslog Enabled**: {'✅' if result.get('syslogEnabled') else '❌'}\n\n"
                
                for i, rule in enumerate(rules[:10], 1):  # Show first 10 rules
                    response += f"## Rule {i}: {rule.get('comment', 'No comment')}\n"
                    response += f"- **Policy**: {rule.get('policy', 'N/A')}\n"
                    response += f"- **Protocol**: {rule.get('protocol', 'any')}\n"
                    response += f"- **Source**: {rule.get('srcCidr', 'any')}\n"
                    
                    if rule.get('srcPort'):
                        response += f"- **Source Port**: {rule.get('srcPort')}\n"
                    
                    response += f"- **Destination**: {rule.get('destCidr', 'any')}\n"
                    
                    if rule.get('destPort'):
                        response += f"- **Destination Port**: {rule.get('destPort')}\n"
                    
                    response += "\n"
                
                if len(rules) > 10:
                    response += f"*...and {len(rules) - 10} more rules*\n"
            else:
                response += "*No inbound firewall rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting inbound firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_cellular_rules",
        description="📱 Get cellular firewall rules for network"
    )
    def get_network_appliance_firewall_cellular_rules(network_id: str):
        """Get cellular firewall rules for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallCellularFirewallRules(network_id)
            
            response = f"# 📱 Cellular Firewall Rules - {network_id}\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules[:10], 1):
                    response += f"## Rule {i}: {rule.get('comment', 'No comment')}\n"
                    response += f"- **Policy**: {rule.get('policy', 'N/A')}\n"
                    response += f"- **Protocol**: {rule.get('protocol', 'any')}\n"
                    response += f"- **Source**: {rule.get('srcCidr', 'any')}\n"
                    response += f"- **Destination**: {rule.get('destCidr', 'any')}\n"
                    
                    if rule.get('destPort'):
                        response += f"- **Destination Port**: {rule.get('destPort')}\n"
                    
                    response += "\n"
                
                if len(rules) > 10:
                    response += f"*...and {len(rules) - 10} more rules*\n"
            else:
                response += "*No cellular firewall rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting cellular firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_vlan",
        description="🏷️ Get specific VLAN configuration by VLAN ID"
    )
    def get_network_appliance_vlan(network_id: str, vlan_id: str):
        """Get specific VLAN configuration by VLAN ID."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceVlan(network_id, vlan_id)
            
            response = f"# 🏷️ VLAN {vlan_id} Details - {network_id}\n\n"
            response += f"**Name**: {result.get('name', 'Unnamed')}\n"
            response += f"**VLAN ID**: {result.get('id', 'N/A')}\n"
            response += f"**Subnet**: {result.get('subnet', 'N/A')}\n"
            response += f"**Appliance IP**: {result.get('applianceIp', 'N/A')}\n"
            response += f"**DHCP Handling**: {result.get('dhcpHandling', 'N/A')}\n"
            
            if result.get('dhcpLeaseTime'):
                response += f"**DHCP Lease Time**: {result.get('dhcpLeaseTime')}\n"
            
            if result.get('dnsNameservers'):
                response += f"**DNS Nameservers**: {result.get('dnsNameservers')}\n"
            
            if result.get('groupPolicyId'):
                response += f"**Group Policy ID**: {result.get('groupPolicyId')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting VLAN {vlan_id}: {str(e)}"
    
    @app.tool(
        name="get_device_appliance_dhcp_subnets",
        description="🌐 Get DHCP subnet information for appliance device"
    )
    def get_device_appliance_dhcp_subnets(device_serial: str):
        """Get DHCP subnet information for an appliance device."""
        try:
            result = meraki_client.dashboard.appliance.getDeviceApplianceDhcpSubnets(device_serial)
            
            response = f"# 🌐 DHCP Subnets - {device_serial}\n\n"
            
            if result:
                response += f"**Total DHCP Subnets**: {len(result)}\n\n"
                
                for subnet in result:
                    response += f"## Subnet: {subnet.get('subnet', 'Unknown')}\n"
                    response += f"- **VLAN ID**: {subnet.get('vlanId', 'N/A')}\n"
                    response += f"- **Used Count**: {subnet.get('usedCount', '0')}\n"
                    response += f"- **Free Count**: {subnet.get('freeCount', '0')}\n"
                    response += "\n"
            else:
                response += "*No DHCP subnets found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DHCP subnets: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_single_lan",
        description="🔌 Get single LAN configuration for network"
    )
    def get_network_appliance_single_lan(network_id: str):
        """Get single LAN configuration for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceSingleLan(network_id)
            
            response = f"# 🔌 Single LAN Configuration - {network_id}\n\n"
            response += f"**Subnet**: {result.get('subnet', 'N/A')}\n"
            response += f"**Appliance IP**: {result.get('applianceIp', 'N/A')}\n"
            
            ipv6 = result.get('ipv6', {})
            if ipv6:
                response += f"\n## IPv6 Configuration\n"
                response += f"- **Enabled**: {'✅' if ipv6.get('enabled') else '❌'}\n"
                if ipv6.get('prefixAssignments'):
                    response += f"- **Prefix Assignments**: {len(ipv6['prefixAssignments'])} configured\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting single LAN configuration: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_traffic_shaping_rules",
        description="⚡ Get traffic shaping rules for network"
    )
    def get_network_appliance_traffic_shaping_rules(network_id: str):
        """Get traffic shaping rules for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShaping(network_id)
            
            response = f"# ⚡ Traffic Shaping - {network_id}\n\n"
            
            if result:
                # Global bandwidth limits
                global_limits = result.get('globalBandwidthLimits')
                if global_limits:
                    response += "## Global Bandwidth Limits\n"
                    response += f"- **Upload Limit**: {global_limits.get('limitUp', 'Unlimited')} Kbps\n"
                    response += f"- **Download Limit**: {global_limits.get('limitDown', 'Unlimited')} Kbps\n\n"
                
                # Rules
                rules = result.get('rules', [])
                if rules:
                    response += f"## Traffic Shaping Rules ({len(rules)})\n"
                    for i, rule in enumerate(rules[:5], 1):
                        response += f"### Rule {i}\n"
                        response += f"- **Priority**: {rule.get('priority', 'N/A')}\n"
                        
                        # Definitions
                        definitions = rule.get('definitions', [])
                        if definitions:
                            response += f"- **Definitions**: {len(definitions)} configured\n"
                        
                        # Per-client bandwidth limits
                        per_client = rule.get('perClientBandwidthLimits')
                        if per_client:
                            response += f"- **Per-Client Up**: {per_client.get('limitUp', 'Unlimited')} Kbps\n"
                            response += f"- **Per-Client Down**: {per_client.get('limitDown', 'Unlimited')} Kbps\n"
                        
                        response += "\n"
                    
                    if len(rules) > 5:
                        response += f"*...and {len(rules) - 5} more rules*\n"
                else:
                    response += "*No traffic shaping rules configured*\n"
            else:
                response += "*No traffic shaping configuration*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting traffic shaping: {str(e)}"
    
    
    @app.tool(
        name="get_network_appliance_one_to_one_nat_rules",
        description="🔄 Get 1:1 NAT rules for network appliance"
    )
    def get_network_appliance_one_to_one_nat_rules(network_id: str):
        """Get 1:1 NAT rules for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceOneToOneNatRules(network_id)
            
            response = f"# 🔄 1:1 NAT Rules - {network_id}\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    response += f"## Rule {i}: {rule.get('name', 'Unnamed')}\n"
                    response += f"- **Public IP**: {rule.get('publicIp', 'N/A')}\n"
                    response += f"- **LAN IP**: {rule.get('lanIp', 'N/A')}\n"
                    response += f"- **Uplink**: {rule.get('uplink', 'N/A')}\n"
                    response += f"- **Allowed Inbound**:\n"
                    
                    allowed_inbound = rule.get('allowedInbound', [])
                    for inbound in allowed_inbound:
                        response += f"  - {inbound.get('protocol', 'N/A')} ports {inbound.get('destinationPorts', 'any')}\n"
                    
                    response += "\n"
            else:
                response += "*No 1:1 NAT rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting 1:1 NAT rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_one_to_many_nat_rules",
        description="🔀 Get 1:many NAT rules for network appliance"
    )
    def get_network_appliance_one_to_many_nat_rules(network_id: str):
        """Get 1:many NAT rules for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceOneToManyNatRules(network_id)
            
            response = f"# 🔀 1:Many NAT Rules - {network_id}\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    response += f"## Rule {i}\n"
                    response += f"- **Public IP**: {rule.get('publicIp', 'N/A')}\n"
                    response += f"- **Uplink**: {rule.get('uplink', 'N/A')}\n"
                    
                    port_rules = rule.get('portRules', [])
                    if port_rules:
                        response += f"- **Port Rules**: {len(port_rules)} configured\n"
                        for pr in port_rules[:3]:  # Show first 3
                            response += f"  - {pr.get('protocol', 'N/A')} {pr.get('publicPort', 'N/A')} → {pr.get('localIp', 'N/A')}:{pr.get('localPort', 'N/A')}\n"
                        if len(port_rules) > 3:
                            response += f"  - *...and {len(port_rules) - 3} more*\n"
                    
                    response += "\n"
            else:
                response += "*No 1:many NAT rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting 1:many NAT rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_client_security_events",
        description="🚨 Get security events for network appliance clients"
    )
    def get_network_appliance_client_security_events(
        network_id: str, 
        timespan: int = 86400,
        per_page: int = 1000
    ):
        """Get security events for clients on a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceClientSecurityEvents(
                network_id, 
                timespan=timespan,
                perPage=per_page,
                total_pages='all'
            )
            
            response = f"# 🚨 Client Security Events - {network_id}\n\n"
            response += f"**Timespan**: {timespan} seconds ({timespan/3600:.1f} hours)\n\n"
            
            if result:
                response += f"**Total Events**: {len(result)}\n\n"
                
                # Group events by type
                event_types = {}
                for event in result:
                    event_type = event.get('eventType', 'Unknown')
                    event_types[event_type] = event_types.get(event_type, 0) + 1
                
                # Show event type summary
                response += "## Event Summary\n"
                for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
                    response += f"- **{event_type}**: {count} events\n"
                
                # Show recent events
                response += f"\n## Recent Events (showing first 10)\n"
                for i, event in enumerate(result[:10], 1):
                    response += f"### {i}. {event.get('eventType', 'Unknown Event')}\n"
                    response += f"- **Time**: {event.get('ts', 'N/A')}\n"
                    response += f"- **Client MAC**: {event.get('clientMac', 'N/A')}\n"
                    response += f"- **Client Name**: {event.get('clientName', 'Unknown')}\n"
                    
                    if event.get('srcIp'):
                        response += f"- **Source IP**: {event.get('srcIp')}\n"
                    if event.get('destIp'):
                        response += f"- **Destination IP**: {event.get('destIp')}\n"
                    if event.get('disposition'):
                        response += f"- **Action**: {event.get('disposition')}\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"*...and {len(result) - 10} more events*\n"
            else:
                response += "*No security events found in the specified timespan*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting client security events: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_uplinks_settings",
        description="📡 Get uplink settings for network appliance"
    )
    def get_network_appliance_uplinks_settings(network_id: str):
        """Get uplink settings for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceUplinksSettings(network_id)
            
            response = f"# 📡 Uplink Settings - {network_id}\n\n"
            
            interfaces = result.get('interfaces', {})
            
            # WAN1 settings
            wan1 = interfaces.get('wan1', {})
            if wan1:
                response += "## WAN1 Interface\n"
                response += f"- **Enabled**: {'✅' if wan1.get('enabled') else '❌'}\n"
                response += f"- **Using Static IP**: {'✅' if wan1.get('usingStaticIp') else '❌ DHCP'}\n"
                
                if wan1.get('staticIp'):
                    response += f"- **Static IP**: {wan1.get('staticIp')}\n"
                if wan1.get('staticSubnetMask'):
                    response += f"- **Subnet Mask**: {wan1.get('staticSubnetMask')}\n"
                if wan1.get('staticGatewayIp'):
                    response += f"- **Gateway**: {wan1.get('staticGatewayIp')}\n"
                if wan1.get('staticDns'):
                    response += f"- **DNS**: {wan1.get('staticDns')}\n"
                
                response += "\n"
            
            # WAN2 settings
            wan2 = interfaces.get('wan2', {})
            if wan2:
                response += "## WAN2 Interface\n"
                response += f"- **Enabled**: {'✅' if wan2.get('enabled') else '❌'}\n"
                response += f"- **Using Static IP**: {'✅' if wan2.get('usingStaticIp') else '❌ DHCP'}\n"
                
                if wan2.get('staticIp'):
                    response += f"- **Static IP**: {wan2.get('staticIp')}\n"
                if wan2.get('staticSubnetMask'):
                    response += f"- **Subnet Mask**: {wan2.get('staticSubnetMask')}\n"
                if wan2.get('staticGatewayIp'):
                    response += f"- **Gateway**: {wan2.get('staticGatewayIp')}\n"
                if wan2.get('staticDns'):
                    response += f"- **DNS**: {wan2.get('staticDns')}\n"
                
                response += "\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting uplink settings: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_connectivity_monitoring",
        description="🌐 Get connectivity monitoring destinations"
    )
    def get_network_appliance_connectivity_monitoring(network_id: str):
        """Get connectivity monitoring destinations for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceConnectivityMonitoringDestinations(network_id)
            
            response = f"# 🌐 Connectivity Monitoring - {network_id}\n\n"
            
            destinations = result.get('destinations', [])
            if destinations:
                response += f"**Total Destinations**: {len(destinations)}\n\n"
                
                for i, dest in enumerate(destinations, 1):
                    response += f"## Destination {i}\n"
                    response += f"- **IP**: {dest.get('ip', 'N/A')}\n"
                    response += f"- **Description**: {dest.get('description', 'No description')}\n"
                    response += f"- **Default**: {'✅' if dest.get('default') else '❌'}\n"
                    response += "\n"
            else:
                response += "*No connectivity monitoring destinations configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting connectivity monitoring: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_security_events",
        description="🚨 Get organization-wide appliance security events"
    )
    def get_organization_appliance_security_events(
        organization_id: str,
        timespan: int = 86400,
        per_page: int = 1000
    ):
        """Get organization-wide appliance security events."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceSecurityEvents(
                organization_id,
                timespan=timespan,
                perPage=per_page,
                total_pages='all'
            )
            
            response = f"# 🚨 Organization Security Events\n"
            response += f"*Last {timespan//3600} hours across all networks*\n\n"
            
            if not result:
                response += "✅ No security events detected organization-wide\n"
                return response
            
            response += f"**Total Events**: {len(result)}\n\n"
            
            # Group by network and event type
            network_events = {}
            event_types = {}
            
            for event in result:
                network_name = event.get('networkName', 'Unknown Network')
                event_type = event.get('eventType', 'Unknown')
                
                if network_name not in network_events:
                    network_events[network_name] = 0
                network_events[network_name] += 1
                
                if event_type not in event_types:
                    event_types[event_type] = 0
                event_types[event_type] += 1
            
            # Network summary
            response += "## Events by Network\n"
            for network, count in sorted(network_events.items(), key=lambda x: x[1], reverse=True)[:10]:
                response += f"- **{network}**: {count} events\n"
            
            # Event type summary
            response += "\n## Event Types\n"
            for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
                response += f"- **{event_type}**: {count} events\n"
            
            response += f"\n## Recent Events (showing first 5)\n"
            for i, event in enumerate(result[:5], 1):
                response += f"### {i}. {event.get('eventType', 'Unknown')}\n"
                response += f"- **Network**: {event.get('networkName', 'Unknown')}\n"
                response += f"- **Time**: {event.get('ts', 'Unknown')}\n"
                response += f"- **Source**: {event.get('srcIp', 'Unknown')}\n"
                response += f"- **Destination**: {event.get('destIp', 'Unknown')}\n"
                
                if event.get('message'):
                    response += f"- **Message**: {event['message']}\n"
                
                response += "\n"
            
            if len(result) > 5:
                response += f"*...and {len(result) - 5} more events across the organization*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization security events: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_security_intrusion",
        description="🛡️ Get organization-wide IDS/IPS settings"
    )
    def get_organization_appliance_security_intrusion(
        organization_id: str,
        per_page: int = 1000
    ):
        """Get organization-wide appliance intrusion detection settings."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceSecurityIntrusion(
                organization_id,
                perPage=per_page,
                total_pages='all'
            )
            
            response = f"# 🛡️ Organization IDS/IPS Settings\n\n"
            
            if not result:
                response += "*No networks with appliance intrusion detection configured*\n"
                return response
            
            response += f"**Total Networks**: {len(result)}\n\n"
            
            # Group by mode
            mode_counts = {}
            for network in result:
                mode = network.get('mode', 'disabled')
                mode_counts[mode] = mode_counts.get(mode, 0) + 1
            
            response += "## IDS/IPS Mode Summary\n"
            for mode, count in sorted(mode_counts.items()):
                if mode == 'prevention':
                    response += f"- **🛡️ Prevention**: {count} networks (blocking threats)\n"
                elif mode == 'detection':
                    response += f"- **🔍 Detection**: {count} networks (monitoring only)\n"
                else:
                    response += f"- **❌ Disabled**: {count} networks\n"
            
            response += f"\n## Network Details (showing first 10)\n"
            for network in result[:10]:
                response += f"### {network.get('networkName', 'Unknown Network')}\n"
                response += f"- **Network ID**: {network.get('networkId', 'N/A')}\n"
                response += f"- **Mode**: {network.get('mode', 'disabled')}\n"
                response += f"- **Ruleset**: {network.get('idsRulesets', 'N/A')}\n"
                
                protected = network.get('protectedNetworks', {})
                if protected:
                    use_default = protected.get('useDefault', True)
                    response += f"- **Protected Networks**: {'Default' if use_default else 'Custom'}\n"
                
                response += "\n"
            
            if len(result) > 10:
                response += f"*...and {len(result) - 10} more networks*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization IDS/IPS settings: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_dhcp_reservations",
        description="🏷️ Get DHCP reservations for network appliance VLANs"
    )
    def get_network_appliance_dhcp_reservations(network_id: str, vlan_id: str = None):
        """Get DHCP reservations for network appliance VLANs."""
        try:
            vlans = meraki_client.dashboard.appliance.getNetworkApplianceVlans(network_id)
            
            response = f"# 🏷️ DHCP Reservations - {network_id}\n\n"
            
            total_reservations = 0
            
            for vlan in vlans:
                current_vlan_id = str(vlan.get('id', ''))
                
                # Skip if specific VLAN requested and this isn't it
                if vlan_id and current_vlan_id != str(vlan_id):
                    continue
                
                fixed_assignments = vlan.get('fixedIpAssignments', {})
                
                if fixed_assignments:
                    response += f"## VLAN {current_vlan_id}: {vlan.get('name', 'Unnamed')}\n"
                    response += f"**Subnet**: {vlan.get('subnet', 'N/A')}\n"
                    response += f"**Reservations**: {len(fixed_assignments)}\n\n"
                    
                    for mac, info in fixed_assignments.items():
                        response += f"**{mac.upper()}**\n"
                        response += f"  - IP: `{info.get('ip')}`\n"
                        response += f"  - Name: {info.get('name', 'No name')}\n"
                        total_reservations += 1
                    
                    response += "\n"
                elif vlan_id is not None:
                    response += f"## VLAN {current_vlan_id}: {vlan.get('name', 'Unknown')}\n"
                    response += "No DHCP reservations configured.\n\n"
            
            if vlan_id is not None and total_reservations == 0:
                response += "No DHCP reservations found for the specified VLAN.\n"
            elif vlan_id is None and total_reservations == 0:
                response += "No DHCP reservations configured on any VLAN.\n"
            else:
                response += f"**Total Reservations**: {total_reservations}\n"
            
            return response
        except Exception as e:
            return f"❌ Error listing DHCP reservations: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_uplink_statuses",
        description="📡 Get uplink status across organization appliances"
    )
    def get_organization_appliance_uplink_statuses(
        organization_id: str, 
        per_page: int = 1000,
        network_ids: Optional[str] = None
    ):
        """Get uplink status across organization appliances."""
        try:
            kwargs = {'perPage': per_page, 'total_pages': 'all'}
            
            if network_ids:
                kwargs['networkIds'] = network_ids.split(',')
            
            result = meraki_client.dashboard.appliance.getOrganizationApplianceUplinkStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📡 Organization Appliance Uplink Status\n\n"
            
            if not result:
                response += "*No appliance uplink data found*\n"
                return response
            
            response += f"**Total Networks**: {len(result)}\n\n"
            
            # Group by uplink status
            uplink_summary = {
                'active': 0,
                'connecting': 0,
                'not_connected': 0,
                'ready': 0,
                'failed': 0
            }
            
            for network in result:
                uplinks = network.get('uplinks', [])
                for uplink in uplinks:
                    status = uplink.get('status', '').lower().replace(' ', '_')
                    if status in uplink_summary:
                        uplink_summary[status] += 1
            
            response += "## Uplink Status Summary\n"
            for status, count in uplink_summary.items():
                if count > 0:
                    emoji = "✅" if status == "active" else "🔄" if status == "connecting" else "❌"
                    response += f"- **{emoji} {status.replace('_', ' ').title()}**: {count} uplinks\n"
            
            response += f"\n## Network Details (showing first 10)\n"
            for network in result[:10]:
                response += f"### {network.get('networkName', 'Unknown Network')}\n"
                response += f"- **Network ID**: {network.get('networkId', 'N/A')}\n"
                response += f"- **Serial**: {network.get('serial', 'N/A')}\n"
                
                uplinks = network.get('uplinks', [])
                for i, uplink in enumerate(uplinks, 1):
                    status = uplink.get('status', 'Unknown')
                    emoji = "✅" if status.lower() == "active" else "❌"
                    response += f"- **Uplink {i}**: {emoji} {status}\n"
                    if uplink.get('ip'):
                        response += f"  - IP: {uplink.get('ip')}\n"
                    if uplink.get('provider'):
                        response += f"  - Provider: {uplink.get('provider')}\n"
                
                response += "\n"
            
            if len(result) > 10:
                response += f"*...and {len(result) - 10} more networks*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization uplink statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_vpn_third_party_peers",
        description="🔗 Get third-party VPN peers for organization"
    )
    def get_organization_appliance_vpn_third_party_peers(
        organization_id: str, 
        per_page: int = 1000
    ):
        """Get third-party VPN peers configured across the organization."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnThirdPartyVpnPeers(
                organization_id, 
                perPage=per_page,
                total_pages='all'
            )
            
            response = f"# 🔗 Third-Party VPN Peers\n\n"
            
            if not result:
                response += "*No third-party VPN peers configured*\n"
                return response
            
            response += f"**Total Peers**: {len(result)}\n\n"
            
            # Group by peer type/vendor
            peer_types = {}
            for peer in result:
                peer_name = peer.get('name', 'Unknown')
                vendor = peer_name.split('-')[0] if '-' in peer_name else 'Unknown'
                peer_types[vendor] = peer_types.get(vendor, 0) + 1
            
            if len(peer_types) > 1:
                response += "## Peer Distribution\n"
                for vendor, count in sorted(peer_types.items(), key=lambda x: x[1], reverse=True):
                    response += f"- **{vendor}**: {count} peers\n"
                response += "\n"
            
            response += "## Peer Details\n"
            for peer in result:
                response += f"### {peer.get('name', 'Unnamed Peer')}\n"
                response += f"- **Public IP**: {peer.get('publicIp', 'N/A')}\n"
                response += f"- **Remote ID**: {peer.get('remoteId', 'N/A')}\n"
                
                # Private subnets
                private_subnets = peer.get('privateSubnets', [])
                if private_subnets:
                    response += f"- **Private Subnets**: {', '.join(private_subnets)}\n"
                
                # IPsec policies
                ipsec_policies = peer.get('ipsecPolicies', {})
                if ipsec_policies:
                    response += f"- **IKE Version**: {ipsec_policies.get('ikeVersion', 'N/A')}\n"
                    if ipsec_policies.get('childLifetime'):
                        response += f"- **Child Lifetime**: {ipsec_policies.get('childLifetime')}s\n"
                
                response += f"- **Secret**: {'Configured' if peer.get('secret') else 'Not configured'}\n"
                response += "\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting third-party VPN peers: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_l7_categories",
        description="🔍 Get L7 application firewall categories"
    )
    def get_network_appliance_firewall_l7_categories(network_id: str):
        """Get L7 application firewall categories."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(network_id)
            
            response = f"# 🔍 L7 Application Categories - {network_id}\n\n"
            
            categories = result.get('applicationCategories', [])
            if categories:
                response += f"**Total Categories**: {len(categories)}\n\n"
                
                # Group by category type
                by_type = {}
                for cat in categories:
                    cat_name = cat.get('name', 'Unknown')
                    cat_id = cat.get('id', 'N/A')
                    
                    # Extract category type from name
                    if '.' in cat_name:
                        cat_type = cat_name.split('.')[0]
                    else:
                        cat_type = 'Other'
                    
                    if cat_type not in by_type:
                        by_type[cat_type] = []
                    by_type[cat_type].append((cat_name, cat_id))
                
                for cat_type, items in sorted(by_type.items()):
                    response += f"## {cat_type}\n"
                    for name, cat_id in items[:5]:
                        response += f"- {name} ({cat_id})\n"
                    if len(items) > 5:
                        response += f"  ...and {len(items)-5} more\n"
                    response += "\n"
            else:
                response += "*No application categories available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting L7 categories: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_firewalled_services",
        description="🛡️ Get firewalled services settings"
    )
    def get_network_appliance_firewall_firewalled_services(network_id: str):
        """Get firewalled services for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallFirewalledServices(network_id)
            
            response = f"# 🛡️ Firewalled Services - {network_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Services**: {len(result)}\n\n"
                
                for service in result:
                    response += f"## {service.get('service', 'Unknown')}\n"
                    response += f"- **Access**: {service.get('access', 'N/A')}\n"
                    
                    allowed = service.get('allowedIps', [])
                    if allowed:
                        response += f"- **Allowed IPs**: {', '.join(allowed)}\n"
                    else:
                        response += f"- **Allowed IPs**: Any\n"
                    
                    response += "\n"
            else:
                response += "*No firewalled services configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting firewalled services: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_prefixes_delegated",
        description="🔢 Get delegated IPv6 prefixes"
    )
    def get_network_appliance_prefixes_delegated(network_id: str):
        """Get delegated IPv6 prefixes for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkAppliancePrefixesDelegated(network_id)
            
            response = f"# 🔢 Delegated IPv6 Prefixes - {network_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Prefixes**: {len(result)}\n\n"
                
                for prefix in result:
                    response += f"## {prefix.get('prefix', 'Unknown')}\n"
                    response += f"- **Origin**: {prefix.get('origin', 'N/A')}\n"
                    response += f"- **Description**: {prefix.get('description', 'N/A')}\n"
                    
                    if prefix.get('createdAt'):
                        response += f"- **Created**: {prefix.get('createdAt')}\n"
                    if prefix.get('updatedAt'):
                        response += f"- **Updated**: {prefix.get('updatedAt')}\n"
                    
                    response += "\n"
            else:
                response += "*No delegated prefixes configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting delegated prefixes: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_vpn_statuses",
        description="🔗 Get VPN status across organization appliances"  
    )
    def get_organization_appliance_vpn_statuses(
        organization_id: str,
        per_page: int = 1000,
        network_ids: Optional[str] = None
    ):
        """Get VPN status across organization appliances."""
        try:
            kwargs = {'perPage': per_page, 'total_pages': 'all'}
            
            if network_ids:
                kwargs['networkIds'] = network_ids.split(',')
            
            result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 🔗 Organization VPN Status\n\n"
            
            if not result:
                response += "*No VPN status data found*\n"
                return response
            
            response += f"**Total Networks**: {len(result)}\n\n"
            
            # Group by VPN status
            vpn_summary = {
                'connected': 0,
                'not_connected': 0,
                'connecting': 0
            }
            
            for network in result:
                vpn_mode = network.get('vpnMode', 'None')
                
                # Check VPN peer statuses
                peers = network.get('merakiVpnPeers', [])
                for peer in peers:
                    reachability = peer.get('reachability', '').lower().replace(' ', '_')
                    if reachability == 'reachable':
                        vpn_summary['connected'] += 1
                    elif reachability == 'unreachable':
                        vpn_summary['not_connected'] += 1
                    else:
                        vpn_summary['connecting'] += 1
            
            response += "## VPN Status Summary\n"
            for status, count in vpn_summary.items():
                if count > 0:
                    emoji = "✅" if status == "connected" else "❌" if status == "not_connected" else "🔄"
                    response += f"- **{emoji} {status.replace('_', ' ').title()}**: {count} peers\n"
            
            response += f"\n## Network Details (showing first 10)\n"
            for network in result[:10]:
                response += f"### {network.get('networkName', 'Unknown Network')}\n"
                response += f"- **Network ID**: {network.get('networkId', 'N/A')}\n"
                response += f"- **VPN Mode**: {network.get('vpnMode', 'None')}\n"
                
                # Show peer status
                peers = network.get('merakiVpnPeers', [])
                if peers:
                    response += f"- **VPN Peers**: {len(peers)} configured\n"
                    for peer in peers[:3]:  # Show first 3 peers
                        reachability = peer.get('reachability', 'Unknown')
                        emoji = "✅" if reachability.lower() == "reachable" else "❌"
                        response += f"  - {emoji} {peer.get('networkName', 'Unknown')}: {reachability}\n"
                    if len(peers) > 3:
                        response += f"  - *...and {len(peers) - 3} more peers*\n"
                else:
                    response += f"- **VPN Peers**: None configured\n"
                
                response += "\n"
            
            if len(result) > 10:
                response += f"*...and {len(result) - 10} more networks*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization VPN statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_security_malware",
        description="🦠 Get organization-wide malware protection settings"
    )
    def get_organization_appliance_security_malware(
        organization_id: str,
        per_page: int = 1000
    ):
        """Get organization-wide appliance malware protection settings."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceSecurityMalware(
                organization_id,
                perPage=per_page,
                total_pages='all'
            )
            
            response = f"# 🦠 Organization Malware Protection\n\n"
            
            if not result:
                response += "*No networks with malware protection configured*\n"
                return response
            
            response += f"**Total Networks**: {len(result)}\n\n"
            
            # Group by malware protection mode
            mode_counts = {}
            for network in result:
                mode = network.get('mode', 'disabled')
                mode_counts[mode] = mode_counts.get(mode, 0) + 1
            
            response += "## Malware Protection Summary\n"
            for mode, count in sorted(mode_counts.items()):
                if mode == 'enabled':
                    response += f"- **🛡️ Enabled**: {count} networks (blocking malware)\n"
                else:
                    response += f"- **❌ Disabled**: {count} networks\n"
            
            response += f"\n## Network Details (showing first 10)\n"
            for network in result[:10]:
                response += f"### {network.get('networkName', 'Unknown Network')}\n"
                response += f"- **Network ID**: {network.get('networkId', 'N/A')}\n"
                response += f"- **Mode**: {network.get('mode', 'disabled')}\n"
                
                # Show allowed URLs/files if mode is enabled
                if network.get('mode') == 'enabled':
                    allowed_urls = network.get('allowedUrls', [])
                    allowed_files = network.get('allowedFiles', [])
                    
                    if allowed_urls:
                        response += f"- **Allowed URLs**: {len(allowed_urls)} configured\n"
                    if allowed_files:
                        response += f"- **Allowed Files**: {len(allowed_files)} configured\n"
                
                response += "\n"
            
            if len(result) > 10:
                response += f"*...and {len(result) - 10} more networks*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization malware protection: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_traffic_shaping_custom_classes",
        description="🎯 Get all custom performance classes for traffic shaping"
    )
    def get_network_appliance_traffic_shaping_custom_classes(network_id: str):
        """Get all custom performance classes for traffic shaping."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClasses(network_id)
            
            response = f"# 🎯 Custom Performance Classes - {network_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Classes**: {len(result)}\n\n"
                
                for class_obj in result:
                    response += f"## {class_obj.get('name', 'Unnamed')}\n"
                    response += f"- **ID**: {class_obj.get('customPerformanceClassId', 'N/A')}\n"
                    response += f"- **Max Latency**: {class_obj.get('maxLatency', 'N/A')}ms\n"
                    response += f"- **Max Jitter**: {class_obj.get('maxJitter', 'N/A')}ms\n"
                    response += f"- **Max Loss**: {class_obj.get('maxLossPercentage', 'N/A')}%\n"
                    response += "\n"
            else:
                response += "*No custom performance classes configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting custom performance classes: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_traffic_shaping_custom_class",
        description="🎯 Get specific custom performance class details"
    )
    def get_network_appliance_traffic_shaping_custom_class(
        network_id: str, 
        custom_performance_class_id: str
    ):
        """Get specific custom performance class details."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id, custom_performance_class_id
            )
            
            response = f"# 🎯 Custom Performance Class Details\n\n"
            response += f"**ID**: {custom_performance_class_id}\n"
            response += f"**Name**: {result.get('name', 'N/A')}\n"
            response += f"**Max Latency**: {result.get('maxLatency', 'N/A')}ms\n"
            response += f"**Max Jitter**: {result.get('maxJitter', 'N/A')}ms\n"
            response += f"**Max Loss**: {result.get('maxLossPercentage', 'N/A')}%\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting performance class: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_ssids",
        description="📶 Get wireless SSID settings for MX appliance"
    )
    def get_network_appliance_ssids(network_id: str):
        """Get wireless SSID settings for an MX appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceSsids(network_id)
            
            response = f"# 📶 MX Appliance SSIDs - {network_id}\n\n"
            
            if result:
                response += f"**Total SSIDs**: {len(result)}\n\n"
                
                for ssid in result:
                    response += f"## SSID {ssid.get('number', 'Unknown')}: {ssid.get('name', 'Unnamed')}\n"
                    response += f"- **Enabled**: {'✅' if ssid.get('enabled') else '❌'}\n"
                    response += f"- **Auth Mode**: {ssid.get('authMode', 'N/A')}\n"
                    response += f"- **Encryption**: {ssid.get('encryptionMode', 'N/A')}\n"
                    response += f"- **WPA Version**: {ssid.get('wpaEncryptionMode', 'N/A')}\n"
                    
                    if ssid.get('radiusServers'):
                        response += f"- **RADIUS Servers**: {len(ssid['radiusServers'])} configured\n"
                    
                    response += "\n"
            else:
                response += "*No SSID configuration found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting appliance SSIDs: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_ssid",
        description="📶 Get specific SSID configuration for MX appliance"
    )
    def get_network_appliance_ssid(network_id: str, number: str):
        """Get specific SSID configuration for an MX appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceSsid(network_id, number)
            
            response = f"# 📶 MX SSID {number} Details - {network_id}\n\n"
            response += f"**Name**: {result.get('name', 'Unnamed')}\n"
            response += f"**Enabled**: {'✅' if result.get('enabled') else '❌'}\n"
            response += f"**Auth Mode**: {result.get('authMode', 'N/A')}\n"
            response += f"**Encryption**: {result.get('encryptionMode', 'N/A')}\n"
            response += f"**WPA Version**: {result.get('wpaEncryptionMode', 'N/A')}\n"
            
            # RADIUS settings
            radius_servers = result.get('radiusServers', [])
            if radius_servers:
                response += f"\n## RADIUS Servers ({len(radius_servers)})\n"
                for i, server in enumerate(radius_servers, 1):
                    response += f"### Server {i}\n"
                    response += f"- **Host**: {server.get('host', 'N/A')}\n"
                    response += f"- **Port**: {server.get('port', '1812')}\n"
                    response += f"- **Secret**: {'Configured' if server.get('secret') else 'Not configured'}\n"
                    response += "\n"
            
            # DHCP settings
            dhcp_enforced_deauth = result.get('dhcpEnforcedDeauthentication', {})
            if dhcp_enforced_deauth:
                response += f"## DHCP Enforced Deauth\n"
                response += f"- **Enabled**: {'✅' if dhcp_enforced_deauth.get('enabled') else '❌'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting SSID {number}: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_uplinks_usage_by_network",
        description="📊 Get uplink usage by network across organization"
    )
    def get_organization_appliance_uplinks_usage_by_network(
        organization_id: str,
        per_page: int = 1000,
        timespan: int = 86400
    ):
        """Get uplink usage by network across organization appliances."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceUplinksUsageByNetwork(
                organization_id,
                perPage=per_page,
                timespan=timespan,
                total_pages='all'
            )
            
            response = f"# 📊 Organization Uplink Usage by Network\n"
            response += f"*Last {timespan//3600} hours*\n\n"
            
            if not result:
                response += "*No uplink usage data found*\n"
                return response
            
            response += f"**Total Networks**: {len(result)}\n\n"
            
            # Calculate total usage
            total_sent = sum(network.get('bytesSent', 0) for network in result)
            total_received = sum(network.get('bytesReceived', 0) for network in result)
            
            response += "## Organization Summary\n"
            response += f"- **Total Sent**: {total_sent:,} bytes ({total_sent/1024/1024/1024:.2f} GB)\n"
            response += f"- **Total Received**: {total_received:,} bytes ({total_received/1024/1024/1024:.2f} GB)\n"
            response += f"- **Total Transfer**: {(total_sent + total_received):,} bytes ({(total_sent + total_received)/1024/1024/1024:.2f} GB)\n\n"
            
            # Sort by total usage
            sorted_networks = sorted(result, key=lambda x: x.get('bytesSent', 0) + x.get('bytesReceived', 0), reverse=True)
            
            response += "## Top Networks by Usage (first 10)\n"
            for network in sorted_networks[:10]:
                sent = network.get('bytesSent', 0)
                received = network.get('bytesReceived', 0)
                total = sent + received
                
                response += f"### {network.get('networkName', 'Unknown Network')}\n"
                response += f"- **Network ID**: {network.get('networkId', 'N/A')}\n"
                response += f"- **Sent**: {sent:,} bytes ({sent/1024/1024:.1f} MB)\n"
                response += f"- **Received**: {received:,} bytes ({received/1024/1024:.1f} MB)\n"
                response += f"- **Total**: {total:,} bytes ({total/1024/1024:.1f} MB)\n"
                response += "\n"
            
            if len(sorted_networks) > 10:
                response += f"*...and {len(sorted_networks) - 10} more networks*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting uplink usage by network: {str(e)}"
    
    # Additional comprehensive appliance tools
    @app.tool(
        name="get_organization_appliance_traffic_shaping_vpn_exclusions",
        description="🚫 Get VPN exclusions for traffic shaping"
    )
    def get_organization_appliance_traffic_shaping_vpn_exclusions(
        organization_id: str, 
        per_page: int = 1000
    ):
        """Get traffic shaping VPN exclusions across organization."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceTrafficShapingVpnExclusionsByNetwork(
                organization_id,
                perPage=per_page,
                total_pages='all'
            )
            
            response = f"# 🚫 Traffic Shaping VPN Exclusions\n\n"
            
            if not result:
                response += "*No VPN exclusions configured*\n"
                return response
            
            response += f"**Total Networks**: {len(result)}\n\n"
            
            for network in result:
                exclusions = network.get('custom', [])
                if exclusions:
                    response += f"## {network.get('networkName', 'Unknown Network')}\n"
                    response += f"- **Network ID**: {network.get('networkId', 'N/A')}\n"
                    response += f"- **Custom Exclusions**: {len(exclusions)}\n"
                    
                    for exclusion in exclusions[:5]:
                        response += f"  - {exclusion.get('value', 'N/A')}\n"
                    
                    if len(exclusions) > 5:
                        response += f"  - *...and {len(exclusions) - 5} more*\n"
                    
                    response += "\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting VPN exclusions: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_rf_profile",
        description="📡 Get specific RF profile details"
    )
    def get_network_appliance_rf_profile(network_id: str, rf_profile_id: str):
        """Get specific RF profile details."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceRfProfile(network_id, rf_profile_id)
            
            response = f"# 📡 RF Profile Details\n\n"
            response += f"**Profile ID**: {rf_profile_id}\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**Network ID**: {result.get('networkId', 'N/A')}\n"
            
            # Two-four GHz settings
            two_four_ghz = result.get('twoFourGhzSettings', {})
            if two_four_ghz:
                response += f"\n## 2.4 GHz Settings\n"
                response += f"- **Max Power**: {two_four_ghz.get('maxPower', 'N/A')} dBm\n"
                response += f"- **Min Power**: {two_four_ghz.get('minPower', 'N/A')} dBm\n"
            
            # Five GHz settings
            five_ghz = result.get('fiveGhzSettings', {})
            if five_ghz:
                response += f"\n## 5 GHz Settings\n"
                response += f"- **Max Power**: {five_ghz.get('maxPower', 'N/A')} dBm\n"
                response += f"- **Min Power**: {five_ghz.get('minPower', 'N/A')} dBm\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting RF profile: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_l7_application_categories",
        description="🔍 Get L7 firewall application categories"
    )
    def get_network_appliance_firewall_l7_application_categories(network_id: str):
        """Get L7 firewall application categories."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(network_id)
            
            response = f"# 🔍 L7 Application Categories - {network_id}\n\n"
            
            categories = result.get('applicationCategories', [])
            if categories:
                response += f"**Total Categories**: {len(categories)}\n\n"
                
                # Group by category type
                by_type = {}
                for cat in categories:
                    cat_name = cat.get('name', 'Unknown')
                    cat_id = cat.get('id', 'N/A')
                    
                    # Extract category type from name
                    if '.' in cat_name:
                        cat_type = cat_name.split('.')[0]
                    else:
                        cat_type = 'Other'
                    
                    if cat_type not in by_type:
                        by_type[cat_type] = []
                    by_type[cat_type].append((cat_name, cat_id))
                
                for cat_type, items in sorted(by_type.items()):
                    response += f"## {cat_type}\n"
                    for name, cat_id in items[:10]:  # Show first 10
                        response += f"- {name} ({cat_id})\n"
                    if len(items) > 10:
                        response += f"  ...and {len(items)-10} more\n"
                    response += "\n"
            else:
                response += "*No application categories available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting L7 categories: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_settings",
        description="⚙️ Get general appliance settings for network"
    )
    def get_network_appliance_settings(network_id: str):
        """Get general appliance settings for network."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceSettings(network_id)
            
            response = f"# ⚙️ Appliance Settings - {network_id}\n\n"
            
            # Client tracking method
            client_tracking = result.get('clientTrackingMethod', 'MAC address')
            response += f"**Client Tracking Method**: {client_tracking}\n"
            
            # Deployment mode
            deployment_mode = result.get('deploymentMode', 'routed')
            response += f"**Deployment Mode**: {deployment_mode}\n"
            
            # Dynamic DNS
            dynamic_dns = result.get('dynamicDns', {})
            if dynamic_dns:
                response += f"\n## Dynamic DNS\n"
                response += f"- **Enabled**: {'✅' if dynamic_dns.get('enabled') else '❌'}\n"
                if dynamic_dns.get('prefix'):
                    response += f"- **Prefix**: {dynamic_dns.get('prefix')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting appliance settings: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_traffic_shaping_uplink_bandwidth",
        description="⚡ Get uplink bandwidth settings for traffic shaping"
    )
    def get_network_appliance_traffic_shaping_uplink_bandwidth(network_id: str):
        """Get uplink bandwidth settings for traffic shaping."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingUplinkBandwidth(network_id)
            
            response = f"# ⚡ Uplink Bandwidth Settings - {network_id}\n\n"
            
            # Bandwidth limits
            bandwidth_limits = result.get('bandwidthLimits', {})
            
            # WAN1
            wan1 = bandwidth_limits.get('wan1', {})
            if wan1:
                response += "## WAN1 Bandwidth\n"
                response += f"- **Limit Up**: {wan1.get('limitUp', 'Unlimited')} Kbps\n"
                response += f"- **Limit Down**: {wan1.get('limitDown', 'Unlimited')} Kbps\n\n"
            
            # WAN2
            wan2 = bandwidth_limits.get('wan2', {})
            if wan2:
                response += "## WAN2 Bandwidth\n"
                response += f"- **Limit Up**: {wan2.get('limitUp', 'Unlimited')} Kbps\n"
                response += f"- **Limit Down**: {wan2.get('limitDown', 'Unlimited')} Kbps\n\n"
            
            # Cellular
            cellular = bandwidth_limits.get('cellular', {})
            if cellular:
                response += "## Cellular Bandwidth\n"
                response += f"- **Limit Up**: {cellular.get('limitUp', 'Unlimited')} Kbps\n"
                response += f"- **Limit Down**: {cellular.get('limitDown', 'Unlimited')} Kbps\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting uplink bandwidth settings: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_devices_statuses",
        description="📊 Get device status across organization appliances"
    )
    def get_organization_appliance_devices_statuses(
        organization_id: str,
        per_page: int = 1000,
        network_ids: Optional[str] = None
    ):
        """Get device status across organization appliances."""
        try:
            kwargs = {'perPage': per_page, 'total_pages': 'all'}
            
            if network_ids:
                kwargs['networkIds'] = network_ids.split(',')
            
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDevicesStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Organization Appliance Device Status\n\n"
            
            if not result:
                response += "*No appliance device data found*\n"
                return response
            
            response += f"**Total Appliances**: {len(result)}\n\n"
            
            # Group by status
            status_summary = {
                'online': 0,
                'offline': 0,
                'alerting': 0,
                'dormant': 0
            }
            
            for device in result:
                status = device.get('status', '').lower()
                if status in status_summary:
                    status_summary[status] += 1
            
            response += "## Device Status Summary\n"
            for status, count in status_summary.items():
                if count > 0:
                    emoji = "✅" if status == "online" else "⚠️" if status == "alerting" else "❌"
                    response += f"- **{emoji} {status.title()}**: {count} devices\n"
            
            response += f"\n## Device Details (showing first 10)\n"
            for device in result[:10]:
                response += f"### {device.get('name', 'Unknown Device')}\n"
                response += f"- **Serial**: {device.get('serial', 'N/A')}\n"
                response += f"- **Model**: {device.get('model', 'N/A')}\n"
                response += f"- **Status**: {device.get('status', 'Unknown')}\n"
                response += f"- **Network**: {device.get('networkName', 'Unknown')}\n"
                
                if device.get('lastReportedAt'):
                    response += f"- **Last Reported**: {device.get('lastReportedAt')}\n"
                
                response += "\n"
            
            if len(result) > 10:
                response += f"*...and {len(result) - 10} more devices*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization device statuses: {str(e)}"
    
    # More comprehensive appliance tools (both GET and UPDATE/CREATE)
    @app.tool(
        name="get_network_appliance_uplinks",
        description="🔗 Get uplink configuration for network appliance"
    )
    def get_network_appliance_uplinks(network_id: str):
        """Get uplink configuration for network appliance."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceUplinks(network_id)
            
            response = f"# 🔗 Appliance Uplinks - {network_id}\n\n"
            
            if result:
                response += f"**Total Uplinks**: {len(result)}\n\n"
                
                for uplink in result:
                    response += f"## {uplink.get('interface', 'Unknown Interface')}\n"
                    response += f"- **Status**: {uplink.get('status', 'Unknown')}\n"
                    response += f"- **IP**: {uplink.get('ip', 'N/A')}\n"
                    response += f"- **Gateway**: {uplink.get('gateway', 'N/A')}\n"
                    response += f"- **DNS**: {', '.join(uplink.get('dns', []))}\n"
                    response += f"- **Using Static IP**: {'✅' if uplink.get('usingStaticIp') else '❌ DHCP'}\n"
                    response += "\n"
            else:
                response += "*No uplink configuration found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting uplinks: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_uplinks_settings",
        description="🔧 Update uplink settings for network appliance"
    )
    def update_network_appliance_uplinks_settings(
        network_id: str,
        wan1_enabled: bool = None,
        wan1_vlan_tagging_enabled: bool = None,
        wan1_vlan_tagging_vlan_id: int = None,
        wan1_static_ip: str = None,
        wan1_static_subnet_mask: str = None,
        wan1_static_gateway_ip: str = None,
        wan1_static_dns: str = None
    ):
        """Update uplink settings for network appliance."""
        try:
            interfaces = {}
            
            if any([wan1_enabled is not None, wan1_vlan_tagging_enabled is not None, 
                   wan1_static_ip, wan1_static_subnet_mask, wan1_static_gateway_ip, wan1_static_dns]):
                wan1 = {}
                
                if wan1_enabled is not None:
                    wan1['enabled'] = wan1_enabled
                    
                if wan1_vlan_tagging_enabled is not None:
                    wan1['vlanTagging'] = {
                        'enabled': wan1_vlan_tagging_enabled
                    }
                    if wan1_vlan_tagging_vlan_id is not None:
                        wan1['vlanTagging']['vlanId'] = wan1_vlan_tagging_vlan_id
                
                if wan1_static_ip:
                    wan1['usingStaticIp'] = True
                    wan1['staticIp'] = wan1_static_ip
                    if wan1_static_subnet_mask:
                        wan1['staticSubnetMask'] = wan1_static_subnet_mask
                    if wan1_static_gateway_ip:
                        wan1['staticGatewayIp'] = wan1_static_gateway_ip
                    if wan1_static_dns:
                        wan1['staticDns'] = wan1_static_dns.split(',')
                
                interfaces['wan1'] = wan1
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceUplinksSettings(
                network_id, interfaces=interfaces
            )
            
            response = f"# ✅ Uplink Settings Updated - {network_id}\n\n"
            
            # Show what was updated
            if 'wan1' in interfaces:
                response += "## WAN1 Updates\n"
                wan1_updates = interfaces['wan1']
                for key, value in wan1_updates.items():
                    response += f"- **{key}**: {value}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating uplink settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_static_route",
        description="🛣️ Update static route for network appliance"
    )
    def update_network_appliance_static_route(
        network_id: str,
        static_route_id: str,
        name: str = None,
        subnet: str = None,
        gateway_ip: str = None,
        enabled: bool = None
    ):
        """Update static route for network appliance."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if subnet:
                kwargs['subnet'] = subnet
            if gateway_ip:
                kwargs['gatewayIp'] = gateway_ip
            if enabled is not None:
                kwargs['enabled'] = enabled
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceStaticRoute(
                network_id, static_route_id, **kwargs
            )
            
            response = f"# ✅ Static Route Updated\n\n"
            response += f"**Route ID**: {static_route_id}\n"
            
            for key, value in kwargs.items():
                response += f"**{key}**: {value}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating static route: {str(e)}"
    
    @app.tool(
        name="delete_network_appliance_static_route",
        description="🗑️ Delete static route from network appliance"
    )
    def delete_network_appliance_static_route(network_id: str, static_route_id: str):
        """Delete static route from network appliance."""
        try:
            meraki_client.dashboard.appliance.deleteNetworkApplianceStaticRoute(
                network_id, static_route_id
            )
            
            response = f"# ✅ Static Route Deleted\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Route ID**: {static_route_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting static route: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_static_route",
        description="🛣️ Get specific static route details"
    )
    def get_network_appliance_static_route(network_id: str, static_route_id: str):
        """Get specific static route details."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceStaticRoute(
                network_id, static_route_id
            )
            
            response = f"# 🛣️ Static Route Details\n\n"
            response += f"**Route ID**: {static_route_id}\n"
            response += f"**Name**: {result.get('name', 'Unnamed')}\n"
            response += f"**Subnet**: {result.get('subnet', 'N/A')}\n"
            response += f"**Gateway IP**: {result.get('gatewayIp', 'N/A')}\n"
            response += f"**Enabled**: {'✅' if result.get('enabled') else '❌'}\n"
            
            # Fixed IP assignments
            fixed_assignments = result.get('fixedIpAssignments', {})
            if fixed_assignments:
                response += f"\n## Fixed IP Assignments ({len(fixed_assignments)})\n"
                for mac, assignment in fixed_assignments.items():
                    response += f"- **{mac}**: {assignment.get('ip')} ({assignment.get('name', 'No name')})\n"
            
            # Reserved IP ranges
            reserved_ranges = result.get('reservedIpRanges', [])
            if reserved_ranges:
                response += f"\n## Reserved IP Ranges ({len(reserved_ranges)})\n"
                for range_item in reserved_ranges:
                    response += f"- {range_item.get('start')} - {range_item.get('end')}: {range_item.get('comment', 'No comment')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting static route: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_settings", 
        description="⚙️ Update network appliance general settings"
    )
    def update_network_appliance_settings(
        network_id: str,
        client_tracking_method: str = None,
        deployment_mode: str = None,
        dynamic_dns: dict = None
    ):
        """Update network appliance general settings."""
        try:
            kwargs = {}
            if client_tracking_method:
                kwargs['clientTrackingMethod'] = client_tracking_method
            if deployment_mode:
                kwargs['deploymentMode'] = deployment_mode
            if dynamic_dns:
                kwargs['dynamicDns'] = dynamic_dns
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceSettings(network_id, **kwargs)
            
            response = f"# ⚙️ Network Appliance Settings Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            if result.get('clientTrackingMethod'):
                response += f"**Client Tracking Method**: {result['clientTrackingMethod']}\n"
            if result.get('deploymentMode'):
                response += f"**Deployment Mode**: {result['deploymentMode']}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating appliance settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_ssid",
        description="📶 Update appliance SSID configuration"
    )
    def update_network_appliance_ssid(
        network_id: str,
        number: str,
        name: str = None,
        enabled: bool = None,
        default_vlan_id: int = None,
        auth_mode: str = None,
        encryption_mode: str = None,
        psk: str = None,
        wpa_encryption_mode: str = None,
        dhcp_enforced_deauthentication: dict = None
    ):
        """Update appliance SSID configuration."""
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if enabled is not None:
                kwargs['enabled'] = enabled
            if default_vlan_id is not None:
                kwargs['defaultVlanId'] = default_vlan_id
            if auth_mode:
                kwargs['authMode'] = auth_mode
            if encryption_mode:
                kwargs['encryptionMode'] = encryption_mode
            if psk:
                kwargs['psk'] = psk
            if wpa_encryption_mode:
                kwargs['wpaEncryptionMode'] = wpa_encryption_mode
            if dhcp_enforced_deauthentication:
                kwargs['dhcpEnforcedDeauthentication'] = dhcp_enforced_deauthentication
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceSsid(network_id, number, **kwargs)
            
            response = f"# 📶 Appliance SSID Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**SSID Number**: {number}\n"
            if result.get('name'):
                response += f"**Name**: {result['name']}\n"
            if 'enabled' in result:
                response += f"**Enabled**: {result['enabled']}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating appliance SSID: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_traffic_shaping",
        description="🚦 Update network appliance traffic shaping rules"
    )
    def update_network_appliance_traffic_shaping(
        network_id: str,
        global_bandwidth_limits: dict = None,
        rules: list = None
    ):
        """Update network appliance traffic shaping rules."""
        try:
            kwargs = {}
            if global_bandwidth_limits:
                kwargs['globalBandwidthLimits'] = global_bandwidth_limits
            if rules:
                kwargs['rules'] = rules
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShaping(network_id, **kwargs)
            
            response = f"# 🚦 Traffic Shaping Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            if result.get('globalBandwidthLimits'):
                response += f"**Global Limits**: Configured\n"
            if result.get('rules'):
                response += f"**Rules Count**: {len(result['rules'])}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating traffic shaping: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_traffic_shaping_custom_perf_class",
        description="🎯 Update custom performance class for traffic shaping"
    )
    def update_network_appliance_traffic_shaping_custom_perf_class(
        network_id: str,
        custom_performance_class_id: str,
        name: str = None,
        max_latency: int = None,
        max_jitter: int = None,
        max_loss_percentage: int = None
    ):
        """Update custom performance class for appliance traffic shaping."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if max_latency is not None:
                kwargs['maxLatency'] = max_latency
            if max_jitter is not None:
                kwargs['maxJitter'] = max_jitter
            if max_loss_percentage is not None:
                kwargs['maxLossPercentage'] = max_loss_percentage
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id, custom_performance_class_id, **kwargs
            )
            
            response = f"# 🎯 Custom Performance Class Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Class ID**: {custom_performance_class_id}\n"
            if result.get('name'):
                response += f"**Name**: {result['name']}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating custom performance class: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_traffic_shaping_uplink_bandwidth",
        description="⬆️ Update uplink bandwidth settings for traffic shaping"
    )
    def update_network_appliance_traffic_shaping_uplink_bandwidth(
        network_id: str,
        bandwidth_limits: dict = None,
        cellular_failover: dict = None
    ):
        """Update uplink bandwidth settings for appliance traffic shaping."""
        try:
            kwargs = {}
            if bandwidth_limits:
                kwargs['bandwidthLimits'] = bandwidth_limits
            if cellular_failover:
                kwargs['cellularFailover'] = cellular_failover
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingUplinkBandwidth(
                network_id, **kwargs
            )
            
            response = f"# ⬆️ Uplink Bandwidth Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            if result.get('bandwidthLimits'):
                response += f"**Bandwidth Limits**: Configured\n"
            if result.get('cellularFailover'):
                response += f"**Cellular Failover**: Configured\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating uplink bandwidth: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_vpn_bgp",
        description="🌐 Update BGP configuration for appliance VPN"
    )
    def update_network_appliance_vpn_bgp(
        network_id: str,
        enabled: bool,
        as_number: int = None,
        ibgp_holdtimer: int = None,
        neighbors: list = None
    ):
        """Update BGP configuration for appliance VPN."""
        try:
            kwargs = {'enabled': enabled}
            if as_number is not None:
                kwargs['asNumber'] = as_number
            if ibgp_holdtimer is not None:
                kwargs['ibgpHoldtimer'] = ibgp_holdtimer
            if neighbors:
                kwargs['neighbors'] = neighbors
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVpnBgp(network_id, **kwargs)
            
            response = f"# 🌐 BGP Configuration Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Enabled**: {result.get('enabled', enabled)}\n"
            if result.get('asNumber'):
                response += f"**AS Number**: {result['asNumber']}\n"
            if result.get('neighbors'):
                response += f"**Neighbors**: {len(result['neighbors'])} configured\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating BGP configuration: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_vpn_site_to_site_vpn",
        description="🔗 Update site-to-site VPN configuration"
    )
    def update_network_appliance_vpn_site_to_site_vpn(
        network_id: str,
        mode: str,
        hubs: list = None,
        subnets: list = None
    ):
        """Update site-to-site VPN configuration for appliance."""
        try:
            kwargs = {'mode': mode}
            if hubs:
                kwargs['hubs'] = hubs
            if subnets:
                kwargs['subnets'] = subnets
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(network_id, **kwargs)
            
            response = f"# 🔗 Site-to-Site VPN Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Mode**: {result.get('mode', mode)}\n"
            if result.get('hubs'):
                response += f"**Hubs**: {len(result['hubs'])} configured\n"
            if result.get('subnets'):
                response += f"**Subnets**: {len(result['subnets'])} configured\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating site-to-site VPN: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_l3_firewall_rules",
        description="🔥 Update Layer 3 firewall rules"
    )
    def update_network_appliance_firewall_l3_firewall_rules(
        network_id: str,
        rules: list,
        syslog_default_rule: bool = None
    ):
        """Update Layer 3 firewall rules for appliance."""
        try:
            kwargs = {'rules': rules}
            if syslog_default_rule is not None:
                kwargs['syslogDefaultRule'] = syslog_default_rule
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
                network_id, **kwargs
            )
            
            response = f"# 🔥 L3 Firewall Rules Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Rules Count**: {len(result.get('rules', []))}\n"
            if 'syslogDefaultRule' in result:
                response += f"**Syslog Default Rule**: {result['syslogDefaultRule']}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating L3 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_l7_firewall_rules",
        description="🔥 Update Layer 7 firewall rules"
    )
    def update_network_appliance_firewall_l7_firewall_rules(
        network_id: str,
        rules: list = None
    ):
        """Update Layer 7 firewall rules for appliance."""
        try:
            kwargs = {}
            if rules:
                kwargs['rules'] = rules
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL7FirewallRules(
                network_id, **kwargs
            )
            
            response = f"# 🔥 L7 Firewall Rules Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Rules Count**: {len(result.get('rules', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_inbound_firewall_rules",
        description="🔥 Update inbound firewall rules"
    )
    def update_network_appliance_firewall_inbound_firewall_rules(
        network_id: str,
        rules: list,
        syslog_default_rule: bool = None
    ):
        """Update inbound firewall rules for appliance."""
        try:
            kwargs = {'rules': rules}
            if syslog_default_rule is not None:
                kwargs['syslogDefaultRule'] = syslog_default_rule
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallInboundFirewallRules(
                network_id, **kwargs
            )
            
            response = f"# 🔥 Inbound Firewall Rules Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Rules Count**: {len(result.get('rules', []))}\n"
            if 'syslogDefaultRule' in result:
                response += f"**Syslog Default Rule**: {result['syslogDefaultRule']}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating inbound firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_inbound_cellular_fw_rules",
        description="📱 Update inbound cellular firewall rules"
    )
    def update_network_appliance_firewall_inbound_cellular_fw_rules(
        network_id: str,
        rules: list = None
    ):
        """Update inbound cellular firewall rules for appliance."""
        try:
            kwargs = {}
            if rules:
                kwargs['rules'] = rules
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallInboundCellularFirewallRules(
                network_id, **kwargs
            )
            
            response = f"# 📱 Inbound Cellular Firewall Rules Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Rules Count**: {len(result.get('rules', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating inbound cellular firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_one_to_many_nat_rules",
        description="🔀 Update one-to-many NAT rules"
    )
    def update_network_appliance_firewall_one_to_many_nat_rules(
        network_id: str,
        rules: list
    ):
        """Update one-to-many NAT rules for appliance."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallOneToManyNatRules(
                network_id, rules=rules
            )
            
            response = f"# 🔀 One-to-Many NAT Rules Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Rules Count**: {len(result.get('rules', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating one-to-many NAT rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_single_lan",
        description="🏠 Update single LAN configuration"
    )
    def update_network_appliance_single_lan(
        network_id: str,
        subnet: str = None,
        appliance_ip: str = None,
        ipv6: dict = None
    ):
        """Update single LAN configuration for appliance."""
        try:
            kwargs = {}
            if subnet:
                kwargs['subnet'] = subnet
            if appliance_ip:
                kwargs['applianceIp'] = appliance_ip
            if ipv6:
                kwargs['ipv6'] = ipv6
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceSingleLan(
                network_id, **kwargs
            )
            
            response = f"# 🏠 Single LAN Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            if result.get('subnet'):
                response += f"**Subnet**: {result['subnet']}\n"
            if result.get('applianceIp'):
                response += f"**Appliance IP**: {result['applianceIp']}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating single LAN: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_vlans_settings",
        description="🏷️ Update VLANs settings for network appliance"
    )
    def update_network_appliance_vlans_settings(
        network_id: str,
        vlans_enabled: bool = None
    ):
        """Update VLANs settings for network appliance."""
        try:
            kwargs = {}
            if vlans_enabled is not None:
                kwargs['vlansEnabled'] = vlans_enabled
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVlansSettings(
                network_id, **kwargs
            )
            
            response = f"# 🏷️ VLANs Settings Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            if 'vlansEnabled' in result:
                response += f"**VLANs Enabled**: {result['vlansEnabled']}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating VLANs settings: {str(e)}"
    
    @app.tool(
        name="update_organization_appliance_vpn_third_party_vpn_peers",
        description="🔗 Update organization third-party VPN peers"
    )
    def update_organization_appliance_vpn_third_party_vpn_peers(
        organization_id: str,
        peers: list
    ):
        """Update third-party VPN peers for organization appliance."""
        try:
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceVpnThirdPartyVPNPeers(
                organization_id, peers=peers
            )
            
            response = f"# 🔗 Third-Party VPN Peers Updated\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Peers Count**: {len(result.get('peers', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating third-party VPN peers: {str(e)}"
    
    @app.tool(
        name="update_organization_appliance_vpn_vpn_firewall_rules",
        description="🔥 Update organization VPN firewall rules"
    )
    def update_organization_appliance_vpn_vpn_firewall_rules(
        organization_id: str,
        rules: list = None,
        syslog_default_rule: bool = None
    ):
        """Update VPN firewall rules for organization appliance."""
        try:
            kwargs = {}
            if rules:
                kwargs['rules'] = rules
            if syslog_default_rule is not None:
                kwargs['syslogDefaultRule'] = syslog_default_rule
                
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceVpnVpnFirewallRules(
                organization_id, **kwargs
            )
            
            response = f"# 🔥 Organization VPN Firewall Rules Updated\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Rules Count**: {len(result.get('rules', []))}\n"
            if 'syslogDefaultRule' in result:
                response += f"**Syslog Default Rule**: {result['syslogDefaultRule']}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating organization VPN firewall rules: {str(e)}"
    
    @app.tool(
        name="get_device_appliance_performance",
        description="📊 Get device appliance performance metrics"
    )
    def get_device_appliance_performance(serial: str, t0: str = None, t1: str = None, timespan: int = 3600):
        """Get device appliance performance metrics."""
        try:
            kwargs = {}
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
                
            result = meraki_client.dashboard.appliance.getDeviceAppliancePerformance(serial, **kwargs)
            
            response = f"# 📊 Device Appliance Performance\n\n"
            response += f"**Device Serial**: {serial}\n"
            
            if result:
                for metric in result:
                    response += f"**Timestamp**: {metric.get('startTs', 'N/A')}\n"
                    if 'perfScore' in metric:
                        response += f"**Performance Score**: {metric['perfScore']}\n"
                    if 'latencyMs' in metric:
                        response += f"**Latency**: {metric['latencyMs']}ms\n"
                    response += "\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting device performance: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_sdwan_internet_policies",
        description="🌐 Update SD-WAN internet policies"
    )
    def update_network_appliance_sdwan_internet_policies(
        network_id: str,
        wan_traffic_uplink_preferences: list = None
    ):
        """Update SD-WAN internet policies for appliance."""
        try:
            kwargs = {}
            if wan_traffic_uplink_preferences:
                kwargs['wanTrafficUplinkPreferences'] = wan_traffic_uplink_preferences
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceSdwanInternetPolicies(network_id, **kwargs)
            
            response = f"# 🌐 SD-WAN Internet Policies Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            if result.get('wanTrafficUplinkPreferences'):
                response += f"**Policies Count**: {len(result['wanTrafficUplinkPreferences'])}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating SD-WAN policies: {str(e)}"

    # DNS Management Tools (NEW in 2025 SDK)
    
    @app.tool(
        name="bulk_org_appliance_dns_local_profiles_assignments_create",
        description="📋 Bulk create DNS local profile assignments"
    )
    def bulk_organization_appliance_dns_local_profiles_assignments_create(
        organization_id: str,
        profiles: list
    ):
        """Bulk create DNS local profile assignments."""
        try:
            result = meraki_client.dashboard.appliance.bulkOrganizationApplianceDnsLocalProfilesAssignmentsCreate(
                organization_id, profiles=profiles
            )
            
            response = f"# 📋 DNS Profile Assignments Created\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Assignments**: {len(result)} created\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating DNS profile assignments: {str(e)}"
    
    @app.tool(
        name="create_organization_appliance_dns_local_profile",
        description="🌐 Create DNS local profile"
    )
    def create_organization_appliance_dns_local_profile(
        organization_id: str,
        name: str,
        dns_servers: list,
        description: str = None
    ):
        """Create DNS local profile."""
        try:
            kwargs = {'name': name, 'dnsServers': dns_servers}
            if description:
                kwargs['description'] = description
                
            result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsLocalProfile(
                organization_id, **kwargs
            )
            
            response = f"# 🌐 DNS Local Profile Created\n\n"
            response += f"**Profile ID**: {result.get('profileId', 'N/A')}\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**DNS Servers**: {len(result.get('dnsServers', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating DNS local profile: {str(e)}"
    
    @app.tool(
        name="create_organization_appliance_dns_local_record",
        description="📝 Create DNS local record"
    )
    def create_organization_appliance_dns_local_record(
        organization_id: str,
        profile_id: str,
        fqdn: str,
        value: str
    ):
        """Create DNS local record."""
        try:
            result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsLocalRecord(
                organization_id, profileId=profile_id, fqdn=fqdn, value=value
            )
            
            response = f"# 📝 DNS Local Record Created\n\n"
            response += f"**Record ID**: {result.get('recordId', 'N/A')}\n"
            response += f"**FQDN**: {result.get('fqdn', fqdn)}\n"
            response += f"**Value**: {result.get('value', value)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating DNS local record: {str(e)}"
    
    @app.tool(
        name="delete_organization_appliance_dns_local_profile",
        description="🗑️ Delete DNS local profile"
    )
    def delete_organization_appliance_dns_local_profile(
        organization_id: str,
        profile_id: str
    ):
        """Delete DNS local profile."""
        try:
            meraki_client.dashboard.appliance.deleteOrganizationApplianceDnsLocalProfile(
                organization_id, profile_id
            )
            
            response = f"# 🗑️ DNS Local Profile Deleted\n\n"
            response += f"**Profile ID**: {profile_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting DNS local profile: {str(e)}"
    
    @app.tool(
        name="delete_organization_appliance_dns_local_record",
        description="🗑️ Delete DNS local record"
    )
    def delete_organization_appliance_dns_local_record(
        organization_id: str,
        record_id: str
    ):
        """Delete DNS local record."""
        try:
            meraki_client.dashboard.appliance.deleteOrganizationApplianceDnsLocalRecord(
                organization_id, record_id
            )
            
            response = f"# 🗑️ DNS Local Record Deleted\n\n"
            response += f"**Record ID**: {record_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting DNS local record: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_dns_local_profiles",
        description="📋 Get DNS local profiles"
    )
    def get_organization_appliance_dns_local_profiles(organization_id: str):
        """Get DNS local profiles."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsLocalProfiles(
                organization_id
            )
            
            response = f"# 📋 DNS Local Profiles\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Profiles Count**: {len(result)}\n\n"
            
            for profile in result:
                response += f"## {profile.get('name', 'Unnamed')}\n"
                response += f"- **Profile ID**: {profile.get('profileId', 'N/A')}\n"
                response += f"- **DNS Servers**: {len(profile.get('dnsServers', []))}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DNS local profiles: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_dns_local_profiles_assignments",
        description="📋 Get DNS local profile assignments"
    )
    def get_organization_appliance_dns_local_profiles_assignments(organization_id: str):
        """Get DNS local profile assignments."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsLocalProfilesAssignments(
                organization_id
            )
            
            response = f"# 📋 DNS Profile Assignments\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Assignments Count**: {len(result)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DNS profile assignments: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_dns_local_records",
        description="📝 Get DNS local records"
    )
    def get_organization_appliance_dns_local_records(organization_id: str):
        """Get DNS local records."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsLocalRecords(
                organization_id
            )
            
            response = f"# 📝 DNS Local Records\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Records Count**: {len(result)}\n\n"
            
            for record in result:
                response += f"## {record.get('fqdn', 'N/A')}\n"
                response += f"- **Value**: {record.get('value', 'N/A')}\n"
                response += f"- **Record ID**: {record.get('recordId', 'N/A')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DNS local records: {str(e)}"
    
    @app.tool(
        name="update_organization_appliance_dns_local_profile",
        description="🔄 Update DNS local profile"
    )
    def update_organization_appliance_dns_local_profile(
        organization_id: str,
        profile_id: str,
        name: str = None,
        dns_servers: list = None,
        description: str = None
    ):
        """Update DNS local profile."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if dns_servers:
                kwargs['dnsServers'] = dns_servers
            if description:
                kwargs['description'] = description
                
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceDnsLocalProfile(
                organization_id, profile_id, **kwargs
            )
            
            response = f"# 🔄 DNS Local Profile Updated\n\n"
            response += f"**Profile ID**: {profile_id}\n"
            response += f"**Name**: {result.get('name', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating DNS local profile: {str(e)}"
    
    @app.tool(
        name="update_organization_appliance_dns_local_record",
        description="🔄 Update DNS local record"
    )
    def update_organization_appliance_dns_local_record(
        organization_id: str,
        record_id: str,
        fqdn: str = None,
        value: str = None
    ):
        """Update DNS local record."""
        try:
            kwargs = {}
            if fqdn:
                kwargs['fqdn'] = fqdn
            if value:
                kwargs['value'] = value
                
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceDnsLocalRecord(
                organization_id, record_id, **kwargs
            )
            
            response = f"# 🔄 DNS Local Record Updated\n\n"
            response += f"**Record ID**: {record_id}\n"
            response += f"**FQDN**: {result.get('fqdn', 'N/A')}\n"
            response += f"**Value**: {result.get('value', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating DNS local record: {str(e)}"
    
    # Split DNS Tools (NEW in 2025 SDK)
    
    @app.tool(
        name="create_organization_appliance_dns_split_profile",
        description="🔀 Create DNS split profile"
    )
    def create_organization_appliance_dns_split_profile(
        organization_id: str,
        name: str,
        domains: list,
        description: str = None
    ):
        """Create DNS split profile."""
        try:
            kwargs = {'name': name, 'domains': domains}
            if description:
                kwargs['description'] = description
                
            result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsSplitProfile(
                organization_id, **kwargs
            )
            
            response = f"# 🔀 DNS Split Profile Created\n\n"
            response += f"**Profile ID**: {result.get('profileId', 'N/A')}\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**Domains**: {len(result.get('domains', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating DNS split profile: {str(e)}"
    
    @app.tool(
        name="delete_organization_appliance_dns_split_profile",
        description="🗑️ Delete DNS split profile"
    )
    def delete_organization_appliance_dns_split_profile(
        organization_id: str,
        profile_id: str
    ):
        """Delete DNS split profile."""
        try:
            meraki_client.dashboard.appliance.deleteOrganizationApplianceDnsSplitProfile(
                organization_id, profile_id
            )
            
            response = f"# 🗑️ DNS Split Profile Deleted\n\n"
            response += f"**Profile ID**: {profile_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting DNS split profile: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_dns_split_profiles",
        description="🔀 Get DNS split profiles"
    )
    def get_organization_appliance_dns_split_profiles(organization_id: str):
        """Get DNS split profiles."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsSplitProfiles(
                organization_id
            )
            
            response = f"# 🔀 DNS Split Profiles\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Profiles Count**: {len(result)}\n\n"
            
            for profile in result:
                response += f"## {profile.get('name', 'Unnamed')}\n"
                response += f"- **Profile ID**: {profile.get('profileId', 'N/A')}\n"
                response += f"- **Domains**: {len(profile.get('domains', []))}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DNS split profiles: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_dns_split_profiles_assignments",
        description="🔀 Get DNS split profile assignments"
    )
    def get_organization_appliance_dns_split_profiles_assignments(organization_id: str):
        """Get DNS split profile assignments."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsSplitProfilesAssignments(
                organization_id
            )
            
            response = f"# 🔀 DNS Split Profile Assignments\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Assignments Count**: {len(result)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DNS split profile assignments: {str(e)}"
    
    @app.tool(
        name="update_organization_appliance_dns_split_profile",
        description="🔄 Update DNS split profile"
    )
    def update_organization_appliance_dns_split_profile(
        organization_id: str,
        profile_id: str,
        name: str = None,
        domains: list = None,
        description: str = None
    ):
        """Update DNS split profile."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if domains:
                kwargs['domains'] = domains
            if description:
                kwargs['description'] = description
                
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceDnsSplitProfile(
                organization_id, profile_id, **kwargs
            )
            
            response = f"# 🔄 DNS Split Profile Updated\n\n"
            response += f"**Profile ID**: {profile_id}\n"
            response += f"**Name**: {result.get('name', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating DNS split profile: {str(e)}"
    
    # Device-Level Appliance Tools
    
    @app.tool(
        name="get_device_appliance_prefixes_delegated",
        description="📡 Get device appliance delegated prefixes"
    )
    def get_device_appliance_prefixes_delegated(serial: str):
        """Get device appliance delegated prefixes."""
        try:
            result = meraki_client.dashboard.appliance.getDeviceAppliancePrefixesDelegated(serial)
            
            response = f"# 📡 Device Appliance Delegated Prefixes\n\n"
            response += f"**Device Serial**: {serial}\n"
            response += f"**Prefixes Count**: {len(result)}\n\n"
            
            for prefix in result:
                response += f"## Prefix: {prefix.get('prefix', 'N/A')}\n"
                response += f"- **Origin**: {prefix.get('origin', 'N/A')}\n"
                response += f"- **Description**: {prefix.get('description', 'N/A')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting delegated prefixes: {str(e)}"
    
    @app.tool(
        name="get_device_appliance_prefixes_delegated_vlan_assignments",
        description="🏷️ Get device appliance delegated prefix VLAN assignments"
    )
    def get_device_appliance_prefixes_delegated_vlan_assignments(
        serial: str,
        prefix_id: str
    ):
        """Get device appliance delegated prefix VLAN assignments."""
        try:
            result = meraki_client.dashboard.appliance.getDeviceAppliancePrefixesDelegatedVlanAssignments(
                serial, prefix_id
            )
            
            response = f"# 🏷️ Delegated Prefix VLAN Assignments\n\n"
            response += f"**Device Serial**: {serial}\n"
            response += f"**Prefix ID**: {prefix_id}\n"
            response += f"**Assignments Count**: {len(result)}\n\n"
            
            for assignment in result:
                response += f"## VLAN {assignment.get('vlanId', 'N/A')}\n"
                response += f"- **Prefix**: {assignment.get('prefix', 'N/A')}\n"
                response += f"- **Origin**: {assignment.get('origin', 'N/A')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting VLAN assignments: {str(e)}"
    
    @app.tool(
        name="get_device_appliance_radio_settings",
        description="📻 Get device appliance radio settings"
    )
    def get_device_appliance_radio_settings(serial: str):
        """Get device appliance radio settings."""
        try:
            result = meraki_client.dashboard.appliance.getDeviceApplianceRadioSettings(serial)
            
            response = f"# 📻 Device Appliance Radio Settings\n\n"
            response += f"**Device Serial**: {serial}\n"
            response += f"**RF Profile ID**: {result.get('rfProfileId', 'N/A')}\n"
            response += f"**Two Four Ghz Settings**:\n"
            
            two_four_ghz = result.get('twoFourGhzSettings', {})
            response += f"- **Channel**: {two_four_ghz.get('channel', 'N/A')}\n"
            response += f"- **Target Power**: {two_four_ghz.get('targetPower', 'N/A')}\n"
            
            response += f"**Five Ghz Settings**:\n"
            five_ghz = result.get('fiveGhzSettings', {})
            response += f"- **Channel**: {five_ghz.get('channel', 'N/A')}\n"
            response += f"- **Target Power**: {five_ghz.get('targetPower', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting radio settings: {str(e)}"
    
    @app.tool(
        name="update_device_appliance_radio_settings",
        description="🔄 Update device appliance radio settings"
    )
    def update_device_appliance_radio_settings(
        serial: str,
        rf_profile_id: str = None,
        two_four_ghz_settings: dict = None,
        five_ghz_settings: dict = None
    ):
        """Update device appliance radio settings."""
        try:
            kwargs = {}
            if rf_profile_id:
                kwargs['rfProfileId'] = rf_profile_id
            if two_four_ghz_settings:
                kwargs['twoFourGhzSettings'] = two_four_ghz_settings
            if five_ghz_settings:
                kwargs['fiveGhzSettings'] = five_ghz_settings
                
            result = meraki_client.dashboard.appliance.updateDeviceApplianceRadioSettings(
                serial, **kwargs
            )
            
            response = f"# 🔄 Radio Settings Updated\n\n"
            response += f"**Device Serial**: {serial}\n"
            response += f"**RF Profile ID**: {result.get('rfProfileId', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating radio settings: {str(e)}"
    
    @app.tool(
        name="get_device_appliance_uplinks_settings",
        description="⬆️ Get device appliance uplink settings"
    )
    def get_device_appliance_uplinks_settings(serial: str):
        """Get device appliance uplink settings."""
        try:
            result = meraki_client.dashboard.appliance.getDeviceApplianceUplinksSettings(serial)
            
            response = f"# ⬆️ Device Appliance Uplink Settings\n\n"
            response += f"**Device Serial**: {serial}\n"
            
            interfaces = result.get('interfaces', {})
            for interface_name, settings in interfaces.items():
                response += f"## {interface_name}\n"
                response += f"- **Enabled**: {settings.get('enabled', 'N/A')}\n"
                response += f"- **VLAN Tagging**: {settings.get('vlanTagging', {}).get('enabled', 'N/A')}\n"
                response += f"- **SVIS**: {len(settings.get('svis', {}))}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting uplink settings: {str(e)}"
    
    @app.tool(
        name="update_device_appliance_uplinks_settings",
        description="🔄 Update device appliance uplink settings"
    )
    def update_device_appliance_uplinks_settings(
        serial: str,
        interfaces: dict
    ):
        """Update device appliance uplink settings."""
        try:
            result = meraki_client.dashboard.appliance.updateDeviceApplianceUplinksSettings(
                serial, interfaces=interfaces
            )
            
            response = f"# 🔄 Uplink Settings Updated\n\n"
            response += f"**Device Serial**: {serial}\n"
            response += f"**Interfaces**: {len(result.get('interfaces', {}))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating uplink settings: {str(e)}"
    
    # VMX Authentication Token
    
    @app.tool(
        name="create_device_appliance_vmx_authentication_token",
        description="🔐 Create VMX authentication token"
    )
    def create_device_appliance_vmx_authentication_token(serial: str):
        """Create VMX authentication token."""
        try:
            result = meraki_client.dashboard.appliance.createDeviceApplianceVmxAuthenticationToken(serial)
            
            response = f"# 🔐 VMX Authentication Token Created\n\n"
            response += f"**Device Serial**: {serial}\n"
            response += f"**Token**: {result.get('token', 'N/A')}\n"
            response += f"**Expires At**: {result.get('expiresAt', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating VMX authentication token: {str(e)}"
    
    # Multicast, VPN Exclusions and Missing Organization Tools
    
    @app.tool(
        name="get_org_appliance_firewall_multicast_forwarding_by_network",
        description="📡 Get multicast forwarding by network"
    )
    def get_organization_appliance_firewall_multicast_forwarding_by_network(
        organization_id: str
    ):
        """Get multicast forwarding by network."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceFirewallMulticastForwardingByNetwork(
                organization_id
            )
            
            response = f"# 📡 Multicast Forwarding by Network\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Networks Count**: {len(result)}\n\n"
            
            for network in result:
                response += f"## Network: {network.get('networkId', 'N/A')}\n"
                response += f"- **Name**: {network.get('networkName', 'N/A')}\n"
                response += f"- **Rules**: {len(network.get('rules', []))}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting multicast forwarding: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_multicast_forwarding",
        description="🔄 Update multicast forwarding"
    )
    def update_network_appliance_firewall_multicast_forwarding(
        network_id: str,
        rules: list
    ):
        """Update multicast forwarding."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallMulticastForwarding(
                network_id, rules=rules
            )
            
            response = f"# 🔄 Multicast Forwarding Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Rules**: {len(result.get('rules', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating multicast forwarding: {str(e)}"
    
    @app.tool(
        name="get_org_appliance_traffic_shaping_vpn_exclusions_by_network",
        description="🚫 Get VPN exclusions by network"
    )
    def get_organization_appliance_traffic_shaping_vpn_exclusions_by_network(
        organization_id: str
    ):
        """Get VPN exclusions by network."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceTrafficShapingVpnExclusionsByNetwork(
                organization_id
            )
            
            response = f"# 🚫 VPN Exclusions by Network\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Networks Count**: {len(result)}\n\n"
            
            for network in result:
                response += f"## Network: {network.get('networkId', 'N/A')}\n"
                response += f"- **Name**: {network.get('networkName', 'N/A')}\n"
                response += f"- **Custom**: {len(network.get('custom', []))}\n"
                response += f"- **Major Applications**: {len(network.get('majorApplications', []))}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting VPN exclusions: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_traffic_shaping_vpn_exclusions",
        description="🔄 Update VPN exclusions"
    )
    def update_network_appliance_traffic_shaping_vpn_exclusions(
        network_id: str,
        custom: list = None,
        major_applications: list = None
    ):
        """Update VPN exclusions."""
        try:
            kwargs = {}
            if custom:
                kwargs['custom'] = custom
            if major_applications:
                kwargs['majorApplications'] = major_applications
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingVpnExclusions(
                network_id, **kwargs
            )
            
            response = f"# 🔄 VPN Exclusions Updated\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Custom**: {len(result.get('custom', []))}\n"
            response += f"**Major Applications**: {len(result.get('majorApplications', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating VPN exclusions: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_uplinks_statuses_overview",
        description="📊 Get uplinks statuses overview"
    )
    def get_organization_appliance_uplinks_statuses_overview(organization_id: str):
        """Get uplinks statuses overview."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceUplinksStatusesOverview(
                organization_id
            )
            
            response = f"# 📊 Uplinks Statuses Overview\n\n"
            response += f"**Organization ID**: {organization_id}\n"
            response += f"**Counts**:\n"
            
            counts = result.get('counts', {})
            response += f"- **Total**: {counts.get('total', 0)}\n"
            response += f"- **Online**: {counts.get('online', 0)}\n"
            response += f"- **Offline**: {counts.get('offline', 0)}\n"
            response += f"- **Warning**: {counts.get('warning', 0)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting uplinks overview: {str(e)}"
    
    # Missing Network-Level Appliance Tools
    
    @app.tool(
        name="get_network_appliance_connectivity_monitoring_destinations",
        description="🔍 Get connectivity monitoring destinations"
    )
    def get_network_appliance_connectivity_monitoring_destinations(network_id: str):
        """Get connectivity monitoring destinations."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceConnectivityMonitoringDestinations(
                network_id
            )
            
            response = f"# 🔍 Connectivity Monitoring Destinations\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Destinations Count**: {len(result.get('destinations', []))}\n\n"
            
            for dest in result.get('destinations', []):
                response += f"## {dest.get('ip', 'N/A')}\n"
                response += f"- **Description**: {dest.get('description', 'N/A')}\n"
                response += f"- **Default**: {dest.get('default', False)}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting monitoring destinations: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_cellular_firewall_rules",
        description="📱 Get cellular firewall rules"
    )
    def get_network_appliance_firewall_cellular_firewall_rules(network_id: str):
        """Get cellular firewall rules."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallCellularFirewallRules(
                network_id
            )
            
            response = f"# 📱 Cellular Firewall Rules\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Rules Count**: {len(result.get('rules', []))}\n\n"
            
            for rule in result.get('rules', []):
                response += f"## Rule: {rule.get('comment', 'No comment')}\n"
                response += f"- **Policy**: {rule.get('policy', 'N/A')}\n"
                response += f"- **Protocol**: {rule.get('protocol', 'N/A')}\n"
                response += f"- **Source**: {rule.get('srcCidr', 'N/A')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting cellular firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_firewalled_service",
        description="🔥 Get firewalled service"
    )
    def get_network_appliance_firewall_firewalled_service(
        network_id: str,
        service: str
    ):
        """Get firewalled service."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallFirewalledService(
                network_id, service
            )
            
            response = f"# 🔥 Firewalled Service\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Service**: {result.get('service', service)}\n"
            response += f"**Access**: {result.get('access', 'N/A')}\n"
            response += f"**Allowed IPs**: {result.get('allowedIps', [])}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting firewalled service: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_l7_fw_rules_app_categories",
        description="📱 Get L7 firewall application categories"
    )
    def get_network_appliance_firewall_l7_firewall_rules_application_categories(
        network_id: str
    ):
        """Get L7 firewall application categories."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(
                network_id
            )
            
            response = f"# 📱 L7 Firewall Application Categories\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Categories Count**: {len(result.get('applicationCategories', []))}\n\n"
            
            for category in result.get('applicationCategories', []):
                response += f"## {category.get('name', 'N/A')}\n"
                response += f"- **ID**: {category.get('id', 'N/A')}\n"
                response += f"- **Applications**: {len(category.get('applications', []))}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting application categories: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_traffic_shaping_custom_perf_classes",
        description="🎯 Get custom performance classes"
    )
    def get_network_appliance_traffic_shaping_custom_performance_classes(
        network_id: str
    ):
        """Get custom performance classes."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClasses(
                network_id
            )
            
            response = f"# 🎯 Custom Performance Classes\n\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Classes Count**: {len(result)}\n\n"
            
            for perf_class in result:
                response += f"## {perf_class.get('name', 'Unnamed')}\n"
                response += f"- **ID**: {perf_class.get('customPerformanceClassId', 'N/A')}\n"
                response += f"- **Max Latency**: {perf_class.get('maxLatency', 'N/A')}ms\n"
                response += f"- **Max Jitter**: {perf_class.get('maxJitter', 'N/A')}ms\n"
                response += f"- **Max Loss**: {perf_class.get('maxLossPercentage', 'N/A')}%\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting custom performance classes: {str(e)}"
    
    @app.tool(
        name="create_network_appliance_rf_profile",
        description="📻 Create RF profile"
    )
    def create_network_appliance_rf_profile(
        network_id: str,
        name: str,
        two_four_ghz_settings: dict = None,
        five_ghz_settings: dict = None,
        per_ssid_settings: dict = None
    ):
        """Create RF profile."""
        try:
            kwargs = {'name': name}
            if two_four_ghz_settings:
                kwargs['twoFourGhzSettings'] = two_four_ghz_settings
            if five_ghz_settings:
                kwargs['fiveGhzSettings'] = five_ghz_settings
            if per_ssid_settings:
                kwargs['perSsidSettings'] = per_ssid_settings
                
            result = meraki_client.dashboard.appliance.createNetworkApplianceRfProfile(
                network_id, **kwargs
            )
            
            response = f"# 📻 RF Profile Created\n\n"
            response += f"**Profile ID**: {result.get('id', 'N/A')}\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**Network ID**: {result.get('networkId', network_id)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating RF profile: {str(e)}"
    
# Register additional appliance tools in main handler

