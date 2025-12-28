#!/usr/bin/env python3
"""Fix the _decode method syntax error"""

with open('src/urllib3/response.py', 'r') as f:
    lines = f.readlines()

# Find and fix the duplicate try block around line 577-580
result = []
skip_next_try = False
for i, line in enumerate(lines):
    # Look for the pattern where we have duplicate try blocks
    if i > 0 and 'try:' in line and 'try:' in lines[i-1]:
        # Skip the duplicate try
        skip_next_try = True
        continue
    
    # Also fix the malformed if statement
    if skip_next_try and 'if max_length is None or flush_decoder:' in line:
        # This line should be inside the try block but was orphaned
        result.append('        try:\n')
        result.append(line)
        skip_next_try = False
        continue
    
    result.append(line)

with open('src/urllib3/response.py', 'w') as f:
    f.writelines(result)

print("✅ Fixed duplicate try block")
