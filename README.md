# urllib3-lts-py37 🛡️

**Security Backport for Python 3.7**
Base: `urllib3 v2.0.7` | Patch Level: `2025.66471`

## 🚨 Security Fixes Included

| CVE ID | Severity | Description |
|:---|:---|:---|
| **CVE-2025-66471** | 🔴 HIGH | **Compression Bomb DoS:** Added `max_length` limits to decompression. |
| **CVE-2025-66418** | 🔴 HIGH | **Unbounded Links:** Limited decompression chain depth. |
| **CVE-2025-50181** | 🟡 MOD | **Redirect Bypass:** Fixed retry logic when redirects disabled. |
| **CVE-2024-37891** | 🟡 MOD | **Header Leak:** Strips Proxy-Authorization on redirect. |

## 📦 Installation
```bash
pip install urllib3-lts-py37==2025.66471
```

## 🌐 The OmniPKG Ecosystem
Maintained by **1minds3t**.

*   **[filelock-lts](https://pypi.org/project/filelock-lts/)**: Secure file locking for legacy Python.
*   **[omnipkg](https://pypi.org/project/omnipkg/)**: The ultimate environment scanner.

**Scan your whole environment for vulnerabilities:**
```bash
pip install omnipkg
omnipkg scan --fix
```
