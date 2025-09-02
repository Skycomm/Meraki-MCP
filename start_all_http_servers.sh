#!/bin/bash
# Start all Meraki MCP HTTP/SSE servers with different profiles
# Each server runs on a different port for simultaneous use

echo "🚀 Starting All Meraki MCP HTTP/SSE Servers"
echo "============================================"
echo ""

# Set API key if not already set
export MERAKI_API_KEY="${MERAKI_API_KEY:-1ac5962056ad56da8cea908864f136adc5878a43}"

# Function to start a server in background
start_server() {
    local profile=$1
    local port=$2
    local description=$3
    
    echo "Starting $profile server on port $port..."
    
    # Export environment variables
    export MCP_PROFILE=$profile
    export SERVER_PORT=$port
    export AUTH_TOKENS_ADMIN="admin-$profile-token"
    export AUTH_TOKENS_READONLY="readonly-$profile-token"
    export MCP_READ_ONLY_MODE=false
    
    # Start server in background
    nohup .venv/bin/python http_server.py > logs/http_${profile}_${port}.log 2>&1 &
    local pid=$!
    
    # Save PID for later
    echo $pid > logs/${profile}.pid
    
    # Check if started successfully
    sleep 2
    if kill -0 $pid 2>/dev/null; then
        echo "✅ $profile server started (PID: $pid) - $description"
        echo "   URL: http://localhost:$port"
    else
        echo "❌ Failed to start $profile server"
    fi
    echo ""
}

# Create logs directory if it doesn't exist
mkdir -p logs

# Kill any existing servers
echo "Stopping any existing servers..."
for pidfile in logs/*.pid; do
    if [ -f "$pidfile" ]; then
        pid=$(cat "$pidfile")
        if kill -0 $pid 2>/dev/null; then
            kill $pid 2>/dev/null
            echo "Stopped server with PID $pid"
        fi
        rm "$pidfile"
    fi
done
echo ""

# Start all servers
start_server "WIRELESS" "8001" "~179 tools (Wireless, RF, SSIDs)"
start_server "NETWORK" "8002" "~402 tools (Switch, Appliance, VPN)"
start_server "ORGANIZATIONS" "8003" "~126 tools (Org admin, policies)"
start_server "MONITORING" "8004" "~141 tools (Devices, cameras, analytics)"
start_server "FULL" "8000" "833 tools (Complete API coverage)"

echo "============================================"
echo "All servers started! Available endpoints:"
echo ""
echo "  Wireless:      http://localhost:8001"
echo "  Network:       http://localhost:8002"
echo "  Organizations: http://localhost:8003"
echo "  Monitoring:    http://localhost:8004"
echo "  Full:          http://localhost:8000"
echo ""
echo "Health check endpoints:"
echo "  curl http://localhost:8001/health"
echo "  curl http://localhost:8002/health"
echo "  curl http://localhost:8003/health"
echo "  curl http://localhost:8004/health"
echo "  curl http://localhost:8000/health"
echo ""
echo "Logs available in: logs/"
echo ""
echo "To stop all servers: ./stop_all_http_servers.sh"