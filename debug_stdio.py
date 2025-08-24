#!/usr/bin/env python3
"""Debug stdio communication"""

import json
import sys
import asyncio
from contextlib import redirect_stderr, redirect_stdout
import io

# Redirect stdout/stderr to capture any print statements
debug_buffer = io.StringIO()

with redirect_stderr(debug_buffer):
    try:
        from server.main import app
        
        # Create a simple test that mimics what Claude Desktop would do
        async def test_stdio():
            # Read from stdin in a loop
            sys.stderr.write("Debug: Server starting in stdio mode...\n")
            sys.stderr.flush()
            
            # The app.run() method should handle stdio protocol
            # But let's see what happens
            await app.run_stdio_async()
        
        # Run the async function
        asyncio.run(test_stdio())
        
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.stderr.write(f"Debug output: {debug_buffer.getvalue()}\n")
        sys.stderr.flush()