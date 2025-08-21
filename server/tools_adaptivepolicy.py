"""
Adaptive Policy Tools for Cisco Meraki MCP Server
Manage adaptive policies, ACLs, and policy groups for dynamic network segmentation
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


def get_organization_adaptive_policy_acls(org_id: str) -> str:
    """
    🔒 Get adaptive policy ACLs.
    
    Lists Access Control Lists for adaptive policy enforcement.
    
    Args:
        org_id: Organization ID
    
    Returns:
        List of adaptive policy ACLs
    """
    try:
        with safe_api_call("get adaptive policy ACLs"):
            acls = meraki.dashboard.organizations.getOrganizationAdaptivePolicyAcls(org_id)
            
            output = ["🔒 Adaptive Policy ACLs", "=" * 50, ""]
            
            if not acls:
                output.append("No adaptive policy ACLs configured")
                output.append("\n💡 Use create_organization_adaptive_policy_acl() to add")
                return "\n".join(output)
            
            output.append(f"Total ACLs: {len(acls)}")
            output.append("")
            
            # Show each ACL
            for i, acl in enumerate(acls, 1):
                acl_id = acl.get('aclId', 'Unknown')
                name = acl.get('name', 'Unnamed ACL')
                description = acl.get('description', '')
                
                output.append(f"{i}. 📋 {name}")
                output.append(f"   ID: {acl_id}")
                if description:
                    output.append(f"   Description: {description}")
                
                # IP version
                ip_version = acl.get('ipVersion', 'any')
                output.append(f"   IP Version: {ip_version}")
                
                # Rules
                rules = acl.get('rules', [])
                if rules:
                    output.append(f"   Rules: {len(rules)}")
                    
                    # Show first few rules
                    for j, rule in enumerate(rules[:3], 1):
                        policy = rule.get('policy', 'allow')
                        protocol = rule.get('protocol', 'any')
                        
                        policy_icon = '✅' if policy == 'allow' else '🚫'
                        output.append(f"      {j}. {policy_icon} {protocol.upper()}")
                        
                        # Source
                        src_port = rule.get('srcPort', 'any')
                        if src_port != 'any':
                            output.append(f"         Source Port: {src_port}")
                        
                        # Destination
                        dst_port = rule.get('dstPort', 'any')
                        if dst_port != 'any':
                            output.append(f"         Dest Port: {dst_port}")
                    
                    if len(rules) > 3:
                        output.append(f"      ... and {len(rules) - 3} more rules")
                
                output.append("")
            
            # ACL usage
            output.append("💡 ACL Usage:")
            output.append("• Apply to adaptive policy rules")
            output.append("• Control traffic between groups")
            output.append("• Enforce microsegmentation")
            output.append("• Support Zero Trust model")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get adaptive policy ACLs", e)


def create_organization_adaptive_policy_acl(
    org_id: str,
    name: str,
    rules: List[Dict[str, Any]],
    description: Optional[str] = None,
    ip_version: str = "any"
) -> str:
    """
    ➕ Create adaptive policy ACL.
    
    Define access control rules for adaptive policies.
    
    Args:
        org_id: Organization ID
        name: ACL name
        rules: List of ACL rules
        description: ACL description
        ip_version: IP version (any, ipv4, ipv6)
    
    Returns:
        Created ACL details
    """
    try:
        with safe_api_call("create adaptive policy ACL"):
            # Build ACL data
            acl_data = {
                "name": name,
                "rules": rules,
                "ipVersion": ip_version
            }
            
            if description:
                acl_data["description"] = description
            
            # Create the ACL
            acl = meraki.dashboard.organizations.createOrganizationAdaptivePolicyAcl(
                org_id,
                **acl_data
            )
            
            output = ["✅ Adaptive Policy ACL Created", "=" * 50, ""]
            output.append(f"Name: {acl.get('name', name)}")
            output.append(f"ID: {acl.get('aclId', 'N/A')}")
            if description:
                output.append(f"Description: {description}")
            output.append(f"IP Version: {acl.get('ipVersion', ip_version)}")
            output.append("")
            
            # Show rules
            created_rules = acl.get('rules', [])
            output.append(f"📋 Rules ({len(created_rules)}):")
            
            for i, rule in enumerate(created_rules, 1):
                policy = rule.get('policy', 'allow')
                protocol = rule.get('protocol', 'any')
                
                policy_icon = '✅' if policy == 'allow' else '🚫'
                output.append(f"   {i}. {policy_icon} {protocol.upper()}")
                
                if rule.get('srcPort') and rule['srcPort'] != 'any':
                    output.append(f"      Src Port: {rule['srcPort']}")
                if rule.get('dstPort') and rule['dstPort'] != 'any':
                    output.append(f"      Dst Port: {rule['dstPort']}")
            
            output.append("\n🚀 Next Steps:")
            output.append("1. Create adaptive policy groups")
            output.append("2. Define policies between groups")
            output.append("3. Apply this ACL to policies")
            output.append("4. Test policy enforcement")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create adaptive policy ACL", e)


def get_organization_adaptive_policy_groups(org_id: str) -> str:
    """
    👥 Get adaptive policy groups.
    
    Lists groups for adaptive policy assignment.
    
    Args:
        org_id: Organization ID
    
    Returns:
        List of adaptive policy groups
    """
    try:
        with safe_api_call("get adaptive policy groups"):
            groups = meraki.dashboard.organizations.getOrganizationAdaptivePolicyGroups(org_id)
            
            output = ["👥 Adaptive Policy Groups", "=" * 50, ""]
            
            if not groups:
                output.append("No adaptive policy groups configured")
                output.append("\n💡 Use create_organization_adaptive_policy_group() to add")
                return "\n".join(output)
            
            output.append(f"Total Groups: {len(groups)}")
            output.append("")
            
            # Categorize groups
            user_groups = []
            device_groups = []
            
            for group in groups:
                if group.get('isDefaultGroup'):
                    continue  # Skip default groups for now
                    
                # Determine type based on attributes
                if group.get('sgt'):
                    device_groups.append(group)
                else:
                    user_groups.append(group)
            
            # Show user groups
            if user_groups:
                output.append("👤 User Groups:")
                for group in user_groups[:5]:
                    group_id = group.get('groupId', 'Unknown')
                    name = group.get('name', 'Unnamed Group')
                    sgt = group.get('sgt', 'N/A')
                    
                    output.append(f"\n   📁 {name}")
                    output.append(f"      ID: {group_id}")
                    output.append(f"      SGT: {sgt}")
                    
                    # Policy objects
                    policy_objects = group.get('policyObjects', [])
                    if policy_objects:
                        output.append(f"      Objects: {len(policy_objects)}")
                
                if len(user_groups) > 5:
                    output.append(f"\n   ... and {len(user_groups) - 5} more user groups")
            
            # Show device groups
            if device_groups:
                output.append("\n🖥️ Device Groups:")
                for group in device_groups[:5]:
                    group_id = group.get('groupId', 'Unknown')
                    name = group.get('name', 'Unnamed Group')
                    sgt = group.get('sgt', 'N/A')
                    
                    output.append(f"\n   📁 {name}")
                    output.append(f"      ID: {group_id}")
                    output.append(f"      SGT: {sgt}")
                
                if len(device_groups) > 5:
                    output.append(f"\n   ... and {len(device_groups) - 5} more device groups")
            
            # Show default groups
            default_groups = [g for g in groups if g.get('isDefaultGroup')]
            if default_groups:
                output.append("\n🔧 Default Groups:")
                for group in default_groups:
                    output.append(f"   • {group.get('name', 'Unknown')}")
            
            # Group usage
            output.append("\n💡 Group Usage:")
            output.append("• Assign users via RADIUS attributes")
            output.append("• Tag devices with SGTs")
            output.append("• Define policies between groups")
            output.append("• Enable dynamic segmentation")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get adaptive policy groups", e)


def create_organization_adaptive_policy_group(
    org_id: str,
    name: str,
    sgt: int,
    description: Optional[str] = None,
    policy_objects: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    ➕ Create adaptive policy group.
    
    Define a group for adaptive policy segmentation.
    
    Args:
        org_id: Organization ID
        name: Group name
        sgt: Scalable Group Tag (SGT) value
        description: Group description
        policy_objects: List of policy objects
    
    Returns:
        Created group details
    """
    try:
        with safe_api_call("create adaptive policy group"):
            # Build group data
            group_data = {
                "name": name,
                "sgt": sgt
            }
            
            if description:
                group_data["description"] = description
            
            if policy_objects:
                group_data["policyObjects"] = policy_objects
            
            # Create the group
            group = meraki.dashboard.organizations.createOrganizationAdaptivePolicyGroup(
                org_id,
                **group_data
            )
            
            output = ["✅ Adaptive Policy Group Created", "=" * 50, ""]
            output.append(f"Name: {group.get('name', name)}")
            output.append(f"ID: {group.get('groupId', 'N/A')}")
            output.append(f"SGT: {group.get('sgt', sgt)}")
            if description:
                output.append(f"Description: {description}")
            
            # Policy objects
            if policy_objects:
                output.append(f"\n📋 Policy Objects: {len(policy_objects)}")
            
            output.append("\n🚀 Next Steps:")
            output.append("1. Assign users/devices to group")
            output.append("2. Create policies for this group")
            output.append("3. Configure RADIUS for SGT assignment")
            output.append("4. Test group membership")
            
            output.append("\n💡 SGT Assignment Methods:")
            output.append("• RADIUS attribute (Cisco-AVPair)")
            output.append("• Manual device tagging")
            output.append("• Identity-based assignment")
            output.append("• Network admission control")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create adaptive policy group", e)


def get_organization_adaptive_policy_policies(org_id: str) -> str:
    """
    📜 Get adaptive policies.
    
    Lists policies defining traffic rules between groups.
    
    Args:
        org_id: Organization ID
    
    Returns:
        List of adaptive policies
    """
    try:
        with safe_api_call("get adaptive policies"):
            policies = meraki.dashboard.organizations.getOrganizationAdaptivePolicyPolicies(org_id)
            
            output = ["📜 Adaptive Policies", "=" * 50, ""]
            
            if not policies:
                output.append("No adaptive policies configured")
                output.append("\n💡 Use create_organization_adaptive_policy_policy() to add")
                return "\n".join(output)
            
            output.append(f"Total Policies: {len(policies)}")
            output.append("")
            
            # Show each policy
            for i, policy in enumerate(policies, 1):
                policy_id = policy.get('adaptivePolicyId', 'Unknown')
                
                # Source and destination groups
                src_group = policy.get('sourceGroup', {})
                dst_group = policy.get('destinationGroup', {})
                
                output.append(f"{i}. Policy ID: {policy_id}")
                output.append(f"   Source: {src_group.get('name', 'Unknown')} (SGT: {src_group.get('sgt', 'N/A')})")
                output.append(f"   Destination: {dst_group.get('name', 'Unknown')} (SGT: {dst_group.get('sgt', 'N/A')})")
                
                # ACLs
                acls = policy.get('acls', [])
                if acls:
                    output.append("   ACLs:")
                    for acl in acls:
                        output.append(f"      • {acl.get('name', 'Unknown')} (ID: {acl.get('id', 'N/A')})")
                else:
                    output.append("   ACLs: None (Deny all)")
                
                # Last updated
                if policy.get('lastUpdatedAt'):
                    output.append(f"   Updated: {policy['lastUpdatedAt']}")
                
                output.append("")
            
            # Policy matrix
            output.append("📊 Policy Summary:")
            
            # Count policies by action
            allow_count = sum(1 for p in policies if p.get('acls'))
            deny_count = len(policies) - allow_count
            
            output.append(f"   Allow policies: {allow_count}")
            output.append(f"   Deny policies: {deny_count}")
            
            output.append("\n💡 Policy Best Practices:")
            output.append("• Start with deny-all default")
            output.append("• Create specific allow rules")
            output.append("• Group similar resources")
            output.append("• Document policy purpose")
            output.append("• Test thoroughly")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get adaptive policies", e)


def create_organization_adaptive_policy_policy(
    org_id: str,
    source_group_id: str,
    destination_group_id: str,
    acl_ids: Optional[List[str]] = None
) -> str:
    """
    ➕ Create adaptive policy.
    
    Define traffic rules between adaptive policy groups.
    
    Args:
        org_id: Organization ID
        source_group_id: Source group ID
        destination_group_id: Destination group ID
        acl_ids: List of ACL IDs to apply (None = deny all)
    
    Returns:
        Created policy details
    """
    try:
        with safe_api_call("create adaptive policy"):
            # Build policy data
            policy_data = {
                "sourceGroup": {"id": source_group_id},
                "destinationGroup": {"id": destination_group_id}
            }
            
            if acl_ids:
                policy_data["acls"] = [{"id": acl_id} for acl_id in acl_ids]
            
            # Create the policy
            policy = meraki.dashboard.organizations.createOrganizationAdaptivePolicyPolicy(
                org_id,
                **policy_data
            )
            
            output = ["✅ Adaptive Policy Created", "=" * 50, ""]
            output.append(f"Policy ID: {policy.get('adaptivePolicyId', 'N/A')}")
            output.append("")
            
            # Source and destination
            src = policy.get('sourceGroup', {})
            dst = policy.get('destinationGroup', {})
            
            output.append("🔄 Traffic Flow:")
            output.append(f"   From: {src.get('name', 'Unknown')} (SGT: {src.get('sgt', 'N/A')})")
            output.append(f"   To: {dst.get('name', 'Unknown')} (SGT: {dst.get('sgt', 'N/A')})")
            
            # ACLs
            policy_acls = policy.get('acls', [])
            if policy_acls:
                output.append("\n📋 Applied ACLs:")
                for acl in policy_acls:
                    output.append(f"   • {acl.get('name', 'Unknown')}")
                output.append("\n   Result: Traffic allowed per ACL rules")
            else:
                output.append("\n🚫 No ACLs: All traffic denied")
            
            output.append("\n🚀 Policy Active!")
            output.append("• Enforcement begins immediately")
            output.append("• Check device logs for blocks")
            output.append("• Monitor traffic flows")
            output.append("• Adjust ACLs as needed")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create adaptive policy", e)


def get_organization_adaptive_policy_settings(org_id: str) -> str:
    """
    ⚙️ Get adaptive policy settings.
    
    Shows global adaptive policy configuration.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Adaptive policy settings
    """
    try:
        with safe_api_call("get adaptive policy settings"):
            settings = meraki.dashboard.organizations.getOrganizationAdaptivePolicySettings(org_id)
            
            output = ["⚙️ Adaptive Policy Settings", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Enabled networks
            enabled_networks = settings.get('enabledNetworks', [])
            if enabled_networks:
                output.append(f"✅ Enabled on {len(enabled_networks)} networks")
                
                # Show first few
                for net_id in enabled_networks[:5]:
                    output.append(f"   • {net_id}")
                
                if len(enabled_networks) > 5:
                    output.append(f"   ... and {len(enabled_networks) - 5} more networks")
            else:
                output.append("❌ Not enabled on any networks")
            
            output.append("\n💡 Adaptive Policy Benefits:")
            output.append("• Dynamic microsegmentation")
            output.append("• Identity-based access")
            output.append("• Simplified policy management")
            output.append("• Consistent enforcement")
            output.append("• Zero Trust security")
            
            output.append("\n🔧 Requirements:")
            output.append("• Supported switches (MS)")
            output.append("• RADIUS for SGT assignment")
            output.append("• Group and policy configuration")
            output.append("• Compatible firmware")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get adaptive policy settings", e)


def adaptive_policy_examples() -> str:
    """
    📚 Show adaptive policy examples.
    
    Provides example configurations for common scenarios.
    
    Returns:
        Adaptive policy examples
    """
    output = ["📚 Adaptive Policy Examples", "=" * 50, ""]
    
    output.append("1️⃣ Basic Web Access ACL:")
    output.append("""
rules = [
    {
        "policy": "allow",
        "protocol": "tcp",
        "dstPort": "80"
    },
    {
        "policy": "allow",
        "protocol": "tcp",
        "dstPort": "443"
    },
    {
        "policy": "allow",
        "protocol": "udp",
        "dstPort": "53"
    }
]

acl = create_organization_adaptive_policy_acl(
    org_id,
    name="Web-Access",
    rules=rules,
    description="Allow HTTP/HTTPS and DNS"
)
""")
    
    output.append("\n2️⃣ Employee to Server Policy:")
    output.append("""
# Create groups
employee_group = create_organization_adaptive_policy_group(
    org_id,
    name="Employees",
    sgt=100,
    description="Corporate employees"
)

server_group = create_organization_adaptive_policy_group(
    org_id,
    name="Servers",
    sgt=200,
    description="Data center servers"
)

# Create policy allowing access
policy = create_organization_adaptive_policy_policy(
    org_id,
    source_group_id=employee_group['groupId'],
    destination_group_id=server_group['groupId'],
    acl_ids=[web_acl_id, ssh_acl_id]
)
""")
    
    output.append("\n3️⃣ IoT Device Isolation:")
    output.append("""
# IoT devices can only reach IoT servers
iot_to_iot_policy = create_organization_adaptive_policy_policy(
    org_id,
    source_group_id=iot_group_id,
    destination_group_id=iot_server_group_id,
    acl_ids=[mqtt_acl_id]
)

# Block IoT to corporate
iot_to_corp_policy = create_organization_adaptive_policy_policy(
    org_id,
    source_group_id=iot_group_id,
    destination_group_id=corp_group_id,
    acl_ids=[]  # No ACLs = Deny all
)
""")
    
    output.append("\n4️⃣ Guest Isolation with Internet:")
    output.append("""
# Guest to Internet (via firewall)
guest_internet_acl = {
    "rules": [
        {"policy": "allow", "protocol": "any"}
    ]
}

# Guest to Corporate = Denied
guest_to_corp = create_organization_adaptive_policy_policy(
    org_id,
    source_group_id=guest_group_id,
    destination_group_id=corp_group_id,
    acl_ids=[]  # Deny all
)
""")
    
    output.append("\n💡 Design Principles:")
    output.append("• Start with zero trust (deny all)")
    output.append("• Create specific allow policies")
    output.append("• Group similar resources")
    output.append("• Use meaningful SGT values")
    output.append("• Document group purposes")
    
    return "\n".join(output)


def adaptive_policy_help() -> str:
    """
    ❓ Get help with adaptive policy tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """🔐 Adaptive Policy Tools Help
==================================================

Available tools for adaptive policy management:

1. get_organization_adaptive_policy_acls()
   - List ACL definitions
   - View rule details
   - Check IP versions
   - Export configurations

2. create_organization_adaptive_policy_acl()
   - Define access rules
   - Set allow/deny policies
   - Configure protocols/ports
   - Support IPv4/IPv6

3. get_organization_adaptive_policy_groups()
   - View policy groups
   - Check SGT assignments
   - List group members
   - Review descriptions

4. create_organization_adaptive_policy_group()
   - Create user/device groups
   - Assign SGT values
   - Add policy objects
   - Enable segmentation

5. get_organization_adaptive_policy_policies()
   - View traffic policies
   - Check group mappings
   - Review ACL assignments
   - Audit configurations

6. create_organization_adaptive_policy_policy()
   - Define group policies
   - Apply ACL rules
   - Enable/block traffic
   - Implement zero trust

7. get_organization_adaptive_policy_settings()
   - Check enabled networks
   - View global settings
   - Verify requirements
   - Plan deployment

8. adaptive_policy_examples()
   - Common use cases
   - Configuration templates
   - Best practices
   - Design patterns

Adaptive Policy Concepts:
• SGT - Scalable Group Tag
• ACL - Access Control List
• Policy - Rules between groups
• Microsegmentation - Dynamic isolation

Benefits:
• Identity-based access
• Dynamic enforcement
• Simplified management
• Consistent policies
• Zero trust security

Requirements:
• Compatible switches
• RADIUS integration
• Group definitions
• Policy configuration

Common Use Cases:
• User segmentation
• IoT isolation
• Server protection
• Guest access
• Compliance zones
• Partner access

SGT Assignment:
• RADIUS attributes
• 802.1X authentication
• MAC authentication
• Manual tagging
• Default groups

Best Practices:
• Plan group structure
• Use descriptive names
• Start with deny-all
• Test incrementally
• Monitor traffic
• Document policies

Troubleshooting:
• Check switch compatibility
• Verify RADIUS config
• Review group membership
• Test ACL rules
• Monitor denied traffic
• Check SGT propagation
"""


def register_adaptive_policy_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all adaptive policy tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_adaptive_policy_acls, "List adaptive policy ACLs"),
        (create_organization_adaptive_policy_acl, "Create adaptive policy ACL"),
        (get_organization_adaptive_policy_groups, "List adaptive policy groups"),
        (create_organization_adaptive_policy_group, "Create adaptive policy group"),
        (get_organization_adaptive_policy_policies, "List adaptive policies"),
        (create_organization_adaptive_policy_policy, "Create adaptive policy"),
        (get_organization_adaptive_policy_settings, "Get adaptive policy settings"),
        (adaptive_policy_examples, "Show adaptive policy examples"),
        (adaptive_policy_help, "Get help with adaptive policies"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)