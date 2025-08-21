# Cisco Meraki MCP Server

A Model Context Protocol (MCP) server for the Cisco Meraki Dashboard API, providing natural language access to 400+ network management functions through Claude Desktop.

## 🎯 Key Features

- **400+ Functions**: Complete Meraki Dashboard API v1.61.0 coverage
- **Natural Language**: Ask questions in plain English
- **Real-time Monitoring**: Live bandwidth, device status, and analytics
- **Enterprise Ready**: OAuth 2.0, batch operations, and API analytics
- **2025 Features**: Environmental sensors, 5G gateways, enhanced MDM

## 📖 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- [Features Overview](FEATURES.md) - Complete capability list
- [API Reference](https://developer.cisco.com/meraki/api-v1/)

## 🚀 Quick Start

```bash
# 1. Clone and build
git clone https://github.com/yourusername/cisco-meraki-mcp-server.git
cd cisco-meraki-mcp-server
docker build -t meraki-mcp-server .

# 2. Set API key
export MERAKI_API_KEY="your-api-key"

# 3. Test
docker run -e MERAKI_API_KEY=$MERAKI_API_KEY meraki-mcp-server
```

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

## 💬 Example Usage

```text
"What's the bandwidth usage at main office?"
"Show me all offline devices"
"Block Facebook on guest network"
"Lock John's lost iPhone"
"Generate network health report"
```

## 🧪 Testing

```bash
# Run comprehensive test suite (400+ tests)
python test_all_400_plus_functions.py
```

## 📊 What's Included

| Category | Functions | Examples |
|----------|-----------|----------|
| Networks & Devices | 80+ | Device status, inventory, configuration |
| Security | 60+ | Firewall, VPN, content filtering |
| Wireless | 50+ | SSID management, RF optimization |
| Monitoring | 70+ | Bandwidth, analytics, alerts |
| Systems Manager | 40+ | MDM, app deployment, compliance |
| New 2025 Features | 100+ | Sensors, OAuth, 5G, API analytics |

**Total**: 400+ functions covering ~90% of Meraki API v1.61.0

## 🔧 Advanced Configuration

### Environment Variables
```bash
MERAKI_API_KEY=your-key     # Required
LOG_LEVEL=INFO             # Optional (DEBUG, INFO, WARNING)
API_TIMEOUT=30             # Optional (seconds)
```

### Rate Limiting
Automatically handles Meraki's 10 req/sec limit with smart retry logic.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No organizations found" | Verify API key and permissions |
| "Rate limit exceeded" | Wait 1 minute, server auto-retries |
| "Connection timeout" | Check firewall allows HTTPS to api.meraki.com |
| Bandwidth shows 0 | Update to latest version (fixed) |

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/cisco-meraki-mcp-server/issues)
- **Documentation**: [/docs](./docs)
- **API Reference**: [Meraki API Docs](https://developer.cisco.com/meraki/api-v1/)

---

**Version**: 2.0.0-beta | **API**: v1.61.0 | **Updated**: August 2025

*This is an unofficial integration not affiliated with Cisco Meraki.*