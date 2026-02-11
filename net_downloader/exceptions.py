"""Custom exceptions for net_downloader."""


class WebPageReaderError(Exception):
    """Base exception for web page reader errors."""

    pass


class NetworkError(WebPageReaderError):
    """Raised when network request fails."""

    pass


class FileWriteError(WebPageReaderError):
    """Raised when file write operation fails."""

    pass
