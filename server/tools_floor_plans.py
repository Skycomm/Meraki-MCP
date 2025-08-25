"""
Floor Plans management tools for Cisco Meraki MCP Server.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_floor_plans_tools(mcp_app, meraki):
    """Register floor plans tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all floor plans tools
    register_floor_plans_handlers()

def register_floor_plans_handlers():
    """Register all floor plans-related tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_network_floor_plans",
        description="🏢 List all floor plans for a network"
    )
    def get_network_floor_plans(network_id: str):
        """List floor plans for a network."""
        try:
            floor_plans = meraki_client.dashboard.networks.getNetworkFloorPlans(network_id)
            
            if not floor_plans:
                return f"No floor plans found for network {network_id}."
            
            result = f"# 🏢 Floor Plans\n\n"
            result += f"**Total Floor Plans**: {len(floor_plans)}\n\n"
            
            for plan in floor_plans:
                result += f"## {plan.get('name', 'Unnamed')}\n"
                result += f"- ID: {plan.get('floorPlanId')}\n"
                result += f"- Width: {plan.get('width')} ft\n"
                result += f"- Height: {plan.get('height')} ft\n"
                
                devices = plan.get('devices', [])
                if devices:
                    result += f"- Devices: {len(devices)}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving floor plans: {str(e)}"
    
    @app.tool(
        name="create_network_floor_plan",
        description="🏢 Create a floor plan"
    )
    def create_network_floor_plan(network_id: str, name: str, **kwargs):
        """Create a floor plan."""
        try:
            result = meraki_client.dashboard.networks.createNetworkFloorPlan(
                network_id, name, **kwargs
            )
            
            return f"✅ Floor plan '{name}' created successfully!\n\nFloor Plan ID: {result.get('floorPlanId')}"
            
        except Exception as e:
            return f"Error creating floor plan: {str(e)}"
    
    @app.tool(
        name="get_network_floor_plan",
        description="🏢 Get floor plan details"
    )
    def get_network_floor_plan(network_id: str, floorPlanId: str):
        """Get details of a floor plan."""
        try:
            plan = meraki_client.dashboard.networks.getNetworkFloorPlan(network_id, floorPlanId)
            
            result = f"# 🏢 Floor Plan Details\n\n"
            result += f"**Name**: {plan.get('name')}\n"
            result += f"**ID**: {plan.get('floorPlanId')}\n"
            result += f"**Dimensions**: {plan.get('width')} x {plan.get('height')} ft\n"
            
            if plan.get('center'):
                center = plan['center']
                result += f"**Center**: ({center.get('lat')}, {center.get('lng')})\n"
            
            devices = plan.get('devices', [])
            if devices:
                result += f"\n**Devices on Floor Plan**: {len(devices)}\n"
                for device in devices[:10]:
                    result += f"- {device.get('name', 'Unknown')} ({device.get('serial')})\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving floor plan: {str(e)}"
    
    @app.tool(
        name="update_network_floor_plan",
        description="🏢 Update a floor plan"
    )
    def update_network_floor_plan(network_id: str, floorPlanId: str, **kwargs):
        """Update a floor plan."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkFloorPlan(
                network_id, floorPlanId, **kwargs
            )
            
            return f"✅ Floor plan updated successfully!"
            
        except Exception as e:
            return f"Error updating floor plan: {str(e)}"
    
    @app.tool(
        name="delete_network_floor_plan",
        description="🏢 Delete a floor plan"
    )
    def delete_network_floor_plan(network_id: str, floorPlanId: str):
        """Delete a floor plan."""
        try:
            meraki_client.dashboard.networks.deleteNetworkFloorPlan(network_id, floorPlanId)
            
            return f"✅ Floor plan deleted successfully!"
            
        except Exception as e:
            return f"Error deleting floor plan: {str(e)}"