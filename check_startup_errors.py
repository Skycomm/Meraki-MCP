#!/usr/bin/env python3
"""Check for startup errors in the MCP server."""

import sys
import traceback
from collections import defaultdict

# Add server directory to path
sys.path.insert(0, 'server')

def check_startup():
    """Check for common startup issues."""
    print("Checking MCP server startup...")
    
    # Track issues
    issues = []
    
    # 1. Check imports
    print("\n1. Checking module imports...")
    try:
        from main import app
        print("   ✓ Main app imported successfully")
    except ImportError as e:
        issues.append(f"Import error: {e}")
        print(f"   ✗ Import error: {e}")
        return issues
    except Exception as e:
        issues.append(f"Unexpected error during import: {e}")
        print(f"   ✗ Unexpected error: {e}")
        traceback.print_exc()
        return issues
    
    # 2. Check for duplicate tools
    print("\n2. Checking for duplicate tool names...")
    tool_counts = defaultdict(int)
    
    # Get all registered tools
    for tool_name in dir(app):
        if tool_name.startswith('_tool_'):
            tool_counts[tool_name] += 1
    
    duplicates = {k: v for k, v in tool_counts.items() if v > 1}
    if duplicates:
        issues.append(f"Found {len(duplicates)} duplicate tools")
        print(f"   ✗ Found {len(duplicates)} duplicate tools:")
        for name, count in list(duplicates.items())[:5]:
            print(f"      - {name}: {count} times")
    else:
        print("   ✓ No duplicate tools found")
    
    # 3. Check tool name lengths
    print("\n3. Checking tool name lengths...")
    long_names = []
    
    for tool_name in dir(app):
        if tool_name.startswith('_tool_'):
            # Extract actual tool name (remove _tool_ prefix)
            actual_name = tool_name[6:]  # Remove '_tool_' prefix
            if len(actual_name) > 64:
                long_names.append((actual_name, len(actual_name)))
    
    if long_names:
        issues.append(f"Found {len(long_names)} tools with names > 64 characters")
        print(f"   ✗ Found {len(long_names)} tools with names > 64 characters:")
        for name, length in long_names[:5]:
            print(f"      - {name[:50]}... ({length} chars)")
    else:
        print("   ✓ All tool names are within 64 character limit")
    
    # 4. Check for missing required modules
    print("\n4. Checking required modules...")
    required_modules = [
        'meraki',
        'dotenv',
        'mcp',
        'asyncio',
        'json',
        'logging'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✓ {module} module available")
        except ImportError:
            issues.append(f"Missing required module: {module}")
            print(f"   ✗ Missing required module: {module}")
    
    # 5. Check environment variables
    print("\n5. Checking environment variables...")
    import os
    if not os.getenv('MERAKI_API_KEY'):
        issues.append("MERAKI_API_KEY environment variable not set")
        print("   ✗ MERAKI_API_KEY not set")
    else:
        print("   ✓ MERAKI_API_KEY is set")
    
    return issues

if __name__ == "__main__":
    print("=" * 60)
    print("MCP Server Startup Diagnostic")
    print("=" * 60)
    
    issues = check_startup()
    
    print("\n" + "=" * 60)
    if issues:
        print(f"FOUND {len(issues)} ISSUES:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        print("\nThese issues may cause errors when starting conversations.")
    else:
        print("✅ No startup issues detected!")
    print("=" * 60)