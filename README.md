# urllib3-lts 🛡️

**The Long-Term Support Security Release for urllib3.**

This ecosystem backports critical security fixes to legacy Python environments (3.7 & 3.8) that official maintainers have dropped.

## 🏆 Patch Status (v2025.66471)

| Vulnerability | Severity | Impact | Status |
|:---|:---|:---|:---|
| **CVE-2025-66471** | 🔴 HIGH | Compression Bomb DoS | 🛡️ **FIXED** |
| **CVE-2025-66418** | 🔴 HIGH | Unbounded Links DoS | 🛡️ **FIXED** |
| **CVE-2025-50182** | 🟡 MOD | Node.js Redirect Bypass | 🛡️ **FIXED** |
| **CVE-2025-50181** | 🟡 MOD | Redirect Retry Bypass | 🛡️ **FIXED** |
| **CVE-2024-37891** | 🟡 MOD | Proxy-Auth Header Leak | 🛡️ **FIXED** |

## 📦 Usage

**Standard Installation:**
```bash
pip install urllib3-lts
```
*This meta-package automatically detects your Python version and installs the correct secured backport.*

## 🌐 The OmniPKG Ecosystem
Maintained by **1minds3t**.

*   **[filelock-lts](https://pypi.org/project/filelock-lts/)**: Secure file locking for legacy Python.
*   **[omnipkg](https://pypi.org/project/omnipkg/)**: The ultimate environment scanner.

**Scan your whole environment for vulnerabilities:**
```bash
pip install omnipkg
omnipkg scan --fix
```

### 🚧 Coming Soon: omnipkg-runtime
We are building a runtime enforcer that allows configurable **WARN** or **BLOCK** policies for unpatched vulnerabilities. Stay tuned.
