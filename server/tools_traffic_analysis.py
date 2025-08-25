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
            
            mode = traffic.get('mode', 'disabled')
            result = f"# 📈 Traffic Analysis Settings\n\n"
            result += f"**Mode**: {mode}\n"
            
            # Add helpful status indicator
            if mode == 'detailed':
                result += "✅ **Status**: Fully enabled with hostname visibility\n"
            elif mode == 'basic':
                result += "⚠️ **Status**: Basic traffic categories only\n"
            else:
                result += "❌ **Status**: Traffic analysis disabled\n"
            
            if traffic.get('customPieChartItems'):
                items = traffic['customPieChartItems']
                result += f"\n**Custom Categories**: {len(items)}\n"
                for item in items[:5]:
                    result += f"- {item.get('name')} ({item.get('type')})\n"
            
            if mode != 'detailed':
                result += f"\n💡 **Tip**: To enable full traffic analysis, use:\n"
                result += f"`update_network_traffic_analysis(network_id, mode='detailed')`\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving traffic analysis settings: {str(e)}"
    
    @app.tool(
        name="update_network_traffic_analysis",
        description="📈 Update traffic analysis settings (mode: disabled/basic/detailed)"
    )
    def update_network_traffic_analysis(network_id: str, mode: str = None, **kwargs):
        """
        Update traffic analysis settings for a network.
        
        Args:
            network_id: The network ID
            mode: Traffic analysis mode - "disabled", "basic", or "detailed" (for hostname visibility)
            **kwargs: Additional parameters like customPieChartItems
        
        Example: To enable full traffic analysis with hostname visibility:
            update_network_traffic_analysis(network_id, mode="detailed")
        """
        try:
            # Build parameters
            params = {}
            if mode:
                if mode not in ["disabled", "basic", "detailed"]:
                    return f"❌ Invalid mode '{mode}'. Must be: disabled, basic, or detailed"
                params['mode'] = mode
            
            # Add any additional kwargs
            params.update(kwargs)
            
            # If no parameters provided, default to enabling detailed mode
            if not params:
                params['mode'] = 'detailed'
                
            result = meraki_client.dashboard.networks.updateNetworkTrafficAnalysis(
                network_id, **params
            )
            
            mode_desc = params.get('mode', 'unchanged')
            return f"✅ Traffic analysis settings updated successfully! Mode: {mode_desc}"
            
        except Exception as e:
            return f"Error updating traffic analysis settings: {str(e)}"