"""
Syslog Tools for Cisco Meraki MCP Server
Configure syslog servers for event logging and compliance
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


def get_network_syslog_servers(network_id: str) -> str:
    """
    📝 Get syslog servers for a network.
    
    Shows configured syslog servers and their settings.
    
    Args:
        network_id: Network ID
    
    Returns:
        Syslog server configurations
    """
    try:
        with safe_api_call("get syslog servers"):
            syslog = meraki.dashboard.networks.getNetworkSyslogServers(network_id)
            
            output = ["📝 Syslog Servers", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            servers = syslog.get('servers', [])
            if not servers:
                output.append("No syslog servers configured")
                output.append("\n💡 Use update_network_syslog_servers() to add")
                return "\n".join(output)
            
            output.append(f"Total Servers: {len(servers)}")
            output.append("")
            
            # Show each server
            for i, server in enumerate(servers, 1):
                host = server.get('host', 'Unknown')
                port = server.get('port', 514)
                
                output.append(f"{i}. 🖥️ {host}:{port}")
                
                # Roles
                roles = server.get('roles', [])
                if roles:
                    output.append("   📋 Event Types:")
                    for role in roles:
                        output.append(f"      • {role}")
                else:
                    output.append("   📋 Event Types: All")
                
                output.append("")
            
            # Available event types
            output.append("📊 Available Event Types:")
            output.append("• Wireless event log")
            output.append("• Appliance event log")
            output.append("• Switch event log")
            output.append("• Air Marshal events")
            output.append("• Flows")
            output.append("• URLs")
            output.append("• IDS alerts")
            output.append("• Security events")
            
            output.append("\n💡 Syslog Benefits:")
            output.append("• Centralized logging")
            output.append("• Compliance requirements")
            output.append("• Security monitoring")
            output.append("• Long-term retention")
            output.append("• Advanced analysis")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get syslog servers", e)


def update_network_syslog_servers(
    network_id: str,
    servers: List[Dict[str, Any]]
) -> str:
    """
    ✏️ Update syslog servers for a network.
    
    Configure syslog servers for event logging.
    
    Args:
        network_id: Network ID
        servers: List of syslog server configurations
    
    Returns:
        Updated syslog configuration
    """
    try:
        with safe_api_call("update syslog servers"):
            # Update syslog servers
            result = meraki.dashboard.networks.updateNetworkSyslogServers(
                network_id,
                servers=servers
            )
            
            output = ["✏️ Syslog Servers Updated", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            updated_servers = result.get('servers', [])
            output.append(f"Configured Servers: {len(updated_servers)}")
            output.append("")
            
            # Show updated servers
            for i, server in enumerate(updated_servers, 1):
                host = server.get('host', 'Unknown')
                port = server.get('port', 514)
                
                output.append(f"{i}. {host}:{port}")
                
                roles = server.get('roles', [])
                if roles:
                    output.append(f"   Events: {', '.join(roles)}")
                else:
                    output.append("   Events: All")
            
            output.append("\n✅ Configuration Applied")
            
            output.append("\n🔧 Next Steps:")
            output.append("1. Verify syslog server connectivity")
            output.append("2. Check firewall rules (UDP 514)")
            output.append("3. Configure syslog parser")
            output.append("4. Set up alerts/dashboards")
            output.append("5. Test event delivery")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update syslog servers", e)


def get_organization_syslog_servers(org_id: str) -> str:
    """
    🏢 Get organization-wide syslog servers.
    
    Shows syslog servers configured at the organization level.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Organization syslog configurations
    """
    try:
        with safe_api_call("get organization syslog servers"):
            # Note: This might be available in some API versions
            # Fallback to showing network-level guidance
            output = ["🏢 Organization Syslog Configuration", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            output.append("📝 Syslog Configuration Options:")
            output.append("• Configure per network")
            output.append("• Use configuration templates")
            output.append("• Apply via action batches")
            output.append("• Standardize across organization")
            
            output.append("\n🎯 Best Practices:")
            output.append("1. Centralized Logging:")
            output.append("   • Single syslog collector")
            output.append("   • Regional collectors for scale")
            output.append("   • High availability setup")
            
            output.append("\n2. Event Selection:")
            output.append("   • Security events for SOC")
            output.append("   • URLs for web filtering")
            output.append("   • Flows for traffic analysis")
            output.append("   • Wireless for client issues")
            
            output.append("\n3. Compliance:")
            output.append("   • PCI-DSS logging requirements")
            output.append("   • HIPAA audit trails")
            output.append("   • SOX compliance")
            output.append("   • Data retention policies")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get organization syslog servers", e)


def syslog_configuration_examples() -> str:
    """
    📚 Show syslog configuration examples.
    
    Provides example configurations for common syslog scenarios.
    
    Returns:
        Syslog configuration examples
    """
    output = ["📚 Syslog Configuration Examples", "=" * 50, ""]
    
    output.append("1️⃣ Basic Syslog Server:")
    output.append("""
servers = [{
    "host": "syslog.company.com",
    "port": 514,
    "roles": []  # All events
}]

update_network_syslog_servers(network_id, servers)
""")
    
    output.append("\n2️⃣ Security-Focused Logging:")
    output.append("""
servers = [{
    "host": "siem.company.com",
    "port": 514,
    "roles": [
        "Security events",
        "IDS alerts",
        "Air Marshal events"
    ]
}]
""")
    
    output.append("\n3️⃣ Multiple Servers by Function:")
    output.append("""
servers = [
    {
        "host": "security-syslog.company.com",
        "port": 514,
        "roles": ["Security events", "IDS alerts"]
    },
    {
        "host": "network-syslog.company.com",
        "port": 514,
        "roles": ["Appliance event log", "Switch event log"]
    },
    {
        "host": "compliance-syslog.company.com",
        "port": 514,
        "roles": ["URLs", "Flows"]
    }
]
""")
    
    output.append("\n4️⃣ High-Availability Setup:")
    output.append("""
servers = [
    {
        "host": "syslog-primary.company.com",
        "port": 514,
        "roles": []  # All events
    },
    {
        "host": "syslog-secondary.company.com",
        "port": 514,
        "roles": []  # All events (backup)
    }
]
""")
    
    output.append("\n📝 Syslog Message Format:")
    output.append("```")
    output.append("<134>1 2024-01-15T10:30:45.123Z MX84-SERIAL")
    output.append("events - - urls src=192.168.1.100")
    output.append("dst=93.184.216.34 url=example.com")
    output.append("```")
    
    output.append("\n🔧 Server Setup:")
    output.append("• rsyslog: Most common Linux syslog")
    output.append("• syslog-ng: Advanced filtering")
    output.append("• Splunk: Enterprise SIEM")
    output.append("• ELK Stack: Open source analytics")
    output.append("• Graylog: Web-based analysis")
    
    return "\n".join(output)


def analyze_syslog_requirements(network_id: str) -> str:
    """
    📊 Analyze syslog requirements and recommendations.
    
    Provides analysis of logging needs based on network configuration.
    
    Args:
        network_id: Network ID
    
    Returns:
        Syslog requirements analysis
    """
    try:
        with safe_api_call("analyze syslog requirements"):
            output = ["📊 Syslog Requirements Analysis", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            # Get network details
            try:
                network = meraki.dashboard.networks.getNetwork(network_id)
                org_id = network.get('organizationId')
                product_types = network.get('productTypes', [])
                
                output.append("🔍 Network Analysis:")
                output.append(f"   Name: {network.get('name', 'Unknown')}")
                output.append(f"   Products: {', '.join(product_types)}")
                output.append("")
                
                # Product-specific recommendations
                output.append("📋 Recommended Event Types:")
                
                if 'appliance' in product_types:
                    output.append("\n🔥 Security Appliance:")
                    output.append("   • Security events - Track threats")
                    output.append("   • IDS alerts - Intrusion detection")
                    output.append("   • URLs - Web activity monitoring")
                    output.append("   • Flows - Traffic analysis")
                
                if 'wireless' in product_types:
                    output.append("\n📡 Wireless:")
                    output.append("   • Wireless event log - Client issues")
                    output.append("   • Air Marshal - Rogue detection")
                    output.append("   • Security events - Auth failures")
                
                if 'switch' in product_types:
                    output.append("\n🔌 Switches:")
                    output.append("   • Switch event log - Port status")
                    output.append("   • Security events - Port security")
                
            except:
                output.append("Unable to analyze network configuration")
            
            # Volume estimates
            output.append("\n📈 Expected Log Volume:")
            output.append("• Small network (<50 devices): ~1-5 GB/day")
            output.append("• Medium network (50-500): ~5-50 GB/day")
            output.append("• Large network (500+): ~50-500 GB/day")
            
            # Storage recommendations
            output.append("\n💾 Storage Planning:")
            output.append("• 30-day retention: Volume × 30")
            output.append("• 90-day retention: Volume × 90")
            output.append("• Compliance may require 1+ years")
            output.append("• Consider compression (50-80% reduction)")
            
            # Infrastructure recommendations
            output.append("\n🏗️ Infrastructure Sizing:")
            output.append("• CPU: 2-4 cores per 1000 EPS")
            output.append("• RAM: 8-16 GB minimum")
            output.append("• Storage: Fast SSD for hot data")
            output.append("• Network: 1 Gbps+ connection")
            
            # Compliance considerations
            output.append("\n📜 Compliance Requirements:")
            output.append("• PCI-DSS: 1 year retention")
            output.append("• HIPAA: 6 year retention")
            output.append("• SOX: 7 year retention")
            output.append("• GDPR: Privacy considerations")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("analyze syslog requirements", e)


def syslog_parser_examples() -> str:
    """
    🔍 Show syslog parser configuration examples.
    
    Provides parser configurations for common syslog systems.
    
    Returns:
        Syslog parser examples
    """
    output = ["🔍 Syslog Parser Examples", "=" * 50, ""]
    
    output.append("1️⃣ rsyslog Configuration:")
    output.append("""
# /etc/rsyslog.d/10-meraki.conf
$ModLoad imudp
$UDPServerRun 514

# Template for Meraki logs
$template MerakiFormat,"/var/log/meraki/%HOSTNAME%/%$YEAR%-%$MONTH%-%$DAY%.log"

# Rules for Meraki devices
:hostname, startswith, "MX" ?MerakiFormat
:hostname, startswith, "MR" ?MerakiFormat
:hostname, startswith, "MS" ?MerakiFormat
& stop
""")
    
    output.append("\n2️⃣ Splunk Input Configuration:")
    output.append("""
# inputs.conf
[udp://514]
connection_host = dns
sourcetype = meraki:syslog
index = meraki

# props.conf
[meraki:syslog]
SHOULD_LINEMERGE = false
TIME_PREFIX = ^
TIME_FORMAT = %Y-%m-%dT%H:%M:%S.%3N%Z
EXTRACT-meraki = (?<device>[^\\s]+)\\s+(?<type>[^\\s]+)\\s+(?<details>.*)
""")
    
    output.append("\n3️⃣ ELK Stack (Logstash):")
    output.append("""
input {
  udp {
    port => 514
    type => "meraki"
  }
}

filter {
  if [type] == "meraki" {
    grok {
      match => {
        "message" => "<%{NUMBER}>%{NUMBER}\\s+%{TIMESTAMP_ISO8601:timestamp}\\s+%{HOSTNAME:device}\\s+%{WORD:event_type}\\s+%{GREEDYDATA:details}"
      }
    }
    
    kv {
      source => "details"
      field_split => " "
      value_split => "="
    }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "meraki-%{+YYYY.MM.dd}"
  }
}
""")
    
    output.append("\n4️⃣ syslog-ng Configuration:")
    output.append("""
source s_meraki {
    udp(port(514));
};

parser p_meraki {
    csv-parser(
        columns("priority", "version", "timestamp", "hostname", "app", "procid", "msgid", "msg")
        delimiters(" ")
        flags(escape-double-char)
    );
};

destination d_meraki {
    file("/var/log/meraki/${HOST}/${YEAR}${MONTH}${DAY}.log"
        create-dirs(yes)
        template("${timestamp} ${hostname} ${app} ${msg}\\n")
    );
};

log {
    source(s_meraki);
    parser(p_meraki);
    destination(d_meraki);
};
""")
    
    output.append("\n📊 Common Parse Fields:")
    output.append("• timestamp - Event time")
    output.append("• device - Source device")
    output.append("• event_type - Category")
    output.append("• src_ip - Source IP")
    output.append("• dst_ip - Destination IP")
    output.append("• action - Allow/deny")
    output.append("• url - For URL logging")
    output.append("• user - Client identity")
    
    return "\n".join(output)


def syslog_help() -> str:
    """
    ❓ Get help with syslog tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """📝 Syslog Tools Help
==================================================

Available tools for syslog configuration:

1. get_network_syslog_servers()
   - View current servers
   - Check event types
   - Server settings
   - Port configuration

2. update_network_syslog_servers()
   - Add syslog servers
   - Configure event types
   - Set multiple servers
   - Update ports

3. get_organization_syslog_servers()
   - Organization overview
   - Best practices
   - Compliance guidance
   - Setup recommendations

4. syslog_configuration_examples()
   - Server configs
   - Event filtering
   - HA setups
   - Multiple servers

5. analyze_syslog_requirements()
   - Volume estimates
   - Storage planning
   - Infrastructure sizing
   - Compliance needs

6. syslog_parser_examples()
   - rsyslog config
   - Splunk setup
   - ELK/Logstash
   - syslog-ng

Event Types:
📋 Wireless event log
🔥 Appliance event log
🔌 Switch event log
🛡️ Air Marshal events
🌊 Flows
🔗 URLs
🚨 IDS alerts
🔒 Security events

Common Ports:
• 514 - Standard syslog (UDP)
• 6514 - Syslog over TLS
• 601 - Reliable syslog

Message Format:
• RFC 3164 - Traditional
• RFC 5424 - Structured
• Key-value pairs
• JSON (some events)

Best Practices:
• Use dedicated syslog server
• Enable only needed events
• Plan storage capacity
• Implement log rotation
• Secure transport (TLS)
• Regular backup

Compliance:
• Define retention policy
• Secure log storage
• Access controls
• Audit trail
• Encryption at rest
• Regular reviews

Troubleshooting:
• Check firewall rules
• Verify network connectivity
• Test with logger command
• Check server logs
• Monitor disk space
• Validate parsing

Use Cases:
• Security monitoring
• Compliance logging
• Troubleshooting
• Traffic analysis
• Audit trails
• Forensics
"""


def register_syslog_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all syslog tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_network_syslog_servers, "Get syslog servers for a network"),
        (update_network_syslog_servers, "Update syslog server configuration"),
        (get_organization_syslog_servers, "Get organization syslog overview"),
        (syslog_configuration_examples, "Show syslog configuration examples"),
        (analyze_syslog_requirements, "Analyze syslog requirements"),
        (syslog_parser_examples, "Show syslog parser configurations"),
        (syslog_help, "Get help with syslog tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)