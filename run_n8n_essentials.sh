#!/bin/bash
#
# Run Cisco Meraki MCP Server with N8N_ESSENTIALS profile  
# Exactly 128 hand-picked tools for N8N automation workflows
#

export MCP_PROFILE=N8N_ESSENTIALS

echo "🚀 Starting Cisco Meraki MCP Server"
echo "🎯 Profile: N8N Essentials (128 tools max)"
echo "💡 Perfect for: N8N automation workflows"
echo "📊 Features: Client lookup, network diagnostics, performance monitoring"
echo ""
echo "🔍 Your automated workflow:"
echo "   1. Caller ID → Client lookup"
echo "   2. Network discovery → Device status"
echo "   3. Performance checks → Health alerts"
echo "   4. Instant diagnostics for support tickets"
echo ""

.venv/bin/python meraki_server.py