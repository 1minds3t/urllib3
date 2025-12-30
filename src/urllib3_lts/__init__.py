"""urllib3-lts meta-package - dispatcher for Python version-specific patches."""

import sys

# Get version from package metadata (automatically set by setuptools at install time)
try:
    if sys.version_info >= (3, 8):
        from importlib.metadata import version
    else:
        from importlib_metadata import version
    __version__ = version("urllib3-lts")
except Exception:
    __version__ = "unknown"

__all__ = ["__version__"]
