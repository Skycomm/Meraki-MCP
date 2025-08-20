# Traffic Shaping Tools Guide

Configure QoS, bandwidth limits, and traffic prioritization on your Meraki MX devices.

## Prerequisites

**ALWAYS run this first:**
```
check_traffic_shaping_prerequisites(network_id)
```

This verifies:
- MX appliance is present
- Traffic shaping is supported
- License requirements

## Quick Start

### 1. View Current Rules
```
get_network_traffic_shaping_rules(network_id)
```

### 2. Limit Streaming Bandwidth
```python
# Limit Netflix to 5 Mbps down, 1 Mbps up per client
update_network_traffic_shaping_rules(
    network_id,
    rules='[{
        "description": "Limit Netflix streaming",
        "definitions": [{
            "type": "application",
            "value": "Netflix"
        }],
        "perClientBandwidthLimits": {
            "settings": "custom",
            "bandwidthLimits": {
                "limitDown": 5000,
                "limitUp": 1000
            }
        }
    }]'
)
```

### 3. Prioritize VoIP Traffic
```python
# Give VoIP high priority with DSCP marking
update_network_traffic_shaping_rules(
    network_id,
    rules='[{
        "description": "Prioritize VoIP",
        "definitions": [{
            "type": "application",
            "value": "VoIP"
        }],
        "priority": "high",
        "dscpTagValue": 46
    }]'
)
```

## Tools Reference

### Core Tools
- `get_network_traffic_shaping_rules()` - View current QoS configuration
- `update_network_traffic_shaping_rules()` - Configure bandwidth and priority
- `get_traffic_shaping_application_categories()` - List available applications

### Uplink Management
- `get_network_traffic_shaping_uplink_selection()` - View WAN failover settings
- `update_network_traffic_shaping_uplink_selection()` - Configure load balancing

### Advanced Features
- `get_network_traffic_shaping_dscp_tagging()` - View DSCP options
- `get_network_traffic_shaping_custom_performance_classes()` - View QoS profiles
- `create_traffic_shaping_custom_performance_class()` - Create custom QoS class
- `update_traffic_shaping_vpn_exclusions()` - Configure split tunneling

## Common Use Cases

### 1. Limit Guest Network Bandwidth
```python
update_network_traffic_shaping_rules(
    network_id,
    rules='[{
        "description": "Guest network limit",
        "definitions": [{
            "type": "ipRange",
            "value": "192.168.10.0/24"
        }],
        "perClientBandwidthLimits": {
            "settings": "custom",
            "bandwidthLimits": {
                "limitDown": 10000,
                "limitUp": 2000
            }
        }
    }]'
)
```

### 2. Prioritize Business Applications
```python
update_network_traffic_shaping_rules(
    network_id,
    rules='[{
        "description": "Business apps priority",
        "definitions": [{
            "type": "applicationCategory",
            "value": "Business"
        }],
        "priority": "high"
    }]'
)
```

### 3. Route Video Over Primary WAN
```python
update_network_traffic_shaping_uplink_selection(
    network_id,
    wan_traffic_preferences='[{
        "trafficFilters": [{
            "type": "applicationCategory",
            "value": "Video & music"
        }],
        "preferredUplink": "wan1"
    }]'
)
```

## DSCP Values Reference
- 0 - Best Effort (default)
- 8 - Class Selector 1
- 10 - Assured Forwarding 11
- 18 - Assured Forwarding 21
- 26 - Assured Forwarding 31
- 34 - Assured Forwarding 41
- 46 - Expedited Forwarding (VoIP)
- 48 - Network Control

## License Requirements
- **Enterprise** or **Advanced Security** license required
- **SD-WAN Plus** license for advanced features (custom performance classes, VPN exclusions)