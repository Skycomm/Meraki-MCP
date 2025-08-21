"""
MQTT Broker Tools for Cisco Meraki MCP Server
Configure MQTT brokers for real-time data streaming from sensors and devices
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


def get_network_mqtt_brokers(network_id: str) -> str:
    """
    📡 Get MQTT brokers configured for a network.
    
    Lists all MQTT brokers for real-time data streaming.
    
    Args:
        network_id: Network ID
    
    Returns:
        List of configured MQTT brokers
    """
    try:
        with safe_api_call("get MQTT brokers"):
            brokers = meraki.dashboard.networks.getNetworkMqttBrokers(network_id)
            
            output = ["📡 MQTT Brokers", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            if not brokers:
                output.append("No MQTT brokers configured")
                output.append("\n💡 Use create_network_mqtt_broker() to add one")
                return "\n".join(output)
            
            output.append(f"Total Brokers: {len(brokers)}")
            output.append("")
            
            # Show each broker
            for i, broker in enumerate(brokers, 1):
                broker_id = broker.get('id', 'Unknown')
                name = broker.get('name', 'Unnamed Broker')
                host = broker.get('host', 'Unknown')
                port = broker.get('port', 1883)
                
                output.append(f"{i}. 🖥️ {name}")
                output.append(f"   ID: {broker_id}")
                output.append(f"   Host: {host}")
                output.append(f"   Port: {port}")
                
                # Security settings
                security = broker.get('security', {})
                mode = security.get('mode', 'none')
                
                if mode == 'tls':
                    output.append("   🔒 Security: TLS enabled")
                    if security.get('tls', {}).get('caCertificate'):
                        output.append("   📜 CA Certificate: Configured")
                    verify_hostnames = security.get('tls', {}).get('verifyHostnames', False)
                    output.append(f"   🔍 Verify Hostnames: {'Yes' if verify_hostnames else 'No'}")
                else:
                    output.append("   ⚠️ Security: No encryption")
                
                # Authentication
                auth = broker.get('authentication', {})
                if auth.get('username'):
                    output.append(f"   👤 Username: {auth['username']}")
                    output.append("   🔑 Password: ••••••••")
                else:
                    output.append("   ⚠️ Authentication: None")
                
                output.append("")
            
            # MQTT data types available
            output.append("📊 Available Data Streams:")
            output.append("• Sensor data (MT series)")
            output.append("• Location analytics (MR/MV)")
            output.append("• Camera analytics")
            output.append("• Environmental monitoring")
            output.append("• Motion detection")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get MQTT brokers", e)


def get_network_mqtt_broker(
    network_id: str,
    mqtt_broker_id: str
) -> str:
    """
    🔍 Get details of a specific MQTT broker.
    
    Shows configuration details for a single MQTT broker.
    
    Args:
        network_id: Network ID
        mqtt_broker_id: MQTT broker ID
    
    Returns:
        Detailed broker configuration
    """
    try:
        with safe_api_call("get MQTT broker"):
            broker = meraki.dashboard.networks.getNetworkMqttBroker(
                network_id,
                mqtt_broker_id
            )
            
            output = ["🔍 MQTT Broker Details", "=" * 50, ""]
            output.append(f"Name: {broker.get('name', 'Unnamed')}")
            output.append(f"ID: {broker.get('id', mqtt_broker_id)}")
            output.append("")
            
            # Connection details
            output.append("📡 Connection:")
            output.append(f"   Host: {broker.get('host', 'Unknown')}")
            output.append(f"   Port: {broker.get('port', 1883)}")
            
            # Security configuration
            security = broker.get('security', {})
            mode = security.get('mode', 'none')
            
            output.append("\n🔒 Security Configuration:")
            output.append(f"   Mode: {mode.upper()}")
            
            if mode == 'tls':
                tls = security.get('tls', {})
                output.append("   TLS Settings:")
                
                if tls.get('caCertificate'):
                    output.append("      CA Certificate: ✅ Configured")
                else:
                    output.append("      CA Certificate: ❌ Not set")
                
                output.append(f"      Verify Hostnames: {'✅' if tls.get('verifyHostnames') else '❌'}")
                
                # Certificate preview if available
                if tls.get('caCertificate'):
                    cert = tls['caCertificate']
                    if cert.startswith('-----BEGIN CERTIFICATE-----'):
                        output.append("      Certificate Type: PEM format")
            
            # Authentication
            auth = broker.get('authentication', {})
            output.append("\n🔑 Authentication:")
            if auth.get('username'):
                output.append(f"   Username: {auth['username']}")
                output.append("   Password: ••••••••")
            else:
                output.append("   No authentication configured")
            
            # MQTT topics
            output.append("\n📝 MQTT Topics Structure:")
            output.append("   /merakimv/{serial}/raw_detection")
            output.append("   /merakimv/{serial}/light")
            output.append("   /merakimr/{serial}/location")
            output.append("   /merakimt/{serial}/temperature")
            output.append("   /merakimt/{serial}/humidity")
            output.append("   /merakimt/{serial}/water")
            
            # Connection test
            output.append("\n🧪 Testing Connection:")
            output.append(f"   mosquitto_sub -h {broker.get('host')} -p {broker.get('port')} -t '#' -v")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get MQTT broker", e)


def create_network_mqtt_broker(
    network_id: str,
    name: str,
    host: str,
    port: int = 1883,
    security_mode: str = "none",
    ca_certificate: Optional[str] = None,
    verify_hostnames: bool = True,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> str:
    """
    ➕ Create an MQTT broker configuration.
    
    Configures a new MQTT broker for real-time data streaming.
    
    Args:
        network_id: Network ID
        name: Broker name
        host: MQTT broker hostname/IP
        port: MQTT port (default: 1883, TLS: 8883)
        security_mode: Security mode ('none' or 'tls')
        ca_certificate: CA certificate for TLS (PEM format)
        verify_hostnames: Verify TLS hostnames
        username: MQTT username (optional)
        password: MQTT password (optional)
    
    Returns:
        Created broker configuration
    """
    try:
        with safe_api_call("create MQTT broker"):
            # Build broker configuration
            broker_data = {
                "name": name,
                "host": host,
                "port": port
            }
            
            # Security settings
            broker_data["security"] = {"mode": security_mode}
            
            if security_mode == "tls":
                broker_data["security"]["tls"] = {
                    "verifyHostnames": verify_hostnames
                }
                if ca_certificate:
                    broker_data["security"]["tls"]["caCertificate"] = ca_certificate
            
            # Authentication
            if username:
                broker_data["authentication"] = {
                    "username": username
                }
                if password:
                    broker_data["authentication"]["password"] = password
            
            # Create the broker
            broker = meraki.dashboard.networks.createNetworkMqttBroker(
                network_id,
                **broker_data
            )
            
            output = ["✅ MQTT Broker Created", "=" * 50, ""]
            output.append(f"Name: {broker.get('name', name)}")
            output.append(f"ID: {broker.get('id', 'N/A')}")
            output.append(f"Host: {broker.get('host', host)}")
            output.append(f"Port: {broker.get('port', port)}")
            
            if security_mode == "tls":
                output.append("🔒 Security: TLS enabled")
            else:
                output.append("⚠️ Security: No encryption")
            
            if username:
                output.append("🔑 Authentication: Configured")
            
            output.append("\n🚀 Next Steps:")
            output.append("1. Configure sensor gateway (MR/MV)")
            output.append("2. Enable MQTT on devices")
            output.append("3. Subscribe to topics")
            output.append("4. Process real-time data")
            
            output.append("\n📝 Example Subscription:")
            output.append(f"mosquitto_sub -h {host} -p {port} -t '/meraki/+/+' -v")
            if username:
                output.append(f"# Add: -u {username} -P <password>")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create MQTT broker", e)


def update_network_mqtt_broker(
    network_id: str,
    mqtt_broker_id: str,
    name: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    security_mode: Optional[str] = None,
    ca_certificate: Optional[str] = None,
    verify_hostnames: Optional[bool] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> str:
    """
    ✏️ Update MQTT broker configuration.
    
    Modifies settings for an existing MQTT broker.
    
    Args:
        network_id: Network ID
        mqtt_broker_id: MQTT broker ID
        name: New broker name
        host: New hostname/IP
        port: New port
        security_mode: New security mode
        ca_certificate: New CA certificate
        verify_hostnames: New hostname verification
        username: New username
        password: New password
    
    Returns:
        Updated broker configuration
    """
    try:
        with safe_api_call("update MQTT broker"):
            # Build update data
            update_data = {}
            
            if name is not None:
                update_data["name"] = name
            if host is not None:
                update_data["host"] = host
            if port is not None:
                update_data["port"] = port
            
            # Security updates
            if security_mode is not None:
                update_data["security"] = {"mode": security_mode}
                
                if security_mode == "tls":
                    update_data["security"]["tls"] = {}
                    if verify_hostnames is not None:
                        update_data["security"]["tls"]["verifyHostnames"] = verify_hostnames
                    if ca_certificate is not None:
                        update_data["security"]["tls"]["caCertificate"] = ca_certificate
            
            # Authentication updates
            if username is not None:
                if "authentication" not in update_data:
                    update_data["authentication"] = {}
                update_data["authentication"]["username"] = username
                
                if password is not None:
                    update_data["authentication"]["password"] = password
            
            # Update the broker
            broker = meraki.dashboard.networks.updateNetworkMqttBroker(
                network_id,
                mqtt_broker_id,
                **update_data
            )
            
            output = ["✏️ MQTT Broker Updated", "=" * 50, ""]
            output.append(f"Name: {broker.get('name', 'Unknown')}")
            output.append(f"ID: {mqtt_broker_id}")
            output.append("")
            
            output.append("📝 Updated Configuration:")
            if name:
                output.append(f"   Name: {name}")
            if host:
                output.append(f"   Host: {host}")
            if port:
                output.append(f"   Port: {port}")
            if security_mode:
                output.append(f"   Security: {security_mode}")
            
            output.append("\n⚠️ Important:")
            output.append("• Changes may take a few minutes")
            output.append("• Existing connections may be dropped")
            output.append("• Clients will need to reconnect")
            output.append("• Update client configurations")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update MQTT broker", e)


def delete_network_mqtt_broker(
    network_id: str,
    mqtt_broker_id: str
) -> str:
    """
    🗑️ Delete an MQTT broker.
    
    Removes MQTT broker configuration from the network.
    
    Args:
        network_id: Network ID
        mqtt_broker_id: MQTT broker ID
    
    Returns:
        Deletion confirmation
    """
    try:
        with safe_api_call("delete MQTT broker"):
            meraki.dashboard.networks.deleteNetworkMqttBroker(
                network_id,
                mqtt_broker_id
            )
            
            output = ["🗑️ MQTT Broker Deleted", "=" * 50, ""]
            output.append(f"Broker ID: {mqtt_broker_id}")
            output.append(f"Network: {network_id}")
            output.append("")
            output.append("✅ Broker configuration removed")
            output.append("")
            output.append("⚠️ Impact:")
            output.append("• All MQTT streams will stop")
            output.append("• Sensor data won't be published")
            output.append("• Clients will lose connection")
            output.append("• Historical data not affected")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("delete MQTT broker", e)


def get_network_sensor_mqtt_brokers(network_id: str) -> str:
    """
    🌡️ Get MQTT brokers for sensor data.
    
    Shows MQTT broker settings specific to environmental sensors.
    
    Args:
        network_id: Network ID
    
    Returns:
        Sensor MQTT broker configurations
    """
    try:
        with safe_api_call("get sensor MQTT brokers"):
            brokers = meraki.dashboard.sensor.getNetworkSensorMqttBrokers(network_id)
            
            output = ["🌡️ Sensor MQTT Brokers", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            if not brokers:
                output.append("No sensor MQTT brokers configured")
                return "\n".join(output)
            
            # Show each broker configuration
            for i, broker in enumerate(brokers, 1):
                broker_id = broker.get('mqttBrokerId', 'Unknown')
                enabled = broker.get('enabled', False)
                
                output.append(f"{i}. Broker ID: {broker_id}")
                output.append(f"   Status: {'✅ Enabled' if enabled else '❌ Disabled'}")
                
                # Sensor types
                sensor_types = broker.get('sensorTypes', [])
                if sensor_types:
                    output.append("   📊 Sensor Types:")
                    for sensor_type in sensor_types:
                        output.append(f"      • {sensor_type}")
                
                output.append("")
            
            # Sensor data topics
            output.append("📝 Sensor MQTT Topics:")
            output.append("• Temperature: /merakimt/{serial}/temperature")
            output.append("• Humidity: /merakimt/{serial}/humidity")
            output.append("• Water: /merakimt/{serial}/water")
            output.append("• Door: /merakimt/{serial}/door")
            output.append("• PM2.5: /merakimt/{serial}/pm25")
            output.append("• TVOC: /merakimt/{serial}/tvoc")
            output.append("• CO2: /merakimt/{serial}/co2")
            output.append("• Noise: /merakimt/{serial}/noise")
            
            output.append("\n📊 Data Format:")
            output.append("JSON payload with:")
            output.append("• timestamp")
            output.append("• value")
            output.append("• unit")
            output.append("• sensor serial")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get sensor MQTT brokers", e)


def mqtt_integration_guide() -> str:
    """
    📚 MQTT integration guide.
    
    Comprehensive guide for setting up MQTT data streaming.
    
    Returns:
        MQTT setup and integration guide
    """
    output = ["📚 MQTT Integration Guide", "=" * 50, ""]
    
    output.append("🚀 Quick Start:")
    output.append("1. Create MQTT broker configuration")
    output.append("2. Enable on gateway device (MR/MV)")
    output.append("3. Configure sensor settings")
    output.append("4. Subscribe to topics")
    output.append("5. Process real-time data")
    output.append("")
    
    output.append("📡 Supported Devices:")
    output.append("• MT sensors via MR/MV gateway")
    output.append("• MV cameras (analytics data)")
    output.append("• MR access points (location)")
    output.append("• Direct sensor support (newer models)")
    output.append("")
    
    output.append("🔧 Broker Setup:")
    output.append("1. Popular MQTT Brokers:")
    output.append("   • Mosquitto (lightweight)")
    output.append("   • HiveMQ (enterprise)")
    output.append("   • AWS IoT Core (cloud)")
    output.append("   • Azure IoT Hub")
    output.append("")
    
    output.append("2. Security Best Practices:")
    output.append("   • Always use TLS/SSL")
    output.append("   • Strong authentication")
    output.append("   • Network isolation")
    output.append("   • Access control lists")
    output.append("")
    
    output.append("📝 Topic Structure:")
    output.append("/meraki{product}/{serial}/{datatype}")
    output.append("")
    output.append("Examples:")
    output.append("• /merakimt/Q2XX-XXXX-XXXX/temperature")
    output.append("• /merakimv/Q2YY-YYYY-YYYY/raw_detection")
    output.append("• /merakimr/Q2ZZ-ZZZZ-ZZZZ/location")
    output.append("")
    
    output.append("📊 Data Processing:")
    output.append("```python")
    output.append("import paho.mqtt.client as mqtt")
    output.append("import json")
    output.append("")
    output.append("def on_message(client, userdata, msg):")
    output.append("    data = json.loads(msg.payload)")
    output.append("    print(f'{msg.topic}: {data}')")
    output.append("")
    output.append("client = mqtt.Client()")
    output.append("client.on_message = on_message")
    output.append("client.connect('broker.example.com', 8883)")
    output.append("client.subscribe('/meraki/+/+')")
    output.append("client.loop_forever()")
    output.append("```")
    output.append("")
    
    output.append("⚡ Performance Tips:")
    output.append("• Use QoS 0 for sensor data")
    output.append("• Implement local buffering")
    output.append("• Handle reconnections")
    output.append("• Monitor broker load")
    output.append("• Use topic filters wisely")
    
    return "\n".join(output)


def mqtt_help() -> str:
    """
    ❓ Get help with MQTT tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """📡 MQTT Broker Tools Help
==================================================

Available tools for MQTT configuration:

1. get_network_mqtt_brokers()
   - List all MQTT brokers
   - View configurations
   - Security settings
   - Connection details

2. get_network_mqtt_broker()
   - Detailed broker info
   - Connection parameters
   - Security configuration
   - Topic structure

3. create_network_mqtt_broker()
   - Add new MQTT broker
   - Configure security
   - Set authentication
   - Enable streaming

4. update_network_mqtt_broker()
   - Modify broker settings
   - Update credentials
   - Change security
   - Update endpoints

5. delete_network_mqtt_broker()
   - Remove broker config
   - Stop data streaming
   - Clean up settings

6. get_network_sensor_mqtt_brokers()
   - Sensor-specific settings
   - Enabled sensor types
   - Topic mappings
   - Data formats

7. mqtt_integration_guide()
   - Setup instructions
   - Code examples
   - Best practices
   - Troubleshooting

MQTT Use Cases:
🌡️ Environmental monitoring
📍 Real-time location
📹 Camera analytics
🚨 Instant alerts
📊 Data streaming
🔌 IoT integration

Security Modes:
• none - No encryption (not recommended)
• tls - TLS/SSL encryption

Standard Ports:
• 1883 - Plain MQTT
• 8883 - MQTT over TLS

Data Types:
• Sensor readings
• Motion events
• Location updates
• Analytics data
• Device status

Best Practices:
• Use TLS encryption
• Strong passwords
• Topic ACLs
• Monitor usage
• Handle failures
• Buffer locally

Common Issues:
• Connection timeouts
• Certificate errors
• Authentication fails
• Network firewalls
• Topic permissions

Integration Flow:
1. Setup MQTT broker
2. Configure in Meraki
3. Enable on devices
4. Subscribe to topics
5. Process messages
6. Store/visualize data
"""


def register_mqtt_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all MQTT broker tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_network_mqtt_brokers, "List MQTT brokers for a network"),
        (get_network_mqtt_broker, "Get specific MQTT broker details"),
        (create_network_mqtt_broker, "Create new MQTT broker"),
        (update_network_mqtt_broker, "Update MQTT broker configuration"),
        (delete_network_mqtt_broker, "Delete MQTT broker"),
        (get_network_sensor_mqtt_brokers, "Get sensor MQTT settings"),
        (mqtt_integration_guide, "MQTT setup and integration guide"),
        (mqtt_help, "Get help with MQTT tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)