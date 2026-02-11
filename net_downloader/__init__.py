"""net_downloader - Web content downloader and file writer."""

from .client import WebPageReader
from .exceptions import WebPageReaderError

__version__ = "0.1.0"
__all__ = ["WebPageReader", "WebPageReaderError"]
