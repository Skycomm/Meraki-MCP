"""
Switch-related tools for the Cisco Meraki MCP Server - Modern implementation.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_switch_tools(mcp_app, meraki):
    """
    Register switch-related tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all switch tools
    register_switch_tool_handlers()

def register_switch_tool_handlers():
    """Register all switch-related tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_device_switch_ports",
        description="List switch ports for a Meraki switch"
    )
    def get_device_switch_ports(serial: str):
        """
        List switch ports for a Meraki switch.
        
        Args:
            serial: Serial number of the switch
            
        Returns:
            Formatted list of switch ports
        """
        try:
            ports = meraki_client.get_device_switch_ports(serial)
            
            if not ports:
                return f"No switch ports found for device {serial}."
                
            # Format the output for readability
            result = f"# Switch Ports for Device ({serial})\n\n"
            for port in ports:
                port_num = port.get('portId', 'Unknown')
                port_name = port.get('name', f'Port {port_num}')
                
                result += f"## {port_name} (Port {port_num})\n"
                result += f"- Enabled: {port.get('enabled', False)}\n"
                result += f"- Type: {port.get('type', 'Unknown')}\n"
                result += f"- VLAN: {port.get('vlan', 'Unknown')}\n"
                
                # Add additional settings
                poe_enabled = port.get('poeEnabled', False)
                result += f"- PoE Enabled: {poe_enabled}\n"
                
                if poe_enabled:
                    result += f"- PoE Type: {port.get('poeType', 'Unknown')}\n"
                
                stp_enabled = port.get('stpEnabled', False)
                result += f"- STP Enabled: {stp_enabled}\n"
                
                # Add access policy if available
                access_policy = port.get('accessPolicy', 'Open')
                result += f"- Access Policy: {access_policy}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list switch ports for device {serial}: {str(e)}"
    
    @app.tool(
        name="update_device_switch_port",
        description="Update a switch port for a Meraki switch"
    )
    def update_device_switch_port(serial: str, port_number: int, name: str = None, enabled: bool = None, 
                                 vlan: int = None, poe_enabled: bool = None):
        """
        Update a switch port for a Meraki switch.
        
        Args:
            serial: Serial number of the switch
            port_number: Number of the port to update
            name: New name for the port (optional)
            enabled: Whether the port should be enabled (optional)
            vlan: VLAN ID for the port (optional)
            poe_enabled: Whether PoE should be enabled (optional)
            
        Returns:
            Updated port details
        """
        return meraki_client.update_device_switch_port(serial, port_number, name, enabled, vlan, poe_enabled)
    
    @app.tool(
        name="get_device_switch_port_statuses",
        description="Get status information for switch ports"
    )
    def get_device_switch_port_statuses(serial: str):
        """
        Get status information for switch ports.
        
        Args:
            serial: Serial number of the switch
            
        Returns:
            Formatted switch port status information
        """
        try:
            statuses = meraki_client.get_device_switch_port_statuses(serial)
            
            if not statuses:
                return f"No switch port status information found for device {serial}."
                
            # Format the output for readability
            result = f"# Switch Port Statuses for Device ({serial})\n\n"
            for status in statuses:
                port_num = status.get('portId', 'Unknown')
                
                result += f"## Port {port_num}\n"
                result += f"- Status: {status.get('status', 'Unknown')}\n"
                result += f"- Speed: {status.get('speed', 'Unknown')}\n"
                result += f"- Duplex: {status.get('duplex', 'Unknown')}\n"
                
                # Add client details if available
                client = status.get('clientId')
                if client:
                    result += f"- Connected Client: `{client}`\n"
                
                # Add errors if available
                errors = status.get('errors', [])
                if errors:
                    result += "- Errors:\n"
                    for error in errors:
                        result += f"  - {error}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to get switch port statuses for device {serial}: {str(e)}"
    
    @app.tool(
        name="get_device_switch_vlans",
        description="List VLANs for a Meraki switch"
    )
    def get_device_switch_vlans(serial: str):
        """
        List VLANs for a Meraki switch.
        
        Args:
            serial: Serial number of the switch
            
        Returns:
            Formatted list of VLANs
        """
        try:
            vlans = meraki_client.get_device_switch_vlans(serial)
            
            if not vlans:
                return f"No VLANs found for device {serial}."
                
            # Format the output for readability
            result = f"# VLANs for Switch ({serial})\n\n"
            for vlan in vlans:
                vlan_id = vlan.get('id', 'Unknown')
                vlan_name = vlan.get('name', f'VLAN {vlan_id}')
                
                result += f"## {vlan_name} (ID: {vlan_id})\n"
                result += f"- Subnet: {vlan.get('subnet', 'Unknown')}\n"
                result += f"- IP Assignment Mode: {vlan.get('ipAssignmentMode', 'Unknown')}\n"
                
                dhcp_options = vlan.get('dhcpOptions', {})
                if dhcp_options:
                    result += "- DHCP Options:\n"
                    for key, value in dhcp_options.items():
                        result += f"  - {key}: {value}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list VLANs for device {serial}: {str(e)}"
    
    @app.tool(
        name="create_device_switch_vlan",
        description="Create a new VLAN for a Meraki switch"
    )
    def create_device_switch_vlan(serial: str, vlan_id: int, name: str, subnet: str = None):
        """
        Create a new VLAN for a Meraki switch.
        
        Args:
            serial: Serial number of the switch
            vlan_id: ID for the new VLAN
            name: Name for the new VLAN
            subnet: Subnet for the new VLAN (optional)
            
        Returns:
            New VLAN details
        """
        return meraki_client.create_device_switch_vlan(serial, vlan_id, name, subnet)
