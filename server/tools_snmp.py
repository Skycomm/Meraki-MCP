"""
SNMP Tools for Cisco Meraki MCP Server
Configure SNMP for network monitoring and management
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
from meraki_client import MerakiClient
from utils.helpers import format_error_message
from contextlib import contextmanager

# This will be set by register function
mcp_app = None
meraki = None

def format_error(operation: str, error: Exception) -> str:
    """Format error message with operation context."""
    return f"❌ Failed to {operation}: {format_error_message(error)}"

@contextmanager
def safe_api_call(operation: str):
    """Context manager for safe API calls with consistent error handling."""
    try:
        yield
    except Exception as e:
        raise Exception(f"Failed to {operation}: {str(e)}")


def get_network_snmp(network_id: str) -> str:
    """
    🔍 Get SNMP settings for a network.
    
    Shows SNMP configuration including access, traps, and users.
    
    Args:
        network_id: Network ID
    
    Returns:
        SNMP configuration details
    """
    try:
        with safe_api_call("get SNMP settings"):
            snmp = meraki.dashboard.networks.getNetworkSnmp(network_id)
            
            output = ["🔍 SNMP Configuration", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            # Access settings
            access = snmp.get('access', 'none')
            if access == 'none':
                output.append("❌ SNMP Access: Disabled")
                output.append("\n💡 Use update_network_snmp() to enable")
                return "\n".join(output)
            
            output.append(f"✅ SNMP Access: {access.upper()}")
            
            # Community string (v1/v2c)
            if access in ['community', 'users']:
                if snmp.get('communityString'):
                    output.append(f"🔑 Community String: {'•' * 8} (hidden)")
            
            # Location
            if snmp.get('location'):
                output.append(f"📍 Location: {snmp['location']}")
            
            # Contact
            if snmp.get('contact'):
                output.append(f"👤 Contact: {snmp['contact']}")
            
            output.append("")
            
            # SNMP v3 users
            if access == 'users':
                users = snmp.get('users', [])
                if users:
                    output.append("👥 SNMPv3 Users:")
                    for user in users:
                        username = user.get('username', 'Unknown')
                        output.append(f"   • {username}")
                        output.append(f"     Auth: {user.get('authMode', 'N/A').upper()}")
                        output.append(f"     Priv: {user.get('privMode', 'N/A').upper()}")
                    output.append("")
            
            # Trap settings
            output.append("🚨 SNMP Traps:")
            trap_config = {}
            
            # Check various trap-related fields
            if snmp.get('trapCommunityString'):
                output.append("   Community: Configured")
                trap_config['community'] = True
            
            # Network servers
            if snmp.get('networkId'):
                output.append("   Network-level traps: Enabled")
            
            # Show trap destinations if available
            # Note: Trap destinations might be in organization settings
            
            # MIB information
            output.append("\n📋 Supported MIBs:")
            output.append("• RFC1213-MIB (MIB-II)")
            output.append("• IF-MIB")
            output.append("• ENTITY-MIB")
            output.append("• SNMPv2-MIB")
            output.append("• CISCO-PRODUCTS-MIB")
            
            # OID examples
            output.append("\n🔢 Common OIDs:")
            output.append("• System: 1.3.6.1.2.1.1")
            output.append("• Interfaces: 1.3.6.1.2.1.2")
            output.append("• IP: 1.3.6.1.2.1.4")
            output.append("• TCP: 1.3.6.1.2.1.6")
            output.append("• UDP: 1.3.6.1.2.1.7")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get SNMP settings", e)


def update_network_snmp(
    network_id: str,
    access: str,
    community_string: Optional[str] = None,
    location: Optional[str] = None,
    contact: Optional[str] = None,
    users: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    ✏️ Update SNMP settings for a network.
    
    Configure SNMP access, community strings, and users.
    
    Args:
        network_id: Network ID
        access: Access type ('none', 'community', 'users')
        community_string: Community string for v1/v2c
        location: SNMP location string
        contact: SNMP contact string
        users: SNMPv3 users list
    
    Returns:
        Updated SNMP configuration
    """
    try:
        with safe_api_call("update SNMP settings"):
            # Build update data
            update_data = {
                "access": access
            }
            
            if community_string is not None:
                update_data["communityString"] = community_string
            
            if location is not None:
                update_data["location"] = location
                
            if contact is not None:
                update_data["contact"] = contact
            
            if users is not None and access == "users":
                update_data["users"] = users
            
            # Update SNMP settings
            result = meraki.dashboard.networks.updateNetworkSnmp(
                network_id,
                **update_data
            )
            
            output = ["✏️ SNMP Settings Updated", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append(f"Access: {result.get('access', access).upper()}")
            
            if result.get('location'):
                output.append(f"Location: {result['location']}")
            
            if result.get('contact'):
                output.append(f"Contact: {result['contact']}")
            
            output.append("")
            
            if access == 'community':
                output.append("🔧 SNMPv2c Configuration:")
                output.append("• Read-only access enabled")
                output.append("• Use community string for authentication")
                output.append("• Test with: snmpwalk -v 2c -c <community> <device_ip>")
            elif access == 'users':
                output.append("🔒 SNMPv3 Configuration:")
                output.append("• User-based security")
                output.append("• Authentication and privacy")
                output.append("• More secure than v1/v2c")
                
                if users:
                    output.append(f"\nConfigured Users: {len(users)}")
            
            output.append("\n✅ Configuration Applied")
            
            output.append("\n🚀 Next Steps:")
            output.append("1. Configure SNMP monitoring tool")
            output.append("2. Add device IPs to monitoring")
            output.append("3. Set up alerts/thresholds")
            output.append("4. Test SNMP connectivity")
            output.append("5. Monitor performance metrics")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update SNMP settings", e)


def get_organization_snmp(org_id: str) -> str:
    """
    🏢 Get organization SNMP settings.
    
    Shows SNMP trap receivers and organization-wide settings.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Organization SNMP configuration
    """
    try:
        with safe_api_call("get organization SNMP"):
            snmp = meraki.dashboard.organizations.getOrganizationSnmp(org_id)
            
            output = ["🏢 Organization SNMP Settings", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # v2c settings
            v2c_enabled = snmp.get('v2cEnabled', False)
            output.append(f"SNMPv2c: {'✅ Enabled' if v2c_enabled else '❌ Disabled'}")
            
            # v3 settings
            v3_enabled = snmp.get('v3Enabled', False)
            output.append(f"SNMPv3: {'✅ Enabled' if v3_enabled else '❌ Disabled'}")
            
            # Peer IPs
            peer_ips = snmp.get('peerIps', [])
            if peer_ips:
                output.append(f"\n🌐 Allowed Peers: {len(peer_ips)}")
                for ip in peer_ips[:5]:
                    output.append(f"   • {ip}")
                if len(peer_ips) > 5:
                    output.append(f"   ... and {len(peer_ips) - 5} more")
            
            # v2c community string
            if v2c_enabled and snmp.get('v2CommunityString'):
                output.append("\n🔑 v2c Community: Configured")
            
            # v3 authentication
            if v3_enabled:
                output.append("\n🔒 v3 Settings:")
                if snmp.get('v3AuthMode'):
                    output.append(f"   Auth Mode: {snmp['v3AuthMode'].upper()}")
                if snmp.get('v3PrivMode'):
                    output.append(f"   Priv Mode: {snmp['v3PrivMode'].upper()}")
            
            # Trap receivers
            output.append("\n🚨 SNMP Trap Configuration:")
            output.append("• Configure per-network trap destinations")
            output.append("• Use syslog for event notifications")
            output.append("• Webhooks for real-time alerts")
            
            # Best practices
            output.append("\n💡 SNMP Best Practices:")
            output.append("• Use SNMPv3 for security")
            output.append("• Restrict peer IPs")
            output.append("• Strong auth/priv passwords")
            output.append("• Monitor polling frequency")
            output.append("• Secure community strings")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get organization SNMP", e)


def update_organization_snmp(
    org_id: str,
    v2c_enabled: Optional[bool] = None,
    v3_enabled: Optional[bool] = None,
    v2_community_string: Optional[str] = None,
    v3_auth_mode: Optional[str] = None,
    v3_auth_pass: Optional[str] = None,
    v3_priv_mode: Optional[str] = None,
    v3_priv_pass: Optional[str] = None,
    peer_ips: Optional[List[str]] = None
) -> str:
    """
    ✏️ Update organization SNMP settings.
    
    Configure organization-wide SNMP access and security.
    
    Args:
        org_id: Organization ID
        v2c_enabled: Enable SNMPv2c
        v3_enabled: Enable SNMPv3
        v2_community_string: v2c community string
        v3_auth_mode: v3 authentication mode (MD5, SHA)
        v3_auth_pass: v3 authentication password
        v3_priv_mode: v3 privacy mode (DES, AES128)
        v3_priv_pass: v3 privacy password
        peer_ips: Allowed SNMP peer IPs
    
    Returns:
        Updated organization SNMP configuration
    """
    try:
        with safe_api_call("update organization SNMP"):
            # Build update data
            update_data = {}
            
            if v2c_enabled is not None:
                update_data["v2cEnabled"] = v2c_enabled
            
            if v3_enabled is not None:
                update_data["v3Enabled"] = v3_enabled
            
            if v2_community_string is not None:
                update_data["v2CommunityString"] = v2_community_string
            
            if v3_auth_mode is not None:
                update_data["v3AuthMode"] = v3_auth_mode
            
            if v3_auth_pass is not None:
                update_data["v3AuthPass"] = v3_auth_pass
            
            if v3_priv_mode is not None:
                update_data["v3PrivMode"] = v3_priv_mode
                
            if v3_priv_pass is not None:
                update_data["v3PrivPass"] = v3_priv_pass
            
            if peer_ips is not None:
                update_data["peerIps"] = peer_ips
            
            # Update organization SNMP
            result = meraki.dashboard.organizations.updateOrganizationSnmp(
                org_id,
                **update_data
            )
            
            output = ["✏️ Organization SNMP Updated", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Show enabled versions
            if result.get('v2cEnabled'):
                output.append("✅ SNMPv2c: Enabled")
            
            if result.get('v3Enabled'):
                output.append("✅ SNMPv3: Enabled")
                if result.get('v3AuthMode'):
                    output.append(f"   Auth: {result['v3AuthMode'].upper()}")
                if result.get('v3PrivMode'):
                    output.append(f"   Priv: {result['v3PrivMode'].upper()}")
            
            # Peer IPs
            if result.get('peerIps'):
                output.append(f"\n🌐 Allowed Peers: {len(result['peerIps'])}")
            
            output.append("\n✅ Configuration Applied")
            
            output.append("\n⚠️ Important:")
            output.append("• Changes apply organization-wide")
            output.append("• Update monitoring tools")
            output.append("• Test from allowed peers only")
            output.append("• Secure all credentials")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update organization SNMP", e)


def snmp_configuration_examples() -> str:
    """
    📚 Show SNMP configuration examples.
    
    Provides example configurations for common SNMP scenarios.
    
    Returns:
        SNMP configuration examples
    """
    output = ["📚 SNMP Configuration Examples", "=" * 50, ""]
    
    output.append("1️⃣ Basic SNMPv2c Setup:")
    output.append("""
# Enable SNMPv2c
update_network_snmp(
    network_id,
    access="community",
    community_string="public_read_only",
    location="Main Data Center - Rack A5",
    contact="noc@company.com"
)

# Test with:
snmpwalk -v2c -c public_read_only <device_ip> system
""")
    
    output.append("\n2️⃣ Secure SNMPv3 Configuration:")
    output.append("""
# Create SNMPv3 users
users = [
    {
        "username": "monitoring_user",
        "authMode": "SHA",
        "authPass": "StrongAuthPass123!",
        "privMode": "AES128",
        "privPass": "StrongPrivPass456!"
    }
]

update_network_snmp(
    network_id,
    access="users",
    users=users,
    location="Building 1 - Floor 2",
    contact="netops@company.com"
)

# Test with:
snmpwalk -v3 -u monitoring_user -l authPriv \\
  -a SHA -A StrongAuthPass123! \\
  -x AES -X StrongPrivPass456! \\
  <device_ip> system
""")
    
    output.append("\n3️⃣ Organization-Wide Settings:")
    output.append("""
# Configure organization SNMP
update_organization_snmp(
    org_id,
    v3_enabled=True,
    v3_auth_mode="SHA",
    v3_auth_pass="OrgAuthPassword",
    v3_priv_mode="AES128",
    v3_priv_pass="OrgPrivPassword",
    peer_ips=[
        "10.10.10.100",  # Primary NMS
        "10.10.10.101"   # Secondary NMS
    ]
)
""")
    
    output.append("\n4️⃣ Monitoring Tool Integration:")
    output.append("""
# Zabbix Template
- Import Cisco Meraki template
- Add host with SNMP interface
- Set SNMP version and credentials
- Enable discovery rules

# PRTG Network Monitor
- Add SNMP device
- Use Cisco sensor types
- Set polling intervals
- Configure thresholds

# Nagios/Icinga
- Define host with SNMP checks
- Use check_snmp plugin
- Set warning/critical levels
- Configure notifications
""")
    
    output.append("\n📊 Common OID Examples:")
    output.append("""
# System information
sysDescr:    1.3.6.1.2.1.1.1.0
sysUpTime:   1.3.6.1.2.1.1.3.0
sysName:     1.3.6.1.2.1.1.5.0

# Interface statistics
ifInOctets:  1.3.6.1.2.1.2.2.1.10
ifOutOctets: 1.3.6.1.2.1.2.2.1.16
ifOperStatus: 1.3.6.1.2.1.2.2.1.8

# CPU and Memory (device-specific)
cpuUsage:    1.3.6.1.4.1.29671.1.1.5.1.0
memoryUsage: 1.3.6.1.4.1.29671.1.1.6.1.0
""")
    
    return "\n".join(output)


def analyze_snmp_security(network_id: str) -> str:
    """
    🔒 Analyze SNMP security configuration.
    
    Reviews SNMP settings and provides security recommendations.
    
    Args:
        network_id: Network ID
    
    Returns:
        SNMP security analysis and recommendations
    """
    try:
        with safe_api_call("analyze SNMP security"):
            output = ["🔒 SNMP Security Analysis", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            # Get current SNMP settings
            try:
                snmp = meraki.dashboard.networks.getNetworkSnmp(network_id)
                access = snmp.get('access', 'none')
                
                output.append("🔍 Current Configuration:")
                output.append(f"   Access Mode: {access}")
                
                # Security assessment
                if access == 'none':
                    output.append("\n✅ SNMP is disabled (most secure)")
                elif access == 'community':
                    output.append("\n⚠️ SNMPv2c Security Issues:")
                    output.append("   • Plain-text community strings")
                    output.append("   • No encryption")
                    output.append("   • Vulnerable to sniffing")
                    output.append("   • Weak authentication")
                    
                    output.append("\n🛡️ Recommendations:")
                    output.append("   1. Migrate to SNMPv3")
                    output.append("   2. Use complex community strings")
                    output.append("   3. Restrict source IPs")
                    output.append("   4. Use read-only access")
                    output.append("   5. Monitor SNMP queries")
                    
                elif access == 'users':
                    output.append("\n✅ SNMPv3 is enabled (recommended)")
                    
                    users = snmp.get('users', [])
                    if users:
                        output.append(f"   Users configured: {len(users)}")
                        
                        # Check auth/priv modes
                        for user in users:
                            auth = user.get('authMode', 'none')
                            priv = user.get('privMode', 'none')
                            
                            if auth == 'MD5':
                                output.append("\n⚠️ MD5 authentication detected")
                                output.append("   • Consider upgrading to SHA")
                            
                            if priv == 'DES':
                                output.append("\n⚠️ DES encryption detected")
                                output.append("   • Consider upgrading to AES128")
                
            except:
                output.append("Unable to retrieve SNMP settings")
            
            # General security recommendations
            output.append("\n🛡️ Security Best Practices:")
            output.append("1. Protocol Selection:")
            output.append("   • Use SNMPv3 exclusively")
            output.append("   • Disable v1/v2c if possible")
            output.append("   • Enable both auth and priv")
            
            output.append("\n2. Authentication:")
            output.append("   • Use SHA over MD5")
            output.append("   • Strong passwords (15+ chars)")
            output.append("   • Unique per device/user")
            output.append("   • Regular rotation")
            
            output.append("\n3. Encryption:")
            output.append("   • Use AES128 over DES")
            output.append("   • Enable privacy always")
            output.append("   • Protect in transit")
            
            output.append("\n4. Access Control:")
            output.append("   • Whitelist management IPs")
            output.append("   • Use ACLs on devices")
            output.append("   • Limit to read-only")
            output.append("   • Audit access logs")
            
            output.append("\n5. Monitoring:")
            output.append("   • Alert on failed auth")
            output.append("   • Track query volume")
            output.append("   • Monitor source IPs")
            output.append("   • Review regularly")
            
            # Compliance considerations
            output.append("\n📜 Compliance Notes:")
            output.append("• PCI-DSS: Requires SNMPv3")
            output.append("• NIST: Recommends auth+priv")
            output.append("• Use separate read/write users")
            output.append("• Document all access")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("analyze SNMP security", e)


def snmp_help() -> str:
    """
    ❓ Get help with SNMP tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """🔍 SNMP Tools Help
==================================================

Available tools for SNMP configuration:

1. get_network_snmp()
   - View SNMP settings
   - Check access mode
   - List SNMPv3 users
   - See location/contact

2. update_network_snmp()
   - Enable/disable SNMP
   - Set community strings
   - Configure SNMPv3 users
   - Update location/contact

3. get_organization_snmp()
   - Organization settings
   - Version enablement
   - Peer IP restrictions
   - Global configuration

4. update_organization_snmp()
   - Set org-wide settings
   - Configure peer IPs
   - v3 authentication
   - Privacy settings

5. snmp_configuration_examples()
   - Setup examples
   - Tool integration
   - Common OIDs
   - Testing commands

6. analyze_snmp_security()
   - Security assessment
   - Best practices
   - Compliance guidance
   - Recommendations

SNMP Versions:
• v1 - Original, insecure
• v2c - Community-based
• v3 - User-based security

Access Modes:
• none - SNMP disabled
• community - v1/v2c access
• users - v3 access only

SNMPv3 Security:
• noAuthNoPriv - No security
• authNoPriv - Authentication only
• authPriv - Auth + Encryption

Authentication:
• MD5 - Older, weaker
• SHA - Recommended

Encryption:
• DES - Older, weaker
• AES128 - Recommended

Common Uses:
📊 Performance monitoring
🌡️ Environmental sensors
🔌 Interface statistics
⚡ Power monitoring
🚨 Fault detection
📈 Capacity planning

Monitoring Tools:
• Zabbix
• PRTG
• Nagios/Icinga
• SolarWinds
• ManageEngine
• Cacti/MRTG

Best Practices:
• Use SNMPv3 only
• Strong credentials
• Restrict source IPs
• Read-only access
• Regular audits
• Secure storage

Testing Commands:
# SNMPv2c
snmpwalk -v2c -c community host

# SNMPv3
snmpwalk -v3 -u user -l authPriv \\
  -a SHA -A authpass \\
  -x AES -X privpass host
"""


def register_snmp_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all SNMP tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_network_snmp, "Get SNMP settings for a network"),
        (update_network_snmp, "Update network SNMP configuration"),
        (get_organization_snmp, "Get organization SNMP settings"),
        (update_organization_snmp, "Update organization SNMP settings"),
        (snmp_configuration_examples, "Show SNMP configuration examples"),
        (analyze_snmp_security, "Analyze SNMP security configuration"),
        (snmp_help, "Get help with SNMP tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)