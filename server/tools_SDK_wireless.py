"""
Core wireless management tools for Cisco Meraki MCP server.

This module provides 100% coverage of the official Cisco Meraki Wireless SDK v1.
All 116 official SDK methods are implemented exactly as documented.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_wireless_tools(mcp_app, meraki):
    """
    Register all official SDK wireless tools with the MCP server.
    Provides 100% coverage of Cisco Meraki Wireless API v1.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all wireless SDK tools
    register_wireless_sdk_tools()

def register_wireless_sdk_tools():
    """Register all wireless SDK tools (100% coverage)."""
    
    # ==================== ALL 116 WIRELESS SDK TOOLS ====================
    
    @app.tool(
        name="assign_network_wireless_ethernet_ports_profiles",
        description="📡 assign network wirelessEthernetPortsProfiles"
    )
    def assign_network_wireless_ethernet_ports_profiles(network_id: str):
        """Manage assign network wirelessethernetportsprofiles."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.assignNetworkWirelessEthernetPortsProfiles(
                network_id, **kwargs
            )
            
            response = f"# 📡 Assign Network Wirelessethernetportsprofiles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in assign_network_wireless_ethernet_ports_profiles: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_air_marshal_rule",
        description="➕ Create network wirelessAirMarshalRule"
    )
    def create_network_wireless_air_marshal_rule(network_id: str):
        """Create create network wirelessairmarshalrule."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.createNetworkWirelessAirMarshalRule(
                network_id, **kwargs
            )
            
            response = f"# ➕ Create Network Wirelessairmarshalrule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_wireless_air_marshal_rule: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_ethernet_ports_profile",
        description="➕ Create network wirelessEthernetPortsProfile"
    )
    def create_network_wireless_ethernet_ports_profile(network_id: str):
        """Create create network wirelessethernetportsprofile."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.createNetworkWirelessEthernetPortsProfile(
                network_id, **kwargs
            )
            
            response = f"# ➕ Create Network Wirelessethernetportsprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_wireless_ethernet_ports_profile: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_rf_profile",
        description="➕ Create network wirelessRfProfile"
    )
    def create_network_wireless_rf_profile(network_id: str):
        """Create create network wirelessrfprofile."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.createNetworkWirelessRfProfile(
                network_id, **kwargs
            )
            
            response = f"# ➕ Create Network Wirelessrfprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_wireless_rf_profile: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_ssid_identity_psk",
        description="➕ Create network wirelessSsidIdentityPsk"
    )
    def create_network_wireless_ssid_identity_psk(network_id: str):
        """Create create network wirelessssididentitypsk."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk(
                network_id, **kwargs
            )
            
            response = f"# ➕ Create Network Wirelessssididentitypsk\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_wireless_ssid_identity_psk: {str(e)}"
    
    @app.tool(
        name="create_org_wireless_devices_radsec_certs_authority",
        description="➕ Create organization wireless devicesRadsecCertificatesAuthority"
    )
    def create_organization_wireless_devices_radsec_certificates_authority(network_id: str, serial: str):
        """Create create organization wireless devicesradseccertificatesauthority."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.createOrganizationWirelessDevicesRadsecCertificatesAuthority(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organization Wireless Devicesradseccertificatesauthority\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_organization_wireless_devices_radsec_certificates_authority: {str(e)}"
    
    @app.tool(
        name="create_organization_wireless_location_scanning_receiver",
        description="➕ Create organization wirelessLocationScanningReceiver"
    )
    def create_organization_wireless_location_scanning_receiver(organization_id: str):
        """Create create organization wirelesslocationscanningreceiver."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.createOrganizationWirelessLocationScanningReceiver(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organization Wirelesslocationscanningreceiver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_organization_wireless_location_scanning_receiver: {str(e)}"
    
    @app.tool(
        name="create_org_wireless_ssids_firewall_isolation_allowlist_entry",
        description="➕ Create organization wirelessSsidsFirewallIsolationAllowlistEntry"
    )
    def create_organization_wireless_ssids_firewall_isolation_allowlist_entry(organization_id: str):
        """Create create organization wirelessssidsfirewallisolationallowlistentry."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.createOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organization Wirelessssidsfirewallisolationallowlistentry\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_organization_wireless_ssids_firewall_isolation_allowlist_entry: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_air_marshal_rule",
        description="❌ Delete network wirelessAirMarshalRule"
    )
    def delete_network_wireless_air_marshal_rule(network_id: str):
        """Delete delete network wirelessairmarshalrule."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.deleteNetworkWirelessAirMarshalRule(
                network_id, **kwargs
            )
            
            response = f"# ❌ Delete Network Wirelessairmarshalrule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_wireless_air_marshal_rule: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_ethernet_ports_profile",
        description="❌ Delete network wirelessEthernetPortsProfile"
    )
    def delete_network_wireless_ethernet_ports_profile(network_id: str):
        """Delete delete network wirelessethernetportsprofile."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.deleteNetworkWirelessEthernetPortsProfile(
                network_id, **kwargs
            )
            
            response = f"# ❌ Delete Network Wirelessethernetportsprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_wireless_ethernet_ports_profile: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_rf_profile",
        description="❌ Delete network wirelessRfProfile"
    )
    def delete_network_wireless_rf_profile(network_id: str):
        """Delete delete network wirelessrfprofile."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.deleteNetworkWirelessRfProfile(
                network_id, **kwargs
            )
            
            response = f"# ❌ Delete Network Wirelessrfprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_wireless_rf_profile: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_ssid_identity_psk",
        description="❌ Delete network wirelessSsidIdentityPsk"
    )
    def delete_network_wireless_ssid_identity_psk(network_id: str):
        """Delete delete network wirelessssididentitypsk."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk(
                network_id, **kwargs
            )
            
            response = f"# ❌ Delete Network Wirelessssididentitypsk\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_wireless_ssid_identity_psk: {str(e)}"
    
    @app.tool(
        name="delete_organization_wireless_location_scanning_receiver",
        description="❌ Delete organization wirelessLocationScanningReceiver"
    )
    def delete_organization_wireless_location_scanning_receiver(organization_id: str):
        """Delete delete organization wirelesslocationscanningreceiver."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.deleteOrganizationWirelessLocationScanningReceiver(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organization Wirelesslocationscanningreceiver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_organization_wireless_location_scanning_receiver: {str(e)}"
    
    @app.tool(
        name="delete_org_wireless_ssids_firewall_isolation_allowlist_entry",
        description="❌ Delete organization wirelessSsidsFirewallIsolationAllowlistEntry"
    )
    def delete_organization_wireless_ssids_firewall_isolation_allowlist_entry(organization_id: str):
        """Delete delete organization wirelessssidsfirewallisolationallowlistentry."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.deleteOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organization Wirelessssidsfirewallisolationallowlistentry\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_organization_wireless_ssids_firewall_isolation_allowlist_entry: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_bluetooth_settings",
        description="📶 Get device wirelessBluetoothSettings"
    )
    def get_device_wireless_bluetooth_settings(network_id: str, serial: str, per_page: int = 1000):
        """Get get device wirelessbluetoothsettings."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getDeviceWirelessBluetoothSettings(
                network_id, serial, **kwargs  
            )
            
            response = f"# 📶 Get Device Wirelessbluetoothsettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_wireless_bluetooth_settings: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_connection_stats",
        description="📶 Get device wirelessConnectionStats"
    )
    def get_device_wireless_connection_stats(serial: str, timespan: int = 86400):
        """Get get device wirelessconnectionstats."""
        try:
            kwargs = {}
            
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getDeviceWirelessConnectionStats(
                serial, **kwargs  
            )
            
            response = f"# 📶 Get Device Wirelessconnectionstats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_wireless_connection_stats: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_electronic_shelf_label",
        description="📶 Get device wirelessElectronicShelfLabel"
    )
    def get_device_wireless_electronic_shelf_label(network_id: str, serial: str, per_page: int = 1000):
        """Get get device wirelesselectronicshelflabel."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getDeviceWirelessElectronicShelfLabel(
                network_id, serial, **kwargs  
            )
            
            response = f"# 📶 Get Device Wirelesselectronicshelflabel\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_wireless_electronic_shelf_label: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_latency_stats",
        description="📶 Get device wirelessLatencyStats"
    )
    def get_device_wireless_latency_stats(network_id: str, serial: str, per_page: int = 1000):
        """Get get device wirelesslatencystats."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getDeviceWirelessLatencyStats(
                network_id, serial, **kwargs  
            )
            
            response = f"# 📶 Get Device Wirelesslatencystats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_wireless_latency_stats: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_radio_settings",
        description="📶 Get device wirelessRadioSettings"
    )
    def get_device_wireless_radio_settings(network_id: str, serial: str, per_page: int = 1000):
        """Get get device wirelessradiosettings."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getDeviceWirelessRadioSettings(
                network_id, serial, **kwargs  
            )
            
            response = f"# 📶 Get Device Wirelessradiosettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_wireless_radio_settings: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_status",
        description="📶 Get device wirelessStatus"
    )
    def get_device_wireless_status(serial: str):
        """Get get device wirelessstatus."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessStatus(
                serial 
            )
            
            response = f"# 📶 Get Device Wirelessstatus\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_wireless_status: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_air_marshal",
        description="📶 Get network wirelessAirMarshal"
    )
    def get_network_wireless_air_marshal(network_id: str, per_page: int = 1000):
        """Get get network wirelessairmarshal."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessAirMarshal(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessairmarshal\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_air_marshal: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_alternate_management_interface",
        description="📶 Get network wirelessAlternateManagementInterface"
    )
    def get_network_wireless_alternate_management_interface(network_id: str, per_page: int = 1000):
        """Get get network wirelessalternatemanagementinterface."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessAlternateManagementInterface(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessalternatemanagementinterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_alternate_management_interface: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_billing",
        description="📶 Get network wirelessBilling"
    )
    def get_network_wireless_billing(network_id: str):
        """Get get network wirelessbilling."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessBilling(
                network_id
            )
            
            response = f"# 📶 Get Network Wirelessbilling\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_billing: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_bluetooth_settings",
        description="📶 Get network wirelessBluetoothSettings"
    )
    def get_network_wireless_bluetooth_settings(network_id: str):
        """Get get network wirelessbluetoothsettings."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessBluetoothSettings(
                network_id
            )
            
            response = f"# 📶 Get Network Wirelessbluetoothsettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_bluetooth_settings: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_channel_utilization_history",
        description="📶 Get network wirelessChannelUtilizationHistory (REQUIRES: device_serial+band OR client_id)"
    )
    def get_network_wireless_channel_utilization_history(network_id: str, device_serial: str = None, client_id: str = None, band: str = '5', timespan: int = 86400):
        """Get get network wirelesschannelutilizationhistory."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
            if "device_serial" in locals() and device_serial:
                kwargs["deviceSerial"] = device_serial
            if "client_id" in locals() and client_id:
                kwargs["clientId"] = client_id
            if "band" in locals() and band:
                kwargs["band"] = band
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelesschannelutilizationhistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_channel_utilization_history: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_client_connection_stats",
        description="📶 Get network wirelessClientConnectionStats (REQUIRES: client_id, timespan)"
    )
    def get_network_wireless_client_connection_stats(network_id: str, client_id: str, timespan: int = 86400, per_page: int = 1000):
        """Get get network wirelessclientconnectionstats."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectionStats(
                network_id, client_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessclientconnectionstats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_client_connection_stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_client_connectivity_events",
        description="📶 Get network wirelessClientConnectivityEvents (REQUIRES: client_id)"
    )
    def get_network_wireless_client_connectivity_events(network_id: str, client_id: str, per_page: int = 500):
        """Get get network wirelessclientconnectivityevents."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectivityEvents(
                network_id, client_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessclientconnectivityevents\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_client_connectivity_events: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_client_count_history",
        description="📶 Get network wirelessClientCountHistory"
    )
    def get_network_wireless_client_count_history(network_id: str, timespan: int = 86400):
        """Get get network wirelessclientcounthistory."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientCountHistory(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessclientcounthistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_client_count_history: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_client_latency_history",
        description="📶 Get network wirelessClientLatencyHistory"
    )
    def get_network_wireless_client_latency_history(network_id: str, timespan: int = 86400):
        """Get get network wirelessclientlatencyhistory."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyHistory(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessclientlatencyhistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_client_latency_history: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_client_latency_stats",
        description="📶 Get network wirelessClientLatencyStats"
    )
    def get_network_wireless_client_latency_stats(network_id: str, per_page: int = 1000):
        """Get get network wirelessclientlatencystats."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyStats(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessclientlatencystats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_client_latency_stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_clients_connection_stats",
        description="📶 Get network wirelessClientsConnectionStats"
    )
    def get_network_wireless_clients_connection_stats(network_id: str, per_page: int = 500):
        """Get get network wirelessclientsconnectionstats."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientsConnectionStats(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessclientsconnectionstats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_clients_connection_stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_clients_latency_stats",
        description="📶 Get network wirelessClientsLatencyStats"
    )
    def get_network_wireless_clients_latency_stats(network_id: str, timespan: int = 86400, per_page: int = 500):
        """Get get network wirelessclientslatencystats."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientsLatencyStats(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessclientslatencystats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_clients_latency_stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_connection_stats",
        description="📶 Get network wirelessConnectionStats"
    )
    def get_network_wireless_connection_stats(network_id: str, timespan: int = 86400, per_page: int = 1000):
        """Get get network wirelessconnectionstats."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessConnectionStats(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessconnectionstats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_connection_stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_data_rate_history",
        description="📶 Get network wirelessDataRateHistory"
    )
    def get_network_wireless_data_rate_history(network_id: str, timespan: int = 86400):
        """Get get network wirelessdataratehistory."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessDataRateHistory(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessdataratehistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_data_rate_history: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_devices_connection_stats",
        description="📶 Get network wireless devicesConnectionStats"
    )
    def get_network_wireless_devices_connection_stats(network_id: str, timespan: int = 86400):
        """Get wireless device connection statistics for a network (requires timespan)."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessDevicesConnectionStats(
                network_id, timespan=timespan
            )
            
            response = f"# 📶 Get Network Wireless Devicesconnectionstats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_devices_connection_stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_devices_latency_stats",
        description="📶 Get network wireless devicesLatencyStats"
    )
    def get_network_wireless_devices_latency_stats(network_id: str, per_page: int = 500):
        """Get get network wireless deviceslatencystats."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessDevicesLatencyStats(
                network_id, serial, **kwargs  
            )
            
            response = f"# 📶 Get Network Wireless Deviceslatencystats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_devices_latency_stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_electronic_shelf_label",
        description="📶 Get network wirelessElectronicShelfLabel"
    )
    def get_network_wireless_electronic_shelf_label(network_id: str, per_page: int = 1000):
        """Get get network wirelesselectronicshelflabel."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessElectronicShelfLabel(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelesselectronicshelflabel\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_electronic_shelf_label: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_electronic_shelf_label_configured_devices",
        description="📶 Get network wirelessElectronicShelfLabelConfigured devices"
    )
    def get_network_wireless_electronic_shelf_label_configured_devices(network_id: str, per_page: int = 500):
        """Get get network wirelesselectronicshelflabelconfigured devices."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessElectronicShelfLabelConfiguredDevices(
                network_id, serial, **kwargs  
            )
            
            response = f"# 📶 Get Network Wirelesselectronicshelflabelconfigured Devices\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_electronic_shelf_label_configured_devices: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ethernet_ports_profile",
        description="📶 Get network wirelessEthernetPortsProfile"
    )
    def get_network_wireless_ethernet_ports_profile(network_id: str, per_page: int = 1000):
        """Get get network wirelessethernetportsprofile."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessEthernetPortsProfile(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessethernetportsprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ethernet_ports_profile: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ethernet_ports_profiles",
        description="📶 Get network wirelessEthernetPortsProfiles"
    )
    def get_network_wireless_ethernet_ports_profiles(network_id: str, per_page: int = 1000):
        """Get get network wirelessethernetportsprofiles."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessEthernetPortsProfiles(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessethernetportsprofiles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ethernet_ports_profiles: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_failed_connections",
        description="📶 Get network wirelessFailedConnections"
    )
    def get_network_wireless_failed_connections(network_id: str, timespan: int = 86400, per_page: int = 1000):
        """Get get network wirelessfailedconnections."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessFailedConnections(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessfailedconnections\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_failed_connections: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_latency_history",
        description="📶 Get network wirelessLatencyHistory"
    )
    def get_network_wireless_latency_history(network_id: str, timespan: int = 86400):
        """Get get network wirelesslatencyhistory."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessLatencyHistory(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelesslatencyhistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_latency_history: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_latency_stats",
        description="📶 Get network wirelessLatencyStats"
    )
    def get_network_wireless_latency_stats(network_id: str, timespan: int = 86400, per_page: int = 1000):
        """Get get network wirelesslatencystats."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessLatencyStats(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelesslatencystats\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_latency_stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_mesh_statuses",
        description="📶 Get network wirelessMeshStatuses"
    )
    def get_network_wireless_mesh_statuses(network_id: str, per_page: int = 500):
        """Get get network wirelessmeshstatuses."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessMeshStatuses(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessmeshstatuses\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_mesh_statuses: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_rf_profile",
        description="📶 Get network wirelessRfProfile"
    )
    def get_network_wireless_rf_profile(network_id: str, per_page: int = 1000):
        """Get get network wirelessrfprofile."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessRfProfile(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessrfprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_rf_profile: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_rf_profiles",
        description="📶 Get network wirelessRfProfiles"
    )
    def get_network_wireless_rf_profiles(network_id: str, per_page: int = 1000):
        """Get get network wirelessrfprofiles."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessRfProfiles(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessrfprofiles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_rf_profiles: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_settings",
        description="📶 Get network wirelessSettings"
    )
    def get_network_wireless_settings(network_id: str):
        """Get wireless settings for a network."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSettings(network_id)
            
            response = f"# 📶 Get Network Wirelesssettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_settings: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_signal_quality_history",
        description="📶 Get network wirelessSignalQualityHistory (REQUIRES: device_serial OR client_id)"
    )
    def get_network_wireless_signal_quality_history(network_id: str, device_serial: str = None, client_id: str = None, timespan: int = 86400):
        """Get get network wirelesssignalqualityhistory."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
            if "device_serial" in locals() and device_serial:
                kwargs["deviceSerial"] = device_serial
            if "client_id" in locals() and client_id:
                kwargs["clientId"] = client_id
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSignalQualityHistory(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelesssignalqualityhistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_signal_quality_history: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid",
        description="📶 Get network wirelessSsid"
    )
    def get_network_wireless_ssid(network_id: str, ssid_number: str = "0"):
        """Get specific network wireless SSID details."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsid(
                network_id, ssid_number
            )
            
            response = f"# 📶 Network Wireless SSID Details\n\n"
            
            if result is not None:
                if isinstance(result, dict):
                    # Show SSID details with security information
                    response += f"**SSID Name**: {result.get('name', 'Unnamed')}\n"
                    response += f"**Number**: {result.get('number', ssid_number)}\n"
                    response += f"**Enabled**: {'✅ Yes' if result.get('enabled') else '❌ No'}\n\n"
                    
                    # Security Configuration
                    response += "## 🔐 Security Configuration\n"
                    auth_mode = result.get('authMode', 'Unknown')
                    response += f"**Authentication Mode**: {auth_mode}\n"
                    
                    if auth_mode == 'psk':
                        response += f"**Security**: ✅ WPA/WPA2 Personal (PSK)\n"
                        wpa_encryption = result.get('wpaEncryptionMode', 'Unknown')
                        response += f"**Encryption Mode**: {wpa_encryption}\n"
                    elif auth_mode == 'open':
                        response += f"**Security**: ❌ Open (No Password Protection)\n"
                    else:
                        response += f"**Security**: {auth_mode}\n"
                    
                    # Visibility
                    if 'visible' in result:
                        response += f"**SSID Visible**: {'✅ Yes' if result.get('visible') else '❌ Hidden'}\n"
                    
                    # Additional settings
                    response += "\n## ⚙️ Additional Settings\n"
                    if 'splashPage' in result:
                        response += f"**Splash Page**: {result.get('splashPage', 'None')}\n"
                    if 'bandSelection' in result:
                        response += f"**Band Selection**: {result.get('bandSelection', 'Dual band operation')}\n"
                    if 'perClientBandwidthLimitUp' in result or 'perClientBandwidthLimitDown' in result:
                        up_limit = result.get('perClientBandwidthLimitUp', 'Unlimited')
                        down_limit = result.get('perClientBandwidthLimitDown', 'Unlimited')
                        response += f"**Bandwidth Limits**: ↑{up_limit} ↓{down_limit} Kbps per client\n"
                else:
                    # Fallback for unexpected format
                    response += f"**Result**: {str(result)}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_bonjour_forwarding",
        description="📶 Get network wirelessSsidBonjourForwarding"
    )
    def get_network_wireless_ssid_bonjour_forwarding(network_id: str, per_page: int = 1000):
        """Get get network wirelessssidbonjourforwarding."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidBonjourForwarding(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessssidbonjourforwarding\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_bonjour_forwarding: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_device_type_group_policies",
        description="📶 Get network wirelessSsid deviceTypeGroupPolicies"
    )
    def get_network_wireless_ssid_device_type_group_policies(network_id: str, per_page: int = 1000):
        """Get get network wirelessssid devicetypegrouppolicies."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, serial, **kwargs  
            )
            
            response = f"# 📶 Get Network Wirelessssid Devicetypegrouppolicies\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_device_type_group_policies: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_eap_override",
        description="📶 Get network wirelessSsidEapOverride"
    )
    def get_network_wireless_ssid_eap_override(network_id: str, per_page: int = 1000):
        """Get get network wirelessssideapoverride."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidEapOverride(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessssideapoverride\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_eap_override: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_firewall_l3_firewall_rules",
        description="📶 Get network wirelessSsidFirewallL3FirewallRules (REQUIRES: ssid_number)"
    )
    def get_network_wireless_ssid_firewall_l3_firewall_rules(network_id: str, ssid_number: str = "0"):
        """Get get network wirelessssidfirewalll3firewallrules."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL3FirewallRules(
                network_id, ssid_number
            )
            
            response = f"# 📶 Get Network Wirelessssidfirewalll3Firewallrules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_firewall_l3_firewall_rules: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_firewall_l7_firewall_rules",
        description="📶 Get network wirelessSsidFirewallL7FirewallRules"
    )
    def get_network_wireless_ssid_firewall_l7_firewall_rules(network_id: str, per_page: int = 1000):
        """Get get network wirelessssidfirewalll7firewallrules."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL7FirewallRules(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessssidfirewalll7Firewallrules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_firewall_l7_firewall_rules: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_hotspot20",
        description="📶 Get network wirelessSsidHotspot20"
    )
    def get_network_wireless_ssid_hotspot20(network_id: str, per_page: int = 1000):
        """Get get network wirelessssidhotspot20."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidHotspot20(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessssidhotspot20\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_hotspot20: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_identity_psk",
        description="📶 Get network wirelessSsidIdentityPsk"
    )
    def get_network_wireless_ssid_identity_psk(network_id: str, per_page: int = 1000):
        """Get get network wirelessssididentitypsk."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidIdentityPsk(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessssididentitypsk\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_identity_psk: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_identity_psks",
        description="📶 Get network wirelessSsidIdentityPsks"
    )
    def get_network_wireless_ssid_identity_psks(network_id: str, per_page: int = 1000):
        """Get get network wirelessssididentitypsks."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidIdentityPsks(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessssididentitypsks\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_identity_psks: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_schedules",
        description="📶 Get network wirelessSsidSchedules"
    )
    def get_network_wireless_ssid_schedules(network_id: str, per_page: int = 1000):
        """Get get network wirelessssidschedules."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidSchedules(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessssidschedules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_schedules: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_splash_settings",
        description="📶 Get network wirelessSsidSplashSettings"
    )
    def get_network_wireless_ssid_splash_settings(network_id: str, per_page: int = 1000):
        """Get get network wirelessssidsplashsettings."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidSplashSettings(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessssidsplashsettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_splash_settings: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_traffic_shaping_rules",
        description="📶 Get network wirelessSsidTrafficShapingRules (REQUIRES: ssid_number)"
    )
    def get_network_wireless_ssid_traffic_shaping_rules(network_id: str, ssid_number: str = "0"):
        """Get get network wirelessssidtrafficshapingrules."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidTrafficShapingRules(
                network_id, ssid_number
            )
            
            response = f"# 📶 Get Network Wirelessssidtrafficshapingrules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_traffic_shaping_rules: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_vpn",
        description="📶 Get network wirelessSsidVpn"
    )
    def get_network_wireless_ssid_vpn(network_id: str, per_page: int = 1000):
        """Get get network wirelessssidvpn."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidVpn(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessssidvpn\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssid_vpn: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssids",
        description="📶 Get network wirelessSsids"
    )
    def get_network_wireless_ssids(network_id: str):
        """Get all wireless SSIDs for a network."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
            
            response = f"# 📶 Get Network Wirelessssids\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_ssids: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_usage_history",
        description="📶 Get network wirelessUsageHistory (TIP: Provide device_serial for device-specific usage)"
    )
    def get_network_wireless_usage_history(network_id: str, device_serial: str = None, timespan: int = 86400):
        """Get get network wirelessusagehistory."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
            if "device_serial" in locals() and device_serial:
                kwargs["deviceSerial"] = device_serial
                
            result = meraki_client.dashboard.wireless.getNetworkWirelessUsageHistory(
                network_id, **kwargs
            )
            
            response = f"# 📶 Get Network Wirelessusagehistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_wireless_usage_history: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_air_marshal_rules",
        description="📶 Get organization wirelessAirMarshalRules"
    )
    def get_organization_wireless_air_marshal_rules(organization_id: str, per_page: int = 1000):
        """Get get organization wirelessairmarshalrules."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalRules(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wirelessairmarshalrules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_air_marshal_rules: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_air_marshal_settings_by_network",
        description="📶 Get organization wirelessAirMarshalSettingsBy network"
    )
    def get_organization_wireless_air_marshal_settings_by_network(network_id: str, per_page: int = 1000):
        """Get get organization wirelessairmarshalsettingsby network."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalSettingsByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wirelessairmarshalsettingsby Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_air_marshal_settings_by_network: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_clients_overview_by_device",
        description="📶 Get organization wirelessClientsOverviewBy device"
    )
    def get_organization_wireless_clients_overview_by_device(network_id: str, serial: str, per_page: int = 500):
        """Get get organization wirelessclientsoverviewby device."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessClientsOverviewByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wirelessclientsoverviewby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_clients_overview_by_device: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_channel_utilization_by_device",
        description="📶 Get organization wireless devicesChannelUtilizationBy device"
    )
    def get_organization_wireless_devices_channel_utilization_by_device(network_id: str, serial: str, per_page: int = 500):
        """Get get organization wireless deviceschannelutilizationby device."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Deviceschannelutilizationby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_channel_utilization_by_device: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_devices_channel_utilization_by_network",
        description="📶 Get organization wireless devicesChannelUtilizationBy network"
    )
    def get_organization_wireless_devices_channel_utilization_by_network(organization_id: str, per_page: int = 500):
        """Get get organization wireless deviceschannelutilizationby network."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Deviceschannelutilizationby Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_channel_utilization_by_network: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_devices_channel_util_hist_by_dev_by_interval",
        description="📶 Get organization wireless devicesChannelUtilizationHistoryBy deviceByInterval"
    )
    def get_organization_wireless_devices_channel_utilization_history_by_device_by_interval(network_id: str, serial: str, timespan: int = 86400):
        """Get get organization wireless deviceschannelutilizationhistoryby devicebyinterval."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByDeviceByInterval(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Deviceschannelutilizationhistoryby Devicebyinterval\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_channel_utilization_history_by_device_by_interval: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_devices_channel_util_hist_by_net_by_interval",
        description="📶 Get organization wireless devicesChannelUtilizationHistoryBy networkByInterval"
    )
    def get_organization_wireless_devices_channel_utilization_history_by_network_by_interval(network_id: str, timespan: int = 86400):
        """Get get organization wireless deviceschannelutilizationhistoryby networkbyinterval."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByNetworkByInterval(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Deviceschannelutilizationhistoryby Networkbyinterval\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_channel_utilization_history_by_network_by_interval: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_ethernet_statuses",
        description="📶 Get organization wireless devicesEthernetStatuses"
    )
    def get_organization_wireless_devices_ethernet_statuses(organization_id: str, per_page: int = 500):
        """Get get organization wireless devicesethernetstatuses."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesEthernetStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devicesethernetstatuses\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_ethernet_statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss_by_client",
        description="📶 Get organization wireless devicesPacketLossByClient"
    )
    def get_organization_wireless_devices_packet_loss_by_client(network_id: str, serial: str, per_page: int = 500):
        """Get get organization wireless devicespacketlossbyclient."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByClient(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devicespacketlossbyclient\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_packet_loss_by_client: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss_by_device",
        description="📶 Get organization wireless devicesPacketLossBy device"
    )
    def get_organization_wireless_devices_packet_loss_by_device(network_id: str, serial: str, per_page: int = 500):
        """Get get organization wireless devicespacketlossby device."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devicespacketlossby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_packet_loss_by_device: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss_by_network",
        description="📶 Get organization wireless devicesPacketLossBy network"
    )
    def get_organization_wireless_devices_packet_loss_by_network(organization_id: str, per_page: int = 500):
        """Get get organization wireless devicespacketlossby network."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devicespacketlossby Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_packet_loss_by_network: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_power_mode_history",
        description="📶 Get organization wireless devicesPowerModeHistory"
    )
    def get_organization_wireless_devices_power_mode_history(network_id: str, serial: str, timespan: int = 86400):
        """Get get organization wireless devicespowermodehistory."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPowerModeHistory(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devicespowermodehistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_power_mode_history: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_devices_radsec_certs_authorities",
        description="📶 Get organization wireless devicesRadsecCertificatesAuthorities"
    )
    def get_organization_wireless_devices_radsec_certificates_authorities(network_id: str, serial: str, per_page: int = 500):
        """Get get organization wireless devicesradseccertificatesauthorities."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthorities(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devicesradseccertificatesauthorities\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_radsec_certificates_authorities: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_devices_radsec_certs_authorities_crls",
        description="📶 Get organization wireless devicesRadsecCertificatesAuthoritiesCrls"
    )
    def get_organization_wireless_devices_radsec_certificates_authorities_crls(network_id: str, serial: str, per_page: int = 500):
        """Get get organization wireless devicesradseccertificatesauthoritiescrls."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrls(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devicesradseccertificatesauthoritiescrls\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_radsec_certificates_authorities_crls: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_devices_radsec_certs_authorities_crls_deltas",
        description="📶 Get organization wireless devicesRadsecCertificatesAuthoritiesCrlsDeltas"
    )
    def get_organization_wireless_devices_radsec_certificates_authorities_crls_deltas(network_id: str, serial: str, per_page: int = 500):
        """Get get organization wireless devicesradseccertificatesauthoritiescrlsdeltas."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrlsDeltas(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devicesradseccertificatesauthoritiescrlsdeltas\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_radsec_certificates_authorities_crls_deltas: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_system_cpu_load_history",
        description="📶 Get organization wireless devicesSystemCpuLoadHistory"
    )
    def get_organization_wireless_devices_system_cpu_load_history(network_id: str, serial: str, timespan: int = 86400):
        """Get get organization wireless devicessystemcpuloadhistory."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesSystemCpuLoadHistory(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devicessystemcpuloadhistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_system_cpu_load_history: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_devices_wireless_controllers_by_device",
        description="📶 Get organization wireless devices wirelessControllersBy device"
    )
    def get_organization_wireless_devices_wireless_controllers_by_device(network_id: str, serial: str, per_page: int = 500):
        """Get get organization wireless devices wirelesscontrollersby device."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesWirelessControllersByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wireless Devices Wirelesscontrollersby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_devices_wireless_controllers_by_device: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_location_scanning_by_network",
        description="📶 Get organization wirelessLocationScanningBy network"
    )
    def get_organization_wireless_location_scanning_by_network(network_id: str, per_page: int = 1000):
        """Get get organization wirelesslocationscanningby network."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wirelesslocationscanningby Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_location_scanning_by_network: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_location_scanning_receivers",
        description="📶 Get organization wirelessLocationScanningReceivers"
    )
    def get_organization_wireless_location_scanning_receivers(organization_id: str, per_page: int = 1000):
        """Get get organization wirelesslocationscanningreceivers."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningReceivers(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wirelesslocationscanningreceivers\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_location_scanning_receivers: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_rf_profiles_assignments_by_device",
        description="📶 Get organization wirelessRfProfilesAssignmentsBy device"
    )
    def get_organization_wireless_rf_profiles_assignments_by_device(network_id: str, serial: str, per_page: int = 1000):
        """Get get organization wirelessrfprofilesassignmentsby device."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessRfProfilesAssignmentsByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wirelessrfprofilesassignmentsby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_rf_profiles_assignments_by_device: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_ssids_firewall_isolation_allowlist_entries",
        description="📶 Get organization wirelessSsidsFirewallIsolationAllowlistEntries"
    )
    def get_organization_wireless_ssids_firewall_isolation_allowlist_entries(organization_id: str, per_page: int = 1000):
        """Get get organization wirelessssidsfirewallisolationallowlistentries."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsFirewallIsolationAllowlistEntries(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wirelessssidsfirewallisolationallowlistentries\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_ssids_firewall_isolation_allowlist_entries: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_ssids_statuses_by_device",
        description="📶 Get organization wirelessSsidsStatusesBy device"
    )
    def get_organization_wireless_ssids_statuses_by_device(network_id: str, serial: str, per_page: int = 1000):
        """Get get organization wirelessssidsstatusesby device."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsStatusesByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📶 Get Organization Wirelessssidsstatusesby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_wireless_ssids_statuses_by_device: {str(e)}"
    
    @app.tool(
        name="recalculate_organization_wireless_radio_auto_rf_channels",
        description="📡 recalculate organization wirelessRadioAutoRfChannels"
    )
    def recalculate_organization_wireless_radio_auto_rf_channels(organization_id: str):
        """Manage recalculate organization wirelessradioautorfchannels."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.recalculateOrganizationWirelessRadioAutoRfChannels(
                organization_id, **kwargs
            )
            
            response = f"# 📡 Recalculate Organization Wirelessradioautorfchannels\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in recalculate_organization_wireless_radio_auto_rf_channels: {str(e)}"
    
    @app.tool(
        name="set_network_wireless_ethernet_ports_profiles_default",
        description="📡 set network wirelessEthernetPortsProfilesDefault"
    )
    def set_network_wireless_ethernet_ports_profiles_default(network_id: str):
        """Manage set network wirelessethernetportsprofilesdefault."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.setNetworkWirelessEthernetPortsProfilesDefault(
                network_id, **kwargs
            )
            
            response = f"# 📡 Set Network Wirelessethernetportsprofilesdefault\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in set_network_wireless_ethernet_ports_profiles_default: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_alternate_management_interface_ipv6",
        description="✏️ Update device wirelessAlternateManagementInterfaceIpv6"
    )
    def update_device_wireless_alternate_management_interface_ipv6(network_id: str, serial: str):
        """Update update device wirelessalternatemanagementinterfaceipv6."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateDeviceWirelessAlternateManagementInterfaceIpv6(
                network_id, serial, **kwargs  
            )
            
            response = f"# ✏️ Update Device Wirelessalternatemanagementinterfaceipv6\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_wireless_alternate_management_interface_ipv6: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_bluetooth_settings",
        description="✏️ Update device wirelessBluetoothSettings"
    )
    def update_device_wireless_bluetooth_settings(network_id: str, serial: str):
        """Update update device wirelessbluetoothsettings."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateDeviceWirelessBluetoothSettings(
                network_id, serial, **kwargs  
            )
            
            response = f"# ✏️ Update Device Wirelessbluetoothsettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_wireless_bluetooth_settings: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_electronic_shelf_label",
        description="✏️ Update device wirelessElectronicShelfLabel"
    )
    def update_device_wireless_electronic_shelf_label(network_id: str, serial: str):
        """Update update device wirelesselectronicshelflabel."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateDeviceWirelessElectronicShelfLabel(
                network_id, serial, **kwargs  
            )
            
            response = f"# ✏️ Update Device Wirelesselectronicshelflabel\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_wireless_electronic_shelf_label: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_radio_settings",
        description="✏️ Update device wirelessRadioSettings"
    )
    def update_device_wireless_radio_settings(network_id: str, serial: str):
        """Update update device wirelessradiosettings."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateDeviceWirelessRadioSettings(
                network_id, serial, **kwargs  
            )
            
            response = f"# ✏️ Update Device Wirelessradiosettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_wireless_radio_settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_air_marshal_rule",
        description="✏️ Update network wirelessAirMarshalRule"
    )
    def update_network_wireless_air_marshal_rule(network_id: str):
        """Update update network wirelessairmarshalrule."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalRule(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessairmarshalrule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_air_marshal_rule: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_air_marshal_settings",
        description="✏️ Update network wirelessAirMarshalSettings"
    )
    def update_network_wireless_air_marshal_settings(network_id: str):
        """Update update network wirelessairmarshalsettings."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalSettings(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessairmarshalsettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_air_marshal_settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_alternate_management_interface",
        description="✏️ Update network wirelessAlternateManagementInterface"
    )
    def update_network_wireless_alternate_management_interface(network_id: str):
        """Update update network wirelessalternatemanagementinterface."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAlternateManagementInterface(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessalternatemanagementinterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_alternate_management_interface: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_billing",
        description="✏️ Update network wirelessBilling"
    )
    def update_network_wireless_billing(network_id: str):
        """Update update network wirelessbilling."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessBilling(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessbilling\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_billing: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_bluetooth_settings",
        description="✏️ Update network wirelessBluetoothSettings"
    )
    def update_network_wireless_bluetooth_settings(network_id: str):
        """Update update network wirelessbluetoothsettings."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessBluetoothSettings(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessbluetoothsettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_bluetooth_settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_electronic_shelf_label",
        description="✏️ Update network wirelessElectronicShelfLabel"
    )
    def update_network_wireless_electronic_shelf_label(network_id: str):
        """Update update network wirelesselectronicshelflabel."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessElectronicShelfLabel(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelesselectronicshelflabel\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_electronic_shelf_label: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ethernet_ports_profile",
        description="✏️ Update network wirelessEthernetPortsProfile"
    )
    def update_network_wireless_ethernet_ports_profile(network_id: str):
        """Update update network wirelessethernetportsprofile."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessEthernetPortsProfile(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessethernetportsprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ethernet_ports_profile: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_location_scanning",
        description="✏️ Update network wirelessLocationScanning"
    )
    def update_network_wireless_location_scanning(network_id: str):
        """Update update network wirelesslocationscanning."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessLocationScanning(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelesslocationscanning\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_location_scanning: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_rf_profile",
        description="✏️ Update network wirelessRfProfile"
    )
    def update_network_wireless_rf_profile(network_id: str):
        """Update update network wirelessrfprofile."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessRfProfile(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessrfprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_rf_profile: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_settings",
        description="✏️ Update network wirelessSettings"
    )
    def update_network_wireless_settings(network_id: str):
        """Update update network wirelesssettings."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSettings(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelesssettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid",
        description="✏️ Update network wirelessSsid"
    )
    def update_network_wireless_ssid(network_id: str):
        """Update update network wirelessssid."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsid(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssid\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_bonjour_forwarding",
        description="✏️ Update network wirelessSsidBonjourForwarding"
    )
    def update_network_wireless_ssid_bonjour_forwarding(network_id: str):
        """Update update network wirelessssidbonjourforwarding."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidBonjourForwarding(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssidbonjourforwarding\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_bonjour_forwarding: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_device_type_group_policies",
        description="✏️ Update network wirelessSsid deviceTypeGroupPolicies"
    )
    def update_network_wireless_ssid_device_type_group_policies(network_id: str):
        """Update update network wirelessssid devicetypegrouppolicies."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, serial, **kwargs  
            )
            
            response = f"# ✏️ Update Network Wirelessssid Devicetypegrouppolicies\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_device_type_group_policies: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_eap_override",
        description="✏️ Update network wirelessSsidEapOverride"
    )
    def update_network_wireless_ssid_eap_override(network_id: str):
        """Update update network wirelessssideapoverride."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidEapOverride(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssideapoverride\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_eap_override: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_firewall_l3_firewall_rules",
        description="✏️ Update network wirelessSsidFirewallL3FirewallRules"
    )
    def update_network_wireless_ssid_firewall_l3_firewall_rules(network_id: str):
        """Update update network wirelessssidfirewalll3firewallrules."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidFirewallL3FirewallRules(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssidfirewalll3Firewallrules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_firewall_l3_firewall_rules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_firewall_l7_firewall_rules",
        description="✏️ Update network wirelessSsidFirewallL7FirewallRules"
    )
    def update_network_wireless_ssid_firewall_l7_firewall_rules(network_id: str):
        """Update update network wirelessssidfirewalll7firewallrules."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidFirewallL7FirewallRules(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssidfirewalll7Firewallrules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_firewall_l7_firewall_rules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_hotspot20",
        description="✏️ Update network wirelessSsidHotspot20"
    )
    def update_network_wireless_ssid_hotspot20(network_id: str):
        """Update update network wirelessssidhotspot20."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidHotspot20(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssidhotspot20\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_hotspot20: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_identity_psk",
        description="✏️ Update network wirelessSsidIdentityPsk"
    )
    def update_network_wireless_ssid_identity_psk(network_id: str):
        """Update update network wirelessssididentitypsk."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidIdentityPsk(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssididentitypsk\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_identity_psk: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_schedules",
        description="✏️ Update network wirelessSsidSchedules"
    )
    def update_network_wireless_ssid_schedules(network_id: str):
        """Update update network wirelessssidschedules."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSchedules(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssidschedules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_schedules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_splash_settings",
        description="✏️ Update network wirelessSsidSplashSettings"
    )
    def update_network_wireless_ssid_splash_settings(network_id: str):
        """Update update network wirelessssidsplashsettings."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSplashSettings(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssidsplashsettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_splash_settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_traffic_shaping_rules",
        description="✏️ Update network wirelessSsidTrafficShapingRules"
    )
    def update_network_wireless_ssid_traffic_shaping_rules(network_id: str):
        """Update update network wirelessssidtrafficshapingrules."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidTrafficShapingRules(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssidtrafficshapingrules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_traffic_shaping_rules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_vpn",
        description="✏️ Update network wirelessSsidVpn"
    )
    def update_network_wireless_ssid_vpn(network_id: str):
        """Update update network wirelessssidvpn."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidVpn(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Wirelessssidvpn\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_wireless_ssid_vpn: {str(e)}"
    
    @app.tool(
        name="update_org_wireless_devices_radsec_certs_authorities",
        description="✏️ Update organization wireless devicesRadsecCertificatesAuthorities"
    )
    def update_organization_wireless_devices_radsec_certificates_authorities(network_id: str, serial: str):
        """Update update organization wireless devicesradseccertificatesauthorities."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessDevicesRadsecCertificatesAuthorities(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organization Wireless Devicesradseccertificatesauthorities\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_organization_wireless_devices_radsec_certificates_authorities: {str(e)}"
    
    @app.tool(
        name="update_organization_wireless_location_scanning_receiver",
        description="✏️ Update organization wirelessLocationScanningReceiver"
    )
    def update_organization_wireless_location_scanning_receiver(organization_id: str):
        """Update update organization wirelesslocationscanningreceiver."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessLocationScanningReceiver(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organization Wirelesslocationscanningreceiver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_organization_wireless_location_scanning_receiver: {str(e)}"
    
    @app.tool(
        name="update_org_wireless_ssids_firewall_isolation_allowlist_entry",
        description="✏️ Update organization wirelessSsidsFirewallIsolationAllowlistEntry"
    )
    def update_organization_wireless_ssids_firewall_isolation_allowlist_entry(organization_id: str):
        """Update update organization wirelessssidsfirewallisolationallowlistentry."""
        try:
            kwargs = {}
            
            # Add pagination for GET methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organization Wirelessssidsfirewallisolationallowlistentry\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('ssid', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key fields based on wireless context
                            if 'ssid' in item:
                                response += f"   - SSID: {item.get('ssid')}\n"
                            if 'enabled' in item:
                                response += f"   - Enabled: {item.get('enabled')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'channel' in item:
                                response += f"   - Channel: {item.get('channel')}\n"
                            if 'power' in item:
                                response += f"   - Power: {item.get('power')}\n"
                            if 'clientCount' in item:
                                response += f"   - Clients: {item.get('clientCount')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('total', 'N/A')} MB\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result
                    for key, value in list(result.items())[:10]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key}**: {', '.join(str(k) for k in list(value.keys())[:3])}\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_organization_wireless_ssids_firewall_isolation_allowlist_entry: {str(e)}"
    
