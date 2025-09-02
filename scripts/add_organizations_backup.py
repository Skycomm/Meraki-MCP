#!/usr/bin/env python3
"""
Script to add organizations tools from consolidated backup to current module.
Extracts all @app.tool functions and adds them to the organizations module.
"""

import re

def extract_and_add_backup_tools():
    """Extract tools from backup and add to current organizations module."""
    
    # Read the backup file
    print("📖 Reading backup file...")
    with open('server/backup/tools_organizations_consolidated.py', 'r') as f:
        backup_content = f.read()
    
    # Read current organizations file
    with open('server/tools_SDK_organizations.py', 'r') as f:
        current_content = f.read()
    
    # Extract all tool functions from backup (everything after the register function)
    # Find start of tools (after the register function definition)
    start_pattern = r'def register_organizations_tools.*?\):'
    start_match = re.search(start_pattern, backup_content, re.DOTALL)
    
    if start_match:
        tools_content = backup_content[start_match.end():]
        
        # Clean up the content - remove the function definition wrapper
        # Keep only the @app.tool functions and their implementations
        
        # Split into lines and find tool functions
        lines = tools_content.split('\n')
        tool_functions = []
        current_function = []
        in_function = False
        indent_level = 0
        
        for line in lines:
            # Skip empty lines at start
            if not line.strip() and not in_function:
                continue
                
            # Found a tool decorator
            if line.strip().startswith('@app.tool('):
                if current_function:  # Save previous function
                    tool_functions.append('\n'.join(current_function))
                current_function = [line]
                in_function = True
                indent_level = len(line) - len(line.lstrip())
            elif in_function:
                current_function.append(line)
                
                # Check if this line ends the function (next @app.tool or end of significant indentation)
                if line.strip() and not line.startswith(' ' * (indent_level + 1)) and not line.strip().startswith('@app.tool('):
                    # This line has less indentation, might be end of function
                    # But keep going until we hit another @app.tool or clear break
                    pass
        
        # Add the last function
        if current_function:
            tool_functions.append('\n'.join(current_function))
        
        print(f"🔍 Found {len(tool_functions)} tool functions in backup")
        
        # Add these functions to the register_backup_organizations_tools function
        tools_to_add = '\n\n    '.join(tool_functions)
        
        # Find the location to insert (after the first tool in register_backup_organizations_tools)
        insertion_point = current_content.find("return f\"❌ Error getting adaptive policy ACLs: {str(e)}\"")
        
        if insertion_point != -1:
            # Find end of that function
            end_point = current_content.find('\n\n', insertion_point) + 2
            
            # Insert all the backup tools
            new_content = (
                current_content[:end_point] + 
                '\n    # ==================== MORE BACKUP TOOLS ====================\n\n    ' +
                tools_to_add.replace('\n', '\n    ') +  # Add proper indentation
                '\n' +
                current_content[end_point:]
            )
            
            # Write the updated file
            with open('server/tools_SDK_organizations.py', 'w') as f:
                f.write(new_content)
            
            print(f"✅ Successfully added {len(tool_functions)} tools to organizations module")
            
            # Verify the count
            import subprocess
            result = subprocess.run(['grep', '-c', '@app.tool(', 'server/tools_SDK_organizations.py'], 
                                  capture_output=True, text=True)
            new_count = int(result.stdout.strip())
            print(f"🎯 New tool count: {new_count}")
            
        else:
            print("❌ Could not find insertion point in current file")
    else:
        print("❌ Could not find register function in backup file")

if __name__ == "__main__":
    extract_and_add_backup_tools()