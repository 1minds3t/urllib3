#!/usr/bin/env python3
"""Part 3 FIXED: Update _decode(), read(), stream() to use max_length"""

import re

with open('src/urllib3/response.py', 'r') as f:
    content = f.read()

print("🔧 Applying Part 3 (Fixed): _decode(), read(), stream() methods...")

# ============================================================================
# STEP 6: Update _decode() method signature
# ============================================================================
old_decode_sig = r'    def _decode\(\s*self, data: bytes, decode_content: bool \| None, flush_decoder: bool\s*\) -> bytes:'

new_decode_sig = '''    def _decode(
        self,
        data: bytes,
        decode_content: bool | None,
        flush_decoder: bool,
        max_length: int | None = None,
    ) -> bytes:'''

content = re.sub(old_decode_sig, new_decode_sig, content, flags=re.MULTILINE)
print("✅ Updated _decode() signature")

# Find and replace the decoder.decompress call with max_length logic
# Look for the pattern after "return data" in _decode
old_decode_body = r'(\s+return data\s+)(try:\s+if self\._decoder:\s+data = self\._decoder\.decompress\(data\))'

new_decode_body = r'''\1
        if max_length is None or flush_decoder:
            max_length = -1

        try:
            if self._decoder:
                data = self._decoder.decompress(data, max_length=max_length)'''

content = re.sub(old_decode_body, new_decode_body, content, flags=re.MULTILINE | re.DOTALL)
print("✅ Updated _decode() to pass max_length to decoder")

# ============================================================================
# STEP 7: Update read() method to check has_unconsumed_tail
# ============================================================================
# Pattern 1: Add unconsumed_tail check after "cache_content = False"
old_read_check = r'(elif amt is not None:\s+cache_content = False\s+)(if len\(self\._decoded_buffer\) >= amt:)'

new_read_check = r'''\1
            if self._decoder and self._decoder.has_unconsumed_tail:
                decoded_data = self._decode(
                    b"",
                    decode_content,
                    flush_decoder=False,
                    max_length=amt - len(self._decoded_buffer),
                )
                self._decoded_buffer.put(decoded_data)
            \2'''

content = re.sub(old_read_check, new_read_check, content, flags=re.MULTILINE)
print("✅ Added unconsumed_tail check in read() for amt case")

# Pattern 2: Update the data check to include unconsumed_tail
old_data_check = r'        if not data and len\(self\._decoded_buffer\) == 0:\s+return data'

new_data_check = r'''        if (
            not data
            and len(self._decoded_buffer) == 0
            and not (self._decoder and self._decoder.has_unconsumed_tail)
        ):
            return data'''

content = re.sub(old_data_check, new_data_check, content, flags=re.MULTILINE)
print("✅ Updated data check to include unconsumed_tail")

# Pattern 3: Update _decode calls in read() to pass max_length
# This is tricky - need to find each occurrence individually

# First occurrence: in the "if amt is None" branch
old_decode1 = r'(if amt is None:.*?)(decoded_data = self\._decode\(data, decode_content, flush_decoder\))'
new_decode1 = r'''\1decoded_data = self._decode(
                data,
                decode_content,
                flush_decoder,
                max_length=amt - len(self._decoded_buffer),
            )'''
content = re.sub(old_decode1, new_decode1, content, flags=re.DOTALL)

# Second occurrence: in the while loop
old_decode2 = r'(while len\(self\._decoded_buffer\) < amt and data:.*?data = self\._raw_read\(amt\)\s+)(decoded_data = self\._decode\(data, decode_content, flush_decoder\))'
new_decode2 = r'''\1decoded_data = self._decode(
                    data,
                    decode_content,
                    flush_decoder,
                    max_length=amt - len(self._decoded_buffer),
                )'''
content = re.sub(old_decode2, new_decode2, content, flags=re.DOTALL)

print("✅ Updated _decode() calls in read() to pass max_length")

# ============================================================================
# STEP 8: Update stream() method
# ============================================================================
old_stream_condition = r'            while not is_fp_closed\(self\._fp\) or len\(self\._decoded_buffer\) > 0:'

new_stream_condition = r'''            while (
                not is_fp_closed(self._fp)
                or len(self._decoded_buffer) > 0
                or (self._decoder and self._decoder.has_unconsumed_tail)
            ):'''

content = re.sub(old_stream_condition, new_stream_condition, content, flags=re.MULTILINE)
print("✅ Updated stream() to check unconsumed_tail")

# ============================================================================
# STEP 9: Update read1() method (if it exists and needs updating)
# ============================================================================
# The read1 method also needs max_length in its _decode calls
old_read1_decode = r'(def read1.*?while True:.*?flush_decoder = not data\s+)(decoded_data = self\._decode\(data, decode_content, flush_decoder\))'
new_read1_decode = r'''\1decoded_data = self._decode(
                data,
                decode_content,
                flush_decoder,
                max_length=amt,
            )'''
content = re.sub(old_read1_decode, new_read1_decode, content, flags=re.DOTALL)
print("✅ Updated read1() to pass max_length")

with open('src/urllib3/response.py', 'w') as f:
    f.write(content)

print("🎉 Part 3 complete!")
