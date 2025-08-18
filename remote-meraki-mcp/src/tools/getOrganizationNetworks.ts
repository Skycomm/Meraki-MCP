import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

export async function getOrganizationNetworks(server: Server) {
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      {
        name: "get_organization_networks",
        description: "Get all networks in a Meraki organization",
        inputSchema: {
          type: "object",
          properties: {
            org_id: {
              type: "string",
              description: "Organization ID",
            },
          },
          required: ["org_id"],
        },
      },
    ],
  }));

  server.setRequestHandler("tools/call", async (request, context) => {
    if (request.params.name !== "get_organization_networks") return null;

    const apiKey = context.environment?.MERAKI_API_KEY;
    const { org_id } = request.params.arguments as { org_id: string };

    try {
      const response = await fetch(
        `https://api.meraki.com/api/v1/organizations/${org_id}/networks`,
        {
          headers: {
            "X-Cisco-Meraki-API-Key": apiKey,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const networks = await response.json();
      
      let result = `# Networks in Organization ${org_id}\n\n`;
      result += `Total Networks: ${networks.length}\n\n`;
      
      for (const network of networks) {
        result += `## ${network.name}\n`;
        result += `- **ID**: ${network.id}\n`;
        result += `- **Type**: ${network.productTypes?.join(", ") || "Unknown"}\n`;
        result += `- **Time Zone**: ${network.timeZone}\n`;
        if (network.tags?.length > 0) {
          result += `- **Tags**: ${network.tags.join(", ")}\n`;
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
            text: `Error retrieving networks: ${error.message}`,
          },
        ],
      };
    }
  });
}