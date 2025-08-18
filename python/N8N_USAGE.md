# Using Meraki MCP Server with n8n

## Current Status
- **Server URL**: http://10.0.5.188:8000
- **Auth Token**: zmGlz_WLbMJU-sFdz6k4AW-CnKHItcGby7wiSMSo5Oc
- **Total Tools**: 97 tools available

## n8n Integration Options

### Option 1: MCP Client Tool (Recommended for 2025)
n8n now has native MCP support! Use the **MCP Client Tool** node:

1. Add "MCP Client Tool" node to your workflow
2. Configure:
   - **SSE Endpoint**: http://10.0.5.188:8000/sse
   - **Authentication**: Bearer Token
   - **Token**: zmGlz_WLbMJU-sFdz6k4AW-CnKHItcGby7wiSMSo5Oc

### Option 2: HTTP Request Node (Traditional)
Use standard HTTP Request node:

1. Add "HTTP Request" node
2. Configure:
   - **Method**: POST
   - **URL**: http://10.0.5.188:8000/api/v1/execute
   - **Authentication**: Header Auth
   - **Header Name**: Authorization
   - **Header Value**: Bearer zmGlz_WLbMJU-sFdz6k4AW-CnKHItcGby7wiSMSo5Oc
   - **Body Type**: JSON
   - **Body**:
     ```json
     {
       "tool": "list_organizations",
       "arguments": {}
     }
     ```

## Available Tools (97 total)

### Quick Examples

1. **List Organizations**
   ```json
   {"tool": "list_organizations", "arguments": {}}
   ```

2. **Get Networks**
   ```json
   {"tool": "get_networks", "arguments": {"org_id": "686470"}}
   ```

3. **Check Uplinks**
   ```json
   {"tool": "check_uplinks", "arguments": {"org_id": "686470", "timespan": 300}}
   ```

4. **Get Device Status**
   ```json
   {"tool": "get_device_statuses", "arguments": {"org_id": "686470"}}
   ```

### Getting All Tools
To see all 97 available tools with their parameters:
- **GET** http://10.0.5.188:8000/api/v1/tools
- Include Bearer token in header

## Example n8n Workflow

### Monitor Uplinks Every 5 Minutes
1. **Schedule Trigger**: Every 5 minutes
2. **HTTP Request**: Call check_uplinks
3. **If Node**: Check for packet loss > 1%
4. **Slack/Email**: Send alert if issues found

### Daily Network Report
1. **Schedule Trigger**: Daily at 9 AM
2. **HTTP Request**: list_organizations
3. **Loop**: For each org
4. **HTTP Request**: get_networks
5. **HTTP Request**: get_device_statuses
6. **Format**: Create report
7. **Email**: Send report

## Testing
Test the connection:
```bash
curl -X POST http://10.0.5.188:8000/api/v1/execute \
  -H "Authorization: Bearer zmGlz_WLbMJU-sFdz6k4AW-CnKHItcGby7wiSMSo5Oc" \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_organizations", "arguments": {}}'
```