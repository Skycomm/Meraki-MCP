"""
DHCP helper tools to determine which DHCP tools to use.
Helps users identify their network type before using DHCP tools.
"""

import logging

logger = logging.getLogger(__name__)

def register_dhcp_helper_tools(mcp_app, meraki):
    """Register DHCP helper tools to guide users to the correct DHCP tools."""
    
    @mcp_app.tool()
    def check_dhcp_network_type(network_id: str) -> str:
        """
        🔍 Check network type to determine which DHCP tools to use.
        
        ALWAYS RUN THIS FIRST before using any DHCP tools!
        
        Args:
            network_id: Network ID to check
            
        Returns:
            Network type information and which DHCP tools to use
        """
        try:
            # Get network info
            network = meraki.get_network(network_id)
            network_name = network.get('name', 'Unknown')
            
            result = f"# DHCP Network Type Check\n\n"
            result += f"**Network**: {network_name} ({network_id})\n"
            result += f"**Product Types**: {', '.join(network.get('productTypes', []))}\n\n"
            
            # Check if network has appliance capability
            if 'appliance' not in network.get('productTypes', []):
                result += "❌ **No DHCP Support**: This network doesn't have an MX appliance.\n"
                result += "DHCP is only available on networks with MX security appliances.\n"
                return result
            
            # Check VLAN status
            try:
                vlan_settings = meraki.dashboard.appliance.getNetworkApplianceVlansSettings(network_id)
                vlans_enabled = vlan_settings.get('vlansEnabled', False)
                
                if vlans_enabled:
                    # VLAN-enabled network
                    result += "## ✅ VLAN-Enabled Network\n\n"
                    
                    # Get VLANs
                    vlans = meraki.get_network_vlans(network_id)
                    result += f"**VLANs configured**: {len(vlans)}\n\n"
                    
                    result += "### Available VLANs:\n"
                    for vlan in vlans:
                        result += f"- **VLAN {vlan['id']}**: {vlan.get('name', 'Unnamed')} "
                        result += f"(Subnet: {vlan.get('subnet', 'Not configured')})\n"
                    
                    result += "\n### 📌 Use these VLAN DHCP tools:\n"
                    result += "- `get_vlan_dhcp_settings` - View DHCP config for a VLAN\n"
                    result += "- `update_vlan_dhcp_server` - Configure DHCP server\n"
                    result += "- `add_dhcp_fixed_assignment` - Add DHCP reservation\n"
                    result += "- `remove_dhcp_fixed_assignment` - Remove reservation\n"
                    result += "- `add_custom_dhcp_option` - Add DHCP option\n"
                    result += "\n**Example**: `get_vlan_dhcp_settings(network_id=\"{}\", vlan_id=\"10\")`\n".format(network_id)
                    
                else:
                    # Single LAN network
                    result += "## ✅ Single LAN Network (No VLANs)\n\n"
                    
                    # Get Single LAN config
                    try:
                        single_lan = meraki.get_network_appliance_single_lan(network_id)
                        result += f"**Subnet**: {single_lan.get('subnet', 'Not configured')}\n"
                        result += f"**Appliance IP**: {single_lan.get('applianceIp', 'Not configured')}\n"
                        result += f"**DHCP**: {single_lan.get('dhcpHandling', 'Not configured')}\n\n"
                        
                        # Show current reservations count
                        fixed_ips = single_lan.get('fixedIpAssignments', {})
                        dhcp_options = single_lan.get('dhcpOptions', [])
                        result += f"**Current Reservations**: {len(fixed_ips)}\n"
                        result += f"**Custom DHCP Options**: {len(dhcp_options)}\n"
                        
                    except Exception as e:
                        logger.error(f"Error getting Single LAN config: {e}")
                    
                    result += "\n### 📌 Use these Single LAN DHCP tools:\n"
                    result += "- `get_single_lan_dhcp_settings` - View DHCP configuration\n"
                    result += "- `list_single_lan_fixed_ips` - List all reservations\n"
                    result += "- `add_single_lan_fixed_ip` - Add DHCP reservation\n"
                    result += "- `remove_single_lan_fixed_ip` - Remove reservation\n"
                    result += "- `add_single_lan_dhcp_option` - Add DHCP option\n"
                    result += "- `remove_single_lan_dhcp_option` - Remove DHCP option\n"
                    result += "\n**Example**: `list_single_lan_fixed_ips(network_id=\"{}\")`\n".format(network_id)
                    
                    result += "\n⚠️ **Common Mistake**: The subnet 192.168.5.0/24 does NOT mean VLAN 5!\n"
                    result += "The '5' is just part of the IP address range, not a VLAN ID.\n"
                    
            except Exception as e:
                result += f"❌ **Error checking VLAN status**: {str(e)}\n"
                result += "Unable to determine network type.\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking network type: {e}")
            return f"❌ Error checking network type: {str(e)}"
    
    @mcp_app.tool()
    def dhcp_tools_help() -> str:
        """
        📚 Get help on using DHCP tools correctly.
        
        Returns:
            Comprehensive guide on DHCP tool usage
        """
        result = """# DHCP Tools Help Guide

## 🔍 Step 1: Always Check Network Type First!

Run: `check_dhcp_network_type(network_id="YOUR_NETWORK_ID")`

This tells you:
- Whether your network has VLANs enabled
- Which set of DHCP tools to use
- Current DHCP configuration summary

## 📋 DHCP Tool Categories

### 1. VLAN DHCP Tools (for networks with VLANs enabled)
These tools require both network_id AND vlan_id:
- `get_vlan_dhcp_settings` - View VLAN DHCP config
- `update_vlan_dhcp_server` - Configure DHCP server
- `configure_dhcp_relay` - Set up DHCP relay
- `disable_vlan_dhcp` - Turn off DHCP
- `add_dhcp_fixed_assignment` - Add reservation (requires vlan_id)
- `remove_dhcp_fixed_assignment` - Remove reservation
- `add_dhcp_reserved_range` - Reserve IP ranges
- `configure_dhcp_boot_options` - PXE boot settings
- `add_custom_dhcp_option` - Add DHCP options
- `enable_mandatory_dhcp` - Force DHCP usage

### 2. Single LAN DHCP Tools (for networks WITHOUT VLANs)
These tools only need network_id:
- `get_single_lan_dhcp_settings` - View DHCP config
- `list_single_lan_fixed_ips` - List all reservations
- `add_single_lan_fixed_ip` - Add reservation
- `remove_single_lan_fixed_ip` - Remove reservation
- `add_single_lan_dhcp_option` - Add DHCP option
- `remove_single_lan_dhcp_option` - Remove DHCP option

## ⚠️ Common Mistakes to Avoid

1. **Subnet ≠ VLAN ID**: 
   - 192.168.5.0/24 does NOT mean VLAN 5
   - 10.88.100.0/24 does NOT mean VLAN 100
   
2. **Wrong Tool Set**:
   - Don't use VLAN tools on Single LAN networks
   - Don't use Single LAN tools on VLAN networks

3. **Network ID Format**:
   - Correct: "N_726205439913520306" or "L_669347494617953785"
   - Wrong: "726205439913520306" (missing prefix)

## 💡 Examples

### For Single LAN Network:
```python
# First check network type
check_dhcp_network_type(network_id="N_726205439913520306")

# List current reservations
list_single_lan_fixed_ips(network_id="N_726205439913520306")

# Add a printer reservation
add_single_lan_fixed_ip(
    network_id="N_726205439913520306",
    mac_address="00:17:C8:BE:3A:24",
    ip_address="192.168.5.77",
    name="Printer1"
)
```

### For VLAN Network:
```python
# First check network type
check_dhcp_network_type(network_id="L_669347494617953785")

# View DHCP for VLAN 10
get_vlan_dhcp_settings(
    network_id="L_669347494617953785",
    vlan_id="10"
)

# Add reservation to VLAN 10
add_dhcp_fixed_assignment(
    network_id="L_669347494617953785",
    vlan_id="10",
    mac_address="00:17:C8:BE:3A:24",
    ip_address="10.88.10.77",
    name="Printer1"
)
```

## 🆘 Still Having Issues?

1. Run `check_dhcp_network_type` first
2. Use the exact tool names shown for your network type
3. Include all required parameters
4. Check that IP addresses match the subnet range
"""
        return result