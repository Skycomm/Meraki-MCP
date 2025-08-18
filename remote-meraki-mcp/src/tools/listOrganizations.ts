import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

export async function listOrganizations(server: Server) {
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      {
        name: "list_organizations",
        description: "List all Meraki organizations the API key has access to",
        inputSchema: {
          type: "object",
          properties: {},
          required: [],
        },
      },
    ],
  }));

  server.setRequestHandler("tools/call", async (request, context) => {
    if (request.params.name !== "list_organizations") return null;

    const apiKey = context.environment?.MERAKI_API_KEY;
    const userLogin = context.environment?.USER_LOGIN;

    if (!apiKey) {
      return {
        content: [
          {
            type: "text",
            text: "Error: Meraki API key not configured",
          },
        ],
      };
    }

    try {
      const response = await fetch("https://api.meraki.com/api/v1/organizations", {
        headers: {
          "X-Cisco-Meraki-API-Key": apiKey,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const organizations = await response.json();
      
      // Format the response
      let result = `# Meraki Organizations (User: ${userLogin})\n\n`;
      result += `Total Organizations: ${organizations.length}\n\n`;
      
      for (const org of organizations) {
        result += `## ${org.name}\n`;
        result += `- **ID**: ${org.id}\n`;
        result += `- **URL**: ${org.url}\n`;
        if (org.api?.enabled) {
          result += `- **API**: ✅ Enabled\n`;
        }
        result += `\n`;
      }

      return {
        content: [
          {
            type: "text",
            text: result,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error listing organizations: ${error.message}`,
          },
        ],
      };
    }
  });
}