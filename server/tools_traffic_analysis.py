"""
Traffic Analysis tools for the Cisco Meraki MCP Server.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_traffic_analysis_tools(mcp_app, meraki):
    """
    Register traffic analysis tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Traffic Analysis
    @app.tool(
        name="get_network_traffic_analysis",
        description="📈 Get traffic analysis settings"
    )
    def get_network_traffic_analysis(network_id: str):
        """Get traffic analysis settings for a network."""
        try:
            traffic = meraki_client.dashboard.networks.getNetworkTrafficAnalysis(network_id)
            
            result = f"# 📈 Traffic Analysis Settings\n\n"
            result += f"**Mode**: {traffic.get('mode', 'Disabled')}\n"
            
            if traffic.get('customPieChartItems'):
                items = traffic['customPieChartItems']
                result += f"\n**Custom Categories**: {len(items)}\n"
                for item in items[:5]:
                    result += f"- {item.get('name')} ({item.get('type')})\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving traffic analysis settings: {str(e)}"
    
    @app.tool(
        name="update_network_traffic_analysis",
        description="📈 Update traffic analysis settings"
    )
    def update_network_traffic_analysis(network_id: str, **kwargs):
        """Update traffic analysis settings for a network."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkTrafficAnalysis(
                network_id, **kwargs
            )
            
            return f"✅ Traffic analysis settings updated successfully!"
            
        except Exception as e:
            return f"Error updating traffic analysis settings: {str(e)}"