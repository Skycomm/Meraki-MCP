# Cisco Meraki DHCP Tools Guide

## 🚨 IMPORTANT: Read This First!

**Always run `check_dhcp_network_type` before using any DHCP tools!**

This guide explains how to use the DHCP tools correctly based on your network configuration.

## Quick Start

```python
# Step 1: Check your network type
check_dhcp_network_type(network_id="YOUR_NETWORK_ID")

# This tells you:
# - If your network has VLANs enabled or not
# - Which DHCP tools to use
# - Current configuration summary
```

## Understanding Network Types

### 1. VLAN-Enabled Networks
- Have multiple VLANs configured (e.g., VLAN 10, VLAN 100)
- Each VLAN has its own subnet and DHCP settings
- Require VLAN ID for DHCP operations

### 2. Single LAN Networks
- No VLANs configured
- One flat network with a single subnet
- Simpler DHCP configuration

## Common Confusion: Subnet ≠ VLAN ID

❌ **WRONG**: "I have subnet 192.168.5.0/24, so I'll use VLAN 5"
✅ **RIGHT**: The "5" in 192.168.5.0 is just part of the IP address, NOT a VLAN ID

Examples:
- 192.168.5.0/24 → NOT VLAN 5
- 10.88.100.0/24 → NOT VLAN 100
- 172.16.20.0/24 → NOT VLAN 20

## Tool Categories

### 🔷 VLAN DHCP Tools (11 tools)
For networks WITH VLANs enabled:

| Tool | Purpose | Required Parameters |
|------|---------|-------------------|
| `get_vlan_dhcp_settings` | View DHCP config | network_id, vlan_id |
| `update_vlan_dhcp_server` | Configure DHCP server | network_id, vlan_id |
| `configure_dhcp_relay` | Set up DHCP relay | network_id, vlan_id, relay_server_ips |
| `disable_vlan_dhcp` | Turn off DHCP | network_id, vlan_id |
| `add_dhcp_fixed_assignment` | Add reservation | network_id, vlan_id, mac, ip |
| `remove_dhcp_fixed_assignment` | Remove reservation | network_id, vlan_id, mac |
| `add_dhcp_reserved_range` | Reserve IP ranges | network_id, vlan_id, start, end |
| `configure_dhcp_boot_options` | PXE boot settings | network_id, vlan_id |
| `add_custom_dhcp_option` | Add DHCP option | network_id, vlan_id, code, type, value |
| `enable_mandatory_dhcp` | Force DHCP usage | network_id, vlan_id |
| `get_appliance_dhcp_subnets` | Get subnet stats | serial |

### 🔶 Single LAN DHCP Tools (6 tools)
For networks WITHOUT VLANs:

| Tool | Purpose | Required Parameters |
|------|---------|-------------------|
| `get_single_lan_dhcp_settings` | View DHCP config | network_id |
| `list_single_lan_fixed_ips` | List all reservations | network_id |
| `add_single_lan_fixed_ip` | Add reservation | network_id, mac, ip |
| `remove_single_lan_fixed_ip` | Remove reservation | network_id, mac |
| `add_single_lan_dhcp_option` | Add DHCP option | network_id, code, type, value |
| `remove_single_lan_dhcp_option` | Remove DHCP option | network_id, code |

### 🔍 Helper Tools (2 tools)
Use these first:

| Tool | Purpose |
|------|---------|
| `check_dhcp_network_type` | Identify network type and which tools to use |
| `dhcp_tools_help` | Get this help guide |

## Real Examples

### Example 1: South Perth (Single LAN Network)
```python
# 1. Check network type
check_dhcp_network_type(network_id="N_726205439913520306")
# Result: Single LAN network, subnet 192.168.5.0/24

# 2. List current reservations
list_single_lan_fixed_ips(network_id="N_726205439913520306")

# 3. Add printer reservation
add_single_lan_fixed_ip(
    network_id="N_726205439913520306",
    mac_address="00:17:C8:BE:3A:24",
    ip_address="192.168.5.77",
    name="KMBE3A24.WENTS.local"
)

# 4. Add domain name option
add_single_lan_dhcp_option(
    network_id="N_726205439913520306",
    code=15,
    type="text",
    value="wents.local"
)
```

### Example 2: Taiwan (VLAN Network)
```python
# 1. Check network type
check_dhcp_network_type(network_id="L_669347494617953785")
# Result: VLAN network with VLAN 10 and VLAN 100

# 2. View DHCP for VLAN 10
get_vlan_dhcp_settings(
    network_id="L_669347494617953785",
    vlan_id="10"  # Note: This is the VLAN ID, not subnet
)

# 3. Add printer to VLAN 10
add_dhcp_fixed_assignment(
    network_id="L_669347494617953785",
    vlan_id="10",
    mac_address="00:17:C8:BE:3A:24",
    ip_address="10.88.10.77",  # Must be in VLAN 10's subnet
    name="Printer-VLAN10"
)
```

## Troubleshooting

### Error: "VLAN X not found"
- You're using VLAN tools on a Single LAN network
- Solution: Use Single LAN tools instead

### Error: "This network doesn't have VLANs enabled"
- You're using Single LAN tools on a VLAN network
- Solution: Use VLAN tools with the correct VLAN ID

### Error: "None of the fields were specified"
- This is an internal API issue (now fixed)
- Make sure you're using the latest version

### Can't find your test reservation?
1. Check you're using the right tool set
2. For Single LAN: `list_single_lan_fixed_ips`
3. For VLAN: `get_vlan_dhcp_settings` with correct VLAN ID

## DHCP Options Reference

Common DHCP options you might need:

| Option | Purpose | Type | Example |
|--------|---------|------|---------|
| 15 | Domain Name | text | "company.local" |
| 66 | TFTP Server | text | "tftp.company.com" |
| 67 | Boot Filename | text | "pxeboot.0" |
| 119 | Domain Search | text | "dept1.company.com,dept2.company.com" |

## Best Practices

1. **Always check network type first** - Don't assume based on subnet
2. **Use the correct tool set** - VLAN tools for VLAN networks, Single LAN tools for flat networks
3. **Verify IP addresses** - Ensure they're within the correct subnet range
4. **Document your changes** - Use descriptive names for reservations
5. **Test after changes** - Verify DHCP is working as expected

## Still Need Help?

1. Run `dhcp_tools_help()` for quick reference
2. Run `check_dhcp_network_type()` to identify your network
3. Check the error messages - they now provide helpful guidance
4. Look at the examples above for your network type