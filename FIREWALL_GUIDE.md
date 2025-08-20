# Firewall Management Tools Guide

Configure L3/L7 firewall rules, port forwarding, and security policies on your Meraki MX devices.

## Prerequisites

**ALWAYS run this first:**
```
check_firewall_prerequisites(network_id)
```

This verifies:
- MX appliance is present
- Firewall features are available
- Current rule status

## Quick Start

### 1. View Current Rules
```python
# Layer 3 (IP-based) rules
get_network_appliance_firewall_l3_rules(network_id)

# Layer 7 (Application-based) rules  
get_network_appliance_firewall_l7_rules(network_id)

# Port forwarding rules
get_network_appliance_firewall_port_forwarding_rules(network_id)
```

### 2. Block Malicious IP
```python
update_network_appliance_firewall_l3_rules(
    network_id,
    rules='[{
        "comment": "Block malicious IP",
        "policy": "deny",
        "protocol": "any",
        "srcCidr": "192.168.100.50/32",
        "destCidr": "Any",
        "syslogEnabled": true
    }]'
)
```

### 3. Block Social Media
```python
update_network_appliance_firewall_l7_rules(
    network_id,
    rules='[{
        "type": "applicationCategory",
        "policy": "deny",
        "value": {
            "id": "meraki:layer7/category/7",
            "name": "Social web & photo sharing"
        }
    }]'
)
```

## Tools Reference

### Layer 3 Firewall (IP-based)
- `get_network_appliance_firewall_l3_rules()` - View IP firewall rules
- `update_network_appliance_firewall_l3_rules()` - Configure IP filtering

### Layer 7 Firewall (Application-based)
- `get_network_appliance_firewall_l7_rules()` - View app firewall rules
- `update_network_appliance_firewall_l7_rules()` - Block/allow applications
- `get_layer7_application_categories()` - List available app categories

### Port Forwarding
- `get_network_appliance_firewall_port_forwarding_rules()` - View NAT rules
- `update_network_appliance_firewall_port_forwarding_rules()` - Configure port forwarding

### Firewall Services
- `get_network_appliance_firewall_services()` - View service settings
- `update_network_appliance_firewall_services()` - Configure ICMP/SNMP/web access

### Cellular Firewall
- `get_network_appliance_firewall_inbound_cellular_rules()` - View cellular rules

## Common Use Cases

### 1. Allow HTTPS from Office Network
```python
update_network_appliance_firewall_l3_rules(
    network_id,
    rules='[{
        "comment": "Allow HTTPS from office",
        "policy": "allow",
        "protocol": "tcp",
        "srcCidr": "10.0.0.0/24",
        "destPort": "443",
        "destCidr": "Any"
    }]'
)
```

### 2. Forward Web Server
```python
update_network_appliance_firewall_port_forwarding_rules(
    network_id,
    rules='[{
        "name": "Web Server",
        "publicPort": "80",
        "localIp": "192.168.1.100",
        "localPort": "80",
        "protocol": "tcp",
        "allowedIps": ["any"]
    }]'
)
```

### 3. Block Gambling Sites
```python
update_network_appliance_firewall_l7_rules(
    network_id,
    rules='[{
        "type": "blockedUrlPatterns",
        "value": [
            "*.gambling.com",
            "*.casino.*",
            "*poker*"
        ]
    }]'
)
```

### 4. Allow Ping from Monitoring
```python
update_network_appliance_firewall_services(
    network_id,
    service="ICMP",
    access="restricted",
    allowed_ips='["10.0.0.5", "10.0.0.6"]'
)
```

### 5. Secure RDP Access
```python
update_network_appliance_firewall_port_forwarding_rules(
    network_id,
    rules='[{
        "name": "RDP - Admin Only",
        "publicPort": "3389",
        "localIp": "192.168.1.50",
        "localPort": "3389",
        "protocol": "tcp",
        "allowedIps": ["203.0.113.0/29"]
    }]'
)
```

## Best Practices

### Rule Order
- L3 rules are processed top to bottom
- Put most specific rules first
- Default action is at the bottom

### Security Tips
1. **Deny by default** - Block everything, then allow exceptions
2. **Use comments** - Document why each rule exists
3. **Enable syslog** - For security-critical rules
4. **Restrict sources** - Use specific IPs instead of "any"
5. **Regular audits** - Review rules quarterly

### Common L7 Categories
- Social web & photo sharing
- Peer-to-peer
- Gaming
- Video & music streaming
- File sharing
- Adult content

### Protocol Values
- `"tcp"` - TCP only
- `"udp"` - UDP only  
- `"any"` - Both TCP and UDP
- `"icmp"` - ICMP (ping)

### Service Access Levels
- `"blocked"` - No access
- `"restricted"` - Specific IPs only
- `"unrestricted"` - Open access

## Troubleshooting

### Rules not working?
1. Check rule order - most specific first
2. Verify source/destination IPs
3. Check protocol (tcp vs udp)
4. Enable syslog to see blocks

### Can't access service?
1. Check port forwarding rules
2. Verify local IP is correct
3. Check allowed source IPs
4. Test from allowed IP

### Application still accessible?
1. L7 rules may take time to apply
2. Clear browser cache
3. Check for alternate app names
4. Verify category includes app