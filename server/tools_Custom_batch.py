"""
Batch operations tools for Cisco Meraki MCP server.

This module provides tools for bulk operations across all Meraki modules.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_custom_batch_tools(mcp_app, meraki):
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    """
    Register batch tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    
    # ==================== BATCH OPERATIONS ====================
    
    @app.tool(
        name="batch_organizations",
        description="🔄📦 Execute batch operations for organizations (actions: JSON array)"
    )
    def batch_organizations(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """
        Execute batch operations for organizations.
        
        Args:
            organization_id: Organization ID
            actions: JSON array of actions to perform
            confirmed: Confirm execution (must be true)
            synchronous: Execute synchronously (default true)
        """
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            # Parse actions JSON
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.organizations(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Organizations Operation\n\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Unknown')}\n"
                response += f"**Batch ID**: {result.get('id', 'N/A')}\n"
                response += f"**Actions**: {len(actions_list)} operations\n\n"
                
                # Show errors if any
                errors = result.get('errors', [])
                if errors:
                    response += "## ❌ Errors\n"
                    for error in errors[:5]:
                        response += f"- {error}\n"
            else:
                response += "*Batch operation submitted*\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_networks",
        description="🔄🌐 Execute batch operations for networks (actions: JSON array)"
    )
    def batch_networks(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """
        Execute batch operations for networks.
        
        Args:
            organization_id: Organization ID
            actions: JSON array of network actions
            confirmed: Confirm execution (must be true)
            synchronous: Execute synchronously
        """
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.networks(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Networks Operation\n\n"
            response += f"**Actions**: {len(actions_list)} network operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
                response += f"**Batch ID**: {result.get('id', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_devices",
        description="🔄📱 Execute batch operations for devices (actions: JSON array)"
    )
    def batch_devices(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """
        Execute batch operations for devices.
        
        Args:
            organization_id: Organization ID
            actions: JSON array of device actions
            confirmed: Confirm execution (must be true)
            synchronous: Execute synchronously
        """
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.devices(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Devices Operation\n\n"
            response += f"**Actions**: {len(actions_list)} device operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
                response += f"**Batch ID**: {result.get('id', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_appliance",
        description="🔄🔧 Execute batch operations for appliance (actions: JSON array)"
    )
    def batch_appliance(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """Execute batch operations for appliance devices."""
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.appliance(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Appliance Operation\n\n"
            response += f"**Actions**: {len(actions_list)} appliance operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_switch",
        description="🔄🔌 Execute batch operations for switches (actions: JSON array)"
    )
    def batch_switch(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """Execute batch operations for switches."""
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.switch(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Switch Operation\n\n"
            response += f"**Actions**: {len(actions_list)} switch operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_wireless",
        description="🔄📡 Execute batch operations for wireless (actions: JSON array)"
    )
    def batch_wireless(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """Execute batch operations for wireless devices."""
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.wireless(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Wireless Operation\n\n"
            response += f"**Actions**: {len(actions_list)} wireless operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_camera",
        description="🔄📷 Execute batch operations for cameras (actions: JSON array)"
    )
    def batch_camera(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """Execute batch operations for cameras."""
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.camera(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Camera Operation\n\n"
            response += f"**Actions**: {len(actions_list)} camera operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_cellular_gateway",
        description="🔄📱 Execute batch operations for cellular gateways (actions: JSON array)"
    )
    def batch_cellular_gateway(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """Execute batch operations for cellular gateways."""
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.cellularGateway(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Cellular Gateway Operation\n\n"
            response += f"**Actions**: {len(actions_list)} cellular gateway operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_sm",
        description="🔄📱 Execute batch operations for Systems Manager (actions: JSON array)"
    )
    def batch_sm(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """Execute batch operations for Systems Manager."""
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.sm(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch SM Operation\n\n"
            response += f"**Actions**: {len(actions_list)} SM operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_sensor",
        description="🔄🌡️ Execute batch operations for sensors (actions: JSON array)"
    )
    def batch_sensor(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """Execute batch operations for sensors."""
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.sensor(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Sensor Operation\n\n"
            response += f"**Actions**: {len(actions_list)} sensor operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    @app.tool(
        name="batch_insight",
        description="🔄📊 Execute batch operations for Insight (actions: JSON array)"
    )
    def batch_insight(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = True
    ):
        """Execute batch operations for Insight."""
        try:
            if not confirmed:
                return "⚠️ Batch operations require confirmed=true to execute"
            
            try:
                actions_list = json.loads(actions)
            except:
                return "❌ Invalid JSON format for actions parameter"
            
            kwargs = {
                'actions': actions_list,
                'confirmed': confirmed,
                'synchronous': synchronous
            }
            
            result = meraki_client.dashboard.batch.insight(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Batch Insight Operation\n\n"
            response += f"**Actions**: {len(actions_list)} insight operations\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'Processing')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error executing batch: {str(e)}"
    
    # ==================== BATCH OPERATION HELPERS ====================
    
    @app.tool(
        name="batch_operation_example",
        description="📚🔄 Get example batch operation JSON for a specific module"
    )
    def batch_operation_example(
        module: str
    ):
        """
        Get example batch operation JSON.
        
        Args:
            module: Module name (networks, devices, wireless, switch, etc.)
        """
        examples = {
            'networks': '''[
    {
        "resource": "/networks/{networkId}",
        "operation": "update",
        "body": {
            "name": "Updated Network Name",
            "timeZone": "America/Los_Angeles"
        }
    }
]''',
            'devices': '''[
    {
        "resource": "/devices/{serial}",
        "operation": "update",
        "body": {
            "name": "New Device Name",
            "tags": ["tag1", "tag2"],
            "address": "123 Main St"
        }
    }
]''',
            'wireless': '''[
    {
        "resource": "/networks/{networkId}/wireless/ssids/0",
        "operation": "update",
        "body": {
            "name": "Guest WiFi",
            "enabled": true,
            "authMode": "psk",
            "psk": "SecurePassword123!"
        }
    }
]''',
            'switch': '''[
    {
        "resource": "/devices/{serial}/switch/ports/1",
        "operation": "update",
        "body": {
            "name": "Uplink Port",
            "enabled": true,
            "type": "trunk",
            "vlan": 1
        }
    }
]''',
            'appliance': '''[
    {
        "resource": "/networks/{networkId}/appliance/vlans",
        "operation": "create",
        "body": {
            "id": "100",
            "name": "Guest VLAN",
            "subnet": "192.168.100.0/24",
            "applianceIp": "192.168.100.1"
        }
    }
]'''
        }
        
        if module.lower() in examples:
            response = f"# 📚 Batch Operation Example - {module.title()}\n\n"
            response += f"## JSON Format for `actions` parameter:\n\n"
            response += f"```json\n{examples[module.lower()]}\n```\n\n"
            response += "## Important Notes:\n"
            response += "- Replace {networkId}, {serial} with actual values\n"
            response += "- Set confirmed=true to execute\n"
            response += "- Operations: create, update, delete\n"
            response += "- Resource paths match API endpoints\n"
            response += "- Body contains the parameters for the operation\n"
        else:
            response = f"# 📚 Available Batch Modules\n\n"
            response += "Use one of these module names for examples:\n"
            for mod in examples.keys():
                response += f"- {mod}\n"
        
        return response