import sys

file_path = "src/urllib3/util/retry.py"
target_string = 'DEFAULT_REMOVE_HEADERS_ON_REDIRECT = frozenset(["Cookie", "Authorization"])'
replacement = 'DEFAULT_REMOVE_HEADERS_ON_REDIRECT = frozenset(["Cookie", "Authorization", "Proxy-Authorization"])'

with open(file_path, "r") as f:
    content = f.read()

if target_string in content:
    new_content = content.replace(target_string, replacement)
    with open(file_path, "w") as f:
        f.write(new_content)
    print("✅ Successfully patched CVE-2024-37891 in src/urllib3/util/retry.py")
else:
    print("❌ Target line not found! Please check the file content manually.")
    sys.exit(1)
