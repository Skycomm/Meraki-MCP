"""
Resource handling for the Cisco Meraki MCP Server - Modern implementation.
"""

import json
import mcp.types as types
from utils.helpers import format_resource_uri, create_resource, create_content, format_error_message

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_resources(mcp_app, meraki):
    """
    Register resource handlers with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all resources
    register_resource_handlers()

def register_resource_handlers():
    """Register all resource handlers using the decorator pattern."""
    
    # Organizations resources
    @app.resource("organizations://")
    def get_organizations():
        """List all Meraki organizations."""
        return meraki_client.get_organizations()

    @app.resource("organizations://{org_id}")
    def get_organization(org_id):
        """Get details for a specific organization."""
        return meraki_client.get_organization(org_id)

    @app.resource("organizations://{org_id}/networks")
    def get_organization_networks(org_id):
        """Get networks for a specific organization."""
        return meraki_client.get_organization_networks(org_id)
        
    @app.resource("organizations://{org_id}/alerts")
    def get_organization_alerts(org_id):
        """Get alerts for a specific organization."""
        return meraki_client.get_organization_alerts(org_id)
        
    @app.resource("organizations://{org_id}/firmware")
    def get_organization_firmware(org_id):
        """Get firmware upgrades for a specific organization."""
        return meraki_client.get_organization_firmware_upgrades(org_id)

    # Networks resources
    @app.resource("networks://")
    def get_networks():
        """List all networks (requires organization context, so returns help message)."""
        return {"help": "Please use organizations://{org_id}/networks to list networks for a specific organization"}

    @app.resource("networks://{network_id}")
    def get_network(network_id):
        """Get details for a specific network."""
        return meraki_client.get_network(network_id)
        
    @app.resource("networks://{network_id}/devices")
    def get_network_devices(network_id):
        """Get devices in a specific network."""
        return meraki_client.get_network_devices(network_id)
        
    @app.resource("networks://{network_id}/clients")
    def get_network_clients(network_id):
        """Get clients in a specific network."""
        return meraki_client.get_network_clients(network_id)
        
    @app.resource("networks://{network_id}/wireless/ssids")
    def get_network_ssids(network_id):
        """Get wireless SSIDs for a specific network."""
        return meraki_client.get_network_wireless_ssids(network_id)
        
    @app.resource("networks://{network_id}/vlans")
    def get_network_vlans(network_id):
        """Get VLANs for a specific network."""
        return meraki_client.get_network_vlans(network_id)

    # Devices resources
    @app.resource("devices://")
    def get_devices():
        """List all devices (requires network context, so returns help message)."""
        return {"help": "Please use networks://{network_id}/devices to list devices for a specific network"}

    @app.resource("devices://{serial}")
    def get_device(serial):
        """Get details for a specific device."""
        return meraki_client.get_device(serial)
        
    @app.resource("devices://{serial}/switch/ports")
    def get_device_switch_ports(serial):
        """Get switch ports for a specific device."""
        return meraki_client.get_device_switch_ports(serial)
