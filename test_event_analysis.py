#!/usr/bin/env python3
"""
Test Event Log Analysis Tools
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.tools_event_analysis import (
    search_event_logs,
    analyze_error_patterns,
    identify_root_causes,
    correlate_events,
    generate_incident_timeline,
    event_analysis_help
)

# Test data
NETWORK_ID = "L_669347494617953785"  # Taiwan network

def test_event_analysis_tools():
    """Test all event analysis tools."""
    print("🧪 Testing Event Log Analysis Tools")
    print("=" * 60)
    
    # Test 1: Help tool
    print("\n1️⃣ Testing event_analysis_help()...")
    result = event_analysis_help()
    print(f"✅ Help returned: {len(result)} characters")
    assert "Event Log Analysis" in result
    
    # Test 2: Search event logs
    print("\n2️⃣ Testing search_event_logs()...")
    result = search_event_logs(
        network_id=NETWORK_ID,
        search_term="authentication",
        timespan=3600
    )
    print(f"✅ Search returned: {len(result)} characters")
    assert "Event Log Search" in result or "No events found" in result
    
    # Test 3: Analyze error patterns
    print("\n3️⃣ Testing analyze_error_patterns()...")
    result = analyze_error_patterns(
        network_id=NETWORK_ID,
        pattern_type="authentication",
        timespan=86400
    )
    print(f"✅ Pattern analysis returned: {len(result)} characters")
    assert "Error Pattern Analysis" in result
    
    # Test 4: Identify root causes
    print("\n4️⃣ Testing identify_root_causes()...")
    result = identify_root_causes(
        network_id=NETWORK_ID,
        issue_description="Users can't connect to WiFi",
        timespan=3600
    )
    print(f"✅ Root cause analysis returned: {len(result)} characters")
    assert "Root Cause Analysis" in result
    
    # Test 5: Correlate events
    print("\n5️⃣ Testing correlate_events()...")
    result = correlate_events(
        network_id=NETWORK_ID,
        timestamp="2025-01-20T10:00:00Z",
        window_minutes=30
    )
    print(f"✅ Event correlation returned: {len(result)} characters")
    assert "Event Correlation" in result
    
    # Test 6: Generate incident timeline
    print("\n6️⃣ Testing generate_incident_timeline()...")
    result = generate_incident_timeline(
        network_id=NETWORK_ID,
        start_time="2025-01-20T09:00:00Z",
        end_time="2025-01-20T11:00:00Z",
        incident_type="outage"
    )
    print(f"✅ Incident timeline returned: {len(result)} characters")
    assert "Incident Timeline" in result
    
    print("\n✅ All Event Log Analysis tools tested successfully!")
    
    # Natural language tests
    print("\n" + "=" * 60)
    print("🗣️ Natural Language Tests")
    print("=" * 60)
    
    natural_language_tests = [
        {
            "question": "Find all authentication failures in the last hour",
            "expected_tool": "search_event_logs",
            "test": lambda: search_event_logs(NETWORK_ID, search_term="authentication failed", timespan=3600)
        },
        {
            "question": "What error patterns are happening?",
            "expected_tool": "analyze_error_patterns", 
            "test": lambda: analyze_error_patterns(NETWORK_ID)
        },
        {
            "question": "Why can't users connect to the network?",
            "expected_tool": "identify_root_causes",
            "test": lambda: identify_root_causes(NETWORK_ID, "Users can't connect")
        },
        {
            "question": "What happened around 10:30 AM?",
            "expected_tool": "correlate_events",
            "test": lambda: correlate_events(NETWORK_ID, "2025-01-20T10:30:00Z")
        },
        {
            "question": "Create an incident report for this morning's outage",
            "expected_tool": "generate_incident_timeline",
            "test": lambda: generate_incident_timeline(NETWORK_ID, "2025-01-20T09:00:00Z", "2025-01-20T12:00:00Z", "outage")
        },
        {
            "question": "How do I use the event analysis tools?",
            "expected_tool": "event_analysis_help",
            "test": lambda: event_analysis_help()
        }
    ]
    
    passed = 0
    for test in natural_language_tests:
        print(f"\n❓ \"{test['question']}\"")
        print(f"   Expected tool: {test['expected_tool']}")
        try:
            result = test['test']()
            if result and len(result) > 0:
                print("   ✅ Tool executed successfully")
                print(f"   Preview: {result[:100]}...")
                passed += 1
            else:
                print("   ❌ Tool returned empty result")
        except Exception as e:
            print(f"   ❌ Tool failed: {e}")
    
    print(f"\n📊 Natural Language Tests: {passed}/{len(natural_language_tests)} passed")
    
    return passed == len(natural_language_tests)

if __name__ == "__main__":
    success = test_event_analysis_tools()
    sys.exit(0 if success else 1)