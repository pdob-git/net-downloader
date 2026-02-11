"""Utility functions for net_downloader."""

import os
from typing import Any, Dict


def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables.

    Returns:
        Dictionary containing configuration values.
    """
    return {
        "default_url": os.getenv("DEFAULT_URL", "https://example.com"),
        "default_output_dir": os.getenv("DEFAULT_OUTPUT_DIR", "output"),
        "timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
    }


def generate_filename(url: str, extension: str = "txt") -> str:
    """Generate a filename from a URL.

    Args:
        url: The URL to generate filename from.
        extension: File extension to use.

    Returns:
        Generated filename.
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/").replace("/", "_") or "index"
    return f"{domain}_{path}.{extension}"
