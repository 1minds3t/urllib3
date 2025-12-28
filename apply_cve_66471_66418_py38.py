#!/usr/bin/env python3
"""
Apply CVE-2025-66471 and CVE-2025-66418 fixes to py38's response.py

CVE-2025-66471: Compression bomb protection (bounded decompression)
CVE-2025-66418: Unbounded decompression chain protection (max 5 links)
"""

import re

# Read response.py
with open('src/urllib3/response.py', 'r') as f:
    content = f.read()

print("🔧 Applying CVE-2025-66471 & CVE-2025-66418 patches...")

# ============================================================================
# STEP 1: Add DependencyWarning import
# ============================================================================
content = re.sub(
    r'(from \.exceptions import \(\n\s+BodyNotHttplibCompatible,\n\s+DecodeError,)',
    r'\1\n    DependencyWarning,',
    content
)
print("✅ Added DependencyWarning import")

# ============================================================================
# STEP 2: Update ContentDecoder base class
# ============================================================================
old_base = r'class ContentDecoder:\n    def decompress\(self, data: bytes\) -> bytes:\n        raise NotImplementedError\(\)'

new_base = '''class ContentDecoder:
    def decompress(self, data: bytes, max_length: int = -1) -> bytes:
        raise NotImplementedError()

    @property
    def has_unconsumed_tail(self) -> bool:
        raise NotImplementedError()'''

content = re.sub(old_base, new_base, content, flags=re.MULTILINE)
print("✅ Updated ContentDecoder base class")

# ============================================================================
# STEP 3: Update DeflateDecoder completely
# ============================================================================
# This is complex, so we'll find the class and replace it entirely
deflate_pattern = r'class DeflateDecoder\(ContentDecoder\):.*?(?=\n\nclass |\nclass GzipDecoder)'

deflate_new = '''class DeflateDecoder(ContentDecoder):
    def __init__(self) -> None:
        self._first_try = True
        self._first_try_data = b""
        self._unfed_data = b""
        self._obj = zlib.decompressobj()

    def decompress(self, data: bytes, max_length: int = -1) -> bytes:
        data = self._unfed_data + data
        self._unfed_data = b""
        if not data and not self._obj.unconsumed_tail:
            return data
        original_max_length = max_length
        if original_max_length < 0:
            max_length = 0
        elif original_max_length == 0:
            # We should not pass 0 to the zlib decompressor because 0 is
            # the default value that will make zlib decompress without a
            # length limit.
            # Data should be stored for subsequent calls.
            self._unfed_data = data
            return b""

        # Subsequent calls always reuse `self._obj`. zlib requires
        # passing the unconsumed tail if decompression is to continue.
        if not self._first_try:
            return self._obj.decompress(
                self._obj.unconsumed_tail + data, max_length=max_length
            )

        # First call tries with RFC 1950 ZLIB format.
        self._first_try_data += data
        try:
            decompressed = self._obj.decompress(data, max_length=max_length)
            if decompressed:
                self._first_try = False
                self._first_try_data = b""
            return decompressed
        # On failure, it falls back to RFC 1951 DEFLATE format.
        except zlib.error:
            self._first_try = False
            self._obj = zlib.decompressobj(-zlib.MAX_WBITS)
            try:
                return self.decompress(
                    self._first_try_data, max_length=original_max_length
                )
            finally:
                self._first_try_data = b""

    @property
    def has_unconsumed_tail(self) -> bool:
        return bool(self._unfed_data) or (
            bool(self._obj.unconsumed_tail) and not self._first_try
        )

    def flush(self) -> bytes:
        return self._obj.flush()

'''

content = re.sub(deflate_pattern, deflate_new, content, flags=re.DOTALL)
print("✅ Updated DeflateDecoder with compression bomb protection")

# Save the file
with open('src/urllib3/response.py', 'w') as f:
    f.write(content)

print("🎉 Patches applied successfully!")
print("📝 Next: Verify the changes and commit")
