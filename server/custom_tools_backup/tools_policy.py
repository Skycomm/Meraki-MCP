"""
Policy Objects tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_policy_tools(mcp_app, meraki):
    """
    Register policy tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all policy tools
    register_policy_tool_handlers()

def register_policy_tool_handlers():
    """Register all policy tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="get_organization_policy_objects",
        description="🛡️ List all policy objects in an organization"
    )
    def get_organization_policy_objects(org_id: str):
        """
        List all policy objects for an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of policy objects
        """
        try:
            objects = meraki_client.get_organization_policy_objects(org_id)
            
            if not objects:
                return f"No policy objects found for organization {org_id}."
                
            result = f"# 🛡️ Policy Objects - Organization {org_id}\n\n"
            result += f"**Total Objects**: {len(objects)}\n\n"
            
            # Group by category
            categories = {}
            for obj in objects:
                category = obj.get('category', 'uncategorized')
                if category not in categories:
                    categories[category] = []
                categories[category].append(obj)
            
            # Display by category
            for category, cat_objects in categories.items():
                result += f"## {category.title()} ({len(cat_objects)} objects)\n"
                
                for obj in cat_objects[:10]:
                    obj_id = obj.get('id', 'Unknown')
                    name = obj.get('name', 'Unnamed')
                    obj_type = obj.get('type', 'unknown')
                    
                    result += f"### 🔸 {name}\n"
                    result += f"- **ID**: {obj_id}\n"
                    result += f"- **Type**: {obj_type}\n"
                    
                    # Type-specific details
                    if obj_type == 'ipv4':
                        cidr = obj.get('cidr')
                        if cidr:
                            result += f"- **CIDR**: {cidr}\n"
                    elif obj_type == 'fqdn':
                        fqdn = obj.get('fqdn')
                        if fqdn:
                            result += f"- **FQDN**: {fqdn}\n"
                    elif obj_type == 'applicationCategory':
                        app_category_id = obj.get('applicationCategoryId')
                        if app_category_id:
                            result += f"- **App Category ID**: {app_category_id}\n"
                    
                    # Group associations
                    group_ids = obj.get('groupIds', [])
                    if group_ids:
                        result += f"- **Groups**: {len(group_ids)} groups\n"
                    
                    # Network associations
                    network_ids = obj.get('networkIds', [])
                    if network_ids:
                        result += f"- **Networks**: {len(network_ids)} networks\n"
                    
                    result += "\n"
                
                if len(cat_objects) > 10:
                    result += f"... and {len(cat_objects) - 10} more {category} objects\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving policy objects: {str(e)}"
    
    @app.tool(
        name="create_organization_policy_object",
        description="🛡️ Create a new policy object"
    )
    def create_organization_policy_object(org_id: str, name: str, category: str, type: str, cidr: str = None, fqdn: str = None, ip: str = None):
        """
        Create a new policy object.
        
        Args:
            org_id: Organization ID
            name: Object name
            category: Category (e.g., 'network', 'application')
            type: Type (e.g., 'ipv4', 'fqdn', 'ipv4Range')
            cidr: CIDR notation for IP objects (e.g., '10.0.0.0/24')
            fqdn: Fully qualified domain name for FQDN objects
            ip: Single IP address
            
        Returns:
            Created policy object
        """
        try:
            # Map our type names to Meraki API type names
            type_mapping = {
                'ipv4': 'cidr',
                'fqdn': 'fqdn',
                'ipv4Range': 'ipAndMask'
            }
            
            meraki_type = type_mapping.get(type, type)
            
            kwargs = {
                'name': name,
                'category': category,
                'type': meraki_type
            }
            
            # Add type-specific parameters
            if type == 'ipv4' and cidr:
                kwargs['cidr'] = cidr
            elif type == 'fqdn' and fqdn:
                kwargs['fqdn'] = fqdn
            elif type == 'ipv4' and ip:
                # Convert single IP to CIDR
                kwargs['cidr'] = f"{ip}/32"
            else:
                return f"Error: Missing required parameter for type {type}"
            
            result = meraki_client.create_organization_policy_object(org_id, **kwargs)
            
            response = f"# 🛡️ Policy Object Created\n\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**Category**: {result.get('category', category)}\n"
            response += f"**Type**: {result.get('type', type)}\n"
            
            if result.get('cidr'):
                response += f"**CIDR**: {result.get('cidr')}\n"
            if result.get('fqdn'):
                response += f"**FQDN**: {result.get('fqdn')}\n"
                
            return response
            
        except Exception as e:
            return f"Error creating policy object: {str(e)}"
    
    @app.tool(
        name="update_organization_policy_object",
        description="📝 Update an existing policy object"
    )
    def update_organization_policy_object(org_id: str, policy_object_id: str, name: str = None, cidr: str = None, fqdn: str = None):
        """
        Update an existing policy object.
        
        Args:
            org_id: Organization ID
            policy_object_id: Policy object ID
            name: New name (optional)
            cidr: New CIDR for IP objects (optional)
            fqdn: New FQDN for domain objects (optional)
            
        Returns:
            Updated policy object
        """
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if cidr:
                kwargs['cidr'] = cidr
            if fqdn:
                kwargs['fqdn'] = fqdn
                
            result = meraki_client.update_organization_policy_object(org_id, policy_object_id, **kwargs)
            
            response = f"# 📝 Policy Object Updated\n\n"
            response += f"**ID**: {policy_object_id}\n"
            response += f"**Name**: {result.get('name', 'N/A')}\n"
            
            if result.get('cidr'):
                response += f"**CIDR**: {result.get('cidr')}\n"
            if result.get('fqdn'):
                response += f"**FQDN**: {result.get('fqdn')}\n"
                
            return response
            
        except Exception as e:
            return f"Error updating policy object: {str(e)}"
    
    @app.tool(
        name="delete_organization_policy_object",
        description="🗑️ Delete a policy object"
    )
    def delete_organization_policy_object(org_id: str, policy_object_id: str):
        """
        Delete a policy object.
        
        Args:
            org_id: Organization ID
            policy_object_id: Policy object ID to delete
            
        Returns:
            Deletion confirmation
        """
        try:
            meraki_client.delete_organization_policy_object(org_id, policy_object_id)
            
            return f"# 🗑️ Policy Object Deleted\n\n**ID**: {policy_object_id}\n\n✅ Policy object successfully deleted."
            
        except Exception as e:
            return f"Error deleting policy object: {str(e)}"
    
    @app.tool(
        name="get_organization_policy_objects_groups",
        description="📁 List all policy object groups"
    )
    def get_organization_policy_objects_groups(org_id: str):
        """
        List all policy object groups for an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of policy object groups
        """
        try:
            groups = meraki_client.get_organization_policy_objects_groups(org_id)
            
            if not groups:
                return f"No policy object groups found for organization {org_id}."
                
            result = f"# 📁 Policy Object Groups - Organization {org_id}\n\n"
            result += f"**Total Groups**: {len(groups)}\n\n"
            
            for group in groups:
                group_id = group.get('id', 'Unknown')
                name = group.get('name', 'Unnamed')
                category = group.get('category', 'uncategorized')
                
                result += f"## 📂 {name}\n"
                result += f"- **ID**: {group_id}\n"
                result += f"- **Category**: {category}\n"
                
                # Object IDs in this group
                object_ids = group.get('objectIds', [])
                if object_ids:
                    result += f"- **Objects**: {len(object_ids)} objects\n"
                    # Show first few
                    for obj_id in object_ids[:5]:
                        result += f"  - {obj_id}\n"
                    if len(object_ids) > 5:
                        result += f"  - ... and {len(object_ids) - 5} more\n"
                
                # Network associations
                network_ids = group.get('networkIds', [])
                if network_ids:
                    result += f"- **Networks**: {len(network_ids)} networks\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving policy object groups: {str(e)}"
    
    @app.tool(
        name="create_organization_policy_objects_group",
        description="📁 Create a new policy object group"
    )
    def create_organization_policy_objects_group(org_id: str, name: str, category: str, object_ids: str = None):
        """
        Create a new policy object group.
        
        Args:
            org_id: Organization ID
            name: Group name
            category: Category (must match objects' category)
            object_ids: Comma-separated policy object IDs to include
            
        Returns:
            Created policy object group
        """
        try:
            kwargs = {
                'name': name,
                'category': category
            }
            
            if object_ids:
                ids_list = [id.strip() for id in object_ids.split(',')]
                kwargs['objectIds'] = ids_list
            
            result = meraki_client.create_organization_policy_objects_group(org_id, **kwargs)
            
            response = f"# 📁 Policy Object Group Created\n\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**Category**: {result.get('category', category)}\n"
            
            obj_ids = result.get('objectIds', [])
            if obj_ids:
                response += f"**Objects**: {len(obj_ids)} objects included\n"
                
            return response
            
        except Exception as e:
            return f"Error creating policy object group: {str(e)}"