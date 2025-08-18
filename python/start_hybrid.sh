#!/bin/bash
# Start the hybrid server locally for testing

echo "🚀 Starting Meraki MCP Hybrid Server..."

# Check for API key
if ! grep -q "MERAKI_API_KEY=" .env || grep -q "your-key-here" .env; then
    echo "❌ Please edit .env and add your actual MERAKI_API_KEY"
    exit 1
fi

# Load environment
source .env

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Run the hybrid server
echo "Starting server on http://localhost:8000"
python src/hybrid_server.py