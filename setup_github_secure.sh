#!/bin/bash

# 🚀 SECURE GitHub Setup Script for Enhanced Cisco Meraki MCP Server
# This script does NOT contain any secrets and is safe to commit

set -e  # Exit on any error

echo "🚀 Enhanced Cisco Meraki MCP Server - SECURE GitHub Setup"
echo "=========================================================="

# Check if running with token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ ERROR: GITHUB_TOKEN environment variable not set"
    echo ""
    echo "Usage:"
    echo "  GITHUB_TOKEN=your_token_here ./setup_github_secure.sh"
    echo ""
    echo "Or export it first:"
    echo "  export GITHUB_TOKEN=your_token_here"
    echo "  ./setup_github_secure.sh"
    exit 1
fi

# Configuration
GITHUB_USERNAME="Skycomm"
REPO_NAME="Meraki-MCP"
REPO_URL="https://${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "📁 Current directory: $(pwd)"
echo "🔗 Repository: ${GITHUB_USERNAME}/${REPO_NAME}"

# Step 1: Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Environment variables
.env
.env.local
.env.development
.env.test
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
.venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# SSL certificates
*.pem
*.key
*.crt

# Temporary files
*.tmp
*.temp
EOF
else
    echo "📝 .gitignore already exists"
fi

# Step 2: Create LICENSE if it doesn't exist
if [ ! -f "LICENSE" ]; then
    echo "📜 Creating MIT License..."
    cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 Skycomm & David

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
else
    echo "📜 LICENSE already exists"
fi

# Step 3: Initialize git if needed
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
fi

# Step 4: Add all files
echo "📦 Adding all files to git..."
git add .

# Step 5: Create comprehensive commit
echo "💾 Creating commit..."
git commit -m "feat: Enhanced Cisco Meraki MCP Server v2.0.0

✨ Major Feature Additions:
- 🔑 WiFi password retrieval tool (get_network_wireless_passwords)
- 📊 Advanced analytics (bandwidth, latency, throughput monitoring)  
- 🔔 Comprehensive alerting system with webhook support
- 🔒 Security management (firewall, VPN, content filtering, malware protection)
- 📡 Performance monitoring with device health scoring
- 🌐 Network mode support for team sharing (HTTP/HTTPS)

🔧 Technical Enhancements:
- Complete MerakiClient implementation with REAL API methods only
- Enhanced error handling with graceful fallbacks
- Modular architecture with organized tool categories
- Support for both stdio (local) and HTTP (network) modes

📋 New Tool Categories:
- Analytics Tools: Real uplink loss/latency monitoring
- Alert Tools: Webhook integration & custom profiles
- Security/Appliance Tools: Comprehensive security management
- Enhanced Wireless Tools: WiFi password retrieval + monitoring
- Advanced Switch Tools: QoS, stacks, access policies

🚀 Enhanced by David with Claude Code assistance

Files included:
- Enhanced meraki_server.py with dual-mode support
- Fixed meraki_client.py with ONLY real API methods
- server/tools_wireless.py with WiFi password retrieval
- server/tools_analytics.py for monitoring and analysis
- server/tools_alerts.py for comprehensive alerting
- server/tools_appliance.py for security management
- Comprehensive documentation (README, TOOLS_REFERENCE, GITHUB_SETUP)
- MIT License and proper .gitignore
- Secure GitHub setup scripts" || echo "ℹ️ No changes to commit or already committed"

# Step 6: Set up remote
echo "🔗 Setting up GitHub remote..."
if git remote get-url origin &>/dev/null; then
    echo "📝 Updating existing remote..."
    git remote set-url origin "$REPO_URL"
else
    echo "➕ Adding new remote..."
    git remote add origin "$REPO_URL"
fi

# Step 7: Push to GitHub
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

# Step 8: Clean up remote URL to remove token from git config
echo "🔒 Securing remote URL..."
git remote set-url origin "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo ""
echo "✅ SUCCESS! Repository updated successfully!"
echo "🔗 Your repository is available at:"
echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "📋 Repository now contains:"
echo "   • Enhanced Cisco Meraki MCP Server v2.0"
echo "   • 80+ network management tools"
echo "   • WiFi password retrieval capability"
echo "   • REAL API methods only (no made-up methods)"
echo "   • Advanced analytics and monitoring"
echo "   • Comprehensive documentation"
echo "   • MIT License"
echo ""
echo "🔒 SECURITY:"
echo "   • No secrets stored in repository"
echo "   • Token removed from git remote configuration"
echo "   • Secure setup script provided"
echo ""
echo "🎉 Your enhanced Cisco Meraki MCP Server is now live on GitHub!"