"""
Additional Camera endpoints for Cisco Meraki MCP Server.
Auto-generated to achieve 100% API coverage.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def format_dict_response(data: dict, resource_name: str) -> str:
    """Format dictionary response."""
    result = f"# {resource_name}\n\n"
    for key, value in data.items():
        if value is not None:
            result += f"**{key}**: {value}\n"
    return result

def format_list_response(data: list, resource_name: str) -> str:
    """Format list response."""
    if not data:
        return f"No {resource_name.lower()} found."
    
    result = f"# {resource_name}\n\n"
    result += f"**Total**: {len(data)}\n\n"
    
    for idx, item in enumerate(data[:10], 1):
        if isinstance(item, dict):
            name = item.get('name', item.get('id', f'Item {idx}'))
            result += f"## {name}\n"
            for key, value in item.items():
                if value is not None and key not in ['name']:
                    result += f"- **{key}**: {value}\n"
            result += "\n"
        else:
            result += f"- {item}\n"
    
    if len(data) > 10:
        result += f"\n... and {len(data) - 10} more items"
    
    return result

def register_camera_additional_tools(mcp_app, meraki):
    """Register additional camera tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_camera_additional_handlers()

def register_camera_additional_handlers():
    """Register additional camera tool handlers."""

    @app.tool(
        name="create_network_camera_quality_retention_profile",
        description="➕ Create network camera quality retention profile"
    )
    def create_network_camera_quality_retention_profile(network_id: str, **kwargs):
        """Create network camera quality retention profile."""
        try:
            result = meraki_client.dashboard.camera.createNetworkCameraQualityRetentionProfile(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Quality Retention Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Quality Retention Profile")
            else:
                return f"✅ Create network camera quality retention profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_camera_wireless_profile",
        description="➕ Create network camera wireless profile"
    )
    def create_network_camera_wireless_profile(network_id: str, **kwargs):
        """Create network camera wireless profile."""
        try:
            result = meraki_client.dashboard.camera.createNetworkCameraWirelessProfile(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Wireless Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Wireless Profile")
            else:
                return f"✅ Create network camera wireless profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_camera_custom_analytics_artifact",
        description="➕ Create organization camera custom analytics artifact"
    )
    def create_organization_camera_custom_analytics_artifact(organization_id: str, **kwargs):
        """Create organization camera custom analytics artifact."""
        try:
            result = meraki_client.dashboard.camera.createOrganizationCameraCustomAnalyticsArtifact(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Custom Analytics Artifact")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Custom Analytics Artifact")
            else:
                return f"✅ Create organization camera custom analytics artifact completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_camera_role",
        description="➕ Create organization camera role"
    )
    def create_organization_camera_role(organization_id: str, **kwargs):
        """Create organization camera role."""
        try:
            result = meraki_client.dashboard.camera.createOrganizationCameraRole(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Role")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Role")
            else:
                return f"✅ Create organization camera role completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_camera_quality_retention_profile",
        description="🗑️ Delete network camera quality retention profile"
    )
    def delete_network_camera_quality_retention_profile(network_id: str):
        """Delete network camera quality retention profile."""
        try:
            result = meraki_client.dashboard.camera.deleteNetworkCameraQualityRetentionProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Quality Retention Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Quality Retention Profile")
            else:
                return f"✅ Delete network camera quality retention profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_camera_wireless_profile",
        description="🗑️ Delete network camera wireless profile"
    )
    def delete_network_camera_wireless_profile(network_id: str):
        """Delete network camera wireless profile."""
        try:
            result = meraki_client.dashboard.camera.deleteNetworkCameraWirelessProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Wireless Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Wireless Profile")
            else:
                return f"✅ Delete network camera wireless profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_camera_custom_analytics_artifact",
        description="🗑️ Delete organization camera custom analytics artifact"
    )
    def delete_organization_camera_custom_analytics_artifact(organization_id: str):
        """Delete organization camera custom analytics artifact."""
        try:
            result = meraki_client.dashboard.camera.deleteOrganizationCameraCustomAnalyticsArtifact(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Custom Analytics Artifact")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Custom Analytics Artifact")
            else:
                return f"✅ Delete organization camera custom analytics artifact completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_camera_role",
        description="🗑️ Delete organization camera role"
    )
    def delete_organization_camera_role(organization_id: str):
        """Delete organization camera role."""
        try:
            result = meraki_client.dashboard.camera.deleteOrganizationCameraRole(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Role")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Role")
            else:
                return f"✅ Delete organization camera role completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="generate_device_camera_snapshot",
        description="⚡ Execute device camera snapshot"
    )
    def generate_device_camera_snapshot(serial: str):
        """Execute device camera snapshot."""
        try:
            result = meraki_client.dashboard.camera.generateDeviceCameraSnapshot(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Snapshot")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Snapshot")
            else:
                return f"✅ Execute device camera snapshot completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_camera_analytics_live",
        description="📊 Get device camera analytics live"
    )
    def get_device_camera_analytics_live(serial: str):
        """Get device camera analytics live."""
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsLive(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Analytics Live")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Analytics Live")
            else:
                return f"✅ Get device camera analytics live completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_camera_analytics_overview",
        description="📊 Get device camera analytics overview"
    )
    def get_device_camera_analytics_overview(serial: str):
        """Get device camera analytics overview."""
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsOverview(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Analytics Overview")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Analytics Overview")
            else:
                return f"✅ Get device camera analytics overview completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_camera_analytics_recent",
        description="📊 Get device camera analytics recent"
    )
    def get_device_camera_analytics_recent(serial: str):
        """Get device camera analytics recent."""
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsRecent(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Analytics Recent")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Analytics Recent")
            else:
                return f"✅ Get device camera analytics recent completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_camera_analytics_zone_history",
        description="📊 Get device camera analytics zone history"
    )
    def get_device_camera_analytics_zone_history(serial: str):
        """Get device camera analytics zone history."""
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsZoneHistory(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Analytics Zone History")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Analytics Zone History")
            else:
                return f"✅ Get device camera analytics zone history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_camera_custom_analytics",
        description="📊 Get device camera custom analytics"
    )
    def get_device_camera_custom_analytics(serial: str):
        """Get device camera custom analytics."""
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraCustomAnalytics(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Custom Analytics")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Custom Analytics")
            else:
                return f"✅ Get device camera custom analytics completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_camera_quality_and_retention",
        description="📊 Get device camera quality and retention"
    )
    def get_device_camera_quality_and_retention(serial: str):
        """Get device camera quality and retention."""
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraQualityAndRetention(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Quality And Retention")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Quality And Retention")
            else:
                return f"✅ Get device camera quality and retention completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_camera_sense_object_detection_models",
        description="📊 Get device camera sense object detection models"
    )
    def get_device_camera_sense_object_detection_models(serial: str):
        """Get device camera sense object detection models."""
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraSenseObjectDetectionModels(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Sense Object Detection Models")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Sense Object Detection Models")
            else:
                return f"✅ Get device camera sense object detection models completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_camera_wireless_profiles",
        description="📊 Get device camera wireless profiles"
    )
    def get_device_camera_wireless_profiles(serial: str):
        """Get device camera wireless profiles."""
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraWirelessProfiles(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Wireless Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Wireless Profiles")
            else:
                return f"✅ Get device camera wireless profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_camera_quality_retention_profile",
        description="📊 Get network camera quality retention profile"
    )
    def get_network_camera_quality_retention_profile(network_id: str):
        """Get network camera quality retention profile."""
        try:
            result = meraki_client.dashboard.camera.getNetworkCameraQualityRetentionProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Quality Retention Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Quality Retention Profile")
            else:
                return f"✅ Get network camera quality retention profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_camera_quality_retention_profiles",
        description="📊 Get network camera quality retention profiles"
    )
    def get_network_camera_quality_retention_profiles(network_id: str):
        """Get network camera quality retention profiles."""
        try:
            result = meraki_client.dashboard.camera.getNetworkCameraQualityRetentionProfiles(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Quality Retention Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Quality Retention Profiles")
            else:
                return f"✅ Get network camera quality retention profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_camera_schedules",
        description="📊 Get network camera schedules"
    )
    def get_network_camera_schedules(network_id: str):
        """Get network camera schedules."""
        try:
            result = meraki_client.dashboard.camera.getNetworkCameraSchedules(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Schedules")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Schedules")
            else:
                return f"✅ Get network camera schedules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_camera_wireless_profile",
        description="📊 Get network camera wireless profile"
    )
    def get_network_camera_wireless_profile(network_id: str):
        """Get network camera wireless profile."""
        try:
            result = meraki_client.dashboard.camera.getNetworkCameraWirelessProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Wireless Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Wireless Profile")
            else:
                return f"✅ Get network camera wireless profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_camera_wireless_profiles",
        description="📊 Get network camera wireless profiles"
    )
    def get_network_camera_wireless_profiles(network_id: str):
        """Get network camera wireless profiles."""
        try:
            result = meraki_client.dashboard.camera.getNetworkCameraWirelessProfiles(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Wireless Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Wireless Profiles")
            else:
                return f"✅ Get network camera wireless profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_camera_boundaries_areas_by_device",
        description="📊 Get organization camera boundaries areas by device"
    )
    def get_organization_camera_boundaries_areas_by_device(organization_id: str):
        """Get organization camera boundaries areas by device."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraBoundariesAreasByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Boundaries Areas By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Boundaries Areas By Device")
            else:
                return f"✅ Get organization camera boundaries areas by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_camera_boundaries_lines_by_device",
        description="📊 Get organization camera boundaries lines by device"
    )
    def get_organization_camera_boundaries_lines_by_device(organization_id: str):
        """Get organization camera boundaries lines by device."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraBoundariesLinesByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Boundaries Lines By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Boundaries Lines By Device")
            else:
                return f"✅ Get organization camera boundaries lines by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_camera_custom_analytics_artifact",
        description="📊 Get organization camera custom analytics artifact"
    )
    def get_organization_camera_custom_analytics_artifact(organization_id: str):
        """Get organization camera custom analytics artifact."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraCustomAnalyticsArtifact(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Custom Analytics Artifact")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Custom Analytics Artifact")
            else:
                return f"✅ Get organization camera custom analytics artifact completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_camera_custom_analytics_artifacts",
        description="📊 Get organization camera custom analytics artifacts"
    )
    def get_organization_camera_custom_analytics_artifacts(organization_id: str):
        """Get organization camera custom analytics artifacts."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraCustomAnalyticsArtifacts(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Custom Analytics Artifacts")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Custom Analytics Artifacts")
            else:
                return f"✅ Get organization camera custom analytics artifacts completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_camera_detections_by_boundary",
        description="📊 Get organization camera detections history by boundary by interval"
    )
    def get_organization_camera_detections_history_by_boundary_by_interval(organization_id: str):
        """Get organization camera detections history by boundary by interval."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraDetectionsHistoryByBoundaryByInterval(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Detections History By Boundary By Interval")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Detections History By Boundary By Interval")
            else:
                return f"✅ Get organization camera detections history by boundary by interval completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_camera_onboarding_statuses",
        description="📊 Get organization camera onboarding statuses"
    )
    def get_organization_camera_onboarding_statuses(organization_id: str):
        """Get organization camera onboarding statuses."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraOnboardingStatuses(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Onboarding Statuses")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Onboarding Statuses")
            else:
                return f"✅ Get organization camera onboarding statuses completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_camera_permission",
        description="📊 Get organization camera permission"
    )
    def get_organization_camera_permission(organization_id: str):
        """Get organization camera permission."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraPermission(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Permission")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Permission")
            else:
                return f"✅ Get organization camera permission completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_camera_permissions",
        description="📊 Get organization camera permissions"
    )
    def get_organization_camera_permissions(organization_id: str):
        """Get organization camera permissions."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraPermissions(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Permissions")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Permissions")
            else:
                return f"✅ Get organization camera permissions completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_camera_role",
        description="📊 Get organization camera role"
    )
    def get_organization_camera_role(organization_id: str):
        """Get organization camera role."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraRole(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Role")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Role")
            else:
                return f"✅ Get organization camera role completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_camera_roles",
        description="📊 Get organization camera roles"
    )
    def get_organization_camera_roles(organization_id: str):
        """Get organization camera roles."""
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraRoles(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Roles")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Roles")
            else:
                return f"✅ Get organization camera roles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_camera_custom_analytics",
        description="✏️ Update device camera custom analytics"
    )
    def update_device_camera_custom_analytics(serial: str, **kwargs):
        """Update device camera custom analytics."""
        try:
            result = meraki_client.dashboard.camera.updateDeviceCameraCustomAnalytics(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Custom Analytics")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Custom Analytics")
            else:
                return f"✅ Update device camera custom analytics completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_camera_quality_and_retention",
        description="✏️ Update device camera quality and retention"
    )
    def update_device_camera_quality_and_retention(serial: str, **kwargs):
        """Update device camera quality and retention."""
        try:
            result = meraki_client.dashboard.camera.updateDeviceCameraQualityAndRetention(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Quality And Retention")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Quality And Retention")
            else:
                return f"✅ Update device camera quality and retention completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_camera_sense",
        description="✏️ Update device camera sense"
    )
    def update_device_camera_sense(serial: str, **kwargs):
        """Update device camera sense."""
        try:
            result = meraki_client.dashboard.camera.updateDeviceCameraSense(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Sense")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Sense")
            else:
                return f"✅ Update device camera sense completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_camera_wireless_profiles",
        description="✏️ Update device camera wireless profiles"
    )
    def update_device_camera_wireless_profiles(serial: str, **kwargs):
        """Update device camera wireless profiles."""
        try:
            result = meraki_client.dashboard.camera.updateDeviceCameraWirelessProfiles(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Camera Wireless Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Device Camera Wireless Profiles")
            else:
                return f"✅ Update device camera wireless profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_camera_quality_retention_profile",
        description="✏️ Update network camera quality retention profile"
    )
    def update_network_camera_quality_retention_profile(network_id: str, **kwargs):
        """Update network camera quality retention profile."""
        try:
            result = meraki_client.dashboard.camera.updateNetworkCameraQualityRetentionProfile(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Quality Retention Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Quality Retention Profile")
            else:
                return f"✅ Update network camera quality retention profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_camera_wireless_profile",
        description="✏️ Update network camera wireless profile"
    )
    def update_network_camera_wireless_profile(network_id: str, **kwargs):
        """Update network camera wireless profile."""
        try:
            result = meraki_client.dashboard.camera.updateNetworkCameraWirelessProfile(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Camera Wireless Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Camera Wireless Profile")
            else:
                return f"✅ Update network camera wireless profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_camera_onboarding_statuses",
        description="✏️ Update organization camera onboarding statuses"
    )
    def update_organization_camera_onboarding_statuses(organization_id: str, **kwargs):
        """Update organization camera onboarding statuses."""
        try:
            result = meraki_client.dashboard.camera.updateOrganizationCameraOnboardingStatuses(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Onboarding Statuses")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Onboarding Statuses")
            else:
                return f"✅ Update organization camera onboarding statuses completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_camera_role",
        description="✏️ Update organization camera role"
    )
    def update_organization_camera_role(organization_id: str, **kwargs):
        """Update organization camera role."""
        try:
            result = meraki_client.dashboard.camera.updateOrganizationCameraRole(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Camera Role")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Camera Role")
            else:
                return f"✅ Update organization camera role completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
