# Cisco Meraki MCP Server

This project is a Model Context Protocol (MCP) server that integrates with Cisco Meraki's API, allowing AI assistants to interact with Meraki network infrastructure.

## Project Structure

```
Cisco-Meraki-MCP-Server/
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── meraki_server.py           # Main MCP server implementation
├── config.py                  # Configuration utilities
├── meraki_client.py           # Meraki API client
└── utils/
    ├── __init__.py            # Package initializer
    └── helpers.py             # Helper utilities
```

## Setup Instructions

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Meraki API key:
   ```bash
   export MERAKI_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file with:
   ```
   MERAKI_API_KEY=your-api-key-here
   ```

3. Run the server:
   ```bash
   python meraki_server.py
   ```

## Using with Claude Desktop

Configure Claude Desktop to use this server by adding the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "meraki": {
      "command": "python",
      "args": ["/path/to/Cisco-Meraki-MCP-Server/meraki_server.py"],
      "env": {
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```
