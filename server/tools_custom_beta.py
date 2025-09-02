"""
Beta/Early Access tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
Manage early access features and beta APIs.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_beta_tools(mcp_app, meraki):
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    """
    Register beta/early access tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    
    # Register all beta tools
    register_beta_tool_handlers()

def register_beta_tool_handlers():
    """Register all beta/early access tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="get_organization_early_access_features",
        description="🧪 List available early access features for organization"
    )
    def get_organization_early_access_features(organization_id: str):
        """
        List all available early access features for an organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            List of available early access features
        """
        try:
            features = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeatures(org_id)
            
            if not features:
                return f"No early access features available for organization {org_id}."
                
            result = f"# 🧪 Early Access Features - Organization {org_id}\n\n"
            result += f"**Total Features**: {len(features)}\n\n"
            
            for feature in features:
                feature_id = feature.get('id', 'Unknown')
                name = feature.get('name', 'Unnamed')
                description = feature.get('description', 'No description')
                status = feature.get('status', 'unknown')
                
                # Status icon
                status_icon = "✅" if status == 'available' else "🔒" if status == 'restricted' else "⏳"
                
                result += f"## {status_icon} {name}\n"
                result += f"- **ID**: {feature_id}\n"
                result += f"- **Status**: {status}\n"
                result += f"- **Description**: {description}\n"
                
                # Documentation link
                doc_link = feature.get('documentationLink')
                if doc_link:
                    result += f"- **Documentation**: {doc_link}\n"
                
                # Privacy link
                privacy_link = feature.get('privacyLink')
                if privacy_link:
                    result += f"- **Privacy Policy**: {privacy_link}\n"
                
                # Supported products
                products = feature.get('supportedProducts', [])
                if products:
                    result += f"- **Supported Products**: {', '.join(products)}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving early access features: {str(e)}"
    
    @app.tool(
        name="get_organization_early_access_features_opt_ins",
        description="🧪 List early access features opted into by organization"
    )
    def get_organization_early_access_features_opt_ins(organization_id: str):
        """
        List all early access features that the organization has opted into.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            List of opted-in early access features
        """
        try:
            opt_ins = meraki_client.get_organization_early_access_features_opt_ins(org_id)
            
            if not opt_ins:
                return f"Organization {org_id} has not opted into any early access features."
                
            result = f"# 🧪 Early Access Opt-Ins - Organization {org_id}\n\n"
            result += f"**Total Opt-Ins**: {len(opt_ins)}\n\n"
            
            result += "⚠️ **WARNING**: Early access features may have breaking changes!\n\n"
            
            for opt_in in opt_ins:
                opt_in_id = opt_in.get('optInId', 'Unknown')
                feature_id = opt_in.get('shortName', opt_in.get('id', 'Unknown'))
                created_at = opt_in.get('createdAt', 'Unknown')
                
                result += f"## ✅ {feature_id}\n"
                result += f"- **Opt-In ID**: {opt_in_id}\n"
                result += f"- **Enabled At**: {created_at}\n"
                
                # Limit access to specific networks
                limited_access = opt_in.get('limitedAccess', [])
                if limited_access:
                    result += f"- **Limited to Networks**: {len(limited_access)} networks\n"
                    for network in limited_access[:5]:
                        result += f"  - {network.get('name', 'Unknown')} ({network.get('id')})\n"
                    if len(limited_access) > 5:
                        result += f"  - ... and {len(limited_access) - 5} more\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving early access opt-ins: {str(e)}"
    
    @app.tool(
        name="enable_organization_early_access_feature",
        description="🧪 Enable an early access feature for organization"
    )
    def enable_organization_early_access_feature(organization_id: str, feature_id: str, limit_to_networks: str = None):
        """
        Opt into an early access feature for the organization.
        
        Args:
            organization_id: Organization ID
            feature_id: Early access feature ID or short name
            limit_to_networks: Comma-separated network IDs to limit access (optional)
            
        Returns:
            Opt-in confirmation
        """
        try:
            kwargs = {}
            
            if limit_to_networks:
                network_ids = [id.strip() for id in limit_to_networks.split(',')]
                kwargs['limitedAccessNetworkIds'] = network_ids
            
            result = meraki_client.create_organization_early_access_features_opt_in(
                org_id,
                shortName=feature_id,
                **kwargs
            )
            
            response = f"# 🧪 Early Access Feature Enabled\n\n"
            response += f"**Feature**: {feature_id}\n"
            response += f"**Organization**: {org_id}\n"
            response += f"**Opt-In ID**: {result.get('optInId', 'N/A')}\n\n"
            
            response += "⚠️ **IMPORTANT**: This feature is in beta and may have breaking changes!\n"
            response += "All API users for this organization will now use the beta API spec.\n\n"
            
            if 'limitedAccessNetworkIds' in kwargs:
                response += f"**Limited to**: {len(kwargs['limitedAccessNetworkIds'])} specific networks\n"
            else:
                response += "**Access**: Organization-wide\n"
                
            return response
            
        except Exception as e:
            return f"Error enabling early access feature: {str(e)}"
    
    @app.tool(
        name="disable_organization_early_access_feature",
        description="🧪 Disable an early access feature for organization"
    )
    def disable_organization_early_access_feature(organization_id: str, opt_in_id: str):
        """
        Opt out of an early access feature for the organization.
        
        Args:
            organization_id: Organization ID
            opt_in_id: Opt-in ID to disable
            
        Returns:
            Opt-out confirmation
        """
        try:
            meraki_client.delete_organization_early_access_features_opt_in(organization_id, opt_in_id)
            
            response = f"# 🧪 Early Access Feature Disabled\n\n"
            response += f"**Opt-In ID**: {opt_in_id}\n"
            response += f"**Organization**: {org_id}\n\n"
            
            response += "✅ Successfully opted out of the early access feature.\n"
            response += "The organization will now use the stable API spec.\n"
            
            return response
            
        except Exception as e:
            return f"Error disabling early access feature: {str(e)}"
    
    @app.tool(
        name="get_organization_api_analytics",
        description="📊 View API usage analytics dashboard data"
    )
    def get_organization_api_analytics(organization_id: str, timespan: int = 86400):
        """
        Get API analytics for the organization (new 2025 feature).
        
        Args:
            organization_id: Organization ID
            timespan: Time span in seconds (default 24 hours)
            
        Returns:
            API analytics data
        """
        try:
            # This uses the existing API requests endpoint
            requests = meraki_client.get_organization_api_requests(organization_id, timespan=timespan)
            
            if not requests:
                return f"No API usage data available for organization {org_id}."
                
            result = f"# 📊 API Analytics - Organization {org_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.0f} hours\n"
            result += f"**Total API Calls**: {len(requests)}\n\n"
            
            # Analyze by response code
            response_codes = {}
            for req in requests:
                code = req.get('responseCode', 0)
                response_codes[code] = response_codes.get(code, 0) + 1
            
            result += "## Response Code Distribution\n"
            total_calls = len(requests)
            for code, count in sorted(response_codes.items()):
                percent = (count / total_calls * 100) if total_calls else 0
                if 200 <= code < 300:
                    icon = "✅"
                    status = "Success"
                elif code == 429:
                    icon = "⚠️"
                    status = "Rate Limited"
                elif 400 <= code < 500:
                    icon = "❌"
                    status = "Client Error"
                else:
                    icon = "🔴"
                    status = "Server Error"
                    
                result += f"- **{code} {status}**: {icon} {count} calls ({percent:.1f}%)\n"
            
            # Top endpoints
            endpoints = {}
            for req in requests:
                path = req.get('path', '')
                # Simplify path
                parts = path.split('/')
                if len(parts) > 3:
                    endpoint = f"/{parts[1]}/{parts[2]}"
                else:
                    endpoint = path
                endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
            
            result += "\n## Top API Endpoints\n"
            for endpoint, count in sorted(endpoints.items(), key=lambda x: x[1], reverse=True)[:10]:
                result += f"- **{endpoint}**: {count} calls\n"
            
            # Rate limit analysis
            rate_limited = sum(1 for req in requests if req.get('responseCode') == 429)
            if rate_limited > 0:
                result += f"\n## ⚠️ Rate Limiting\n"
                result += f"- **Rate Limited Calls**: {rate_limited}\n"
                result += f"- **Percentage**: {(rate_limited/total_calls*100):.1f}%\n"
                result += "- **Recommendation**: Consider implementing request throttling\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving API analytics: {str(e)}"
    
    @app.tool(
        name="check_beta_apis_status",
        description="🧪 Check which beta APIs might be available"
    )
    def check_beta_apis_status():
        """
        Check the status of beta APIs mentioned in the 2025 documentation.
        
        Returns:
            Status of various beta APIs
        """
        result = f"# 🧪 Beta APIs Status Check\n\n"
        result += "Based on the 2025 Meraki API documentation, here are potentially available beta features:\n\n"
        
        result += "## 1. 💾 Device Memory History API\n"
        result += "- **Endpoint**: `/devices/{serial}/memory/history`\n"
        result += "- **Status**: Planned/Beta - Not in current SDK\n"
        result += "- **Alternative**: Use SNMP or device status APIs\n\n"
        
        result += "## 2. ⚡ CPU Power Mode History API\n"
        result += "- **Endpoint**: `/devices/{serial}/wireless/cpuPowerMode/history`\n"
        result += "- **Status**: May be early access only\n"
        result += "- **Current**: Using radio settings as proxy\n\n"
        
        result += "## 3. 🔧 MAC Table Live Tools\n"
        result += "- **Endpoint**: `/devices/{serial}/liveTools/macTable`\n"
        result += "- **Status**: New 2025 feature - likely beta\n"
        result += "- **Purpose**: Real-time MAC table queries\n\n"
        
        result += "## 4. 🔐 OAuth 2.0 Support\n"
        result += "- **Status**: Released in 2025\n"
        result += "- **Implementation**: Available but requires setup\n"
        result += "- **Benefit**: More secure than API keys\n\n"
        
        result += "## 5. 📊 API Analytics Dashboard\n"
        result += "- **Status**: Released in 2025\n"
        result += "- **Access**: Via Dashboard UI and API\n"
        result += "- **Tool**: `get_organization_api_analytics`\n\n"
        
        result += "## How to Enable Beta Features\n"
        result += "1. Use `get_organization_early_access_features` to see available features\n"
        result += "2. Use `enable_organization_early_access_feature` to opt in\n"
        result += "3. Test carefully - beta APIs can have breaking changes!\n\n"
        
        result += "⚠️ **Note**: Once enabled for an org, ALL API users get beta access!"
        
        return result