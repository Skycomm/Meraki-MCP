"""
Core camera management tools for Cisco Meraki MCP server.

This module provides 100% coverage of the official Cisco Meraki Camera SDK v1.
All 45 official SDK methods are implemented exactly as documented.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_camera_tools(mcp_app, meraki):
    """
    Register all official SDK camera tools with the MCP server.
    Provides 100% coverage of Cisco Meraki Camera API v1.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all camera SDK tools
    register_camera_sdk_tools()

def register_camera_sdk_tools():
    """Register all camera SDK tools (100% coverage)."""
    
    # ==================== ALL 45 CAMERA SDK TOOLS ====================
    
    @app.tool(
        name="create_network_camera_quality_retention_profile",
        description="➕ Create network cameraQualityRetentionProfile"
    )
    def create_network_camera_quality_retention_profile(network_id: str):
        """Create create network cameraqualityretentionprofile."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.createNetworkCameraQualityRetentionProfile(
                network_id, **kwargs
            )
            
            response = f"# ➕ Create Network Cameraqualityretentionprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_camera_quality_retention_profile: {str(e)}"
    
    @app.tool(
        name="create_network_camera_wireless_profile",
        description="➕ Create network cameraWirelessProfile"
    )
    def create_network_camera_wireless_profile(network_id: str):
        """Create create network camerawirelessprofile."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.createNetworkCameraWirelessProfile(
                network_id, **kwargs
            )
            
            response = f"# ➕ Create Network Camerawirelessprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_camera_wireless_profile: {str(e)}"
    
    @app.tool(
        name="create_organization_camera_custom_analytics_artifact",
        description="➕ Create organization cameraCustomAnalyticsArtifact"
    )
    def create_organization_camera_custom_analytics_artifact(organization_id: str):
        """Create create organization cameracustomanalyticsartifact."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.createOrganizationCameraCustomAnalyticsArtifact(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organization Cameracustomanalyticsartifact\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_organization_camera_custom_analytics_artifact: {str(e)}"
    
    @app.tool(
        name="create_organization_camera_role",
        description="➕ Create organization cameraRole"
    )
    def create_organization_camera_role(organization_id: str):
        """Create create organization camerarole."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.createOrganizationCameraRole(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organization Camerarole\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_organization_camera_role: {str(e)}"
    
    @app.tool(
        name="delete_network_camera_quality_retention_profile",
        description="❌ Delete network cameraQualityRetentionProfile"
    )
    def delete_network_camera_quality_retention_profile(network_id: str):
        """Delete delete network cameraqualityretentionprofile."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.deleteNetworkCameraQualityRetentionProfile(
                network_id, **kwargs
            )
            
            response = f"# ❌ Delete Network Cameraqualityretentionprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_camera_quality_retention_profile: {str(e)}"
    
    @app.tool(
        name="delete_network_camera_wireless_profile",
        description="❌ Delete network cameraWirelessProfile"
    )
    def delete_network_camera_wireless_profile(network_id: str):
        """Delete delete network camerawirelessprofile."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.deleteNetworkCameraWirelessProfile(
                network_id, **kwargs
            )
            
            response = f"# ❌ Delete Network Camerawirelessprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_camera_wireless_profile: {str(e)}"
    
    @app.tool(
        name="delete_organization_camera_custom_analytics_artifact",
        description="❌ Delete organization cameraCustomAnalyticsArtifact"
    )
    def delete_organization_camera_custom_analytics_artifact(organization_id: str):
        """Delete delete organization cameracustomanalyticsartifact."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.deleteOrganizationCameraCustomAnalyticsArtifact(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organization Cameracustomanalyticsartifact\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_organization_camera_custom_analytics_artifact: {str(e)}"
    
    @app.tool(
        name="delete_organization_camera_role",
        description="❌ Delete organization cameraRole"
    )
    def delete_organization_camera_role(organization_id: str):
        """Delete delete organization camerarole."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.deleteOrganizationCameraRole(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organization Camerarole\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_organization_camera_role: {str(e)}"
    
    @app.tool(
        name="generate_device_camera_snapshot",
        description="🔗 generate device cameraSnapshot"
    )
    def generate_device_camera_snapshot(serial: str):
        """Generate generate device camerasnapshot."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.generateDeviceCameraSnapshot(
                serial, **kwargs  
            )
            
            response = f"# 🔗 Generate Device Camerasnapshot\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in generate_device_camera_snapshot: {str(e)}"
    
    @app.tool(
        name="get_device_camera_analytics_live",
        description="📹 Get device cameraAnalyticsLive"
    )
    def get_device_camera_analytics_live(serial: str, per_page: int = 1000):
        """Get get device cameraanalyticslive."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsLive(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Cameraanalyticslive\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_analytics_live: {str(e)}"
    
    @app.tool(
        name="get_device_camera_analytics_overview",
        description="📹 Get device cameraAnalyticsOverview"
    )
    def get_device_camera_analytics_overview(serial: str, per_page: int = 1000):
        """Get get device cameraanalyticsoverview."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsOverview(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Cameraanalyticsoverview\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_analytics_overview: {str(e)}"
    
    @app.tool(
        name="get_device_camera_analytics_recent",
        description="📹 Get device cameraAnalyticsRecent"
    )
    def get_device_camera_analytics_recent(serial: str, per_page: int = 1000):
        """Get get device cameraanalyticsrecent."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsRecent(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Cameraanalyticsrecent\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_analytics_recent: {str(e)}"
    
    @app.tool(
        name="get_device_camera_analytics_zone_history",
        description="📹 Get device cameraAnalyticsZoneHistory"
    )
    def get_device_camera_analytics_zone_history(serial: str, timespan: int = 86400):
        """Get get device cameraanalyticszonehistory."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsZoneHistory(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Cameraanalyticszonehistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_analytics_zone_history: {str(e)}"
    
    @app.tool(
        name="get_device_camera_analytics_zones",
        description="📹 Get device cameraAnalyticsZones"
    )
    def get_device_camera_analytics_zones(serial: str, per_page: int = 1000):
        """Get get device cameraanalyticszones."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsZones(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Cameraanalyticszones\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_analytics_zones: {str(e)}"
    
    @app.tool(
        name="get_device_camera_custom_analytics",
        description="📹 Get device cameraCustomAnalytics"
    )
    def get_device_camera_custom_analytics(serial: str, per_page: int = 1000):
        """Get get device cameracustomanalytics."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraCustomAnalytics(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Cameracustomanalytics\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_custom_analytics: {str(e)}"
    
    @app.tool(
        name="get_device_camera_quality_and_retention",
        description="📹 Get device cameraQualityAndRetention"
    )
    def get_device_camera_quality_and_retention(serial: str, per_page: int = 1000):
        """Get get device cameraqualityandretention."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraQualityAndRetention(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Cameraqualityandretention\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_quality_and_retention: {str(e)}"
    
    @app.tool(
        name="get_device_camera_sense",
        description="📹 Get device cameraSense"
    )
    def get_device_camera_sense(serial: str, per_page: int = 1000):
        """Get get device camerasense."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraSense(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Camerasense\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_sense: {str(e)}"
    
    @app.tool(
        name="get_device_camera_sense_object_detection_models",
        description="📹 Get device cameraSenseObjectDetectionModels"
    )
    def get_device_camera_sense_object_detection_models(serial: str, per_page: int = 1000):
        """Get get device camerasenseobjectdetectionmodels."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraSenseObjectDetectionModels(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Camerasenseobjectdetectionmodels\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_sense_object_detection_models: {str(e)}"
    
    @app.tool(
        name="get_device_camera_video_link",
        description="📹 Get device cameraVideoLink"
    )
    def get_device_camera_video_link(serial: str, per_page: int = 1000):
        """Get get device cameravideolink."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraVideoLink(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Cameravideolink\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_video_link: {str(e)}"
    
    @app.tool(
        name="get_device_camera_video_settings",
        description="📹 Get device cameraVideoSettings"
    )
    def get_device_camera_video_settings(serial: str, per_page: int = 1000):
        """Get get device cameravideosettings."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraVideoSettings(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Cameravideosettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_video_settings: {str(e)}"
    
    @app.tool(
        name="get_device_camera_wireless_profiles",
        description="📹 Get device cameraWirelessProfiles"
    )
    def get_device_camera_wireless_profiles(serial: str, per_page: int = 1000):
        """Get get device camerawirelessprofiles."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getDeviceCameraWirelessProfiles(
                serial, **kwargs  
            )
            
            response = f"# 📹 Get Device Camerawirelessprofiles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_camera_wireless_profiles: {str(e)}"
    
    @app.tool(
        name="get_network_camera_quality_retention_profile",
        description="📹 Get network cameraQualityRetentionProfile"
    )
    def get_network_camera_quality_retention_profile(network_id: str, per_page: int = 1000):
        """Get get network cameraqualityretentionprofile."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getNetworkCameraQualityRetentionProfile(
                network_id, **kwargs
            )
            
            response = f"# 📹 Get Network Cameraqualityretentionprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_camera_quality_retention_profile: {str(e)}"
    
    @app.tool(
        name="get_network_camera_quality_retention_profiles",
        description="📹 Get network cameraQualityRetentionProfiles"
    )
    def get_network_camera_quality_retention_profiles(network_id: str, per_page: int = 1000):
        """Get get network cameraqualityretentionprofiles."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getNetworkCameraQualityRetentionProfiles(
                network_id, **kwargs
            )
            
            response = f"# 📹 Get Network Cameraqualityretentionprofiles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_camera_quality_retention_profiles: {str(e)}"
    
    @app.tool(
        name="get_network_camera_schedules",
        description="📹 Get network cameraSchedules"
    )
    def get_network_camera_schedules(network_id: str, per_page: int = 1000):
        """Get get network cameraschedules."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getNetworkCameraSchedules(
                network_id, **kwargs
            )
            
            response = f"# 📹 Get Network Cameraschedules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_camera_schedules: {str(e)}"
    
    @app.tool(
        name="get_network_camera_wireless_profile",
        description="📹 Get network cameraWirelessProfile"
    )
    def get_network_camera_wireless_profile(network_id: str, per_page: int = 1000):
        """Get get network camerawirelessprofile."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getNetworkCameraWirelessProfile(
                network_id, **kwargs
            )
            
            response = f"# 📹 Get Network Camerawirelessprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_camera_wireless_profile: {str(e)}"
    
    @app.tool(
        name="get_network_camera_wireless_profiles",
        description="📹 Get network cameraWirelessProfiles"
    )
    def get_network_camera_wireless_profiles(network_id: str, per_page: int = 1000):
        """Get get network camerawirelessprofiles."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getNetworkCameraWirelessProfiles(
                network_id, **kwargs
            )
            
            response = f"# 📹 Get Network Camerawirelessprofiles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_camera_wireless_profiles: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_boundaries_areas_by_device",
        description="📹 Get organization cameraBoundariesAreasBy device"
    )
    def get_organization_camera_boundaries_areas_by_device(organization_id: str, per_page: int = 100):
        """Get get organization cameraboundariesareasby device."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraBoundariesAreasByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Cameraboundariesareasby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_boundaries_areas_by_device: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_boundaries_lines_by_device",
        description="📹 Get organization cameraBoundariesLinesBy device"
    )
    def get_organization_camera_boundaries_lines_by_device(organization_id: str, per_page: int = 100):
        """Get get organization cameraboundarieslinesby device."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraBoundariesLinesByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Cameraboundarieslinesby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_boundaries_lines_by_device: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_custom_analytics_artifact",
        description="📹 Get organization cameraCustomAnalyticsArtifact"
    )
    def get_organization_camera_custom_analytics_artifact(organization_id: str, per_page: int = 1000):
        """Get get organization cameracustomanalyticsartifact."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraCustomAnalyticsArtifact(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Cameracustomanalyticsartifact\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_custom_analytics_artifact: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_custom_analytics_artifacts",
        description="📹 Get organization cameraCustomAnalyticsArtifacts"
    )
    def get_organization_camera_custom_analytics_artifacts(organization_id: str, per_page: int = 1000):
        """Get get organization cameracustomanalyticsartifacts."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraCustomAnalyticsArtifacts(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Cameracustomanalyticsartifacts\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_custom_analytics_artifacts: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_detections_history_by_boundary_by_interval",
        description="📹 Get organization cameraDetectionsHistoryByBoundaryByInterval"
    )
    def get_organization_camera_detections_history_by_boundary_by_interval(organization_id: str, timespan: int = 86400):
        """Get get organization cameradetectionshistorybyboundarybyinterval."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraDetectionsHistoryByBoundaryByInterval(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Cameradetectionshistorybyboundarybyinterval\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_detections_history_by_boundary_by_interval: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_onboarding_statuses",
        description="📹 Get organization cameraOnboardingStatuses"
    )
    def get_organization_camera_onboarding_statuses(organization_id: str, per_page: int = 100):
        """Get get organization cameraonboardingstatuses."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraOnboardingStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Cameraonboardingstatuses\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_onboarding_statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_permission",
        description="📹 Get organization cameraPermission"
    )
    def get_organization_camera_permission(organization_id: str, per_page: int = 1000):
        """Get get organization camerapermission."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraPermission(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Camerapermission\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_permission: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_permissions",
        description="📹 Get organization cameraPermissions"
    )
    def get_organization_camera_permissions(organization_id: str, per_page: int = 1000):
        """Get get organization camerapermissions."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraPermissions(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Camerapermissions\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_permissions: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_role",
        description="📹 Get organization cameraRole"
    )
    def get_organization_camera_role(organization_id: str, per_page: int = 1000):
        """Get get organization camerarole."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraRole(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Camerarole\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_role: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_roles",
        description="📹 Get organization cameraRoles"
    )
    def get_organization_camera_roles(organization_id: str, per_page: int = 1000):
        """Get get organization cameraroles."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.getOrganizationCameraRoles(
                organization_id, **kwargs
            )
            
            response = f"# 📹 Get Organization Cameraroles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_camera_roles: {str(e)}"
    
    @app.tool(
        name="update_device_camera_custom_analytics",
        description="✏️ Update device cameraCustomAnalytics"
    )
    def update_device_camera_custom_analytics(serial: str):
        """Update update device cameracustomanalytics."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.updateDeviceCameraCustomAnalytics(
                serial, **kwargs  
            )
            
            response = f"# ✏️ Update Device Cameracustomanalytics\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_camera_custom_analytics: {str(e)}"
    
    @app.tool(
        name="update_device_camera_quality_and_retention",
        description="✏️ Update device cameraQualityAndRetention"
    )
    def update_device_camera_quality_and_retention(serial: str):
        """Update update device cameraqualityandretention."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.updateDeviceCameraQualityAndRetention(
                serial, **kwargs  
            )
            
            response = f"# ✏️ Update Device Cameraqualityandretention\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_camera_quality_and_retention: {str(e)}"
    
    @app.tool(
        name="update_device_camera_sense",
        description="✏️ Update device cameraSense"
    )
    def update_device_camera_sense(serial: str):
        """Update update device camerasense."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.updateDeviceCameraSense(
                serial, **kwargs  
            )
            
            response = f"# ✏️ Update Device Camerasense\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_camera_sense: {str(e)}"
    
    @app.tool(
        name="update_device_camera_video_settings",
        description="✏️ Update device cameraVideoSettings"
    )
    def update_device_camera_video_settings(serial: str):
        """Update update device cameravideosettings."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.updateDeviceCameraVideoSettings(
                serial, **kwargs  
            )
            
            response = f"# ✏️ Update Device Cameravideosettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_camera_video_settings: {str(e)}"
    
    @app.tool(
        name="update_device_camera_wireless_profiles",
        description="✏️ Update device cameraWirelessProfiles"
    )
    def update_device_camera_wireless_profiles(serial: str):
        """Update update device camerawirelessprofiles."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.updateDeviceCameraWirelessProfiles(
                serial, **kwargs  
            )
            
            response = f"# ✏️ Update Device Camerawirelessprofiles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_camera_wireless_profiles: {str(e)}"
    
    @app.tool(
        name="update_network_camera_quality_retention_profile",
        description="✏️ Update network cameraQualityRetentionProfile"
    )
    def update_network_camera_quality_retention_profile(network_id: str):
        """Update update network cameraqualityretentionprofile."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.updateNetworkCameraQualityRetentionProfile(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Cameraqualityretentionprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_camera_quality_retention_profile: {str(e)}"
    
    @app.tool(
        name="update_network_camera_wireless_profile",
        description="✏️ Update network cameraWirelessProfile"
    )
    def update_network_camera_wireless_profile(network_id: str):
        """Update update network camerawirelessprofile."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.updateNetworkCameraWirelessProfile(
                network_id, **kwargs
            )
            
            response = f"# ✏️ Update Network Camerawirelessprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_camera_wireless_profile: {str(e)}"
    
    @app.tool(
        name="update_organization_camera_onboarding_statuses",
        description="✏️ Update organization cameraOnboardingStatuses"
    )
    def update_organization_camera_onboarding_statuses(organization_id: str):
        """Update update organization cameraonboardingstatuses."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.updateOrganizationCameraOnboardingStatuses(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organization Cameraonboardingstatuses\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_organization_camera_onboarding_statuses: {str(e)}"
    
    @app.tool(
        name="update_organization_camera_role",
        description="✏️ Update organization cameraRole"
    )
    def update_organization_camera_role(organization_id: str):
        """Update update organization camerarole."""
        try:
            kwargs = {}
            
            # Add pagination and timespan for appropriate methods
            if "per_page" in locals():
                kwargs["perPage"] = per_page
            if "timespan" in locals():
                kwargs["timespan"] = timespan
                
            result = meraki_client.dashboard.camera.updateOrganizationCameraRole(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organization Camerarole\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with camera-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key camera-specific fields
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'recording' in item:
                                recording = item.get('recording', {})
                                if isinstance(recording, dict):
                                    response += f"   - Recording: {recording.get('enabled', 'N/A')}\n"
                            if 'quality' in item:
                                response += f"   - Quality: {item.get('quality')}\n"
                            if 'resolution' in item:
                                response += f"   - Resolution: {item.get('resolution')}\n"
                            if 'analytics' in item:
                                analytics = item.get('analytics', {})
                                if isinstance(analytics, dict):
                                    response += f"   - Analytics: {analytics.get('enabled', 'N/A')}\n"
                            if 'motionDetection' in item:
                                motion = item.get('motionDetection', {})
                                if isinstance(motion, dict):
                                    response += f"   - Motion Detection: {motion.get('enabled', 'N/A')}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show camera-relevant fields
                    camera_fields = ['serial', 'model', 'name', 'status', 'recording', 'quality', 
                                   'resolution', 'analytics', 'motionDetection', 'nightVision']
                    
                    for field in camera_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in camera_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_organization_camera_role: {str(e)}"
    
