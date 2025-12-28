#!/bin/bash
set -e

VERSION="2025.66471"
AUTHOR_NAME="1minds3t"
AUTHOR_EMAIL="1minds3t@proton.me"

# --- 1. UPDATE PYTHON 3.7 BRANCH ---
echo "🔧 Updating py37 metadata to v$VERSION..."
git checkout py37

cat > pyproject.toml << TOML
[build-system]
requires = ["hatchling>=1.6.0"]
build-backend = "hatchling.build"

[project]
name = "urllib3-lts-py37"
version = "$VERSION"
description = "LTS Security Backport for urllib3 (Python 3.7)"
readme = "README.md"
requires-python = ">=3.7, <3.8"
license = "MIT"
authors = [{name = "$AUTHOR_NAME", email = "$AUTHOR_EMAIL"}]
classifiers = [
    "Programming Language :: Python :: 3.7",
    "Topic :: Security",
]
dependencies = []

[project.urls]
Homepage = "https://github.com/1minds3t/urllib3-lts"
TOML

cat > README.md << MD
# urllib3-lts-py37 🛡️

**Security Backport for Python 3.7**
Base: \`urllib3 v2.0.7\` | Patch Level: \`$VERSION\`

## 🚨 Security Fixes Included

| CVE ID | Severity | Description |
|:---|:---|:---|
| **CVE-2025-66471** | 🔴 HIGH | **Compression Bomb DoS:** Added \`max_length\` limits to decompression. |
| **CVE-2025-66418** | 🔴 HIGH | **Unbounded Links:** Limited decompression chain depth. |
| **CVE-2025-50181** | 🟡 MOD | **Redirect Bypass:** Fixed retry logic when redirects disabled. |
| **CVE-2024-37891** | 🟡 MOD | **Header Leak:** Strips Proxy-Authorization on redirect. |

## 📦 Installation
\`\`\`bash
pip install urllib3-lts-py37==$VERSION
\`\`\`

## 🌐 The OmniPKG Ecosystem
Maintained by **1minds3t**.

*   **[filelock-lts](https://pypi.org/project/filelock-lts/)**: Secure file locking for legacy Python.
*   **[omnipkg](https://pypi.org/project/omnipkg/)**: The ultimate environment scanner.

**Scan your whole environment for vulnerabilities:**
\`\`\`bash
pip install omnipkg
omnipkg scan --fix
\`\`\`
MD

git add pyproject.toml README.md
git commit -m "Meta: Bump version to $VERSION" || echo "No changes to commit"
# Move tag to this final state
git tag -f -a CVE-2025-66471-py37 -m "Release: $VERSION (Full Patch Set)"


# --- 2. UPDATE PYTHON 3.8 BRANCH ---
echo "🔧 Updating py38 metadata to v$VERSION..."
git checkout py38

cat > pyproject.toml << TOML
[build-system]
requires = ["hatchling>=1.6.0"]
build-backend = "hatchling.build"

[project]
name = "urllib3-lts-py38"
version = "$VERSION"
description = "LTS Security Backport for urllib3 (Python 3.8)"
readme = "README.md"
requires-python = ">=3.8, <3.9"
license = "MIT"
authors = [{name = "$AUTHOR_NAME", email = "$AUTHOR_EMAIL"}]
classifiers = [
    "Programming Language :: Python :: 3.8",
    "Topic :: Security",
]
dependencies = []

[project.urls]
Homepage = "https://github.com/1minds3t/urllib3-lts"
TOML

cat > README.md << MD
# urllib3-lts-py38 🛡️

**Security Backport for Python 3.8**
Base: \`urllib3 v2.2.3\` | Patch Level: \`$VERSION\`

## 🚨 Security Fixes Included

| CVE ID | Severity | Description |
|:---|:---|:---|
| **CVE-2025-66471** | 🔴 HIGH | **Compression Bomb DoS:** Added \`max_length\` limits to decompression. |
| **CVE-2025-66418** | 🔴 HIGH | **Unbounded Links:** Limited decompression chain depth. |
| **CVE-2025-50182** | 🟡 MOD | **Node.js Bypass:** Enforced manual redirects in emscripten. |
| **CVE-2025-50181** | 🟡 MOD | **Redirect Bypass:** Fixed retry logic when redirects disabled. |

## 📦 Installation
\`\`\`bash
pip install urllib3-lts-py38==$VERSION
\`\`\`

## 🌐 The OmniPKG Ecosystem
Maintained by **1minds3t**.

*   **[filelock-lts](https://pypi.org/project/filelock-lts/)**: Secure file locking for legacy Python.
*   **[omnipkg](https://pypi.org/project/omnipkg/)**: The ultimate environment scanner.

**Scan your whole environment for vulnerabilities:**
\`\`\`bash
pip install omnipkg
omnipkg scan --fix
\`\`\`
MD

git add pyproject.toml README.md
git commit -m "Meta: Bump version to $VERSION" || echo "No changes to commit"
git tag -f -a CVE-2025-66471-py38 -m "Release: $VERSION (Full Patch Set)"


# --- 3. UPDATE MAIN DISPATCHER ---
echo "🔧 Updating main dispatcher to v$VERSION..."
git checkout main

cat > pyproject.toml << TOML
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "urllib3-lts"
version = "$VERSION"
description = "LTS Security Ecosystem for urllib3 (Fixes DoS, Redirects, Leaks)"
readme = "README.md"
requires-python = ">=3.7"
license = "MIT"
authors = [{name = "$AUTHOR_NAME", email = "$AUTHOR_EMAIL"}]
dependencies = [
    "urllib3-lts-py37==$VERSION ; python_version >= '3.7' and python_version < '3.8'",
    "urllib3-lts-py38==$VERSION ; python_version >= '3.8' and python_version < '3.9'",
    "urllib3>=2.3.0 ; python_version >= '3.9'" 
]

[project.urls]
Homepage = "https://github.com/1minds3t/urllib3-lts"
TOML

cat > README.md << MD
# urllib3-lts 🛡️

**The Long-Term Support Security Release for urllib3.**

This ecosystem backports critical security fixes to legacy Python environments (3.7 & 3.8) that official maintainers have dropped.

## 🏆 Patch Status (v$VERSION)

| Vulnerability | Severity | Impact | Status |
|:---|:---|:---|:---|
| **CVE-2025-66471** | 🔴 HIGH | Compression Bomb DoS | 🛡️ **FIXED** |
| **CVE-2025-66418** | 🔴 HIGH | Unbounded Links DoS | 🛡️ **FIXED** |
| **CVE-2025-50182** | 🟡 MOD | Node.js Redirect Bypass | 🛡️ **FIXED** |
| **CVE-2025-50181** | 🟡 MOD | Redirect Retry Bypass | 🛡️ **FIXED** |
| **CVE-2024-37891** | 🟡 MOD | Proxy-Auth Header Leak | 🛡️ **FIXED** |

## 📦 Usage

**Standard Installation:**
\`\`\`bash
pip install urllib3-lts
\`\`\`
*This meta-package automatically detects your Python version and installs the correct secured backport.*

## 🌐 The OmniPKG Ecosystem
Maintained by **1minds3t**.

*   **[filelock-lts](https://pypi.org/project/filelock-lts/)**: Secure file locking for legacy Python.
*   **[omnipkg](https://pypi.org/project/omnipkg/)**: The ultimate environment scanner.

**Scan your whole environment for vulnerabilities:**
\`\`\`bash
pip install omnipkg
omnipkg scan --fix
\`\`\`

### 🚧 Coming Soon: omnipkg-runtime
We are building a runtime enforcer that allows configurable **WARN** or **BLOCK** policies for unpatched vulnerabilities. Stay tuned.
MD

# Create the Publish Workflow (publish.yml)
mkdir -p .github/workflows
cat > .github/workflows/publish.yml << 'YAML'
name: Publish to PyPI

on:
  release:
    types: [published]
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    environment: pypi
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Builder
        run: pip install build

      # --- BUILD STRATEGY ---
      # We must build ALL 3 packages from this one workflow
      # by switching branches dynamically.
      
      - name: Build Main (Dispatcher)
        run: |
          git checkout main
          python -m build
          mv dist dist-main

      - name: Build Py3.7
        run: |
          git checkout py37
          python -m build
          mkdir -p dist-py37
          mv dist/* dist-py37/ 2>/dev/null || mv dist-main/* dist-py37/ 

      - name: Build Py3.8
        run: |
          git checkout py38
          python -m build
          mkdir -p dist-py38
          mv dist/* dist-py38/ 2>/dev/null

      # --- CONSOLIDATE & SANITIZE ---
      - name: Prepare Artifacts
        run: |
          mkdir -p final_dist
          cp dist-main/* final_dist/ 2>/dev/null || true
          cp dist-py37/* final_dist/ 2>/dev/null || true
          cp dist-py38/* final_dist/ 2>/dev/null || true
          
          echo "📦 Artifacts ready for upload:"
          ls -l final_dist/
          
          # Sanitize filenames (Replace - with _ in names)
          cd final_dist
          for f in *; do
            new_name=$(echo "$f" | sed -e 's/-/_/g' -e 's/_tar.gz/.tar.gz/' -e 's/_whl/.whl/')
            if [ "$f" != "$new_name" ]; then
              mv "$f" "$new_name"
            fi
          done

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          packages_dir: final_dist
          skip-existing: true
YAML

git add .
git commit -m "Release: Prepare v$VERSION (Docs, Metadata, Workflow)" || echo "No changes"
git tag -f -a CVE-2025-66471 -m "Global Release: v$VERSION"

echo "✅ Synchronization Complete."
