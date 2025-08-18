import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

// Import Meraki tools
import { listOrganizations } from "./tools/listOrganizations.js";
import { getOrganizationNetworks } from "./tools/getOrganizationNetworks.js";
import { getNetworkDevices } from "./tools/getNetworkDevices.js";
import { getDeviceStatus } from "./tools/getDeviceStatus.js";
import { getUplinkLossLatency } from "./tools/getUplinkLossLatency.js";
import { rebootDevice } from "./tools/rebootDevice.js";
import { pingTest } from "./tools/pingTest.js";
import { throughputTest } from "./tools/throughputTest.js";

export interface Env {
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  MERAKI_API_KEY: string;
  PRIVILEGED_USERS: string;
  KV: KVNamespace;
}

async function verifyGitHubToken(token: string, env: Env): Promise<{ login: string } | null> {
  try {
    const response = await fetch('https://api.github.com/user', {
      headers: {
        'Authorization': `token ${token}`,
        'User-Agent': 'MCP-Server'
      }
    });

    if (!response.ok) {
      return null;
    }

    const data = await response.json() as { login: string };
    return data;
  } catch (error) {
    console.error('Error verifying GitHub token:', error);
    return null;
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 200,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization",
          "Access-Control-Max-Age": "86400",
        },
      });
    }

    // Handle OAuth callback
    if (url.pathname === '/oauth/callback') {
      const code = url.searchParams.get('code');
      if (!code) {
        return new Response('Missing code parameter', { status: 400 });
      }

      // Exchange code for token
      const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code: code
        })
      });

      const tokenData = await tokenResponse.json() as { access_token: string };
      
      if (!tokenData.access_token) {
        return new Response('Failed to get access token', { status: 400 });
      }

      // Verify the token and get user info
      const userInfo = await verifyGitHubToken(tokenData.access_token, env);
      if (!userInfo) {
        return new Response('Failed to verify token', { status: 400 });
      }

      // Store token in KV
      await env.KV.put(`token:${tokenData.access_token}`, JSON.stringify({
        login: userInfo.login,
        created: Date.now()
      }), {
        expirationTtl: 30 * 24 * 60 * 60 // 30 days
      });

      return new Response(`
        <html>
          <body>
            <h1>Authentication Successful!</h1>
            <p>Your token: <code>${tokenData.access_token}</code></p>
            <p>You can now use this token with your MCP client.</p>
            <script>
              // Auto-close after 5 seconds
              setTimeout(() => window.close(), 5000);
            </script>
          </body>
        </html>
      `, {
        headers: { 'Content-Type': 'text/html' }
      });
    }

    // Handle MCP requests
    if (url.pathname === '/') {
      // Check authentication
      const authHeader = request.headers.get('Authorization');
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return new Response('Unauthorized', { 
          status: 401,
          headers: {
            'WWW-Authenticate': 'Bearer',
            'Access-Control-Allow-Origin': '*'
          }
        });
      }

      const token = authHeader.substring(7);
      
      // Check if token exists in KV
      const tokenData = await env.KV.get(`token:${token}`);
      if (!tokenData) {
        return new Response('Invalid token', { 
          status: 401,
          headers: { 'Access-Control-Allow-Origin': '*' }
        });
      }

      const { login } = JSON.parse(tokenData) as { login: string };
      const isPrivileged = env.PRIVILEGED_USERS.split(',').includes(login);

      // Set up MCP server
      const server = new Server({
        name: "remote-meraki-mcp",
        version: "1.0.0",
        capabilities: {
          tools: {},
        },
      }, {
        environment: {
          MERAKI_API_KEY: env.MERAKI_API_KEY,
          USER_LOGIN: login,
          IS_PRIVILEGED: isPrivileged.toString()
        }
      });

      // Register tools based on user privileges
      // Read-only tools for all authenticated users
      await listOrganizations(server);
      await getOrganizationNetworks(server);
      await getNetworkDevices(server);
      await getDeviceStatus(server);
      await getUplinkLossLatency(server);
      await pingTest(server);
      await throughputTest(server);

      // Privileged tools only for specific users
      if (isPrivileged) {
        await rebootDevice(server);
      }

      // Create SSE transport
      const transport = new SSEServerTransport(url.pathname, request);
      await server.connect(transport);

      return transport.response;
    }

    // Home page with auth link
    if (url.pathname === '/auth') {
      const authUrl = `https://github.com/login/oauth/authorize?client_id=${env.GITHUB_CLIENT_ID}&scope=read:user`;
      return Response.redirect(authUrl, 302);
    }

    return new Response(`
      <html>
        <head>
          <title>Remote Meraki MCP Server</title>
          <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
            .button { display: inline-block; padding: 10px 20px; background: #0366d6; color: white; text-decoration: none; border-radius: 5px; }
          </style>
        </head>
        <body>
          <h1>Remote Meraki MCP Server</h1>
          <p>This is a secure, authenticated MCP server for Cisco Meraki management.</p>
          
          <h2>Getting Started</h2>
          <ol>
            <li><a href="/auth" class="button">Authenticate with GitHub</a></li>
            <li>Copy your token from the callback page</li>
            <li>Configure your MCP client with this server URL and token</li>
          </ol>
          
          <h2>Available Tools</h2>
          <h3>All Authenticated Users:</h3>
          <ul>
            <li><code>list_organizations</code> - List all Meraki organizations</li>
            <li><code>get_organization_networks</code> - Get networks in an organization</li>
            <li><code>get_network_devices</code> - Get devices in a network</li>
            <li><code>get_device_status</code> - Get device status</li>
            <li><code>get_uplink_loss_latency</code> - Get uplink packet loss and latency</li>
            <li><code>create_ping_test</code> - Run ping test from device</li>
            <li><code>create_throughput_test</code> - Run throughput test between devices</li>
          </ul>
          
          <h3>Privileged Users Only:</h3>
          <ul>
            <li><code>reboot_device</code> - Reboot a device (requires confirmation)</li>
          </ul>
          
          <h2>Configuration Example</h2>
          <pre>
{
  "mcpServers": {
    "meraki-remote": {
      "url": "${url.origin}/",
      "transport": "sse",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
          </pre>
        </body>
      </html>
    `, {
      headers: { 'Content-Type': 'text/html' }
    });
  },
};