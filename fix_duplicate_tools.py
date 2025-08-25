#!/usr/bin/env python3
"""Fix duplicate tool registrations by commenting out duplicates in tools_networks.py."""

import re

def fix_duplicates():
    """Comment out duplicate tool registrations."""
    
    # Read the file
    with open('server/tools_networks.py', 'r') as f:
        content = f.read()
    
    # List of duplicate functions to comment out
    duplicates = [
        'get_network_mqtt_brokers',
        'get_network_mqtt_broker', 
        'create_network_mqtt_broker',
        'update_network_mqtt_broker',
        'delete_network_mqtt_broker',
        'get_network_snmp',
        'update_network_snmp',
        'get_network_syslog_servers',
        'update_network_syslog_servers'
    ]
    
    changes_made = []
    
    for func_name in duplicates:
        # Find the decorator and function definition
        pattern = rf'(\n    @app\.tool\(\s*name="{func_name}"[^)]*\)\s*def {func_name}\([^)]*\):)'
        
        matches = list(re.finditer(pattern, content, re.MULTILINE | re.DOTALL))
        
        if matches:
            for match in matches:
                # Get the start position
                start = match.start()
                
                # Find the end of the function (next @app.tool or end of register function)
                next_decorator = content.find('\n    @app.tool(', start + 1)
                end_of_register = content.find('\ndef register_', start + 1)
                
                # Determine the end position
                if next_decorator == -1:
                    end = end_of_register if end_of_register != -1 else len(content)
                elif end_of_register == -1:
                    end = next_decorator
                else:
                    end = min(next_decorator, end_of_register)
                
                # Extract the function
                func_content = content[start:end]
                
                # Comment it out with explanation
                commented = f"\n    # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)\n"
                commented += '\n'.join('    # ' + line if line.strip() else '    #' 
                                       for line in func_content.split('\n')[1:])
                
                # Replace in content
                content = content[:start] + commented + content[end:]
                changes_made.append(func_name)
                print(f"✓ Commented out {func_name}")
                break  # Only comment first occurrence
    
    # Write back the file
    with open('server/tools_networks.py', 'w') as f:
        f.write(content)
    
    print(f"\n✅ Fixed {len(changes_made)} duplicate tool registrations")
    return changes_made

if __name__ == "__main__":
    print("Fixing duplicate tool registrations...")
    print("-" * 40)
    fix_duplicates()