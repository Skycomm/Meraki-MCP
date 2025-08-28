"""
Missing organizations API implementations for 100% coverage.
Auto-generated to reach complete API parity.
"""

from typing import Any

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
        orders: Any = None,
        serials: Any = None,
        licenses: Any = None
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
        import json
        
        try:
            params = {}
            
            # Handle orders - MCP may pass as JSON string
            if orders:
                if isinstance(orders, str):
                    if orders.startswith('['):
                        try:
                            orders = json.loads(orders)
                        except:
                            orders = [o.strip() for o in orders.split(',')]
                    else:
                        orders = [o.strip() for o in orders.split(',')]
                elif not isinstance(orders, list):
                    orders = [orders]
                params['orders'] = orders
                
            # Handle serials - MCP may pass as JSON string
            if serials:
                if isinstance(serials, str):
                    if serials.startswith('['):
                        try:
                            serials = json.loads(serials)
                        except:
                            serials = [s.strip().upper() for s in serials.split(',')]
                    else:
                        serials = [s.strip().upper() for s in serials.split(',')]
                elif not isinstance(serials, list):
                    serials = [serials]
                params['serials'] = [s.upper() for s in serials]
                
            # Handle licenses - MCP may pass as JSON string
            if licenses:
                if isinstance(licenses, str):
                    try:
                        licenses = json.loads(licenses)
                    except:
                        pass
                params['licenses'] = licenses
            
            if not params:
                return "❌ Error: Must provide orders, serials, or licenses"
            
            result = meraki_client.dashboard.organizations.claimIntoOrganizationInventory(
                organization_id, **params
            )
            
            # Provide detailed success message
            msg = "✅ Successfully claimed into inventory!"
            if serials and params.get('serials'):
                msg += f"\n- Devices: {', '.join(params['serials'])}"
            if orders and params.get('orders'):
                msg += f"\n- Orders: {', '.join(params['orders'])}"
            if result and isinstance(result, dict):
                msg += f"\n- Details: {result}"
                
            return msg
                
        except Exception as e:
            error_str = str(e)
            
            # Parse and improve error messages
            if 'Device' in error_str and 'not found' in error_str:
                # Extract device serial from error
                import re
                match = re.search(r'Device ([A-Z0-9-]+) not found', error_str)
                if match:
                    serial = match.group(1)
                    return f"""❌ Cannot claim device {serial}
                    
Possible reasons:
1. Device is already claimed in another organization
   - Check: The website may show "already in use" error
   - Solution: Release from current org first
   
2. Invalid serial number
   - Verify serial is correct (format: XXXX-XXXX-XXXX)
   - Check device label for correct serial
   
3. Device not activated
   - Device may need to be registered with Meraki first
   - Contact Meraki support if device is new

Original error: {error_str}"""
                    
            elif 'already in use' in error_str.lower() or 'already claimed' in error_str.lower():
                return f"""❌ Device(s) already claimed in another organization
                
To claim these devices:
1. Find current organization using device search
2. Release devices from that organization
3. Then claim into this organization

Original error: {error_str}"""
                
            elif 'Invalid' in error_str:
                return f"""❌ Invalid input format
                
Check:
- Serial format: XXXX-XXXX-XXXX (with dashes)
- Order numbers are correct
- License keys are valid

Original error: {error_str}"""
                
            else:
                # Generic error with helpful context
                return f"""❌ Failed to claim into inventory
                
Error: {error_str}

Troubleshooting:
- Verify devices are not already in another org
- Check serial numbers are correct
- Ensure you have permission to claim devices
- Try using order number instead of serials"""

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
        description="➕ Create adaptive policy ACL - REQUIRES: name, rules"
    )
    def create_organization_adaptive_policy_acl(
        organization_id: str,
        name: str,
        rules: list,
        **kwargs
    ):
        """Execute createOrganizationAdaptivePolicyAcl API call."""
        try:
            params = {
                'name': name,
                'rules': rules
            }
            params.update(kwargs)
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyAcl(
                organization_id,
                **params
            )
            
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
        description="➕ Create adaptive policy group - REQUIRES: name, sgt (3-65519)"
    )
    def create_organization_adaptive_policy_group(
        organization_id: str,
        name: str,
        sgt: int,
        **kwargs
    ):
        """Execute createOrganizationAdaptivePolicyGroup API call."""
        try:
            if sgt < 3 or sgt > 65519:
                return "❌ Error: sgt must be between 3 and 65519"
            params = {
                'name': name,
                'sgt': sgt
            }
            params.update(kwargs)
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyGroup(
                organization_id,
                **params
            )
            
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
        description="➕ Create adaptive policy - REQUIRES: sourceGroup, destinationGroup"
    )
    def create_organization_adaptive_policy_policy(
        organization_id: str,
        sourceGroup: dict,
        destinationGroup: dict,
        **kwargs
    ):
        """Execute createOrganizationAdaptivePolicyPolicy API call."""
        try:
            params = {
                'sourceGroup': sourceGroup,
                'destinationGroup': destinationGroup
            }
            params.update(kwargs)
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyPolicy(
                organization_id,
                **params
            )
            
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
        description="➕ Create policy object - REQUIRES: name, category, type (+ cidr/fqdn/ip&mask)"
    )
    def create_organization_policy_object(
        organization_id: str,
        name: str,
        category: str,
        type: str,
        **kwargs
    ):
        """Execute createOrganizationPolicyObject API call.
        
        Args:
            organization_id: Organization ID
            name: Name of the policy object
            category: Category ('adaptivePolicy' or 'network')
            type: Type ('adaptivePolicyIpv4Cidr', 'cidr', 'fqdn', or 'ipAndMask')
            **kwargs: Additional params like cidr, fqdn, ip, mask based on type
        """
        try:
            params = {
                'name': name,
                'category': category,
                'type': type
            }
            params.update(kwargs)
            result = meraki_client.dashboard.organizations.createOrganizationPolicyObject(
                organization_id,
                **params
            )
            
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
        description="➕ Create policy objects group - REQUIRES: name, category"
    )
    def create_organization_policy_objects_group(
        organization_id: str,
        name: str,
        category: str,
        **kwargs
    ):
        """Execute createOrganizationPolicyObjectsGroup API call.
        
        Args:
            organization_id: Organization ID
            name: Name of the policy objects group
            category: Category (NetworkObjectGroup/GeoLocationGroup/PortObjectGroup/ApplicationGroup)
            **kwargs: Additional params like objectIds, networkIds
        """
        try:
            params = {
                'name': name,
                'category': category
            }
            params.update(kwargs)
            result = meraki_client.dashboard.organizations.createOrganizationPolicyObjectsGroup(
                organization_id,
                **params
            )
            
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
        description="⚡ Release devices from organization inventory - REQUIRES: organization_id, serials (list)"
    )
    def release_from_organization_inventory(
        organization_id: str,
        serials: Any,
        **kwargs
    ):
        """Execute releaseFromOrganizationInventory API call to unclaim devices."""
        import json
        
        try:
            # Handle serials parameter - MCP may pass as JSON string
            if isinstance(serials, str):
                # Check if it's a JSON string
                if serials.startswith('['):
                    try:
                        serials = json.loads(serials)
                    except:
                        # If not JSON, assume comma-separated
                        serials = [s.strip() for s in serials.split(',')]
                else:
                    # Single serial or comma-separated
                    serials = [s.strip() for s in serials.split(',')]
            elif not isinstance(serials, list):
                # Convert single serial to list
                serials = [serials]
            
            result = meraki_client.dashboard.organizations.releaseFromOrganizationInventory(
                organizationId=organization_id,
                serials=serials,
                **kwargs
            )
            
            if result is None:
                return f"✅ Successfully released {len(serials)} device(s) from organization inventory"
            elif isinstance(result, dict):
                released = result.get('serials', [])
                if released:
                    return f"✅ Successfully released devices: {', '.join(released)}"
                return f"✅ Result: {result}"
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
