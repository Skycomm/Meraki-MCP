"""
Adaptive Policy management tools for Cisco Meraki MCP server.

This module provides tools for managing adaptive policy ACLs, groups, and policies.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
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
    
    # ==================== ADAPTIVE POLICY ACLS ====================
    
    @app.tool(
        name="get_org_adaptive_policy_acls",
        description="🔒 List all adaptive policy ACLs in an organization"
    )
    def get_org_adaptive_policy_acls(
        organization_id: str
    ):
        """Get all adaptive policy ACLs."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcls(
                organization_id
            )
            
            response = f"# 🔒 Adaptive Policy ACLs\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total ACLs**: {len(result)}\n\n"
                
                for acl in result:
                    response += f"## {acl.get('name', 'Unknown')}\n"
                    response += f"- **ID**: {acl.get('id', 'N/A')}\n"
                    response += f"- **Description**: {acl.get('description', 'N/A')}\n"
                    response += f"- **IP Version**: {acl.get('ipVersion', 'N/A')}\n"
                    
                    # Rules
                    rules = acl.get('rules', [])
                    if rules:
                        response += f"- **Rules**: {len(rules)}\n"
                        for i, rule in enumerate(rules[:3], 1):
                            response += f"  {i}. {rule.get('policy', 'N/A')} - "
                            response += f"{rule.get('protocol', 'any')} "
                            response += f"{rule.get('srcPort', 'any')}→{rule.get('dstPort', 'any')}\n"
                        if len(rules) > 3:
                            response += f"  ... and {len(rules)-3} more\n"
                    
                    response += f"- **Created**: {acl.get('createdAt', 'N/A')}\n"
                    response += f"- **Updated**: {acl.get('updatedAt', 'N/A')}\n\n"
            else:
                response += "*No adaptive policy ACLs found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting adaptive policy ACLs: {str(e)}"
    
    @app.tool(
        name="get_org_adaptive_policy_acl",
        description="🔒 Get details of a specific adaptive policy ACL"
    )
    def get_org_adaptive_policy_acl(
        organization_id: str,
        acl_id: str
    ):
        """Get specific adaptive policy ACL details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcl(
                organization_id, acl_id
            )
            
            response = f"# 🔒 Adaptive Policy ACL Details\n\n"
            
            if result:
                response += f"**Name**: {result.get('name', 'Unknown')}\n"
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**Description**: {result.get('description', 'N/A')}\n"
                response += f"**IP Version**: {result.get('ipVersion', 'N/A')}\n\n"
                
                # Rules
                rules = result.get('rules', [])
                if rules:
                    response += f"## Rules ({len(rules)} total)\n\n"
                    for i, rule in enumerate(rules, 1):
                        response += f"### Rule {i}\n"
                        response += f"- **Policy**: {rule.get('policy', 'N/A')}\n"
                        response += f"- **Protocol**: {rule.get('protocol', 'any')}\n"
                        response += f"- **Source Port**: {rule.get('srcPort', 'any')}\n"
                        response += f"- **Dest Port**: {rule.get('dstPort', 'any')}\n"
                        response += "\n"
                
                response += f"**Created**: {result.get('createdAt', 'N/A')}\n"
                response += f"**Updated**: {result.get('updatedAt', 'N/A')}\n"
            else:
                response += "*ACL not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting ACL: {str(e)}"
    
    @app.tool(
        name="create_org_adaptive_policy_acl",
        description="🔒➕ Create a new adaptive policy ACL"
    )
    def create_org_adaptive_policy_acl(
        organization_id: str,
        name: str,
        rules: str,
        ip_version: str = "ipv4",
        description: Optional[str] = None
    ):
        """
        Create a new adaptive policy ACL.
        
        Args:
            organization_id: Organization ID
            name: ACL name
            rules: JSON string of rules array
            ip_version: IP version (ipv4 or ipv6)
            description: ACL description
        """
        try:
            kwargs = {
                'name': name,
                'ipVersion': ip_version,
                'rules': json.loads(rules) if isinstance(rules, str) else rules
            }
            
            if description:
                kwargs['description'] = description
            
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyAcl(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created Adaptive Policy ACL\n\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**IP Version**: {ip_version}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating ACL: {str(e)}"
    
    @app.tool(
        name="update_org_adaptive_policy_acl",
        description="🔒✏️ Update an adaptive policy ACL"
    )
    def update_org_adaptive_policy_acl(
        organization_id: str,
        acl_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        rules: Optional[str] = None,
        ip_version: Optional[str] = None
    ):
        """Update an adaptive policy ACL."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if description:
                kwargs['description'] = description
            if rules:
                kwargs['rules'] = json.loads(rules) if isinstance(rules, str) else rules
            if ip_version:
                kwargs['ipVersion'] = ip_version
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyAcl(
                organization_id, acl_id, **kwargs
            )
            
            response = f"# ✅ Updated Adaptive Policy ACL\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**ID**: {acl_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating ACL: {str(e)}"
    
    @app.tool(
        name="delete_org_adaptive_policy_acl",
        description="🔒❌ Delete an adaptive policy ACL"
    )
    def delete_org_adaptive_policy_acl(
        organization_id: str,
        acl_id: str
    ):
        """Delete an adaptive policy ACL."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyAcl(
                organization_id, acl_id
            )
            
            response = f"# ✅ Deleted Adaptive Policy ACL\n\n"
            response += f"**ACL ID**: {acl_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting ACL: {str(e)}"
    
    # ==================== ADAPTIVE POLICY GROUPS ====================
    
    @app.tool(
        name="get_org_adaptive_policy_groups",
        description="👥 List all adaptive policy groups in an organization"
    )
    def get_org_adaptive_policy_groups(
        organization_id: str
    ):
        """Get all adaptive policy groups."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroups(
                organization_id
            )
            
            response = f"# 👥 Adaptive Policy Groups\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Groups**: {len(result)}\n\n"
                
                for group in result:
                    response += f"## {group.get('name', 'Unknown')}\n"
                    response += f"- **ID**: {group.get('id', 'N/A')}\n"
                    response += f"- **SGT**: {group.get('sgt', 'N/A')}\n"
                    response += f"- **Description**: {group.get('description', 'N/A')}\n"
                    
                    # Policy objects
                    policy_objects = group.get('policyObjects', [])
                    if policy_objects:
                        response += f"- **Policy Objects**: {len(policy_objects)}\n"
                    
                    response += f"- **Created**: {group.get('createdAt', 'N/A')}\n"
                    response += f"- **Updated**: {group.get('updatedAt', 'N/A')}\n\n"
            else:
                response += "*No adaptive policy groups found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting adaptive policy groups: {str(e)}"
    
    @app.tool(
        name="get_org_adaptive_policy_group",
        description="👥 Get details of a specific adaptive policy group"
    )
    def get_org_adaptive_policy_group(
        organization_id: str,
        group_id: str
    ):
        """Get specific adaptive policy group details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroup(
                organization_id, group_id
            )
            
            response = f"# 👥 Adaptive Policy Group Details\n\n"
            
            if result:
                response += f"**Name**: {result.get('name', 'Unknown')}\n"
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**SGT**: {result.get('sgt', 'N/A')}\n"
                response += f"**Description**: {result.get('description', 'N/A')}\n\n"
                
                # Policy objects
                policy_objects = result.get('policyObjects', [])
                if policy_objects:
                    response += f"## Policy Objects ({len(policy_objects)})\n\n"
                    for obj in policy_objects:
                        response += f"- **{obj.get('name', 'Unknown')}** (ID: {obj.get('id', 'N/A')})\n"
                
                response += f"\n**Created**: {result.get('createdAt', 'N/A')}\n"
                response += f"**Updated**: {result.get('updatedAt', 'N/A')}\n"
            else:
                response += "*Group not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting group: {str(e)}"
    
    @app.tool(
        name="create_org_adaptive_policy_group",
        description="👥➕ Create a new adaptive policy group"
    )
    def create_org_adaptive_policy_group(
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
            sgt: Scalable Group Tag value
            description: Group description
            policy_object_ids: Comma-separated policy object IDs
        """
        try:
            kwargs = {
                'name': name,
                'sgt': sgt
            }
            
            if description:
                kwargs['description'] = description
            if policy_object_ids:
                kwargs['policyObjectIds'] = [id.strip() for id in policy_object_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyGroup(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created Adaptive Policy Group\n\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**SGT**: {sgt}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating group: {str(e)}"
    
    @app.tool(
        name="update_org_adaptive_policy_group",
        description="👥✏️ Update an adaptive policy group"
    )
    def update_org_adaptive_policy_group(
        organization_id: str,
        group_id: str,
        name: Optional[str] = None,
        sgt: Optional[int] = None,
        description: Optional[str] = None,
        policy_object_ids: Optional[str] = None
    ):
        """Update an adaptive policy group."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if sgt is not None:
                kwargs['sgt'] = sgt
            if description:
                kwargs['description'] = description
            if policy_object_ids:
                kwargs['policyObjectIds'] = [id.strip() for id in policy_object_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyGroup(
                organization_id, group_id, **kwargs
            )
            
            response = f"# ✅ Updated Adaptive Policy Group\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**ID**: {group_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating group: {str(e)}"
    
    @app.tool(
        name="delete_org_adaptive_policy_group",
        description="👥❌ Delete an adaptive policy group"
    )
    def delete_org_adaptive_policy_group(
        organization_id: str,
        group_id: str
    ):
        """Delete an adaptive policy group."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyGroup(
                organization_id, group_id
            )
            
            response = f"# ✅ Deleted Adaptive Policy Group\n\n"
            response += f"**Group ID**: {group_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting group: {str(e)}"
    
    # ==================== ADAPTIVE POLICIES ====================
    
    @app.tool(
        name="get_org_adaptive_policy_policies",
        description="📋 List all adaptive policies in an organization"
    )
    def get_org_adaptive_policy_policies(
        organization_id: str
    ):
        """Get all adaptive policies."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicies(
                organization_id
            )
            
            response = f"# 📋 Adaptive Policies\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Policies**: {len(result)}\n\n"
                
                for policy in result:
                    response += f"## Policy {policy.get('id', 'Unknown')}\n"
                    
                    # Source and destination groups
                    src_group = policy.get('sourceGroup', {})
                    dst_group = policy.get('destinationGroup', {})
                    response += f"- **Source**: {src_group.get('name', 'Any')} (SGT: {src_group.get('sgt', 'N/A')})\n"
                    response += f"- **Destination**: {dst_group.get('name', 'Any')} (SGT: {dst_group.get('sgt', 'N/A')})\n"
                    
                    # ACLs
                    acls = policy.get('acls', [])
                    if acls:
                        response += f"- **ACLs**: {', '.join([acl.get('name', 'Unknown') for acl in acls])}\n"
                    
                    response += f"- **Last Updated**: {policy.get('lastUpdatedAt', 'N/A')}\n\n"
            else:
                response += "*No adaptive policies found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting adaptive policies: {str(e)}"
    
    @app.tool(
        name="get_org_adaptive_policy_policy",
        description="📋 Get details of a specific adaptive policy"
    )
    def get_org_adaptive_policy_policy(
        organization_id: str,
        policy_id: str
    ):
        """Get specific adaptive policy details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicy(
                organization_id, policy_id
            )
            
            response = f"# 📋 Adaptive Policy Details\n\n"
            
            if result:
                response += f"**Policy ID**: {result.get('id', 'N/A')}\n\n"
                
                # Source group
                src_group = result.get('sourceGroup', {})
                response += f"## Source Group\n"
                response += f"- **Name**: {src_group.get('name', 'Any')}\n"
                response += f"- **ID**: {src_group.get('id', 'N/A')}\n"
                response += f"- **SGT**: {src_group.get('sgt', 'N/A')}\n\n"
                
                # Destination group
                dst_group = result.get('destinationGroup', {})
                response += f"## Destination Group\n"
                response += f"- **Name**: {dst_group.get('name', 'Any')}\n"
                response += f"- **ID**: {dst_group.get('id', 'N/A')}\n"
                response += f"- **SGT**: {dst_group.get('sgt', 'N/A')}\n\n"
                
                # ACLs
                acls = result.get('acls', [])
                if acls:
                    response += f"## ACLs ({len(acls)})\n"
                    for acl in acls:
                        response += f"- **{acl.get('name', 'Unknown')}** (ID: {acl.get('id', 'N/A')})\n"
                
                response += f"\n**Last Updated**: {result.get('lastUpdatedAt', 'N/A')}\n"
            else:
                response += "*Policy not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting policy: {str(e)}"
    
    @app.tool(
        name="create_org_adaptive_policy",
        description="📋➕ Create a new adaptive policy"
    )
    def create_org_adaptive_policy(
        organization_id: str,
        source_group_id: str,
        destination_group_id: str,
        acl_ids: Optional[str] = None
    ):
        """
        Create a new adaptive policy.
        
        Args:
            organization_id: Organization ID
            source_group_id: Source group ID
            destination_group_id: Destination group ID
            acl_ids: Comma-separated ACL IDs
        """
        try:
            kwargs = {
                'sourceGroupId': source_group_id,
                'destinationGroupId': destination_group_id
            }
            
            if acl_ids:
                kwargs['aclIds'] = [id.strip() for id in acl_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyPolicy(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created Adaptive Policy\n\n"
            response += f"**Policy ID**: {result.get('id', 'N/A')}\n"
            response += f"**Source Group**: {source_group_id}\n"
            response += f"**Destination Group**: {destination_group_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating policy: {str(e)}"
    
    @app.tool(
        name="update_org_adaptive_policy",
        description="📋✏️ Update an adaptive policy"
    )
    def update_org_adaptive_policy(
        organization_id: str,
        policy_id: str,
        source_group_id: Optional[str] = None,
        destination_group_id: Optional[str] = None,
        acl_ids: Optional[str] = None
    ):
        """Update an adaptive policy."""
        try:
            kwargs = {}
            
            if source_group_id:
                kwargs['sourceGroupId'] = source_group_id
            if destination_group_id:
                kwargs['destinationGroupId'] = destination_group_id
            if acl_ids:
                kwargs['aclIds'] = [id.strip() for id in acl_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyPolicy(
                organization_id, policy_id, **kwargs
            )
            
            response = f"# ✅ Updated Adaptive Policy\n\n"
            response += f"**Policy ID**: {policy_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating policy: {str(e)}"
    
    @app.tool(
        name="delete_org_adaptive_policy",
        description="📋❌ Delete an adaptive policy"
    )
    def delete_org_adaptive_policy(
        organization_id: str,
        policy_id: str
    ):
        """Delete an adaptive policy."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyPolicy(
                organization_id, policy_id
            )
            
            response = f"# ✅ Deleted Adaptive Policy\n\n"
            response += f"**Policy ID**: {policy_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting policy: {str(e)}"
    
    # ==================== ADAPTIVE POLICY SETTINGS & OVERVIEW ====================
    
    @app.tool(
        name="get_org_adaptive_policy_overview",
        description="📊 Get adaptive policy overview for an organization"
    )
    def get_org_adaptive_policy_overview(
        organization_id: str
    ):
        """Get adaptive policy overview."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyOverview(
                organization_id
            )
            
            response = f"# 📊 Adaptive Policy Overview\n\n"
            
            if result:
                # Summary stats
                summary = result.get('summary', {})
                response += f"## Summary\n"
                response += f"- **Total Policies**: {summary.get('totalPolicies', 0)}\n"
                response += f"- **Total Groups**: {summary.get('totalGroups', 0)}\n"
                response += f"- **Total ACLs**: {summary.get('totalAcls', 0)}\n\n"
                
                # Top policies by hits
                top_policies = result.get('topPoliciesByHits', [])
                if top_policies:
                    response += f"## Top Policies by Hits\n"
                    for i, policy in enumerate(top_policies[:5], 1):
                        response += f"{i}. Policy {policy.get('id', 'N/A')} - {policy.get('hits', 0)} hits\n"
                
                response += f"\n**Last Updated**: {result.get('lastUpdatedAt', 'N/A')}\n"
            else:
                response += "*No overview data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting adaptive policy overview: {str(e)}"
    
    @app.tool(
        name="get_org_adaptive_policy_settings",
        description="⚙️ Get adaptive policy settings for an organization"
    )
    def get_org_adaptive_policy_settings(
        organization_id: str
    ):
        """Get adaptive policy settings."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicySettings(
                organization_id
            )
            
            response = f"# ⚙️ Adaptive Policy Settings\n\n"
            
            if result:
                response += f"**Enabled Networks**: {result.get('enabledNetworks', [])}\n"
                
                return response
            else:
                response += "*No settings found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting adaptive policy settings: {str(e)}"
    
    @app.tool(
        name="update_org_adaptive_policy_settings",
        description="⚙️✏️ Update adaptive policy settings for an organization"
    )
    def update_org_adaptive_policy_settings(
        organization_id: str,
        enabled_network_ids: Optional[str] = None
    ):
        """
        Update adaptive policy settings.
        
        Args:
            organization_id: Organization ID
            enabled_network_ids: Comma-separated network IDs to enable adaptive policy
        """
        try:
            kwargs = {}
            
            if enabled_network_ids:
                kwargs['enabledNetworks'] = [id.strip() for id in enabled_network_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicySettings(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Updated Adaptive Policy Settings\n\n"
            response += f"**Enabled Networks**: {result.get('enabledNetworks', [])}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating adaptive policy settings: {str(e)}"