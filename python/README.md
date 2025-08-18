# Meraki MCP Server - Python Implementation

This is an improved Python implementation of the Meraki MCP server following best practices from successful MCP implementations like mcp-mem0 and remote-mcp-server-with-auth.

## Features

### Core Functionality
- ✅ **Async/await support** for better performance
- ✅ **Rate limiting** to prevent API abuse
- ✅ **Response caching** for frequently accessed data
- ✅ **Structured logging** for better debugging
- ✅ **Role-based access control** for dangerous operations
- ✅ **Comprehensive error handling** with user-friendly messages

### Security
- 🔒 API key stored securely as environment variable
- 🔒 Privileged operations require user authorization
- 🔒 Rate limiting per user
- 🔒 Confirmation required for destructive operations

### Tools Implemented
- `list_organizations` - List all Meraki organizations
- `get_organization_networks` - Get networks in an organization
- `get_uplink_loss_latency` - Real-time packet loss and latency monitoring
- `reboot_device` - Reboot devices (privileged users only)
- `create_ping_test` - Run ping tests from devices
- `get_ping_test_results` - Get ping test results

## Installation

### Using pip/uv

```bash
# Clone the repository
git clone https://github.com/Skycomm/Meraki-MCP.git
cd Meraki-MCP/python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or using uv
uv pip install -r requirements.txt
```

### Using Docker

```bash
# Build the image
docker build -t meraki-mcp-python .

# Run with environment variables
docker run -e MERAKI_API_KEY="your-key" meraki-mcp-python
```

### Using Docker Compose

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your API key

# Start the service
docker-compose up -d
```

## Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `MERAKI_API_KEY` | Yes | Your Meraki Dashboard API key | - |
| `MERAKI_BASE_URL` | No | Custom API base URL | https://api.meraki.com/api/v1 |
| `CACHE_TTL` | No | Cache timeout in seconds | 300 |
| `RATE_LIMIT_REQUESTS` | No | Max requests per window | 100 |
| `RATE_LIMIT_WINDOW` | No | Rate limit window in seconds | 60 |
| `PRIVILEGED_USERS` | No | Comma-separated list of users who can perform dangerous operations | - |
| `LOG_LEVEL` | No | Logging level | INFO |

### Example .env file

```env
MERAKI_API_KEY=your-meraki-api-key-here
PRIVILEGED_USERS=admin@example.com,david,sarah
CACHE_TTL=300
RATE_LIMIT_REQUESTS=100
LOG_LEVEL=INFO
```

## Usage with Claude Desktop

Add this to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "meraki-python": {
      "command": "python",
      "args": ["-m", "meraki_mcp.server"],
      "cwd": "/path/to/meraki-mcp/python",
      "env": {
        "MERAKI_API_KEY": "your-api-key",
        "PRIVILEGED_USERS": "your-email@example.com"
      }
    }
  }
}
```

## Architecture

### Key Design Patterns

1. **Async/Await Pattern**
   - All API calls are asynchronous for better performance
   - Can handle multiple requests concurrently

2. **Decorator-based Tools**
   ```python
   @mcp.tool()
   async def list_organizations(context: Context) -> List[TextContent]:
       # Tool implementation
   ```

3. **Caching Strategy**
   - LRU cache for frequently accessed data
   - Cache invalidation based on time windows
   - Real-time data (like uplink stats) bypasses cache

4. **Rate Limiting**
   - Per-user rate limiting
   - Sliding window algorithm
   - Configurable limits

5. **Error Handling**
   - Consistent error response format
   - User-friendly error messages
   - Detailed logging for debugging

### Project Structure

```
python/
├── src/
│   └── meraki_mcp/
│       ├── __init__.py
│       └── server.py      # Main server implementation
├── tests/
│   ├── __init__.py
│   └── test_server.py     # Comprehensive test suite
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-container setup
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
└── .env.example          # Environment template
```

## Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=meraki_mcp

# Run specific tests
pytest tests/test_server.py::TestRateLimiting
```

## Development

### Code Style

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **Type hints** throughout

```bash
# Format code
black src tests

# Run linter
ruff check src tests

# Fix linting issues
ruff check --fix src tests
```

### Adding New Tools

1. Add the tool function with `@mcp.tool()` decorator:

```python
@mcp.tool()
async def my_new_tool(
    context: Context,
    param1: str = Field(description="Parameter description")
) -> List[TextContent]:
    """Tool description for users"""
    user_id = context.meta.get("user_id", "anonymous")
    
    # Check rate limit
    if not check_rate_limit(user_id):
        return format_response("Rate limit exceeded", False)
    
    # Tool implementation
    try:
        result = await meraki_client.get(f"/endpoint/{param1}")
        return format_response(f"Success: {result}")
    except Exception as e:
        logger.error(f"Error in my_new_tool: {e}")
        return format_response(f"Error: {str(e)}", False)
```

2. Add tests for the new tool
3. Update documentation

## Monitoring

### Logging

Structured logs are written to stdout with the following format:
```
2024-01-20 10:30:45 INFO [meraki_mcp.server] Listed 5 organizations for user david
2024-01-20 10:31:02 WARNING [meraki_mcp.server] Device Q2XX-XXXX rebooted by user admin@example.com
2024-01-20 10:31:15 ERROR [meraki_mcp.server] API error: 404 - Device not found
```

### Optional Sentry Integration

For production monitoring, add Sentry:

```python
# In .env
SENTRY_DSN=your-sentry-dsn-here

# The server will automatically initialize Sentry if DSN is provided
```

## Performance Considerations

1. **Caching**: Frequently accessed data is cached for 5 minutes by default
2. **Rate Limiting**: Prevents API exhaustion
3. **Async Operations**: Non-blocking I/O for better concurrency
4. **Connection Pooling**: HTTP client reuses connections

## Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Limit privileged users** - Only add trusted users to PRIVILEGED_USERS
3. **Require confirmations** - Destructive operations need explicit confirmation
4. **Log security events** - All privileged operations are logged
5. **Use HTTPS** - All API communication is encrypted

## Troubleshooting

### Common Issues

1. **"Rate limit exceeded"**
   - Wait 60 seconds for the rate limit to reset
   - Increase RATE_LIMIT_REQUESTS if needed

2. **"Access Denied" for reboot**
   - Ensure your user ID is in PRIVILEGED_USERS
   - Check the exact spelling/format

3. **"API key not configured"**
   - Set MERAKI_API_KEY environment variable
   - Check .env file is loaded

4. **Connection errors**
   - Verify internet connectivity
   - Check if Meraki API is accessible
   - Verify API key has proper permissions

### Debug Mode

Enable debug logging:

```bash
LOG_LEVEL=DEBUG python -m meraki_mcp.server
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - See LICENSE file for details