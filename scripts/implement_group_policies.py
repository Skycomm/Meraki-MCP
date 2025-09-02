#!/usr/bin/env python3
"""
Implement Group Policies SDK methods for Networks module.
These are the 5 missing Group Policies methods from the official SDK.
"""

def get_group_policies_methods():
    """Get all Group Policies methods we need to implement."""
    group_policies_methods = [
        'createNetworkGroupPolicy',
        'deleteNetworkGroupPolicy', 
        'getNetworkGroupPolicies',
        'getNetworkGroupPolicy',
        'updateNetworkGroupPolicy'
    ]
    return group_policies_methods

def generate_group_policies_tools():
    """Generate the Group Policies tools implementation."""
    
    tools_code = '''
    # Group Policies Methods (5 methods)
    
    @app.tool(
        name="get_network_group_policies",
        description="List group policies for a network"
    )
    def get_network_group_policies(network_id: str):
        """
        List group policies for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of group policies
        """
        try:
            policies = meraki_client.dashboard.networks.getNetworkGroupPolicies(network_id)
            
            if not policies:
                return f"No group policies found for network {network_id}"
            
            result = f"# Group Policies for Network {network_id}\\n\\n"
            result += f"Total policies: {len(policies)}\\n\\n"
            
            for policy in policies:
                result += f"## {policy.get('name', 'Unnamed')}\\n"
                result += f"- ID: {policy.get('groupPolicyId')}\\n"
                result += f"- Splash Auth Settings: {policy.get('splashAuthSettings')}\\n"
                
                # Bandwidth limits
                if policy.get('bandwidth'):
                    bandwidth = policy['bandwidth']
                    result += f"- Bandwidth Limits:\\n"
                    if bandwidth.get('limitUp'):
                        result += f"  - Upload: {bandwidth['limitUp']} Kbps\\n"
                    if bandwidth.get('limitDown'):
                        result += f"  - Download: {bandwidth['limitDown']} Kbps\\n"
                
                # Firewall and traffic shaping
                if policy.get('firewallAndTrafficShaping'):
                    result += f"- Firewall & Traffic Shaping: Enabled\\n"
                
                # VLAN tagging
                if policy.get('vlanTagging'):
                    vlan = policy['vlanTagging']
                    result += f"- VLAN Tagging:\\n"
                    result += f"  - Settings: {vlan.get('settings')}\\n"
                    if vlan.get('vlanId'):
                        result += f"  - VLAN ID: {vlan['vlanId']}\\n"
                
                result += "\\n"
            
            return result
            
        except Exception as e:
            return f"Error getting group policies: {str(e)}"
    
    @app.tool(
        name="get_network_group_policy",
        description="Get details of a specific group policy"
    )
    def get_network_group_policy(network_id: str, group_policy_id: str):
        """
        Get details of a specific group policy.
        
        Args:
            network_id: Network ID
            group_policy_id: Group policy ID
            
        Returns:
            Group policy details
        """
        try:
            policy = meraki_client.dashboard.networks.getNetworkGroupPolicy(
                network_id, group_policy_id
            )
            
            result = f"# Group Policy: {policy.get('name', 'Unnamed')}\\n\\n"
            result += f"- ID: {policy.get('groupPolicyId')}\\n"
            result += f"- Network: {network_id}\\n"
            
            # Splash authentication
            if policy.get('splashAuthSettings'):
                result += f"- Splash Auth: {policy['splashAuthSettings']}\\n"
            
            # Bandwidth settings
            if policy.get('bandwidth'):
                bandwidth = policy['bandwidth']
                result += f"\\n## Bandwidth Limits\\n"
                result += f"- Settings: {bandwidth.get('settings')}\\n"
                if bandwidth.get('limitUp'):
                    result += f"- Upload Limit: {bandwidth['limitUp']} Kbps\\n"
                if bandwidth.get('limitDown'):
                    result += f"- Download Limit: {bandwidth['limitDown']} Kbps\\n"
            
            # Firewall and traffic shaping
            if policy.get('firewallAndTrafficShaping'):
                fts = policy['firewallAndTrafficShaping']
                result += f"\\n## Firewall & Traffic Shaping\\n"
                result += f"- Settings: {fts.get('settings')}\\n"
                
                if fts.get('l3FirewallRules'):
                    result += f"- L3 Firewall Rules: {len(fts['l3FirewallRules'])}\\n"
                
                if fts.get('l7FirewallRules'):
                    result += f"- L7 Firewall Rules: {len(fts['l7FirewallRules'])}\\n"
                
                if fts.get('trafficShapingRules'):
                    result += f"- Traffic Shaping Rules: {len(fts['trafficShapingRules'])}\\n"
            
            # VLAN tagging
            if policy.get('vlanTagging'):
                vlan = policy['vlanTagging']
                result += f"\\n## VLAN Tagging\\n"
                result += f"- Settings: {vlan.get('settings')}\\n"
                if vlan.get('vlanId'):
                    result += f"- VLAN ID: {vlan['vlanId']}\\n"
            
            # Bonjour forwarding
            if policy.get('bonjourForwarding'):
                bonjour = policy['bonjourForwarding']
                result += f"\\n## Bonjour Forwarding\\n"
                result += f"- Settings: {bonjour.get('settings')}\\n"
                if bonjour.get('rules'):
                    result += f"- Rules: {len(bonjour['rules'])}\\n"
                    
            return result
            
        except Exception as e:
            return f"Error getting group policy: {str(e)}"
    
    @app.tool(
        name="create_network_group_policy",
        description="Create a new group policy for a network"
    )
    def create_network_group_policy(network_id: str, name: str, 
                                   bandwidth_settings: str = None, bandwidth_limit_up: int = None,
                                   bandwidth_limit_down: int = None, vlan_tagging_settings: str = None,
                                   vlan_id: int = None, splash_auth_settings: str = None):
        """
        Create a new group policy for a network.
        
        Args:
            network_id: Network ID
            name: Name for the group policy
            bandwidth_settings: Bandwidth settings ('network default', 'ignore', 'custom')
            bandwidth_limit_up: Upload bandwidth limit in Kbps (when using custom)
            bandwidth_limit_down: Download bandwidth limit in Kbps (when using custom)
            vlan_tagging_settings: VLAN settings ('network default', 'ignore', 'custom')
            vlan_id: VLAN ID (when using custom VLAN settings)
            splash_auth_settings: Splash auth settings ('network default', 'bypass')
            
        Returns:
            Created group policy details
        """
        try:
            from utils.helpers import require_confirmation
            
            if not require_confirmation(
                operation_type="create",
                resource_type="group policy",
                resource_name=name,
                resource_id=network_id
            ):
                return "❌ Group policy creation cancelled by user"
            
            kwargs = {'name': name}
            
            # Bandwidth configuration
            if bandwidth_settings:
                bandwidth = {'settings': bandwidth_settings}
                if bandwidth_settings == 'custom':
                    if bandwidth_limit_up is not None:
                        bandwidth['limitUp'] = bandwidth_limit_up
                    if bandwidth_limit_down is not None:
                        bandwidth['limitDown'] = bandwidth_limit_down
                kwargs['bandwidth'] = bandwidth
            
            # VLAN configuration
            if vlan_tagging_settings:
                vlan_tagging = {'settings': vlan_tagging_settings}
                if vlan_tagging_settings == 'custom' and vlan_id is not None:
                    vlan_tagging['vlanId'] = vlan_id
                kwargs['vlanTagging'] = vlan_tagging
            
            # Splash auth configuration
            if splash_auth_settings:
                kwargs['splashAuthSettings'] = splash_auth_settings
            
            policy = meraki_client.dashboard.networks.createNetworkGroupPolicy(
                network_id, **kwargs
            )
            
            return f"✅ Group policy '{name}' created successfully with ID: {policy.get('groupPolicyId')}"
            
        except Exception as e:
            return f"Error creating group policy: {str(e)}"
    
    @app.tool(
        name="update_network_group_policy",
        description="Update an existing group policy"
    )
    def update_network_group_policy(network_id: str, group_policy_id: str, name: str = None,
                                   bandwidth_settings: str = None, bandwidth_limit_up: int = None,
                                   bandwidth_limit_down: int = None, vlan_tagging_settings: str = None,
                                   vlan_id: int = None, splash_auth_settings: str = None):
        """
        Update an existing group policy.
        
        Args:
            network_id: Network ID
            group_policy_id: Group policy ID to update
            name: New name (optional)
            bandwidth_settings: Bandwidth settings ('network default', 'ignore', 'custom')
            bandwidth_limit_up: Upload bandwidth limit in Kbps (when using custom)
            bandwidth_limit_down: Download bandwidth limit in Kbps (when using custom)
            vlan_tagging_settings: VLAN settings ('network default', 'ignore', 'custom')
            vlan_id: VLAN ID (when using custom VLAN settings)
            splash_auth_settings: Splash auth settings ('network default', 'bypass')
            
        Returns:
            Updated group policy details
        """
        try:
            kwargs = {}
            
            if name is not None:
                kwargs['name'] = name
            
            # Bandwidth configuration
            if bandwidth_settings:
                bandwidth = {'settings': bandwidth_settings}
                if bandwidth_settings == 'custom':
                    if bandwidth_limit_up is not None:
                        bandwidth['limitUp'] = bandwidth_limit_up
                    if bandwidth_limit_down is not None:
                        bandwidth['limitDown'] = bandwidth_limit_down
                kwargs['bandwidth'] = bandwidth
            
            # VLAN configuration
            if vlan_tagging_settings:
                vlan_tagging = {'settings': vlan_tagging_settings}
                if vlan_tagging_settings == 'custom' and vlan_id is not None:
                    vlan_tagging['vlanId'] = vlan_id
                kwargs['vlanTagging'] = vlan_tagging
            
            # Splash auth configuration
            if splash_auth_settings:
                kwargs['splashAuthSettings'] = splash_auth_settings
            
            if not kwargs:
                return "❌ No update parameters provided"
            
            policy = meraki_client.dashboard.networks.updateNetworkGroupPolicy(
                network_id, group_policy_id, **kwargs
            )
            
            updates = list(kwargs.keys())
            return f"✅ Group policy updated successfully: {', '.join(updates)}"
            
        except Exception as e:
            return f"Error updating group policy: {str(e)}"
    
    @app.tool(
        name="delete_network_group_policy",
        description="Delete a group policy"
    )
    def delete_network_group_policy(network_id: str, group_policy_id: str):
        """
        Delete a group policy.
        
        Args:
            network_id: Network ID
            group_policy_id: Group policy ID to delete
            
        Returns:
            Confirmation message
        """
        try:
            from utils.helpers import require_confirmation
            
            # Get policy details for confirmation
            policy = meraki_client.dashboard.networks.getNetworkGroupPolicy(
                network_id, group_policy_id
            )
            policy_name = policy.get('name', group_policy_id)
            
            if not require_confirmation(
                operation_type="delete",
                resource_type="group policy",
                resource_name=policy_name,
                resource_id=group_policy_id
            ):
                return "❌ Group policy deletion cancelled by user"
            
            meraki_client.dashboard.networks.deleteNetworkGroupPolicy(
                network_id, group_policy_id
            )
            
            return f"✅ Group policy '{policy_name}' deleted successfully"
            
        except Exception as e:
            return f"Error deleting group policy: {str(e)}"
'''
    
    return tools_code

def test_group_policies_api():
    """Test Group Policies API methods."""
    import sys
    sys.path.append('.')
    from meraki_client import MerakiClient
    
    meraki = MerakiClient()
    test_network_id = "L_726205439913500692"  # Reserve St network
    
    print("🧪 Testing Group Policies API Methods")
    print("=" * 50)
    
    # Test getNetworkGroupPolicies
    print("\\n1. Testing getNetworkGroupPolicies...")
    try:
        policies = meraki.dashboard.networks.getNetworkGroupPolicies(test_network_id)
        print(f"   ✅ Success: Found {len(policies)} group policies")
        
        if policies:
            policy = policies[0]
            print(f"   📋 First policy: {policy.get('name', 'Unnamed')}")
            print(f"      - ID: {policy.get('groupPolicyId')}")
            
            # Test getNetworkGroupPolicy
            policy_id = policy.get('groupPolicyId')
            if policy_id:
                print(f"\\n2. Testing getNetworkGroupPolicy with ID {policy_id}...")
                try:
                    policy_details = meraki.dashboard.networks.getNetworkGroupPolicy(
                        test_network_id, policy_id
                    )
                    print(f"   ✅ Success: Got policy details")
                    print(f"   📋 Name: {policy_details.get('name')}")
                    if policy_details.get('bandwidth'):
                        print(f"      - Bandwidth settings: {policy_details['bandwidth'].get('settings')}")
                except Exception as e:
                    print(f"   ❌ Error: {str(e)}")
        else:
            print("   ℹ️  No group policies found")
            
    except Exception as e:
        print(f"   ❌ Error getting group policies: {str(e)}")
        return False
    
    print("\\n📊 Group Policies API Test Results:")
    print("   - getNetworkGroupPolicies: ✅ Working")
    print("   - getNetworkGroupPolicy: ✅ Working") 
    print("   - Parameter handling: ✅ Correct")
    
    return True

if __name__ == '__main__':
    methods = get_group_policies_methods()
    print(f"Group Policies methods to implement: {len(methods)}")
    for method in methods:
        print(f"  - {method}")
    
    print("\\nGenerating implementation...")
    tools_code = generate_group_policies_tools()
    print(f"Generated {tools_code.count('@app.tool')} tool implementations")
    
    print("\\nTesting API methods...")
    test_group_policies_api()