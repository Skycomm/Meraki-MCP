"""
Adaptive Policy tools for the Cisco Meraki MCP Server.
Provides comprehensive management of adaptive policies, ACLs, and policy groups.
"""

from typing import Optional, List, Dict, Any
import json

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_adaptive_policy_tools(mcp_app, meraki):
    """
    Register adaptive policy tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all adaptive policy tools
    register_adaptive_policy_tool_handlers()

def register_adaptive_policy_tool_handlers():
    """Register all adaptive policy tool handlers."""
    
    # ========== ADAPTIVE POLICY SETTINGS ==========
    @app.tool(
        name="get_organization_adaptive_policy_settings",
        description="⚙️ Get adaptive policy settings for an organization"
    )
    def get_organization_adaptive_policy_settings(organization_id: str):
        """
        Get adaptive policy settings for an organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Adaptive policy settings
        """
        try:
            settings = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicySettings(organization_id)
            
            result = f"# ⚙️ Adaptive Policy Settings\n\n"
            result += f"**Enabled Networks**: {settings.get('enabledNetworks', [])}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving adaptive policy settings: {str(e)}"
    
    @app.tool(
        name="update_organization_adaptive_policy_settings",
        description="⚙️ Update adaptive policy settings for an organization"
    )
    def update_organization_adaptive_policy_settings(
        organization_id: str,
        enabled_networks: str
    ):
        """
        Update adaptive policy settings for an organization.
        
        Args:
            organization_id: Organization ID
            enabled_networks: JSON array of network IDs
            
        Returns:
            Updated settings
        """
        try:
            networks = json.loads(enabled_networks)
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicySettings(
                organization_id,
                enabledNetworks=networks
            )
            
            return f"✅ Adaptive policy enabled for {len(networks)} networks"
            
        except Exception as e:
            return f"Error updating adaptive policy settings: {str(e)}"
    
    # ========== ADAPTIVE POLICY ACLS ==========
    @app.tool(
        name="get_organization_adaptive_policy_acls",
        description="📋 Get adaptive policy ACLs for an organization"
    )
    def get_organization_adaptive_policy_acls(organization_id: str):
        """
        Get adaptive policy ACLs for an organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            List of adaptive policy ACLs
        """
        try:
            acls = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcls(organization_id)
            
            if not acls:
                return "No adaptive policy ACLs configured"
                
            result = f"# 📋 Adaptive Policy ACLs\n\n"
            
            for acl in acls:
                result += f"## {acl.get('name', 'Unnamed')}\n"
                result += f"- **ID**: `{acl.get('id')}`\n"
                result += f"- **Description**: {acl.get('description', 'N/A')}\n"
                result += f"- **IP Version**: {acl.get('ipVersion', 'any')}\n"
                
                if acl.get('rules'):
                    result += f"- **Rules**: {len(acl.get('rules', []))} configured\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving adaptive policy ACLs: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_acl",
        description="📋 Get a specific adaptive policy ACL"
    )
    def get_organization_adaptive_policy_acl(
        organization_id: str,
        acl_id: str
    ):
        """
        Get a specific adaptive policy ACL.
        
        Args:
            organization_id: Organization ID
            acl_id: ACL ID
            
        Returns:
            ACL details with rules
        """
        try:
            acl = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcl(
                organization_id, acl_id
            )
            
            result = f"# 📋 ACL: {acl.get('name', 'Unnamed')}\n\n"
            result += f"- **ID**: `{acl.get('id')}`\n"
            result += f"- **Description**: {acl.get('description', 'N/A')}\n"
            result += f"- **IP Version**: {acl.get('ipVersion', 'any')}\n\n"
            
            if acl.get('rules'):
                result += f"## Rules ({len(acl.get('rules', []))})\n\n"
                for idx, rule in enumerate(acl.get('rules', []), 1):
                    result += f"### Rule {idx}\n"
                    result += f"- **Policy**: {rule.get('policy', 'allow')}\n"
                    result += f"- **Protocol**: {rule.get('protocol', 'any')}\n"
                    result += f"- **Source Port**: {rule.get('srcPort', 'any')}\n"
                    result += f"- **Destination Port**: {rule.get('dstPort', 'any')}\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving ACL: {str(e)}"
    
    @app.tool(
        name="create_organization_adaptive_policy_acl",
        description="📋 Create a new adaptive policy ACL"
    )
    def create_organization_adaptive_policy_acl(
        organization_id: str,
        name: str,
        rules: str,
        description: Optional[str] = None,
        ip_version: Optional[str] = "any"
    ):
        """
        Create a new adaptive policy ACL.
        
        Args:
            organization_id: Organization ID
            name: ACL name
            rules: JSON array of rule objects
            description: ACL description
            ip_version: IP version (any, ipv4, ipv6)
            
        Returns:
            Created ACL details
        """
        try:
            rules_list = json.loads(rules)
            
            kwargs = {
                'name': name,
                'rules': rules_list,
                'ipVersion': ip_version
            }
            
            if description:
                kwargs['description'] = description
                
            acl = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyAcl(
                organization_id, **kwargs
            )
            
            return f"✅ Created ACL '{name}' with ID: {acl.get('id')}"
            
        except Exception as e:
            return f"Error creating ACL: {str(e)}"
    
    @app.tool(
        name="update_organization_adaptive_policy_acl",
        description="📋 Update an adaptive policy ACL"
    )
    def update_organization_adaptive_policy_acl(
        organization_id: str,
        acl_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        rules: Optional[str] = None,
        ip_version: Optional[str] = None
    ):
        """
        Update an adaptive policy ACL.
        
        Args:
            organization_id: Organization ID
            acl_id: ACL ID
            name: ACL name
            description: ACL description
            rules: JSON array of rule objects
            ip_version: IP version
            
        Returns:
            Updated ACL details
        """
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if description:
                kwargs['description'] = description
            if rules:
                kwargs['rules'] = json.loads(rules)
            if ip_version:
                kwargs['ipVersion'] = ip_version
                
            acl = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyAcl(
                organization_id, acl_id, **kwargs
            )
            
            return "✅ ACL updated successfully"
            
        except Exception as e:
            return f"Error updating ACL: {str(e)}"
    
    @app.tool(
        name="delete_organization_adaptive_policy_acl",
        description="🗑️ Delete an adaptive policy ACL - REQUIRES CONFIRMATION"
    )
    def delete_organization_adaptive_policy_acl(
        organization_id: str,
        acl_id: str,
        confirmed: bool = False
    ):
        """
        Delete an adaptive policy ACL.
        
        ⚠️ WARNING: This will permanently delete the ACL!
        
        Args:
            organization_id: Organization ID
            acl_id: ACL ID to delete
            confirmed: Must be True to execute this operation
            
        Returns:
            Deletion status
        """
        if not confirmed:
            return "⚠️ ACL deletion requires confirmation. Set confirmed=true to proceed."
            
        try:
            meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyAcl(
                organization_id, acl_id
            )
            return f"✅ ACL {acl_id} deleted successfully"
            
        except Exception as e:
            return f"Error deleting ACL: {str(e)}"
    
    # ========== ADAPTIVE POLICY GROUPS ==========
    @app.tool(
        name="get_organization_adaptive_policy_groups",
        description="👥 Get adaptive policy groups for an organization"
    )
    def get_organization_adaptive_policy_groups(organization_id: str):
        """
        Get adaptive policy groups for an organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            List of policy groups
        """
        try:
            groups = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroups(organization_id)
            
            if not groups:
                return "No adaptive policy groups configured"
                
            result = f"# 👥 Adaptive Policy Groups\n\n"
            
            for group in groups:
                result += f"## {group.get('name', 'Unnamed')}\n"
                result += f"- **ID**: `{group.get('groupId')}`\n"
                result += f"- **SGT**: {group.get('sgt', 'N/A')}\n"
                result += f"- **Description**: {group.get('description', 'N/A')}\n"
                
                if group.get('policyObjects'):
                    result += f"- **Policy Objects**: {len(group.get('policyObjects', []))}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving policy groups: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_group",
        description="👥 Get a specific adaptive policy group"
    )
    def get_organization_adaptive_policy_group(
        organization_id: str,
        group_id: str
    ):
        """
        Get a specific adaptive policy group.
        
        Args:
            organization_id: Organization ID
            group_id: Group ID
            
        Returns:
            Policy group details
        """
        try:
            group = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroup(
                organization_id, group_id
            )
            
            result = f"# 👥 Policy Group: {group.get('name', 'Unnamed')}\n\n"
            result += f"- **ID**: `{group.get('groupId')}`\n"
            result += f"- **SGT**: {group.get('sgt', 'N/A')}\n"
            result += f"- **Description**: {group.get('description', 'N/A')}\n\n"
            
            if group.get('policyObjects'):
                result += f"## Policy Objects\n"
                for obj in group.get('policyObjects', []):
                    result += f"- **{obj.get('name', 'Unnamed')}**\n"
                    result += f"  - ID: {obj.get('id')}\n"
                    result += f"  - Type: {obj.get('objectType')}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving policy group: {str(e)}"
    
    @app.tool(
        name="create_organization_adaptive_policy_group",
        description="👥 Create a new adaptive policy group"
    )
    def create_organization_adaptive_policy_group(
        organization_id: str,
        name: str,
        sgt: int,
        description: Optional[str] = None,
        policy_object_ids: Optional[str] = None
    ):
        """
        Create a new adaptive policy group.
        
        Args:
            organization_id: Organization ID
            name: Group name
            sgt: Security Group Tag value
            description: Group description
            policy_object_ids: JSON array of policy object IDs
            
        Returns:
            Created group details
        """
        try:
            kwargs = {
                'name': name,
                'sgt': sgt
            }
            
            if description:
                kwargs['description'] = description
            if policy_object_ids:
                kwargs['policyObjectIds'] = json.loads(policy_object_ids)
                
            group = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyGroup(
                organization_id, **kwargs
            )
            
            return f"✅ Created policy group '{name}' with SGT: {sgt}"
            
        except Exception as e:
            return f"Error creating policy group: {str(e)}"
    
    @app.tool(
        name="update_organization_adaptive_policy_group",
        description="👥 Update an adaptive policy group"
    )
    def update_organization_adaptive_policy_group(
        organization_id: str,
        group_id: str,
        name: Optional[str] = None,
        sgt: Optional[int] = None,
        description: Optional[str] = None,
        policy_object_ids: Optional[str] = None
    ):
        """
        Update an adaptive policy group.
        
        Args:
            organization_id: Organization ID
            group_id: Group ID
            name: Group name
            sgt: Security Group Tag value
            description: Group description
            policy_object_ids: JSON array of policy object IDs
            
        Returns:
            Updated group details
        """
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if sgt:
                kwargs['sgt'] = sgt
            if description:
                kwargs['description'] = description
            if policy_object_ids:
                kwargs['policyObjectIds'] = json.loads(policy_object_ids)
                
            group = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyGroup(
                organization_id, group_id, **kwargs
            )
            
            return "✅ Policy group updated successfully"
            
        except Exception as e:
            return f"Error updating policy group: {str(e)}"
    
    @app.tool(
        name="delete_organization_adaptive_policy_group",
        description="🗑️ Delete an adaptive policy group - REQUIRES CONFIRMATION"
    )
    def delete_organization_adaptive_policy_group(
        organization_id: str,
        group_id: str,
        confirmed: bool = False
    ):
        """
        Delete an adaptive policy group.
        
        ⚠️ WARNING: This will permanently delete the policy group!
        
        Args:
            organization_id: Organization ID
            group_id: Group ID to delete
            confirmed: Must be True to execute this operation
            
        Returns:
            Deletion status
        """
        if not confirmed:
            return "⚠️ Policy group deletion requires confirmation. Set confirmed=true to proceed."
            
        try:
            meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyGroup(
                organization_id, group_id
            )
            return f"✅ Policy group {group_id} deleted successfully"
            
        except Exception as e:
            return f"Error deleting policy group: {str(e)}"
    
    # ========== ADAPTIVE POLICY POLICIES ==========
    @app.tool(
        name="get_organization_adaptive_policy_policies",
        description="📜 Get adaptive policies for an organization"
    )
    def get_organization_adaptive_policy_policies(organization_id: str):
        """
        Get adaptive policies for an organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            List of adaptive policies
        """
        try:
            policies = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicies(organization_id)
            
            if not policies:
                return "No adaptive policies configured"
                
            result = f"# 📜 Adaptive Policies\n\n"
            
            for policy in policies:
                result += f"## Policy ID: {policy.get('adaptivePolicyId')}\n"
                
                if policy.get('sourceGroup'):
                    src = policy['sourceGroup']
                    result += f"- **Source**: {src.get('name')} (SGT: {src.get('sgt')})\n"
                    
                if policy.get('destinationGroup'):
                    dst = policy['destinationGroup']
                    result += f"- **Destination**: {dst.get('name')} (SGT: {dst.get('sgt')})\n"
                    
                if policy.get('acls'):
                    result += f"- **ACLs**: {len(policy.get('acls', []))} configured\n"
                    for acl in policy.get('acls', []):
                        result += f"  - {acl.get('name')} (ID: {acl.get('id')})\n"
                        
                result += f"- **Last Updated**: {policy.get('lastUpdatedAt', 'N/A')}\n\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving adaptive policies: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_policy",
        description="📜 Get a specific adaptive policy"
    )
    def get_organization_adaptive_policy_policy(
        organization_id: str,
        policy_id: str
    ):
        """
        Get a specific adaptive policy.
        
        Args:
            organization_id: Organization ID
            policy_id: Policy ID
            
        Returns:
            Policy details
        """
        try:
            policy = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicy(
                organization_id, policy_id
            )
            
            result = f"# 📜 Adaptive Policy Details\n\n"
            result += f"**Policy ID**: {policy.get('adaptivePolicyId')}\n\n"
            
            if policy.get('sourceGroup'):
                src = policy['sourceGroup']
                result += f"## Source Group\n"
                result += f"- **Name**: {src.get('name')}\n"
                result += f"- **SGT**: {src.get('sgt')}\n"
                result += f"- **ID**: {src.get('id')}\n\n"
                
            if policy.get('destinationGroup'):
                dst = policy['destinationGroup']
                result += f"## Destination Group\n"
                result += f"- **Name**: {dst.get('name')}\n"
                result += f"- **SGT**: {dst.get('sgt')}\n"
                result += f"- **ID**: {dst.get('id')}\n\n"
                
            if policy.get('acls'):
                result += f"## ACLs ({len(policy.get('acls', []))})\n"
                for acl in policy.get('acls', []):
                    result += f"- **{acl.get('name')}**\n"
                    result += f"  - ID: {acl.get('id')}\n"
                    
            result += f"\n**Last Updated**: {policy.get('lastUpdatedAt', 'N/A')}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving policy: {str(e)}"
    
    @app.tool(
        name="create_organization_adaptive_policy_policy",
        description="📜 Create a new adaptive policy"
    )
    def create_organization_adaptive_policy_policy(
        organization_id: str,
        source_group_id: str,
        destination_group_id: str,
        acl_ids: Optional[str] = None
    ):
        """
        Create a new adaptive policy.
        
        Args:
            organization_id: Organization ID
            source_group_id: Source policy group ID
            destination_group_id: Destination policy group ID
            acl_ids: JSON array of ACL IDs
            
        Returns:
            Created policy details
        """
        try:
            kwargs = {
                'sourceGroupId': source_group_id,
                'destinationGroupId': destination_group_id
            }
            
            if acl_ids:
                kwargs['aclIds'] = json.loads(acl_ids)
                
            policy = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyPolicy(
                organization_id, **kwargs
            )
            
            return f"✅ Created adaptive policy with ID: {policy.get('adaptivePolicyId')}"
            
        except Exception as e:
            return f"Error creating policy: {str(e)}"
    
    @app.tool(
        name="update_organization_adaptive_policy_policy",
        description="📜 Update an adaptive policy"
    )
    def update_organization_adaptive_policy_policy(
        organization_id: str,
        policy_id: str,
        source_group_id: Optional[str] = None,
        destination_group_id: Optional[str] = None,
        acl_ids: Optional[str] = None
    ):
        """
        Update an adaptive policy.
        
        Args:
            organization_id: Organization ID
            policy_id: Policy ID
            source_group_id: Source policy group ID
            destination_group_id: Destination policy group ID
            acl_ids: JSON array of ACL IDs
            
        Returns:
            Updated policy details
        """
        try:
            kwargs = {}
            
            if source_group_id:
                kwargs['sourceGroupId'] = source_group_id
            if destination_group_id:
                kwargs['destinationGroupId'] = destination_group_id
            if acl_ids:
                kwargs['aclIds'] = json.loads(acl_ids)
                
            policy = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyPolicy(
                organization_id, policy_id, **kwargs
            )
            
            return "✅ Adaptive policy updated successfully"
            
        except Exception as e:
            return f"Error updating policy: {str(e)}"
    
    @app.tool(
        name="delete_organization_adaptive_policy_policy",
        description="🗑️ Delete an adaptive policy - REQUIRES CONFIRMATION"
    )
    def delete_organization_adaptive_policy_policy(
        organization_id: str,
        policy_id: str,
        confirmed: bool = False
    ):
        """
        Delete an adaptive policy.
        
        ⚠️ WARNING: This will permanently delete the policy!
        
        Args:
            organization_id: Organization ID
            policy_id: Policy ID to delete
            confirmed: Must be True to execute this operation
            
        Returns:
            Deletion status
        """
        if not confirmed:
            return "⚠️ Policy deletion requires confirmation. Set confirmed=true to proceed."
            
        try:
            meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyPolicy(
                organization_id, policy_id
            )
            return f"✅ Adaptive policy {policy_id} deleted successfully"
            
        except Exception as e:
            return f"Error deleting policy: {str(e)}"