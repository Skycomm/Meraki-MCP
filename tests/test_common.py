#!/usr/bin/env python3
"""
Common test utilities and safety configuration for all test scripts.
"""

import os
import sys

def setup_test_safety():
    """
    Set up safety features for testing.
    This should be called at the start of every test script.
    
    IMPORTANT: This ensures NO DELETE, UPDATE, or REBOOT operations
    will actually execute during testing.
    """
    # Force read-only mode for all tests
    os.environ['MCP_READ_ONLY_MODE'] = 'true'
    
    # Ensure confirmations are enabled
    os.environ['MCP_REQUIRE_CONFIRMATIONS'] = 'true'
    
    # Enable audit logging
    os.environ['MCP_AUDIT_LOGGING'] = 'true'
    
    print("=" * 60)
    print("🔒 TEST SAFETY MODE ENABLED")
    print("- Read-only mode: ACTIVE (no writes will be performed)")
    print("- Confirmations: ENABLED") 
    print("- Audit logging: ENABLED")
    print("")
    print("✅ SAFE TO RUN: No destructive operations will execute")
    print("   - NO deletes")
    print("   - NO updates") 
    print("   - NO reboots")
    print("   - NO configuration changes")
    print("=" * 60)
    print()
    
    # Add parent directory to path for imports
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)

def print_safety_reminder():
    """Print a reminder about test safety."""
    print("\n" + "=" * 60)
    print("🔒 REMINDER: Running in READ-ONLY mode")
    print("No actual changes will be made to your Meraki environment")
    print("=" * 60 + "\n")