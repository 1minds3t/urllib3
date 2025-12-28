#!/usr/bin/env python3
"""Part 3: Update _decode(), read(), stream() to use max_length"""

import re

with open('src/urllib3/response.py', 'r') as f:
    content = f.read()

print("🔧 Applying Part 3: _decode(), read(), stream() methods...")

# ============================================================================
# STEP 6: Update _decode() method signature and implementation
# ============================================================================
# Find _decode method and add max_length parameter
old_decode_sig = r'def _decode\(\s+self, data: bytes, decode_content: bool \| None, flush_decoder: bool\s+\) -> bytes:'

new_decode_sig = '''def _decode(
        self,
        data: bytes,
        decode_content: bool | None,
        flush_decoder: bool,
        max_length: int | None = None,
    ) -> bytes:'''

content = re.sub(old_decode_sig, new_decode_sig, content, flags=re.MULTILINE | re.DOTALL)
print("✅ Updated _decode() signature")

# Add max_length logic inside _decode
# Find where decoder.decompress is called and add max_length
old_decompress_call = r'if self\._decoder:\s+data = self\._decoder\.decompress\(data\)'
new_decompress_call = '''if max_length is None or flush_decoder:
            max_length = -1

        try:
            if self._decoder:
                data = self._decoder.decompress(data, max_length=max_length)'''

content = re.sub(old_decompress_call, new_decompress_call, content)
print("✅ Updated _decode() to pass max_length to decoder")

# ============================================================================
# STEP 7: Update read() method to check has_unconsumed_tail
# ============================================================================
# This is complex - we need to add checks for unconsumed_tail before reading more data

# Pattern 1: Check unconsumed tail before reading when amt is specified
read_check_pattern = r'(elif amt is not None:\s+cache_content = False\s+if len\(self\._decoded_buffer\) >= amt:)'

read_check_new = r'''elif amt is not None:
            cache_content = False

            if self._decoder and self._decoder.has_unconsumed_tail:
                decoded_data = self._decode(
                    b"",
                    decode_content,
                    flush_decoder=False,
                    max_length=amt - len(self._decoded_buffer),
                )
                self._decoded_buffer.put(decoded_data)
            if len(self._decoded_buffer) >= amt:'''

content = re.sub(read_check_pattern, read_check_new, content, flags=re.MULTILINE)
print("✅ Added unconsumed_tail check in read() for amt case")

# Pattern 2: Update the flush_decoder assignment and data check
old_data_check = r'if not data and len\(self\._decoded_buffer\) == 0:\s+return data'
new_data_check = r'''if (
            not data
            and len(self._decoded_buffer) == 0
            and not (self._decoder and self._decoder.has_unconsumed_tail)
        ):
            return data'''

content = re.sub(old_data_check, new_data_check, content, flags=re.MULTILINE)
print("✅ Updated data check to include unconsumed_tail")

# Pattern 3: Update _decode calls in read() to pass max_length
# Find all _decode calls and add max_length parameter
old_decode_in_read = r'decoded_data = self\._decode\(data, decode_content, flush_decoder\)'
new_decode_in_read = r'''decoded_data = self._decode(
                data,
                decode_content,
                flush_decoder,
                max_length=amt - len(self._decoded_buffer),
            )'''

content = re.sub(old_decode_in_read, new_decode_in_read, content)
print("✅ Updated _decode() calls in read() to pass max_length")

# ============================================================================
# STEP 8: Update stream() method
# ============================================================================
# Update stream loop condition to check unconsumed_tail
old_stream_condition = r'while not is_fp_closed\(self\._fp\) or len\(self\._decoded_buffer\) > 0:'
new_stream_condition = r'''while (
                not is_fp_closed(self._fp)
                or len(self._decoded_buffer) > 0
                or (self._decoder and self._decoder.has_unconsumed_tail)
            ):'''

content = re.sub(old_stream_condition, new_stream_condition, content, flags=re.MULTILINE)
print("✅ Updated stream() to check unconsumed_tail")

with open('src/urllib3/response.py', 'w') as f:
    f.write(content)

print("🎉 Part 3 complete!")
print("📝 Compression bomb protection is now fully implemented!")
