#!/usr/bin/env python3
"""
Test the fixed audit tools with comprehensive output.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app, meraki
from server.tools_Custom_helpers import register_helper_tools

# Register the helper tools
register_helper_tools(app, meraki)

def test_mercy_bariatrics_audit():
    """Test the comprehensive audit on Mercy Bariatrics network."""
    
    print("🧪 TESTING FIXED COMPREHENSIVE AUDIT TOOLS")
    print("=" * 60)
    
    # Mercy Bariatrics network
    network_id = 'L_669347494617957322'
    
    print(f"Testing Network: {network_id} (Mercy Bariatrics - Mt Lawley)")
    print("\nRunning comprehensive security audit...\n")
    
    try:
        # Import the function directly for testing
        from server.tools_Custom_helpers import register_helper_tool_handlers
        
        # Re-register to ensure latest version
        register_helper_tool_handlers()
        
        # Get the perform_security_audit function
        perform_security_audit = None
        for tool in app._tools.values():
            if tool.name == 'perform_security_audit':
                perform_security_audit = tool.func
                break
        
        if perform_security_audit:
            result = perform_security_audit(network_id)
            print(result)
            print("\n✅ Audit completed successfully!")
        else:
            print("❌ Could not find perform_security_audit tool")
            
    except Exception as e:
        print(f"❌ Error running audit: {str(e)}")
        import traceback
        traceback.print_exc()

def test_network_health():
    """Test the network health check tool."""
    
    print("\n" + "=" * 60)
    print("🏥 TESTING NETWORK HEALTH CHECK")
    print("=" * 60)
    
    network_id = 'L_669347494617957322'
    
    try:
        # Get the check_network_health function
        check_network_health = None
        for tool in app._tools.values():
            if tool.name == 'check_network_health':
                check_network_health = tool.func
                break
        
        if check_network_health:
            result = check_network_health(network_id)
            print(result)
            print("\n✅ Health check completed successfully!")
        else:
            print("❌ Could not find check_network_health tool")
            
    except Exception as e:
        print(f"❌ Error running health check: {str(e)}")

if __name__ == "__main__":
    print("🎯 COMPREHENSIVE AUDIT TOOLS TEST")
    print("Testing enhanced security audit and health check tools\n")
    
    # Test security audit
    test_mercy_bariatrics_audit()
    
    # Test network health
    test_network_health()
    
    print("\n" + "=" * 60)
    print("📋 TEST COMPLETE")
    print("=" * 60)
    print("The audit tools should now:")
    print("✅ Work without API method errors")
    print("✅ Provide comprehensive security analysis")
    print("✅ Include security scoring (0-100)")
    print("✅ Show detailed WiFi security status")
    print("✅ Analyze VLANs, VPN, L7 rules, and clients")
    print("✅ Provide prioritized recommendations")