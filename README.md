# urllib3-lts-py38 🛡️

**Security Backport for Python 3.8**
Base: `urllib3 v2.2.3` | Patch Level: `2025.66471`

## 🚨 Security Fixes Included
This release backports fixes for **4 Critical/High/Moderate Vulnerabilities** found in the official `v2.2.3` release.

| CVE ID | Severity | Description | Status |
|:---|:---|:---|:---|
| **CVE-2025-66471** | 🔴 HIGH | **Compression Bomb DoS:** Added `max_length` limits to decompression. | 🛡️ **FIXED** |
| **CVE-2025-66418** | 🔴 HIGH | **Unbounded Links:** Limited decompression chain depth. | 🛡️ **FIXED** |
| **CVE-2025-50182** | 🟡 MOD | **Node.js Bypass:** Enforced manual redirects in emscripten. | 🛡️ **FIXED** |
| **CVE-2025-50181** | 🟡 MOD | **Redirect Bypass:** Fixed retry logic when redirects disabled. | 🛡️ **FIXED** |

## 📦 Installation
```bash
pip install urllib3-lts-py38==2025.66471
```

## 🌐 The OmniPKG Ecosystem
Maintained by **1minds3t**.

**Manage your environment:**
```bash
pip install omnipkg
omnipkg reset -y
```

## ⚠️ Installation Warning

**Uninstall urllib3 before installing this package:**

```bash
pip uninstall urllib3 -y
pip install urllib3-lts-py38
```

This ensures the security patches are applied and not overwritten.
