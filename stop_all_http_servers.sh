#!/bin/bash
# Stop all running Meraki MCP HTTP/SSE servers

echo "🛑 Stopping All Meraki MCP HTTP/SSE Servers"
echo "==========================================="
echo ""

stopped_count=0

# Stop all servers using PID files
for pidfile in logs/*.pid; do
    if [ -f "$pidfile" ]; then
        pid=$(cat "$pidfile")
        profile=$(basename "$pidfile" .pid)
        
        if kill -0 $pid 2>/dev/null; then
            kill $pid
            echo "✅ Stopped $profile server (PID: $pid)"
            stopped_count=$((stopped_count + 1))
        else
            echo "⚠️  $profile server (PID: $pid) was not running"
        fi
        
        rm "$pidfile"
    fi
done

# Also check for any python http_server.py processes
echo ""
echo "Checking for any remaining HTTP server processes..."
for pid in $(ps aux | grep "[p]ython http_server.py" | awk '{print $2}'); do
    kill $pid 2>/dev/null
    echo "✅ Stopped orphaned server process (PID: $pid)"
    stopped_count=$((stopped_count + 1))
done

echo ""
if [ $stopped_count -eq 0 ]; then
    echo "No servers were running."
else
    echo "Stopped $stopped_count server(s)."
fi

echo ""
echo "To start servers again: ./start_all_http_servers.sh"