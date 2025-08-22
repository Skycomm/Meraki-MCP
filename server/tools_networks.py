"""
Network-related tools for the Cisco Meraki MCP Server - Modern implementation.
"""

import os

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_network_tools(mcp_app, meraki):
    """
    Register network-related tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all network tools
    register_network_tool_handlers()

def register_network_tool_handlers():
    """Register all network-related tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_network",
        description="Get details about a specific Meraki network"
    )
    def get_network(network_id: str):
        """
        Get details about a specific Meraki network.
        
        Args:
            network_id: ID of the network to retrieve
            
        Returns:
            Network details
        """
        return meraki_client.get_network(network_id)
    
    @app.tool(
        name="update_network",
        description="Update a Meraki network"
    )
    def update_network(network_id: str, name: str = None, tags: list = None):
        """
        Update a Meraki network.
        
        Args:
            network_id: ID of the network to update
            name: New name for the network (optional)
            tags: New tags for the network (optional)
            
        Returns:
            Updated network details
        """
        try:
            # Get current network details
            network = meraki_client.get_network(network_id)
            current_name = network.get('name', 'Unknown')
            
            # If renaming, require confirmation
            if name and name != current_name:
                from utils.helpers import require_confirmation
                
                if not require_confirmation(
                    operation_type="rename",
                    resource_type="network",
                    resource_name=f"{current_name} → {name}",
                    resource_id=network_id
                ):
                    return "❌ Network rename cancelled by user"
            
            # Perform update
            result = meraki_client.update_network(network_id, name, tags)
            return f"✅ Network updated successfully"
            
        except Exception as e:
            return f"Failed to update network: {str(e)}"
    
    @app.tool(
        name="get_network_devices",
        description="List devices in a Meraki network"
    )
    def get_network_devices(network_id: str):
        """
        List devices in a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of devices
        """
        try:
            devices = meraki_client.get_network_devices(network_id)
            
            if not devices:
                return f"No devices found for network {network_id}."
                
            # Format the output for readability
            result = f"# Devices in Network ({network_id})\n\n"
            for device in devices:
                result += f"- **{device.get('name', 'Unnamed')}** (Model: {device.get('model', 'Unknown')})\n"
                result += f"  - Serial: `{device.get('serial', 'Unknown')}`\n"
                result += f"  - MAC: `{device.get('mac', 'Unknown')}`\n"
                result += f"  - Status: {device.get('status', 'Unknown')}\n"
                
                # Add location if available
                lat = device.get('lat')
                lng = device.get('lng')
                address = device.get('address')
                
                if lat and lng:
                    result += f"  - Location: ({lat}, {lng})\n"
                if address:
                    result += f"  - Address: {address}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list devices for network {network_id}: {str(e)}"
    
    @app.tool(
        name="get_network_clients",
        description="List clients in a Meraki network"
    )
    def get_network_clients(network_id: str):
        """
        List clients in a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of clients
        """
        try:
            clients = meraki_client.get_network_clients(network_id)
            
            if not clients:
                return f"No clients found for network {network_id}."
                
            # Format the output for readability
            result = f"# Clients in Network ({network_id})\n\n"
            for client in clients:
                result += f"- **{client.get('description', 'Unknown Device')}**\n"
                result += f"  - MAC: `{client.get('mac', 'Unknown')}`\n"
                result += f"  - IP: `{client.get('ip', 'Unknown')}`\n"
                result += f"  - VLAN: {client.get('vlan', 'Unknown')}\n"
                result += f"  - Connection: {client.get('status', 'Unknown')}\n"
                
                # Add usage if available
                usage = client.get('usage')
                if usage:
                    result += f"  - Usage: {usage.get('sent', 0)} sent, {usage.get('recv', 0)} received\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list clients for network {network_id}: {str(e)}"
    
    @app.tool(
        name="create_network",
        description="Create a new Meraki network in an organization"
    )
    def create_network(organization_id: str, name: str, product_types: str = "wireless"):
        """
        Create a new Meraki network in an organization.
        
        Args:
            organization_id: ID of the organization to create the network in
            name: Name for the new network
            product_types: Comma-separated product types (appliance,switch,wireless,camera,sensor)
            
        Returns:
            New network details
        """
        # Convert comma-separated string to list
        types_list = [t.strip() for t in product_types.split(',')]
        # BUGFIX: Pass productTypes as named parameter instead of positional
        return meraki_client.create_network(organization_id, name, productTypes=types_list)
    
    @app.tool(
        name="delete_network",
        description="Delete a Meraki network - REQUIRES CONFIRMATION"
    )
    def delete_network(network_id: str):
        """
        Delete a Meraki network.
        
        Args:
            network_id: ID of the network to delete
            
        Returns:
            Success/failure information
        """
        try:
            # Get network details first
            network = meraki_client.get_network(network_id)
            
            # Import helper functions
            from utils.helpers import require_confirmation, get_read_only_message
            
            # Check if in read-only mode first
            if os.getenv("MCP_READ_ONLY_MODE", "false").lower() == "true":
                return get_read_only_message(
                    operation_type="delete",
                    resource_type="network",
                    resource_name=network.get('name', 'Unknown'),
                    resource_id=network_id
                )
            
            # Require confirmation
            if not require_confirmation(
                operation_type="delete",
                resource_type="network", 
                resource_name=network.get('name', 'Unknown'),
                resource_id=network_id
            ):
                return "❌ Network deletion cancelled by user"
            
            # Perform deletion
            meraki_client.delete_network(network_id)
            return f"✅ Network '{network['name']}' deleted successfully"
            
        except Exception as e:
            return f"Failed to delete network: {str(e)}"
