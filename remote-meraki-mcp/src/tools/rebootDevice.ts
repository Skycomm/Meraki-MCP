import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

export async function rebootDevice(server: Server) {
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      {
        name: "reboot_device",
        description: "⚠️ REBOOT a Meraki device - PRIVILEGED USERS ONLY",
        inputSchema: {
          type: "object",
          properties: {
            serial: {
              type: "string",
              description: "Device serial number",
            },
            confirmation: {
              type: "string",
              description: "Must be exactly 'YES-REBOOT-[serial]' to proceed",
            },
          },
          required: ["serial", "confirmation"],
        },
      },
    ],
  }));

  server.setRequestHandler("tools/call", async (request, context) => {
    if (request.params.name !== "reboot_device") return null;

    const apiKey = context.environment?.MERAKI_API_KEY;
    const userLogin = context.environment?.USER_LOGIN;
    const isPrivileged = context.environment?.IS_PRIVILEGED === "true";

    if (!isPrivileged) {
      return {
        content: [
          {
            type: "text",
            text: `❌ Access Denied\n\nUser '${userLogin}' does not have permission to reboot devices.\nThis operation is restricted to privileged users only.`,
          },
        ],
      };
    }

    const { serial, confirmation } = request.params.arguments as { 
      serial: string; 
      confirmation: string;
    };

    const expectedConfirmation = `YES-REBOOT-${serial}`;

    if (confirmation !== expectedConfirmation) {
      return {
        content: [
          {
            type: "text",
            text: `# ⚠️ REBOOT CONFIRMATION REQUIRED

**Device Serial**: ${serial}
**User**: ${userLogin}

**WARNING**: Rebooting this device will:
- 🔴 Disconnect ALL users
- 🔴 Interrupt network services
- 🔴 Take 2-5 minutes to come back online

**To proceed with reboot**:
You must provide exact confirmation: "${expectedConfirmation}"

**Alternative solutions to try first**:
1. Check device status and logs
2. Verify cable connections
3. Check for firmware updates
4. Review recent configuration changes

⚠️ This action cannot be undone!`,
          },
        ],
      };
    }

    try {
      const response = await fetch(
        `https://api.meraki.com/api/v1/devices/${serial}/reboot`,
        {
          method: "POST",
          headers: {
            "X-Cisco-Meraki-API-Key": apiKey,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        }
      );

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`API request failed: ${response.status} - ${error}`);
      }

      return {
        content: [
          {
            type: "text",
            text: `✅ REBOOT INITIATED

**Device**: ${serial}
**Initiated by**: ${userLogin}
**Status**: Reboot command sent successfully
**Expected downtime**: 2-5 minutes

The device is now rebooting. Monitor its status to confirm it comes back online.

Timestamp: ${new Date().toISOString()}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `❌ Error rebooting device: ${error.message}`,
          },
        ],
      };
    }
  });
}