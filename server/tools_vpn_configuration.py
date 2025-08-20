"""
VPN Configuration Tools for Cisco Meraki MCP Server
Configure and manage site-to-site and client VPN connections
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
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


def get_vpn_status(network_id: str) -> str:
    """
    🔐 Get comprehensive VPN status for a network.
    
    Shows site-to-site VPN, client VPN, and third-party VPN status.
    
    Args:
        network_id: Network ID
    
    Returns:
        Formatted VPN status overview
    """
    try:
        with safe_api_call("get VPN status"):
            result = f"""🔐 VPN Configuration Status
==================================================

"""
            
            # Site-to-site VPN status
            try:
                site_to_site = meraki.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(
                    networkId=network_id
                )
                
                mode = site_to_site.get('mode', 'none')
                result += f"🌐 Site-to-Site VPN: {mode.upper()}"
                
                if mode != 'none':
                    subnets = site_to_site.get('subnets', [])
                    result += f"\n   Local Subnets: {len(subnets)}"
                    for subnet in subnets[:3]:  # Show first 3
                        result += f"\n   • {subnet['localSubnet']} ({subnet['useVpn']})"
                    
                    # Peers
                    if 'hubs' in site_to_site:
                        result += f"\n   Hubs: {len(site_to_site['hubs'])}"
                    
            except:
                result += "🌐 Site-to-Site VPN: Not configured"
            
            # Client VPN status
            try:
                client_vpn = meraki.dashboard.appliance.getNetworkApplianceClientSecurityConfig(
                    networkId=network_id
                )
                
                result += f"\n\n💻 Client VPN: {'Enabled' if client_vpn else 'Disabled'}"
                if client_vpn:
                    result += f"\n   Authentication: {client_vpn.get('authMethod', 'N/A')}"
                    result += f"\n   Address Pool: {client_vpn.get('clientAddressPool', 'N/A')}"
                    
            except:
                result += "\n\n💻 Client VPN: Not available"
            
            # Third-party VPN peers
            try:
                third_party = meraki.dashboard.appliance.getNetworkApplianceVpnBgp(
                    networkId=network_id
                )
                
                if third_party.get('enabled'):
                    result += f"\n\n🔗 Third-Party VPN (BGP): Enabled"
                    result += f"\n   AS Number: {third_party.get('asNumber')}"
                    neighbors = third_party.get('neighbors', [])
                    result += f"\n   BGP Neighbors: {len(neighbors)}"
                    
            except:
                pass
            
            # VPN connectivity stats
            try:
                stats = meraki.dashboard.appliance.getNetworkApplianceVpnStats(
                    networkId=network_id,
                    perPage=5
                )
                
                if stats:
                    result += "\n\n📊 Recent VPN Connections:"
                    for peer in stats[:5]:
                        result += f"\n   • {peer.get('peerName', 'Unknown')}: {peer.get('connectionStatus', 'Unknown')}"
                        
            except:
                pass
            
            result += "\n\n💡 Quick Actions:"
            result += "\n   • Enable site-to-site VPN"
            result += "\n   • Configure client VPN"
            result += "\n   • Add VPN peers"
            result += "\n   • Check VPN logs"
            
            return result
            
    except Exception as e:
        return format_error("get VPN status", e)


def configure_site_to_site_vpn(
    network_id: str,
    mode: str = "hub",
    subnets: Optional[List[Dict[str, Any]]] = None,
    hubs: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    🌐 Configure site-to-site VPN settings.
    
    Set up hub, spoke, or mesh VPN topology.
    
    Args:
        network_id: Network ID
        mode: "hub", "spoke", or "none"
        subnets: List of subnet configs [{localSubnet, useVpn}]
        hubs: For spoke mode, list of hub networks
    
    Returns:
        Configuration result
    """
    try:
        with safe_api_call("configure site-to-site VPN"):
            config = {"mode": mode}
            
            # Add subnets if provided
            if subnets:
                config["subnets"] = subnets
            else:
                # Get current subnets
                current = meraki.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(
                    networkId=network_id
                )
                config["subnets"] = current.get("subnets", [])
            
            # Add hubs for spoke mode
            if mode == "spoke" and hubs:
                config["hubs"] = hubs
            
            # Update configuration
            vpn = meraki.dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
                networkId=network_id,
                **config
            )
            
            result = f"""🌐 Site-to-Site VPN Configured
==================================================

VPN Mode: {vpn['mode'].upper()}
"""
            
            if mode == "hub":
                result += "\n🏢 Hub Configuration:"
                result += "\n   • Can accept connections from spokes"
                result += "\n   • Advertises local subnets"
                result += "\n   • Central point for VPN mesh"
                
            elif mode == "spoke":
                result += "\n🏢 Spoke Configuration:"
                result += "\n   • Connects to hub networks"
                result += "\n   • Routes traffic through hubs"
                if hubs:
                    result += f"\n   • Connected Hubs: {len(hubs)}"
            
            # Show subnets
            if vpn.get('subnets'):
                result += f"\n\n📍 Local Subnets ({len(vpn['subnets'])}):"
                for subnet in vpn['subnets']:
                    vpn_status = "✅ In VPN" if subnet['useVpn'] else "❌ Local only"
                    result += f"\n   • {subnet['localSubnet']} - {vpn_status}"
            
            result += "\n\n🔐 Security Settings:"
            result += "\n   • IPsec encryption enabled"
            result += "\n   • Perfect forward secrecy"
            result += "\n   • DPD (Dead Peer Detection)"
            
            result += "\n\n💡 Next Steps:"
            result += "\n   1. Configure firewall rules"
            result += "\n   2. Test VPN connectivity"
            result += "\n   3. Monitor VPN status"
            result += "\n   4. Document network topology"
            
            return result
            
    except Exception as e:
        return format_error("configure site-to-site VPN", e)


def configure_client_vpn(
    network_id: str,
    enabled: bool = True,
    auth_method: str = "Meraki-RADIUS",
    address_pool: Optional[str] = None,
    dns_servers: Optional[List[str]] = None
) -> str:
    """
    💻 Configure client VPN settings.
    
    Enable remote access VPN for users.
    
    Args:
        network_id: Network ID
        enabled: Enable/disable client VPN
        auth_method: "Meraki-RADIUS", "Active-Directory", "LDAP"
        address_pool: IP range for VPN clients (e.g., "10.0.0.0/24")
        dns_servers: DNS servers for VPN clients
    
    Returns:
        Configuration result
    """
    try:
        with safe_api_call("configure client VPN"):
            config = {
                "enabled": enabled,
                "authMethod": auth_method
            }
            
            if address_pool:
                config["clientAddressPool"] = address_pool
                
            if dns_servers:
                config["dnsServers"] = dns_servers
            
            # Update client VPN settings
            client_vpn = meraki.dashboard.appliance.updateNetworkApplianceClientSecurityConfig(
                networkId=network_id,
                **config
            )
            
            result = f"""💻 Client VPN Configuration
==================================================

Status: {'✅ Enabled' if enabled else '❌ Disabled'}
"""
            
            if enabled:
                result += f"\nAuthentication: {client_vpn.get('authMethod', 'N/A')}"
                result += f"\nAddress Pool: {client_vpn.get('clientAddressPool', 'Auto-assigned')}"
                
                if dns_servers:
                    result += "\nDNS Servers:"
                    for dns in dns_servers:
                        result += f"\n   • {dns}"
                
                # Connection info
                result += "\n\n🔗 Client Connection Info:"
                result += "\n   Protocol: L2TP/IPsec"
                result += "\n   Port: UDP 500, 4500"
                result += f"\n   Server: [Check dashboard for public IP]"
                
                # Auth method specific info
                if auth_method == "Meraki-RADIUS":
                    result += "\n\n👤 User Management:"
                    result += "\n   • Add users in Dashboard"
                    result += "\n   • Network > Client VPN > Users"
                    result += "\n   • Set passwords and permissions"
                    
                elif auth_method == "Active-Directory":
                    result += "\n\n🏢 AD Integration:"
                    result += "\n   • Configure AD servers"
                    result += "\n   • Set up RADIUS server"
                    result += "\n   • Map AD groups to VPN"
                
                result += "\n\n📱 Client Setup:"
                result += "\n   1. Built-in VPN client (Windows/Mac)"
                result += "\n   2. Server address: [public IP]"
                result += "\n   3. Account name: [username]"
                result += "\n   4. Password: [user password]"
                result += "\n   5. Shared secret: [from dashboard]"
                
            else:
                result += "\n⚠️ Client VPN is disabled"
                result += "\n   Enable to allow remote access"
            
            return result
            
    except Exception as e:
        return format_error("configure client VPN", e)


def add_vpn_peer(
    network_id: str,
    peer_name: str,
    public_ip: str,
    private_subnets: List[str],
    secret: str,
    ike_version: str = "2"
) -> str:
    """
    🔗 Add third-party VPN peer.
    
    Configure non-Meraki VPN peer connection.
    
    Args:
        network_id: Network ID
        peer_name: Friendly name for the peer
        public_ip: Peer's public IP address
        private_subnets: List of remote subnets
        secret: Pre-shared key
        ike_version: "1" or "2"
    
    Returns:
        Peer configuration result
    """
    try:
        with safe_api_call("add VPN peer"):
            # Get current third-party peers
            current = meraki.dashboard.appliance.getOrganizationApplianceVpnThirdPartyVpnpeers(
                organizationId=meraki._get_org_id()
            )
            
            # Create new peer
            new_peer = {
                "name": peer_name,
                "publicIp": public_ip,
                "privateSubnets": private_subnets,
                "secret": secret,
                "ikeVersion": ike_version,
                "ipsecPolicies": {
                    "ikeCipherAlgo": ["aes256"],
                    "ikeAuthAlgo": ["sha256"],
                    "ikeDiffieHellmanGroup": ["group14"],
                    "ikeLifetime": 28800,
                    "childCipherAlgo": ["aes256"],
                    "childAuthAlgo": ["sha256"],
                    "childPfsGroup": ["group14"],
                    "childLifetime": 3600
                }
            }
            
            # Add to peers list
            peers = current.get("peers", [])
            peers.append(new_peer)
            
            # Update configuration
            updated = meraki.dashboard.appliance.updateOrganizationApplianceVpnThirdPartyVpnpeers(
                organizationId=meraki._get_org_id(),
                peers=peers
            )
            
            result = f"""🔗 VPN Peer Added
==================================================

Peer Configuration:
   Name: {peer_name}
   Public IP: {public_ip}
   IKE Version: {ike_version}
   
Remote Subnets:"""
            
            for subnet in private_subnets:
                result += f"\n   • {subnet}"
            
            result += f"\n\n🔐 Security Settings:"
            result += f"\n   Encryption: AES-256"
            result += f"\n   Authentication: SHA-256"
            result += f"\n   DH Group: 14 (2048-bit)"
            result += f"\n   PFS: Enabled"
            
            result += f"\n\n📋 Peer Configuration Required:"
            result += f"\n   1. Local ID: [Meraki public IP]"
            result += f"\n   2. Remote ID: {public_ip}"
            result += f"\n   3. Pre-shared Key: *** (saved)"
            result += f"\n   4. Phase 1: IKEv{ike_version}, AES-256, SHA-256, DH14"
            result += f"\n   5. Phase 2: ESP, AES-256, SHA-256, PFS14"
            
            result += "\n\n💡 Next Steps:"
            result += "\n   1. Configure peer device"
            result += "\n   2. Add firewall rules"
            result += "\n   3. Test connectivity"
            result += "\n   4. Monitor VPN logs"
            
            return result
            
    except Exception as e:
        return format_error("add VPN peer", e)


def get_vpn_stats(
    network_id: str,
    timespan: Optional[int] = 3600
) -> str:
    """
    📊 Get VPN connection statistics.
    
    Shows latency, packet loss, and connection status.
    
    Args:
        network_id: Network ID
        timespan: Time period in seconds (default: 3600 = 1 hour)
    
    Returns:
        VPN statistics and metrics
    """
    try:
        with safe_api_call("get VPN stats"):
            # Get VPN stats
            stats = meraki.dashboard.appliance.getNetworkApplianceVpnStats(
                networkId=network_id,
                timespan=timespan,
                perPage=20
            )
            
            result = f"""📊 VPN Statistics
==================================================

Time Period: Last {timespan // 3600} hour(s)
"""
            
            if stats:
                result += f"\nActive Peers: {len(stats)}\n"
                
                for peer in stats:
                    peer_name = peer.get('peerName', 'Unknown')
                    status = peer.get('connectionStatus', 'Unknown')
                    
                    # Status indicator
                    if status == 'connected':
                        indicator = '🟢'
                    elif status == 'connecting':
                        indicator = '🟡'
                    else:
                        indicator = '🔴'
                    
                    result += f"\n{indicator} {peer_name}"
                    result += f"\n   Status: {status}"
                    
                    # Connection metrics
                    if peer.get('latency'):
                        result += f"\n   Latency: {peer['latency']} ms"
                    
                    if peer.get('loss'):
                        result += f"\n   Packet Loss: {peer['loss']}%"
                    
                    if peer.get('jitter'):
                        result += f"\n   Jitter: {peer['jitter']} ms"
                    
                    # Traffic stats
                    if peer.get('sent'):
                        sent_mb = peer['sent'] / 1024 / 1024
                        recv_mb = peer.get('received', 0) / 1024 / 1024
                        result += f"\n   Traffic: ↑{sent_mb:.1f} MB / ↓{recv_mb:.1f} MB"
                    
                    result += "\n"
                
                # Summary
                connected = sum(1 for p in stats if p.get('connectionStatus') == 'connected')
                result += f"\n📈 Summary:"
                result += f"\n   Connected: {connected}/{len(stats)}"
                
                # Calculate averages for connected peers
                connected_peers = [p for p in stats if p.get('connectionStatus') == 'connected']
                if connected_peers:
                    avg_latency = sum(p.get('latency', 0) for p in connected_peers) / len(connected_peers)
                    avg_loss = sum(p.get('loss', 0) for p in connected_peers) / len(connected_peers)
                    
                    result += f"\n   Avg Latency: {avg_latency:.1f} ms"
                    result += f"\n   Avg Loss: {avg_loss:.1f}%"
                    
            else:
                result += "\n⚠️ No VPN statistics available"
                result += "\n   • Check if VPN is configured"
                result += "\n   • Verify peers are connected"
            
            result += "\n\n💡 Performance Tips:"
            result += "\n   • Latency < 150ms is good"
            result += "\n   • Packet loss should be < 1%"
            result += "\n   • High jitter affects voice/video"
            
            return result
            
    except Exception as e:
        return format_error("get VPN stats", e)


def troubleshoot_vpn_connection(
    network_id: str,
    peer_identifier: Optional[str] = None
) -> str:
    """
    🔧 Troubleshoot VPN connectivity issues.
    
    Diagnose common VPN problems and provide solutions.
    
    Args:
        network_id: Network ID
        peer_identifier: Specific peer name or IP to troubleshoot
    
    Returns:
        Troubleshooting analysis and recommendations
    """
    try:
        with safe_api_call("troubleshoot VPN"):
            result = f"""🔧 VPN Troubleshooting Analysis
==================================================

"""
            
            # Check VPN configuration
            try:
                site_to_site = meraki.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(
                    networkId=network_id
                )
                vpn_mode = site_to_site.get('mode', 'none')
                
                if vpn_mode == 'none':
                    result += "❌ Site-to-Site VPN is disabled\n"
                    result += "   • Enable VPN in hub or spoke mode\n"
                    return result
                    
                result += f"✅ VPN Mode: {vpn_mode}\n"
                
            except:
                result += "❌ Unable to check VPN configuration\n"
            
            # Check VPN stats
            try:
                stats = meraki.dashboard.appliance.getNetworkApplianceVpnStats(
                    networkId=network_id,
                    perPage=50
                )
                
                if peer_identifier:
                    # Find specific peer
                    peer_stats = None
                    for peer in stats:
                        if peer_identifier in [peer.get('peerName'), peer.get('peerIp')]:
                            peer_stats = peer
                            break
                    
                    if peer_stats:
                        result += f"\n🔍 Peer: {peer_stats['peerName']}"
                        status = peer_stats.get('connectionStatus', 'unknown')
                        
                        if status != 'connected':
                            result += f"\n❌ Status: {status}"
                            result += "\n\n🔧 Troubleshooting Steps:"
                            result += "\n1. Check Phase 1 (IKE):"
                            result += "\n   • Verify pre-shared key"
                            result += "\n   • Check peer public IP"
                            result += "\n   • Confirm IKE version match"
                            
                            result += "\n\n2. Check Phase 2 (IPsec):"
                            result += "\n   • Verify subnet configuration"
                            result += "\n   • Check encryption settings"
                            result += "\n   • Confirm PFS settings"
                            
                            result += "\n\n3. Network Issues:"
                            result += "\n   • Check firewall rules"
                            result += "\n   • Verify NAT traversal"
                            result += "\n   • Test internet connectivity"
                        else:
                            result += f"\n✅ Status: Connected"
                            
                            # Performance issues
                            if peer_stats.get('loss', 0) > 1:
                                result += f"\n⚠️ High packet loss: {peer_stats['loss']}%"
                                result += "\n   • Check internet connection quality"
                                result += "\n   • Verify MTU settings"
                                
                            if peer_stats.get('latency', 0) > 200:
                                result += f"\n⚠️ High latency: {peer_stats['latency']}ms"
                                result += "\n   • Consider closer VPN endpoint"
                                result += "\n   • Check for bandwidth saturation"
                else:
                    # General troubleshooting
                    disconnected = [p for p in stats if p.get('connectionStatus') != 'connected']
                    
                    if disconnected:
                        result += f"\n❌ Disconnected Peers: {len(disconnected)}"
                        for peer in disconnected[:5]:
                            result += f"\n   • {peer['peerName']}: {peer['connectionStatus']}"
                            
                    result += "\n\n🔍 Common VPN Issues:"
                    result += "\n\n1. Pre-shared Key Mismatch"
                    result += "\n   • Double-check PSK on both ends"
                    result += "\n   • No spaces or special characters"
                    
                    result += "\n\n2. NAT/Firewall Issues"
                    result += "\n   • UDP 500 and 4500 must be open"
                    result += "\n   • ESP protocol (50) allowed"
                    
                    result += "\n\n3. Subnet Conflicts"
                    result += "\n   • Local and remote subnets must not overlap"
                    result += "\n   • Check all VPN participants"
                    
                    result += "\n\n4. MTU/Fragmentation"
                    result += "\n   • Try MTU 1400 or lower"
                    result += "\n   • Enable fragmentation"
                
            except Exception as e:
                result += f"\n❌ Unable to get VPN stats: {str(e)}"
            
            result += "\n\n📋 Diagnostic Commands:"
            result += "\n   • Check VPN logs in Dashboard"
            result += "\n   • Event log > Filter by VPN"
            result += "\n   • Packet capture on WAN"
            result += "\n   • Test with known working peer"
            
            return result
            
    except Exception as e:
        return format_error("troubleshoot VPN", e)


def vpn_configuration_help() -> str:
    """
    ❓ Get help with VPN configuration tools.
    
    Shows available tools and common VPN setups.
    
    Returns:
        Formatted help guide
    """
    return """🔐 VPN Configuration Tools Help
==================================================

Available tools for VPN management:

1. get_vpn_status()
   - View all VPN configurations
   - Check connection status
   - See active peers

2. configure_site_to_site_vpn()
   - Set up hub or spoke mode
   - Configure VPN subnets
   - Enable auto-VPN

3. configure_client_vpn()
   - Enable remote user access
   - Set authentication method
   - Configure address pool

4. add_vpn_peer()
   - Add non-Meraki VPN peers
   - Configure IPsec settings
   - Set up third-party connections

5. get_vpn_stats()
   - Monitor VPN performance
   - Check latency and loss
   - View traffic statistics

6. troubleshoot_vpn_connection()
   - Diagnose connection issues
   - Get specific solutions
   - Check common problems

Common VPN Scenarios:

🏢 "Connect branch offices"
1. configure_site_to_site_vpn() on each site
2. Set hub at HQ, spokes at branches
3. get_vpn_stats() to verify

🏠 "Enable remote workers"
1. configure_client_vpn() with auth method
2. Create user accounts
3. Share connection instructions

🔗 "Connect to AWS/Azure"
1. add_vpn_peer() with cloud gateway IP
2. Configure matching IPsec settings
3. troubleshoot_vpn_connection() if needed

💡 VPN Best Practices:
- Use strong pre-shared keys (20+ chars)
- Enable split tunneling for performance
- Monitor VPN logs regularly
- Document all peer configurations
- Test failover scenarios

🔐 Security Recommendations:
- Use IKEv2 when possible
- Enable perfect forward secrecy
- Rotate pre-shared keys quarterly
- Limit VPN subnet access
- Enable 2FA for client VPN
"""


def register_vpn_configuration_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all VPN configuration tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_vpn_status, "View comprehensive VPN status"),
        (configure_site_to_site_vpn, "Configure site-to-site VPN"),
        (configure_client_vpn, "Set up client VPN access"),
        (add_vpn_peer, "Add third-party VPN peer"),
        (get_vpn_stats, "Monitor VPN performance metrics"),
        (troubleshoot_vpn_connection, "Diagnose VPN issues"),
        (vpn_configuration_help, "Get help with VPN configuration"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)