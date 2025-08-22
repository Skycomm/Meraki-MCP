# Test Scripts - SAFE TESTING

## Safety Features

All test scripts in this directory are configured with **READ-ONLY MODE** by default.

### What This Means:
- ✅ **NO DELETE operations** will execute
- ✅ **NO UPDATE operations** will execute  
- ✅ **NO REBOOT operations** will execute
- ✅ **NO configuration changes** will be made
- ✅ **SAFE to run** in production environments

### How It Works:

Every test script imports `test_common.py` which:
1. Sets `MCP_READ_ONLY_MODE=true` 
2. Enables confirmation requirements
3. Enables audit logging
4. Shows clear safety status

### Running Tests:

```bash
# All tests are safe to run
python tests/test_all_apis.py
python tests/test_all_features.py
python tests/test_beta_features.py
```

### Test Output:

When you run any test, you'll see:
```
============================================================
🔒 TEST SAFETY MODE ENABLED
- Read-only mode: ACTIVE (no writes will be performed)
- Confirmations: ENABLED
- Audit logging: ENABLED

✅ SAFE TO RUN: No destructive operations will execute
   - NO deletes
   - NO updates
   - NO reboots
   - NO configuration changes
============================================================
```

### Override (NOT RECOMMENDED):

If you absolutely need to test write operations:
```bash
# DANGER: This allows actual changes!
export MCP_READ_ONLY_MODE=false
python tests/your_test.py
```

⚠️ **WARNING**: Only disable read-only mode if:
- You're using a test organization
- You understand the risks
- You have backups

### Test Scripts:

- `test_all_apis.py` - Tests all API methods (read operations only)
- `test_all_features.py` - Comprehensive feature testing
- `test_beta_features.py` - Beta/early access API testing
- `test_new_apis.py` - Tests for new 2025 APIs
- `test_suite36.py` - Health check for network devices
- `check_early_access.py` - Checks early access status
- `verify_api_structures.py` - Validates API response structures

All scripts skip destructive operations automatically.