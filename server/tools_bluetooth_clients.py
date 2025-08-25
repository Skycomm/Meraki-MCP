"""
Bluetooth Clients management tools for Cisco Meraki MCP Server.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_bluetooth_clients_tools(mcp_app, meraki):
    """Register bluetooth clients tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all bluetooth clients tools
    register_bluetooth_clients_handlers()

def register_bluetooth_clients_handlers():
    """Register all bluetooth clients-related tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_network_bluetooth_clients",
        description="📱 Get Bluetooth clients seen by the network"
    )
    def get_network_bluetooth_clients(network_id: str, **kwargs):
        """Get Bluetooth clients seen by the network."""
        try:
            clients = meraki_client.dashboard.networks.getNetworkBluetoothClients(
                network_id, **kwargs
            )
            
            if not clients:
                return f"No Bluetooth clients found in network {network_id}."
            
            result = f"# 📱 Bluetooth Clients\n\n"
            result += f"**Total Clients**: {len(clients)}\n\n"
            
            for client in clients[:20]:
                result += f"- **{client.get('name', 'Unknown')}**\n"
                result += f"  - MAC: {client.get('mac')}\n"
                result += f"  - Manufacturer: {client.get('manufacturer', 'Unknown')}\n"
                result += f"  - Device Type: {client.get('deviceType', 'Unknown')}\n"
                result += f"  - Last Seen: {client.get('lastSeen')}\n\n"
            
            if len(clients) > 20:
                result += f"... and {len(clients) - 20} more clients\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Bluetooth clients: {str(e)}"
    
    @app.tool(
        name="get_network_bluetooth_client",
        description="📱 Get details for a Bluetooth client"
    )
    def get_network_bluetooth_client(network_id: str, bluetoothClientId: str):
        """Get details for a specific Bluetooth client."""
        try:
            client = meraki_client.dashboard.networks.getNetworkBluetoothClient(
                network_id, bluetoothClientId
            )
            
            result = f"# 📱 Bluetooth Client Details\n\n"
            result += f"**Name**: {client.get('name', 'Unknown')}\n"
            result += f"**MAC**: {client.get('mac')}\n"
            result += f"**Manufacturer**: {client.get('manufacturer', 'Unknown')}\n"
            result += f"**Device Type**: {client.get('deviceType', 'Unknown')}\n"
            result += f"**Last Seen**: {client.get('lastSeen')}\n"
            
            if client.get('tags'):
                result += f"**Tags**: {', '.join(client['tags'])}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Bluetooth client: {str(e)}"