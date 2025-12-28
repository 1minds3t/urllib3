# urllib3-lts 🛡️

**The Long-Term Support Security Release for urllib3.**

This ecosystem backports critical security fixes to legacy Python environments (3.7 & 3.8) that official maintainers have dropped.

## 🏆 Patch Status (v2025.66471)

This release secures **941M+ downloads** against the following vulnerabilities:

| Vulnerability | Severity | Impact | Py3.7 | Py3.8 |
|:---|:---|:---|:---|:---|
| **CVE-2025-66471** | 🔴 HIGH | Compression Bomb DoS | 🛡️ Fixed | 🛡️ Fixed |
| **CVE-2025-66418** | 🔴 HIGH | Unbounded Links DoS | 🛡️ Fixed | 🛡️ Fixed |
| **CVE-2025-50182** | 🟡 MOD | Node.js Redirect Bypass | N/A | 🛡️ Fixed |
| **CVE-2025-50181** | 🟡 MOD | Redirect Retry Bypass | 🛡️ Fixed | 🛡️ Fixed |
| **CVE-2024-37891** | 🟡 MOD | Proxy-Auth Header Leak | 🛡️ Fixed | N/A |

## 📦 Usage

**Standard Installation:**
```bash
pip install urllib3-lts
```
*This meta-package automatically detects your Python version and installs the correct secured backport.*

## 🌐 The OmniPKG Ecosystem
Maintained by **1minds3t**.

**Manage your environment:**
```bash
pip install omnipkg
omnipkg reset -y
```

### 🚧 Coming Soon: omnipkg-runtime
We are building a runtime enforcer that allows configurable **WARN** or **BLOCK** policies for unpatched vulnerabilities. Stay tuned.
