"""
Group Policies management tools for Cisco Meraki MCP Server.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_group_policies_tools(mcp_app, meraki):
    """Register group policies tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all group policies tools
    register_group_policies_handlers()

def register_group_policies_handlers():
    """Register all group policies-related tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_network_group_policies",
        description="👥 List all group policies for a network"
    )
    def get_network_group_policies(network_id: str):
        """List group policies for a network."""
        try:
            policies = meraki_client.dashboard.networks.getNetworkGroupPolicies(network_id)
            
            if not policies:
                return f"No group policies found for network {network_id}."
            
            result = f"# 👥 Group Policies\n\n"
            result += f"**Total Policies**: {len(policies)}\n\n"
            
            for policy in policies:
                result += f"## {policy.get('name', 'Unnamed')}\n"
                result += f"- ID: {policy.get('groupPolicyId')}\n"
                
                if policy.get('bandwidth'):
                    bw = policy['bandwidth']
                    result += f"- Bandwidth: {bw.get('bandwidthLimits', 'No limits')}\n"
                
                if policy.get('firewallAndTrafficShaping'):
                    fw = policy['firewallAndTrafficShaping']
                    if fw.get('l3FirewallRules'):
                        result += f"- L3 Firewall Rules: {len(fw['l3FirewallRules'])}\n"
                    if fw.get('l7FirewallRules'):
                        result += f"- L7 Firewall Rules: {len(fw['l7FirewallRules'])}\n"
                
                if policy.get('vlanTagging'):
                    vlan = policy['vlanTagging']
                    result += f"- VLAN: {vlan.get('vlanId', 'Not set')}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving group policies: {str(e)}"
    
    @app.tool(
        name="create_network_group_policy",
        description="👥 Create a group policy"
    )
    def create_network_group_policy(network_id: str, name: str, **kwargs):
        """Create a group policy."""
        try:
            result = meraki_client.dashboard.networks.createNetworkGroupPolicy(
                network_id, name, **kwargs
            )
            
            return f"✅ Group policy '{name}' created successfully!\n\nPolicy ID: {result.get('groupPolicyId')}"
            
        except Exception as e:
            return f"Error creating group policy: {str(e)}"
    
    @app.tool(
        name="get_network_group_policy",
        description="👥 Get group policy details"
    )
    def get_network_group_policy(network_id: str, groupPolicyId: str):
        """Get details of a group policy."""
        try:
            policy = meraki_client.dashboard.networks.getNetworkGroupPolicy(
                network_id, groupPolicyId
            )
            
            result = f"# 👥 Group Policy Details\n\n"
            result += f"**Name**: {policy.get('name')}\n"
            result += f"**ID**: {policy.get('groupPolicyId')}\n"
            
            if policy.get('bandwidth'):
                result += "\n**Bandwidth Settings**:\n"
                bw = policy['bandwidth']
                settings = bw.get('settings')
                if settings == 'custom':
                    limits = bw.get('bandwidthLimits', {})
                    result += f"- Download: {limits.get('limitDown', 'Unlimited')} Mbps\n"
                    result += f"- Upload: {limits.get('limitUp', 'Unlimited')} Mbps\n"
                else:
                    result += f"- Settings: {settings}\n"
            
            if policy.get('vlanTagging'):
                vlan = policy['vlanTagging']
                result += f"\n**VLAN Settings**:\n"
                result += f"- VLAN ID: {vlan.get('vlanId', 'Not set')}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving group policy: {str(e)}"
    
    @app.tool(
        name="update_network_group_policy",
        description="👥 Update a group policy"
    )
    def update_network_group_policy(network_id: str, groupPolicyId: str, **kwargs):
        """Update a group policy."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkGroupPolicy(
                network_id, groupPolicyId, **kwargs
            )
            
            return f"✅ Group policy updated successfully!"
            
        except Exception as e:
            return f"Error updating group policy: {str(e)}"
    
    @app.tool(
        name="delete_network_group_policy",
        description="👥 Delete a group policy"
    )
    def delete_network_group_policy(network_id: str, groupPolicyId: str):
        """Delete a group policy."""
        try:
            meraki_client.dashboard.networks.deleteNetworkGroupPolicy(network_id, groupPolicyId)
            
            return f"✅ Group policy deleted successfully!"
            
        except Exception as e:
            return f"Error deleting group policy: {str(e)}"