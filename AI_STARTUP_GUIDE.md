# AI Startup Guide - Meraki MCP Server Reorganization

## 🎯 Your Mission
Reorganize the Meraki MCP Server to match Cisco's official API structure by extracting mixed APIs from the mega-module `tools_networks.py` into dedicated category modules.

## 📚 Files You Should Read First (in this order)

### 1. **REORGANIZATION_PLAN.md** 
- The complete plan with step-by-step instructions
- Lists all functions to extract and where they are
- Has the implementation checklist

### 2. **server/tools_networks.py**
- The mega-module with 86 functions
- Contains 66 functions that need to be extracted
- Key sections:
  - Lines 733-844: Group Policies (10 functions)
  - Lines 625-687: Floor Plans (14 functions)
  - Lines 362-394: Bluetooth Clients (5 functions)
  - Lines 1761-1895: PII Management (14 functions)
  - Lines 938-1025: Meraki Auth Users (10 functions)

### 3. **server/main.py**
- Shows how tools are currently registered
- You'll need to update this to register new modules
- Current registration pattern around lines 22-127

### 4. **Example Module: server/tools_devices.py**
- Read this to understand the correct module structure
- Shows the pattern for:
  - Module docstring
  - Global variables (app, meraki_client)
  - Function structure
  - Registration function at the end

### 5. **FINAL_API_COVERAGE_ANALYSIS.md**
- Shows current API coverage
- Identifies what's missing
- Maps official Cisco categories to our modules

## ⚠️ Critical Information

### Current Problems
- **tools_networks.py has 86 functions** mixing many API categories
- When you run the server, you'll see "Tool already exists" errors for duplicates
- The server works but is hard to maintain

### What NOT to Do
- Don't delete functions from tools_networks.py until tested
- Don't change function signatures when extracting
- Don't create modules that duplicate existing ones

### What TO Do
1. Extract functions exactly as they are
2. Comment out (don't delete) originals in tools_networks.py first
3. Test each new module before proceeding
4. Follow the exact pattern from existing modules

## 🚀 Quick Start Commands

```bash
# Check current structure
ls -la server/tools_*.py | wc -l  # Should show 51 modules

# Count functions in tools_networks.py
grep -c "def " server/tools_networks.py  # Shows 86 functions

# Test if server works
python server/main.py  # Will show "Tool already exists" errors

# After creating a new module, test it
python -m py_compile server/tools_[new_module].py
```

## 📝 Template for New Modules

```python
"""
[Category] management tools for Cisco Meraki MCP Server.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_[category]_tools(mcp_app, meraki):
    """Register [category] tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # [Extract functions here from tools_networks.py]
    
    # Register all functions at the end
```

## 🎯 Success Criteria
1. tools_networks.py reduced from 86 to ~20 functions
2. 7 new modules created from extracted functions
3. No "Tool already exists" errors when starting server
4. All 765+ functions still working
5. Clear 1:1 mapping with Cisco's API categories

## 📊 Progress Tracking
Use the checklist in REORGANIZATION_PLAN.md to track progress.

## 💡 Tips
- Start with one category (recommend Group Policies - it's self-contained)
- Test after each extraction
- Keep the original line numbers as comments for reference
- Use git commits after each successful extraction

Good luck! This reorganization will make the codebase much more maintainable.