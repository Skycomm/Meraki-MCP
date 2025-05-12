#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRIPT_PATH="$SCRIPT_DIR/run_meraki_server.sh"

# Make sure run_meraki_server.sh is executable
chmod +x "$SCRIPT_PATH"

# Extract API key from .env file if available
API_KEY=""
if [ -f "$SCRIPT_DIR/.env" ]; then
    API_KEY=$(grep -o 'MERAKI_API_KEY=.*' "$SCRIPT_DIR/.env" | cut -d'=' -f2)
fi

# Generate the Claude Desktop configuration
CONFIG=$(cat <<EOF
{
  "mcpServers": {
    "meraki-mcp": {
      "command": "/bin/bash",
      "args": ["$SCRIPT_PATH"],
      "cwd": "$SCRIPT_DIR",
      "env": {
        "MERAKI_API_KEY": "$API_KEY"
      }
    }
  }
}
EOF
)

# Create a temporary file with the configuration
CONFIG_FILE="$SCRIPT_DIR/claude_config.json"
echo "$CONFIG" > "$CONFIG_FILE"

echo "==========================================================="
echo "Claude Desktop Configuration"
echo "==========================================================="
echo "A configuration file has been created at:"
echo "$CONFIG_FILE"
echo ""
echo "Copy and paste this configuration into Claude Desktop Settings:"
echo ""
cat "$CONFIG_FILE"
echo ""
echo "==========================================================="
echo "IMPORTANT: After copying the configuration, you can delete the"
echo "           claude_config.json file for security reasons."
echo "==========================================================="
