# Beta Release Notes - v2.0.0-beta

## 🎉 What's New

### Major Enhancements
- **400+ Functions**: Doubled functionality from ~200 to 400+ functions
- **Complete API Coverage**: ~90% coverage of Meraki Dashboard API v1.61.0
- **Natural Language Support**: Enhanced query processing for all functions
- **Fixed Critical Issues**: Bandwidth monitoring now shows real data (was showing 0)

### New Feature Categories (200+ new functions)
- 🌡️ **Environmental Sensors**: Temperature, humidity, air quality, water leak detection
- 📶 **Cellular Gateways**: 5G/LTE management, eSIM support, signal monitoring
- 🔐 **OAuth 2.0**: Modern authentication with token management
- 📊 **API Analytics**: Usage dashboards, rate limit monitoring, performance metrics
- 🔧 **Enhanced Licensing**: Per-device licensing, subscriptions, optimization
- 📱 **Enhanced MDM**: Advanced device commands, compliance, security policies
- 🌐 **SD-WAN**: Traffic policies, VoIP priority, custom performance classes
- 🔒 **Adaptive Policy**: Microsegmentation, Zero Trust, SGT assignments
- 📡 **MQTT Streaming**: Real-time data streaming for sensors
- 📋 **Config Templates**: Bulk deployment and management
- 🔔 **Webhooks**: Slack/Teams integration, custom receivers
- 📝 **Syslog/SNMP**: Enhanced monitoring and logging
- 🔑 **SAML SSO**: Okta, Azure AD integration
- 🎨 **Branding**: Custom dashboard themes and logos

## 🐛 Bug Fixes
- Fixed bandwidth monitoring showing 0 Mbps
- Standardized all API calls to use positional parameters
- Fixed API client reference inconsistencies
- Improved error handling across all modules

## 📦 What's Included
- `README.md` - Streamlined documentation
- `QUICKSTART.md` - 5-minute setup guide
- `FEATURES.md` - Complete feature overview
- `test_all_400_plus_functions.py` - Comprehensive test suite
- 49 tool modules in `server/` directory
- Docker support with automated builds

## 🧪 Testing
- 400+ test cases covering all functions
- 100% pass rate on all tests
- Critical bandwidth test verified
- Natural language query support

## 🚀 Getting Started
```bash
docker build -t meraki-mcp-server .
docker run -e MERAKI_API_KEY=$MERAKI_API_KEY meraki-mcp-server
```

## 📝 Notes
- Requires Meraki Dashboard API key with appropriate permissions
- Supports Meraki Dashboard API v1.61.0 (August 2025)
- Backward compatible with existing implementations
- Rate limiting handled automatically

## 🙏 Acknowledgments
Thanks to all contributors and testers who helped make this release possible!