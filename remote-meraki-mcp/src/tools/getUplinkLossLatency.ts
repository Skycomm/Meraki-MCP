import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

export async function getUplinkLossLatency(server: Server) {
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      {
        name: "get_uplink_loss_latency",
        description: "🚨 Get REAL packet loss and latency for organization uplinks (5 minutes)",
        inputSchema: {
          type: "object",
          properties: {
            org_id: {
              type: "string",
              description: "Organization ID",
            },
            timespan: {
              type: "number",
              description: "Timespan in seconds (default: 300, max: 300)",
              default: 300,
            },
          },
          required: ["org_id"],
        },
      },
    ],
  }));

  server.setRequestHandler("tools/call", async (request, context) => {
    if (request.params.name !== "get_uplink_loss_latency") return null;

    const apiKey = context.environment?.MERAKI_API_KEY;
    const userLogin = context.environment?.USER_LOGIN;

    const { org_id, timespan = 300 } = request.params.arguments as {
      org_id: string;
      timespan?: number;
    };

    // Validate timespan
    const validatedTimespan = Math.min(Math.max(1, timespan), 300);

    try {
      const response = await fetch(
        `https://api.meraki.com/api/v1/organizations/${org_id}/devices/uplinks/lossAndLatency?timespan=${validatedTimespan}`,
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

      const lossLatency = await response.json();

      if (!lossLatency || lossLatency.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: `No uplink loss/latency data found for organization ${org_id}.`,
            },
          ],
        };
      }

      // Build formatted result
      let result = `# 🚨 UPLINK LOSS & LATENCY REPORT\n\n`;
      result += `**Organization**: ${org_id}\n`;
      result += `**Time Period**: Last ${validatedTimespan / 60} minutes\n`;
      result += `**Total Uplinks**: ${lossLatency.length}\n`;
      result += `**Requested by**: ${userLogin}\n\n`;

      // Group by device serial
      const devices = {};
      for (const entry of lossLatency) {
        const serial = entry.serial || "Unknown";
        if (!devices[serial]) {
          devices[serial] = {
            network_id: entry.networkId || "Unknown",
            uplinks: [],
          };
        }
        devices[serial].uplinks.push(entry);
      }

      // Format output by device
      for (const [serial, deviceData] of Object.entries(devices)) {
        result += `## 📱 Device: ${serial}\n`;
        result += `Network: ${deviceData.network_id}\n\n`;

        for (const uplink of deviceData.uplinks) {
          const uplinkName = uplink.uplink || "Unknown";
          const ip = uplink.ip || "N/A";

          result += `### 🔗 ${uplinkName.toUpperCase()} (${ip})\n`;

          // Get time series data
          const timeSeries = uplink.timeSeries || [];

          if (timeSeries.length > 0) {
            // Get latest reading
            const latest = timeSeries[timeSeries.length - 1];
            const currentLoss = latest.lossPercent || 0;
            const currentLatency = latest.latencyMs || 0;

            // Calculate statistics
            const losses = timeSeries
              .map((p) => p.lossPercent)
              .filter((v) => v !== null && v !== undefined);
            const latencies = timeSeries
              .map((p) => p.latencyMs)
              .filter((v) => v !== null && v !== undefined);

            const avgLoss = losses.length > 0 ? losses.reduce((a, b) => a + b) / losses.length : 0;
            const maxLoss = losses.length > 0 ? Math.max(...losses) : 0;
            const avgLatency = latencies.length > 0 ? latencies.reduce((a, b) => a + b) / latencies.length : 0;
            const maxLatency = latencies.length > 0 ? Math.max(...latencies) : 0;

            // Status indicators
            const lossIndicator = currentLoss > 5 ? "🔴" : currentLoss > 1 ? "🟡" : "🟢";
            const latencyIndicator = currentLatency > 150 ? "🔴" : currentLatency > 50 ? "🟡" : "🟢";

            result += `**Current Status:**\n`;
            result += `- Packet Loss: ${currentLoss.toFixed(1)}% ${lossIndicator}\n`;
            result += `- Latency: ${currentLatency.toFixed(0)}ms ${latencyIndicator}\n\n`;

            result += `**5-Minute Statistics:**\n`;
            result += `- Avg Loss: ${avgLoss.toFixed(1)}% (Max: ${maxLoss.toFixed(1)}%)\n`;
            result += `- Avg Latency: ${avgLatency.toFixed(0)}ms (Max: ${maxLatency.toFixed(0)}ms)\n`;
            result += `- Data Points: ${timeSeries.length}\n\n`;

            // Alerts
            if (avgLoss > 1) {
              result += `⚠️ **WARNING**: Average packet loss above 1%!\n`;
            }
            if (avgLatency > 100) {
              result += `⚠️ **WARNING**: High average latency detected!\n`;
            }
          } else {
            result += "- **Status**: No data available\n";
          }

          result += "\n";
        }
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
            text: `Error retrieving uplink loss/latency data: ${error.message}`,
          },
        ],
      };
    }
  });
}