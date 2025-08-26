"""
Missing organizations API implementations for 100% coverage.
Auto-generated to reach complete API parity.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_organizations_missing_tools(mcp_app, meraki):
    """
    Register missing organizations tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all missing organizations tools
    register_organizations_missing_handlers()

def register_organizations_missing_handlers():
    """Register missing organizations tool handlers."""

    @app.tool(
        name="claim_into_organization_inventory",
        description="📥 Claim devices/licenses into organization inventory"
    )
    def claim_into_organization_inventory(
        organization_id: str,
        orders: list = None,
        serials: list = None,
        licenses: list = None
    ):
        """Claim devices, licenses, and/or orders into organization inventory.
        
        Args:
            organization_id: Organization ID
            orders: List of order numbers to claim (optional)
            serials: List of device serial numbers to claim (optional)
            licenses: List of license objects to claim (optional)
                Each license: {"key": "...", "mode": "addDevices" or "renew"}
        
        Note: Same as claim_into_organization but may have different behavior.
        """
        try:
            params = {}
            if orders:
                params['orders'] = orders
            if serials:
                params['serials'] = [s.upper() for s in serials]
            if licenses:
                params['licenses'] = licenses
            
            if not params:
                return "❌ Error: Must provide orders, serials, or licenses"
            
            result = meraki_client.dashboard.organizations.claimIntoOrganizationInventory(
                organization_id, **params
            )
            
            if result is None:
                return "✅ Successfully claimed into inventory!"
            elif isinstance(result, dict):
                return f"✅ Claimed into inventory: {result}"
            elif isinstance(result, list):
                return f"✅ Claimed {len(result)} items into inventory"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error claiming into inventory: {str(e)}"

    @app.tool(
        name="combine_organization_networks",
        description="🔀 Combine multiple networks into one"
    )
    def combine_organization_networks(
        organization_id: str,
        name: str,
        networkIds: list,
        enrollmentString: str = None
    ):
        """Combine multiple networks into a single network.
        
        Args:
            organization_id: Organization ID
            name: Name of the combined network (required)
            networkIds: List of network IDs to combine (required)
            enrollmentString: Unique identifier for enrollment (optional)
        """
        try:
            params = {
                'name': name,
                'networkIds': networkIds
            }
            
            if enrollmentString:
                params['enrollmentString'] = enrollmentString
            
            result = meraki_client.dashboard.organizations.combineOrganizationNetworks(
                organization_id, **params
            )
            
            if result is None:
                return f"✅ Successfully combined {len(networkIds)} networks into '{name}'!"
            elif isinstance(result, dict):
                return f"✅ Combined networks into '{name}': {result}"
            elif isinstance(result, list):
                return f"✅ Combined result: {result}"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error combining networks: {str(e)}"

    # Commented out - duplicate of tools_organizations.py version
    # Keeping for reference of full parameter support
    '''
    @app.tool(
        name="create_organization_full",
        description="🏢 Create organization with management details (rarely used)"
    )
    def create_organization_full(
        name: str,
        management: dict = None
    ):
        """Create a new Meraki organization with optional management details.
        
        Args:
            name: Name of the organization (required)
            management: Management details (optional)
                Example: {"details": [{"name": "MSP ID", "value": "123456"}]}
        
        Note: Most users should use create_organization_network to add networks to existing orgs.
        """
        try:
            params = {'name': name}
            
            if management:
                params['management'] = management
            
            result = meraki_client.dashboard.organizations.createOrganization(**params)
            
            if result is None:
                return f"✅ Organization '{name}' created successfully!"
            elif isinstance(result, dict):
                org_id = result.get('id', 'Unknown')
                return f"✅ Organization '{name}' created successfully!\nOrganization ID: {org_id}"
            else:
                return f"✅ Organization created: {result}"
                
        except Exception as e:
            return f"Error creating organization: {str(e)}"
    '''

    @app.tool(
        name="create_organization_adaptive_policy_acl",
        description="➕ Create create organization adaptive policy acl"
    )
    def create_organization_adaptive_policy_acl(**kwargs):
        """Execute createOrganizationAdaptivePolicyAcl API call."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyAcl(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling createOrganizationAdaptivePolicyAcl: {str(e)}"

    @app.tool(
        name="create_organization_adaptive_policy_group",
        description="➕ Create create organization adaptive policy group"
    )
    def create_organization_adaptive_policy_group(**kwargs):
        """Execute createOrganizationAdaptivePolicyGroup API call."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyGroup(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling createOrganizationAdaptivePolicyGroup: {str(e)}"

    @app.tool(
        name="create_organization_adaptive_policy_policy",
        description="➕ Create create organization adaptive policy policy"
    )
    def create_organization_adaptive_policy_policy(**kwargs):
        """Execute createOrganizationAdaptivePolicyPolicy API call."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyPolicy(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling createOrganizationAdaptivePolicyPolicy: {str(e)}"

    @app.tool(
        name="create_organization_inventory_devices_swaps_bulk",
        description="➕ Create create organization inventory devices swaps bulk"
    )
    def create_organization_inventory_devices_swaps_bulk(**kwargs):
        """Execute createOrganizationInventoryDevicesSwapsBulk API call."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationInventoryDevicesSwapsBulk(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling createOrganizationInventoryDevicesSwapsBulk: {str(e)}"

    @app.tool(
        name="create_organization_policy_object",
        description="➕ Create create organization policy object"
    )
    def create_organization_policy_object(**kwargs):
        """Execute createOrganizationPolicyObject API call."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationPolicyObject(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling createOrganizationPolicyObject: {str(e)}"

    @app.tool(
        name="create_organization_policy_objects_group",
        description="➕ Create create organization policy objects group"
    )
    def create_organization_policy_objects_group(**kwargs):
        """Execute createOrganizationPolicyObjectsGroup API call."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationPolicyObjectsGroup(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling createOrganizationPolicyObjectsGroup: {str(e)}"

    @app.tool(
        name="delete_organization",
        description="🗑️ Delete delete organization"
    )
    def delete_organization(**kwargs):
        """Execute deleteOrganization API call."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganization(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling deleteOrganization: {str(e)}"

    @app.tool(
        name="delete_organization_policy_object",
        description="🗑️ Delete delete organization policy object"
    )
    def delete_organization_policy_object(**kwargs):
        """Execute deleteOrganizationPolicyObject API call."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationPolicyObject(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling deleteOrganizationPolicyObject: {str(e)}"

    @app.tool(
        name="get_organization_adaptive_policy_acls",
        description="📊 Get get organization adaptive policy acls"
    )
    def get_organization_adaptive_policy_acls(**kwargs):
        """Execute getOrganizationAdaptivePolicyAcls API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcls(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationAdaptivePolicyAcls: {str(e)}"

    @app.tool(
        name="get_organization_adaptive_policy_groups",
        description="📊 Get get organization adaptive policy groups"
    )
    def get_organization_adaptive_policy_groups(**kwargs):
        """Execute getOrganizationAdaptivePolicyGroups API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroups(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationAdaptivePolicyGroups: {str(e)}"

    @app.tool(
        name="get_organization_adaptive_policy_policies",
        description="📊 Get get organization adaptive policy policies"
    )
    def get_organization_adaptive_policy_policies(**kwargs):
        """Execute getOrganizationAdaptivePolicyPolicies API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicies(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationAdaptivePolicyPolicies: {str(e)}"

    @app.tool(
        name="get_organization_adaptive_policy_settings",
        description="📊 Get get organization adaptive policy settings"
    )
    def get_organization_adaptive_policy_settings(**kwargs):
        """Execute getOrganizationAdaptivePolicySettings API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicySettings(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationAdaptivePolicySettings: {str(e)}"

    @app.tool(
        name="get_organization_api_requests",
        description="📊 Get get organization api requests"
    )
    def get_organization_api_requests(**kwargs):
        """Execute getOrganizationApiRequests API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationApiRequests(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationApiRequests: {str(e)}"

    @app.tool(
        name="get_organization_api_requests_overview",
        description="📊 Get get organization api requests overview"
    )
    def get_organization_api_requests_overview(**kwargs):
        """Execute getOrganizationApiRequestsOverview API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationApiRequestsOverview(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationApiRequestsOverview: {str(e)}"

    @app.tool(
        name="get_organization_early_access_features",
        description="📊 Get get organization early access features"
    )
    def get_organization_early_access_features(**kwargs):
        """Execute getOrganizationEarlyAccessFeatures API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeatures(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationEarlyAccessFeatures: {str(e)}"

    @app.tool(
        name="get_organization_inventory_device",
        description="📊 Get get organization inventory device"
    )
    def get_organization_inventory_device(**kwargs):
        """Execute getOrganizationInventoryDevice API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevice(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationInventoryDevice: {str(e)}"

    @app.tool(
        name="get_organization_inventory_devices",
        description="📊 Get get organization inventory devices"
    )
    def get_organization_inventory_devices(**kwargs):
        """Execute getOrganizationInventoryDevices API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevices(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationInventoryDevices: {str(e)}"

    @app.tool(
        name="get_organization_networks",
        description="📊 Get get organization networks"
    )
    def get_organization_networks(**kwargs):
        """Execute getOrganizationNetworks API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationNetworks(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationNetworks: {str(e)}"

    @app.tool(
        name="get_organization_policy_objects",
        description="📊 Get get organization policy objects"
    )
    def get_organization_policy_objects(**kwargs):
        """Execute getOrganizationPolicyObjects API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationPolicyObjects(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationPolicyObjects: {str(e)}"

    @app.tool(
        name="get_organization_policy_objects_groups",
        description="📊 Get get organization policy objects groups"
    )
    def get_organization_policy_objects_groups(**kwargs):
        """Execute getOrganizationPolicyObjectsGroups API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationPolicyObjectsGroups(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationPolicyObjectsGroups: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_appliances_by_utilization",
        description="📊 Get get organization summary top appliances by utilization"
    )
    def get_organization_summary_top_appliances_by_utilization(**kwargs):
        """Execute getOrganizationSummaryTopAppliancesByUtilization API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopAppliancesByUtilization(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationSummaryTopAppliancesByUtilization: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_applications_by_usage",
        description="📊 Get get organization summary top applications by usage"
    )
    def get_organization_summary_top_applications_by_usage(**kwargs):
        """Execute getOrganizationSummaryTopApplicationsByUsage API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopApplicationsByUsage(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationSummaryTopApplicationsByUsage: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_clients_by_usage",
        description="📊 Get get organization summary top clients by usage"
    )
    def get_organization_summary_top_clients_by_usage(**kwargs):
        """Execute getOrganizationSummaryTopClientsByUsage API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopClientsByUsage(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationSummaryTopClientsByUsage: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_devices_by_usage",
        description="📊 Get get organization summary top devices by usage"
    )
    def get_organization_summary_top_devices_by_usage(**kwargs):
        """Execute getOrganizationSummaryTopDevicesByUsage API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopDevicesByUsage(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationSummaryTopDevicesByUsage: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_ssids_by_usage",
        description="📊 Get get organization summary top ssids by usage"
    )
    def get_organization_summary_top_ssids_by_usage(**kwargs):
        """Execute getOrganizationSummaryTopSsidsByUsage API call."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopSsidsByUsage(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling getOrganizationSummaryTopSsidsByUsage: {str(e)}"

    @app.tool(
        name="move_organization_licenses",
        description="⚡ Execute move organization licenses"
    )
    def move_organization_licenses(**kwargs):
        """Execute moveOrganizationLicenses API call."""
        try:
            result = meraki_client.dashboard.organizations.moveOrganizationLicenses(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling moveOrganizationLicenses: {str(e)}"

    @app.tool(
        name="release_from_organization_inventory",
        description="⚡ Execute release from organization inventory"
    )
    def release_from_organization_inventory(**kwargs):
        """Execute releaseFromOrganizationInventory API call."""
        try:
            result = meraki_client.dashboard.organizations.releaseFromOrganizationInventory(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling releaseFromOrganizationInventory: {str(e)}"

    @app.tool(
        name="renew_organization_licenses_seats",
        description="⚡ Execute renew organization licenses seats"
    )
    def renew_organization_licenses_seats(**kwargs):
        """Execute renewOrganizationLicensesSeats API call."""
        try:
            result = meraki_client.dashboard.organizations.renewOrganizationLicensesSeats(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling renewOrganizationLicensesSeats: {str(e)}"

    @app.tool(
        name="update_organization",
        description="✏️ Update update organization"
    )
    def update_organization(**kwargs):
        """Execute updateOrganization API call."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganization(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling updateOrganization: {str(e)}"

    @app.tool(
        name="update_organization_license",
        description="✏️ Update update organization license"
    )
    def update_organization_license(**kwargs):
        """Execute updateOrganizationLicense API call."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationLicense(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling updateOrganizationLicense: {str(e)}"

    @app.tool(
        name="update_organization_policy_object",
        description="✏️ Update update organization policy object"
    )
    def update_organization_policy_object(**kwargs):
        """Execute updateOrganizationPolicyObject API call."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationPolicyObject(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {result}"
            elif isinstance(result, list):
                return f"✅ Found {len(result)} items"
            else:
                return f"✅ Result: {result}"
                
        except Exception as e:
            return f"Error calling updateOrganizationPolicyObject: {str(e)}"
