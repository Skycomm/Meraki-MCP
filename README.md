# Cisco Meraki MCP Server

An MCP (Model Context Protocol) server that integrates with Cisco Meraki's API, allowing AI assistants to interact with and manage Meraki network infrastructure.

## Author Information
- **Author:** Tomas Vince
- **Version:** 1.0.0
- **Date:** May 01, 2025
- **Contact:** [LinkedIn](https://linkedin.com/in/tomasvince)

## Overview

This MCP server provides a bridge between AI assistants (like Claude) and Cisco Meraki dashboard API. It enables AI assistants to:

- Browse and access Meraki organizations, networks, and devices
- View network clients, wireless SSIDs, VLANs, and switch ports
- Monitor alerts and firmware upgrades
- Get detailed information about devices
- Access camera video links
- Update switch port configurations

## Features

- **Resource Access**: Browse Meraki resources in a hierarchical structure
- **Interactive Tools**: Perform specific operations with friendly input/output formatting
- **Modular Structure**: Organized code for maintainability and extension
- **Docker Support**: Simple containerization for easy deployment
- **Authentication**: Secure access with Meraki API keys

## Installation

### Prerequisites

- Python 3.8 or higher
- Cisco Meraki API key
- uv package manager (recommended by MCP SDK)
- Docker (optional, for containerized deployment)

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/tomique34/cisco-meraki-mcp-server-tvi.git
   cd cisco-meraki-mcp-server-tvi
   ```

2. Install uv (if not already installed):
   ```bash
   # Using pip
   pip install uv
   
   # Alternative: using curl (macOS/Linux)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Create and activate a Python virtual environment using uv:
   ```bash
   # Create a virtual environment
   uv venv
   
   # Activate on Windows
   .venv\Scripts\activate
   
   # Activate on macOS/Linux
   source .venv/bin/activate
   ```

4. Install dependencies using uv:
   ```bash
   uv pip install -r requirements.txt
   ```

5. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

6. Edit the `.env` file and add your Meraki API key:
   ```
   MERAKI_API_KEY=your-api-key-here
   ```

### Standard Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tomique34/cisco-meraki-mcp-server-tvi.git
   cd cisco-meraki-mcp-server-tvi
   ```

2. Install dependencies using uv:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Run the server using uv:
   ```bash
   uv run meraki_server.py
   ```

### Docker Installation Options

#### Option 1: Using Docker Run

1. Build the Docker image:
   ```bash
   docker build -t meraki-mcp-server .
   ```

2. Run the container with environment variable:
   ```bash
   docker run -e MERAKI_API_KEY="your-api-key-here" meraki-mcp-server
   ```
   
   Or using the .env file:
   ```bash
   docker run --env-file .env meraki-mcp-server
   ```

#### Option 2: Using Docker Compose

1. Make sure your `.env` file is configured properly with your Meraki API key.

2. Start the service:
   ```bash
   docker-compose up -d
   ```

3. View logs:
   ```bash
   docker-compose logs -f
   ```

4. Stop the service:
   ```bash
   docker-compose down
   ```

### Kubernetes Deployment

The included Docker Compose file can be used as a reference when creating Kubernetes manifests. For a Kubernetes deployment:

1. Create a ConfigMap or Secret for the environment variables
2. Use the Docker image in your deployment specification
3. Configure proper health checks and resource limits

Example of converting the environment variables to a Kubernetes Secret:
```bash
kubectl create secret generic meraki-secrets --from-env-file=.env
```

## Usage with Claude Desktop

### Easiest Method: Automated Installation Script

For the simplest setup with Claude Desktop, use the included installation script:

1. Run the installation script:
   ```bash
   ./install_in_claude.sh
   ```

2. The script will:
   - Generate a properly formatted Claude Desktop configuration
   - Automatically detect your project paths
   - Extract your API key from the .env file (if available)
   - Create a temporary configuration file you can copy and paste

3. Copy the generated configuration into Claude Desktop settings

This is the most user-friendly approach, requiring minimal manual steps.

### Recommended Approach: Using the Shell Script

The reliable way to use this MCP server with Claude Desktop is via the included shell script, which automatically handles path resolution and environment setup:

1. Ensure the script is executable (only needed once):
   ```bash
   chmod +x run_meraki_server.sh
   ```

2. Add this configuration to your Claude Desktop settings:
   ```json
   {
     "mcpServers": {
       "meraki-mcp": {
         "command": "/bin/bash",
         "args": ["/absolute/path/to/run_meraki_server.sh"],
         "env": {
           "MERAKI_API_KEY": "your-api-key-here"
         }
       }
     }
   }
   ```

3. Replace `/absolute/path/to/run_meraki_server.sh` with the full path to the script on your system.

This approach has several advantages:
- Handles virtual environment activation automatically
- Works with both standard Python and uv installations
- Uses relative paths internally to avoid hardcoding
- Provides clear error messages if the environment isn't set up

### Alternative: Direct uv Approach

If you prefer using uv directly (may require additional environment setup):

```json
{
  "mcpServers": {
    "meraki": {
      "command": "uv",
      "args": ["run", "/absolute/path/to/meraki_server.py"],
      "cwd": "/absolute/path/to/project",
      "env": {
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Alternative: Direct Python Approach

For a simpler setup using the standard Python interpreter:

```json
{
  "mcpServers": {
    "meraki": {
      "command": "python3",
      "args": ["/absolute/path/to/meraki_server.py"],
      "cwd": "/absolute/path/to/project",
      "env": {
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Note:** In all cases, you'll need to replace placeholders with actual paths and your API key. The shell script approach is recommended as it requires the least amount of configuration.

### Option 2: Running as Docker Container

1. Ensure your container is running and the port is exposed:
   ```bash
   docker run -p 8000:8000 -e MERAKI_API_KEY="your-api-key-here" meraki-mcp-server
   ```

2. Run the MCP Inspector with the HTTP URL:
   ```bash
   mcp-inspector --http http://localhost:8000
   ```

### Option 3: Using Docker Socket

You can also configure Claude Desktop to start the Docker container on demand:

```json
{
  "mcpServers": {
    "meraki": {
      "docker": {
        "image": "meraki-mcp-server:latest",
        "env": {
          "MERAKI_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

This approach requires Claude Desktop to have access to the Docker socket, which allows it to create and manage containers on your behalf. Make sure the Docker image is built on your system before using this option.

## Architecture

The server is organized into the following modules:

- `server/main.py`: Core server setup and initialization
- `server/resources.py`: Resource handling functions
- `server/tools_organizations.py`: Organization-related tools
- `server/tools_networks.py`: Network-related tools
- `server/tools_devices.py`: Device-related tools
- `server/tools_wireless.py`: Wireless (SSIDs) related tools
- `server/tools_switch.py`: Switch ports related tools
- `meraki_client.py`: Client for interacting with the Meraki API
- `utils/helpers.py`: Utility functions for resource handling

## Tools Overview

### Organization Tools
- `list_organizations`: List all available Meraki organizations
- `get_organization_networks`: Get networks in an organization
- `get_organization_alerts`: Get alert settings for an organization
- `get_firmware_upgrades`: Get firmware upgrades for an organization

### Network Tools
- `get_network_devices`: Get devices in a network
- `get_network_clients`: Get clients connected to a network
- `get_vlans`: Get VLANs configured in a network

### Device Tools
- `get_device_details`: Get detailed info about a specific device
- `get_camera_video_link`: Get a video link for a Meraki camera

### Wireless Tools
- `get_ssids`: Get wireless SSIDs in a network
- `get_wireless_clients`: Get wireless clients connected to a network

### Switch Tools
- `get_switch_ports`: Get ports on a Meraki switch
- `update_switch_port`: Update switch port configuration

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| MERAKI_API_KEY | Yes | Your Meraki Dashboard API key |
| API_BASE_URL | No | Custom API base URL (default: https://api.meraki.com/api/v1) |
| TIMEOUT | No | Request timeout in seconds (default: 30) |

## Modernized Implementation (MCP SDK 1.6.0)

A modernized version of the server has been implemented following the latest MCP SDK 1.6.0 standards. This implementation uses the recommended `FastMCP` class and decorator patterns for resources and tools.

### Key Improvements

- **Modern FastMCP Class**: Replaced the older `mcp.Server` with the recommended `FastMCP` class
- **Decorator Pattern**: Used decorators for resource and tool registration instead of explicit functions
- **Parameterized Resource Paths**: Implemented URI templates like `organizations://{org_id}` for cleaner resource addressing
- **Simplified Resource Handling**: More direct mapping between URIs and resource handlers
- **Enhanced Maintainability**: Code is more concise and follows current best practices
- **Using uv**: Switched to uv as recommended by the MCP SDK team

### Using the Modernized Server

To use the modernized implementation:

```bash
# Run the modernized server using uv
uv run meraki_server.py
```

This uses the updated implementation that follows the MCP SDK 1.6.0 patterns.

### Architecture of Modernized Implementation

The modernized server is organized into the following modules:

- `server/modern_main.py`: Core server setup using FastMCP
- `server/modern_resources.py`: Resource handlers using decorator pattern
- `server/modern_tools_organizations.py`: Organization tools using decorator pattern
- `server/modern_tools_networks.py`: Network tools using decorator pattern
- `server/modern_tools_devices.py`: Device tools using decorator pattern
- `server/modern_tools_wireless.py`: Wireless tools using decorator pattern
- `server/modern_tools_switch.py`: Switch tools using decorator pattern

### Example of Modern Resource Pattern

```python
@app.resource("organizations://{org_id}")
def get_organization(org_id):
    """Get details for a specific organization."""
    return meraki_client.get_organization(org_id)
```

### Example of Modern Tool Pattern

```python
@app.tool(
    name="list_organizations",
    description="List all Meraki organizations the API key has access to"
)
def list_organizations():
    """List all Meraki organizations the API key has access to."""
    return meraki_client.get_organizations()
```

## Troubleshooting

### Common Issues

- **API Key Errors**: Make sure your API key is valid and has the proper permissions
- **Resource Not Found**: Verify that the organization/network/device exists and is accessible with your API key
- **Permission Denied**: Check that your API key has the necessary permissions for the operation
- **Docker Issues**: Ensure your Docker environment has access to the environment variables

### Logs

The server logs detailed information about errors. Check the logs when troubleshooting:

```bash
# When running directly
uv run meraki_server.py 2> meraki_server.log

# When running with Docker
docker logs meraki-mcp-server

# When running with Docker Compose
docker-compose logs meraki-mcp-server
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Cisco Meraki for providing the Dashboard API
- The Meraki Python SDK developers
- MCP specification contributors

## Testing with MCP Inspector

The MCP Inspector is a valuable tool for testing and debugging MCP servers. It allows you to interact with the server directly to verify functionality before integrating with Claude or other AI assistants.

### Installing MCP Inspector

1. Install the MCP Inspector tool:
   ```bash
   pip install mcp-inspector
   ```

2. Verify the installation:
   ```bash
   mcp-inspector --version
   ```

### Testing the Local Server

To test a locally running instance of the Meraki MCP server:

1. Start the server in one terminal:
   ```bash
   uv run meraki_server.py
   ```

2. In another terminal, run the MCP Inspector:
   ```bash
   mcp-inspector --stdio "uv run meraki_server.py"
   ```

3. The interactive inspector will start, allowing you to:
   - List available resources
   - Read specific resources
   - Execute tools
   - View raw request/response communication

### Testing a Dockerized Server

To test a server running in a Docker container:

1. Ensure your container is running and the port is exposed:
   ```bash
   docker run -p 8000:8000 -e MERAKI_API_KEY="your-api-key-here" meraki-mcp-server
   ```

2. Run the MCP Inspector with the HTTP URL:
   ```bash
   mcp-inspector --http http://localhost:8000
   ```

### Common Test Commands

Once in the MCP Inspector interface, try these commands:

- `list_resources`: View all available resources
- `read_resource meraki://organizations`: View all organizations
- `execute list_organizations`: Run the list organizations tool
- `execute get_organization_networks [org_id]`: Get networks for a specific organization
- `info`: Get information about the server
- `help`: See available commands

### Validation Tips

- Verify that all resources are correctly listed and accessible
- Check that tool execution returns properly formatted results
- Test error handling by providing invalid inputs
- Confirm that resource paths follow the expected format
- Test any write operations carefully in a non-production environment

## Security Considerations

- The API key grants access to your Meraki infrastructure, so keep it secure
- Store your API key in the `.env` file which is excluded from version control
- The server doesn't implement additional authentication beyond the API key
- Consider running the server in a secure environment or network
- Never expose the MCP server to the public internet
- When using Docker or Kubernetes, use secrets management for handling the API key
