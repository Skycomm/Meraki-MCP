"""
NetFlow tools for the Cisco Meraki MCP Server.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_netflow_tools(mcp_app, meraki):
    """
    Register netflow tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Netflow
    @app.tool(
        name="get_network_netflow",
        description="📊 Get NetFlow settings"
    )
    def get_network_netflow(network_id: str):
        """Get NetFlow traffic reporting settings."""
        try:
            netflow = meraki_client.dashboard.networks.getNetworkNetflow(network_id)
            
            result = f"# 📊 NetFlow Settings\n\n"
            result += f"**Reporting Enabled**: {'✅' if netflow.get('reportingEnabled') else '❌'}\n"
            
            if netflow.get('collectorIp'):
                result += f"**Collector IP**: {netflow['collectorIp']}\n"
                result += f"**Collector Port**: {netflow.get('collectorPort', 9996)}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving NetFlow settings: {str(e)}"
    
    @app.tool(
        name="update_network_netflow",
        description="📊 Update NetFlow settings"
    )
    def update_network_netflow(network_id: str, **kwargs):
        """Update NetFlow traffic reporting settings."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkNetflow(
                network_id, **kwargs
            )
            
            return f"✅ NetFlow settings updated successfully!"
            
        except Exception as e:
            return f"Error updating NetFlow settings: {str(e)}"