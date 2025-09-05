#!/usr/bin/env python3
"""
Test the audit as an MCP client would call it - simulating Claude Desktop usage.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app, meraki

def test_mcp_audit_mercy_bariatrics():
    """Test MCP audit call for Mercy Bariatrics MX65W network."""
    
    print("🧪 TESTING MCP CLIENT AUDIT - MERCY BARIATRICS MX65W")
    print("=" * 70)
    
    network_id = 'L_669347494617957322'  # Mt Lawley (MX65W only)
    
    try:
        # This simulates how Claude Desktop would call the audit tool through MCP
        print("📞 Calling perform_security_audit() through MCP server...")
        print(f"Network ID: {network_id}")
        print("-" * 70)
        
        # Get the tool from the registered MCP tools (like Claude Desktop would)
        tool_registry = app._tools
        audit_tool = None
        
        for tool_name, tool_info in tool_registry.items():
            if tool_name == "perform_security_audit":
                audit_tool = tool_info
                break
                
        if not audit_tool:
            raise Exception("perform_security_audit tool not found in MCP registry")
            
        # Call the tool handler directly (simulating MCP call)
        result = audit_tool.handler(network_id)
        
        print("📋 AUDIT RESULT:")
        print("=" * 70)
        print(result)
        print("=" * 70)
        
        # Check for key indicators that it's working correctly
        success_indicators = []
        issues = []
        
        if "MX65W integrated wireless" in result:
            success_indicators.append("✅ Correctly identified MX65W integrated wireless")
        else:
            issues.append("❌ Failed to identify MX65W integrated wireless")
            
        if "WiFi provided by security appliance" in result:
            success_indicators.append("✅ Correctly noted WiFi source")
        else:
            issues.append("❌ Missing WiFi source context")
            
        if "no separate access points" in result:
            success_indicators.append("✅ Correctly noted no separate APs")
        else:
            issues.append("❌ Missing AP context")
            
        # Check that it doesn't make unnecessary wireless monitoring calls
        if "Connection Success Rate" not in result:
            success_indicators.append("✅ Correctly skipped connection stats for MX-only")
        else:
            issues.append("❌ Still checking connection stats for MX-only network")
            
        print("\n📊 ASSESSMENT:")
        print("=" * 70)
        
        if success_indicators:
            print("SUCCESS INDICATORS:")
            for indicator in success_indicators:
                print(f"  {indicator}")
                
        if issues:
            print("\nISSUES FOUND:")
            for issue in issues:
                print(f"  {issue}")
        
        if len(success_indicators) >= 3 and len(issues) == 0:
            print(f"\n🎉 SUCCESS: MCP audit now works correctly for MX*W networks!")
            print(f"✅ No more 'scanning as if there is a MR' behavior")
            print(f"✅ Infrastructure-aware messaging implemented")
            print(f"✅ Proper context for integrated wireless")
            return True
        else:
            print(f"\n⚠️ ISSUES REMAIN: {len(issues)} problems detected")
            return False
            
    except Exception as e:
        print(f"❌ MCP CLIENT TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_mcp_audit_mercy_bariatrics()
    
    if success:
        print("\n" + "=" * 70)
        print("🎯 FINAL RESULT: MCP CLIENT TEST PASSED!")
        print("The audit now properly handles MX*W integrated wireless.")
        print("No more unnecessary wireless API calls for MX-only networks.")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("❌ MCP CLIENT TEST FAILED - Review implementation")
        print("=" * 70)