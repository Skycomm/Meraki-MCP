
from server.main import app, meraki
org_id = "686470"

# Get all tools
tools_list = []
for name in dir(app):
    if not name.startswith('_'):
        attr = getattr(app, name)
        if callable(attr) and hasattr(attr, '__name__'):
            tools_list.append(name)

# Find get_organization_licenses
for tool_name in tools_list:
    if 'organization_licenses' in tool_name and 'get' in tool_name:
        print(f"Found tool: {tool_name}")
        break

# Call it through registered function
from server.tools_licensing import get_organization_licenses_internal
result = get_organization_licenses_internal(org_id)
print(result[:2000])
