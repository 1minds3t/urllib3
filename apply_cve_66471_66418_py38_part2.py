#!/usr/bin/env python3
"""Part 2: Update GzipDecoder and MultiDecoder"""

import re

with open('src/urllib3/response.py', 'r') as f:
    content = f.read()

print("🔧 Applying Part 2: GzipDecoder + MultiDecoder patches...")

# ============================================================================
# STEP 4: Update GzipDecoder completely
# ============================================================================
# Find and replace GzipDecoder class
gzip_pattern = r'class GzipDecoder\(ContentDecoder\):.*?(?=\nif brotli is not None:|\nclass BrotliDecoder|\nclass MultiDecoder)'

gzip_new = '''class GzipDecoder(ContentDecoder):
    def __init__(self) -> None:
        self._obj = zlib.decompressobj(16 + zlib.MAX_WBITS)
        self._state = GzipDecoderState.FIRST_MEMBER
        self._unconsumed_tail = b""

    def decompress(self, data: bytes, max_length: int = -1) -> bytes:
        ret = bytearray()
        if self._state == GzipDecoderState.SWALLOW_DATA:
            return bytes(ret)

        if max_length == 0:
            # We should not pass 0 to the zlib decompressor because 0 is
            # the default value that will make zlib decompress without a
            # length limit.
            # Data should be stored for subsequent calls.
            self._unconsumed_tail += data
            return b""

        # zlib requires passing the unconsumed tail to the subsequent
        # call if decompression is to continue.
        data = self._unconsumed_tail + data
        if not data and self._obj.eof:
            return bytes(ret)

        while True:
            try:
                ret += self._obj.decompress(
                    data, max_length=max(max_length - len(ret), 0)
                )
            except zlib.error:
                previous_state = self._state
                # Ignore data after the first error
                self._state = GzipDecoderState.SWALLOW_DATA
                self._unconsumed_tail = b""
                if previous_state == GzipDecoderState.OTHER_MEMBERS:
                    # Allow trailing garbage acceptable in other gzip clients
                    return bytes(ret)
                raise

            self._unconsumed_tail = data = (
                self._obj.unconsumed_tail or self._obj.unused_data
            )
            if max_length > 0 and len(ret) >= max_length:
                break

            if not data:
                return bytes(ret)
            # When the end of a gzip member is reached, a new decompressor
            # must be created for unused (possibly future) data.
            if self._obj.eof:
                self._state = GzipDecoderState.OTHER_MEMBERS
                self._obj = zlib.decompressobj(16 + zlib.MAX_WBITS)

        return bytes(ret)

    @property
    def has_unconsumed_tail(self) -> bool:
        return bool(self._unconsumed_tail)

    def flush(self) -> bytes:
        return self._obj.flush()


'''

content = re.sub(gzip_pattern, gzip_new, content, flags=re.DOTALL)
print("✅ Updated GzipDecoder with compression bomb protection")

# ============================================================================
# STEP 5: Add max_decode_links to MultiDecoder (CVE-2025-66418)
# ============================================================================
# Find MultiDecoder __init__ and add the check
multidecoder_init_old = r'class MultiDecoder\(ContentDecoder\):\s+""".*?"""\s+def __init__\(self, modes: str\) -> None:\s+self\._decoders = \[_get_decoder\(m\.strip\(\)\) for m in modes\.split\(","\)\]'

multidecoder_init_new = '''class MultiDecoder(ContentDecoder):
    """
    From RFC7231:
        If one or more encodings have been applied to a representation, the
        sender that applied the encodings MUST generate a Content-Encoding
        header field that lists the content codings in the order in which
        they were applied.
    """

    # Maximum allowed number of chained HTTP encodings in the
    # Content-Encoding header.
    max_decode_links = 5

    def __init__(self, modes: str) -> None:
        encodings = [m.strip() for m in modes.split(",")]
        if len(encodings) > self.max_decode_links:
            raise DecodeError(
                "Too many content encodings in the chain: "
                f"{len(encodings)} > {self.max_decode_links}"
            )
        self._decoders = [_get_decoder(e) for e in encodings]'''

content = re.sub(multidecoder_init_old, multidecoder_init_new, content, flags=re.DOTALL)
print("✅ Added CVE-2025-66418 protection (max 5 decode links)")

# Update MultiDecoder.decompress method
multidecoder_decompress_old = r'(class MultiDecoder.*?def flush.*?\n\s+def decompress\(self, data: bytes\) -> bytes:\s+for d in reversed\(self\._decoders\):\s+data = d\.decompress\(data\)\s+return data)'

# This is complex, let me search for it differently
if 'def decompress(self, data: bytes) -> bytes:' in content:
    # Find MultiDecoder's decompress and replace it
    lines = content.split('\n')
    in_multidecoder = False
    in_decompress = False
    result_lines = []
    skip_until_next_method = False
    
    for i, line in enumerate(lines):
        if 'class MultiDecoder(ContentDecoder):' in line:
            in_multidecoder = True
        elif in_multidecoder and line.startswith('class ') and 'MultiDecoder' not in line:
            in_multidecoder = False
        
        if in_multidecoder and '    def decompress(self, data: bytes) -> bytes:' in line:
            in_decompress = True
            skip_until_next_method = True
            # Insert new decompress method
            result_lines.append('    def decompress(self, data: bytes, max_length: int = -1) -> bytes:')
            result_lines.append('        if max_length <= 0:')
            result_lines.append('            for d in reversed(self._decoders):')
            result_lines.append('                data = d.decompress(data)')
            result_lines.append('            return data')
            result_lines.append('')
            result_lines.append('        ret = bytearray()')
            result_lines.append('        # Every while loop iteration goes through all decoders once.')
            result_lines.append('        while True:')
            result_lines.append('            any_data = False')
            result_lines.append('            for d in reversed(self._decoders):')
            result_lines.append('                data = d.decompress(data, max_length=max_length - len(ret))')
            result_lines.append('                if data:')
            result_lines.append('                    any_data = True')
            result_lines.append('            ret += data')
            result_lines.append('            if not any_data or len(ret) >= max_length:')
            result_lines.append('                return bytes(ret)')
            result_lines.append('            data = b""')
            result_lines.append('')
            result_lines.append('    @property')
            result_lines.append('    def has_unconsumed_tail(self) -> bool:')
            result_lines.append('        return any(d.has_unconsumed_tail for d in self._decoders)')
            continue
        
        if skip_until_next_method:
            # Skip old decompress body until we hit next method or end of class
            if line.strip() and not line.startswith('        ') and not line.startswith('\t\t'):
                skip_until_next_method = False
            else:
                continue
        
        result_lines.append(line)
    
    content = '\n'.join(result_lines)
    print("✅ Updated MultiDecoder.decompress with max_length support")

with open('src/urllib3/response.py', 'w') as f:
    f.write(content)

print("🎉 Part 2 complete!")
