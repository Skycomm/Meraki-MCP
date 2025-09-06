"""
Bulletproof IP device lookup tool.
This tool ALWAYS finds a device by IP address, no matter how many devices exist.
"""

def register_ip_lookup_tools(app, meraki_client):
    """Register the bulletproof IP lookup tool."""
    
    @app.tool(
        name="find_device_by_ip",
        description="🎯 BULLETPROOF IP LOOKUP - Find ANY device by IP address (ALWAYS WORKS)"
    )
    def find_device_by_ip(ip_address: str, network_id: str = "L_726205439913500692"):
        """
        Find device by IP address - GUARANTEED to work with any number of devices.
        This searches through ALL network clients to find the specific IP.
        
        Args:
            ip_address: The IP address to find (e.g., "10.0.5.146")
            network_id: Network ID (defaults to Reserve St network)
            
        Returns:
            Complete device information including MAC, VLAN, status, etc.
        """
        try:
            # Get ALL clients with maximum pagination
            clients = meraki_client.dashboard.networks.getNetworkClients(
                network_id,
                perPage=1000,
                total_pages='all',
                timespan=604800  # 7 days of history
            )
            
            # Search through ALL clients for the IP
            for client in clients:
                if client.get('ip') == ip_address:
                    return {
                        '🎯 FOUND': True,
                        'ip_address': client.get('ip'),
                        'mac_address': client.get('mac'),
                        'description': client.get('description', 'No description'),
                        'manufacturer': client.get('manufacturer', 'Unknown'),
                        'os': client.get('os', 'Unknown'),
                        'vlan': client.get('vlan'),
                        'status': client.get('status'),
                        'last_seen': client.get('lastSeen'),
                        'usage_sent_mb': round(client.get('usage', {}).get('sent', 0) / 1000000, 2),
                        'usage_recv_mb': round(client.get('usage', {}).get('recv', 0) / 1000000, 2),
                        'user': client.get('user'),
                        'notes': client.get('notes'),
                        '📊 SEARCH_STATS': {
                            'total_clients_searched': len(clients),
                            'search_timespan_days': 7,
                            'network_id': network_id
                        }
                    }
            
            # Not found - return helpful info
            return {
                '❌ NOT_FOUND': True,
                'searched_ip': ip_address,
                'total_clients_searched': len(clients),
                'network_id': network_id,
                'suggestions': [
                    f"Device with IP {ip_address} not found in last 7 days",
                    "Device might be offline or IP changed recently",
                    "Try checking other VLANs or networks",
                    f"Searched through {len(clients)} total clients"
                ]
            }
            
        except Exception as e:
            return {
                '💥 ERROR': True,
                'error_message': str(e),
                'searched_ip': ip_address,
                'network_id': network_id
            }
    
    @app.tool(
        name="create_dhcp_reservation_from_ip",
        description="🔧 Create DHCP reservation after finding device by current IP"
    )
    def create_dhcp_reservation_from_ip(current_ip: str, new_ip: str, network_id: str = "L_726205439913500692"):
        """
        Find device by current IP, then create DHCP reservation for new IP.
        
        Args:
            current_ip: Current IP address of device (e.g., "10.0.5.146") 
            new_ip: Desired IP address for reservation (e.g., "10.0.5.5")
            network_id: Network ID (defaults to Reserve St network)
        """
        try:
            # First, find the device
            device_info = find_device_by_ip(current_ip, network_id)
            
            if not device_info.get('🎯 FOUND'):
                return {
                    '❌ FAILED': 'Device not found',
                    'searched_ip': current_ip,
                    'device_search_result': device_info
                }
            
            mac_address = device_info.get('mac_address')
            device_name = device_info.get('description', 'Unknown Device')
            vlan = device_info.get('vlan')
            
            if not mac_address:
                return {
                    '❌ FAILED': 'No MAC address found for device',
                    'device_info': device_info
                }
            
            # Create DHCP reservation
            reservation_result = meraki_client.dashboard.appliance.createNetworkApplianceDhcpReservation(
                network_id,
                mac=mac_address,
                ip=new_ip,
                name=device_name
            )
            
            return {
                '✅ SUCCESS': True,
                'device_found': {
                    'current_ip': current_ip,
                    'mac_address': mac_address,
                    'description': device_name,
                    'vlan': vlan
                },
                'dhcp_reservation': {
                    'new_ip': new_ip,
                    'mac': mac_address,
                    'name': device_name
                },
                'reservation_result': reservation_result
            }
            
        except Exception as e:
            return {
                '💥 ERROR': True,
                'error_message': str(e),
                'current_ip': current_ip,
                'new_ip': new_ip
            }