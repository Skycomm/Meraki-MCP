#!/bin/bash

# Rename confusing wireless files to better names
cd /Users/david/docker/cisco-meraki-mcp-server-tvi/server/

# Backup first
echo "Creating backups..."
cp tools_wireless_complete.py tools_wireless_complete.py.backup
cp tools_wireless_final.py tools_wireless_final.py.backup  
cp tools_wireless_100.py tools_wireless_100.py.backup
cp tools_wireless_missing.py tools_wireless_missing.py.backup

# Rename to logical names
echo "Renaming files to logical names..."
mv tools_wireless_complete.py tools_wireless_ssid_features.py
mv tools_wireless_final.py tools_wireless_organization.py
mv tools_wireless_100.py tools_wireless_client_analytics.py
mv tools_wireless_missing.py tools_wireless_infrastructure.py

echo "✅ Files renamed successfully"
echo ""
echo "New structure:"
echo "  tools_wireless.py - Basic SSID/client operations"
echo "  tools_wireless_firewall.py - Security/firewall rules" 
echo "  tools_wireless_advanced.py - Connection/performance stats"
echo "  tools_wireless_rf_profiles.py - RF/radio management"
echo "  tools_wireless_ssid_features.py - Advanced SSID features (was complete)"
echo "  tools_wireless_organization.py - Org-wide analytics (was final)"
echo "  tools_wireless_client_analytics.py - Client stats/health (was 100)"
echo "  tools_wireless_infrastructure.py - Infrastructure/RADSEC (was missing)"
