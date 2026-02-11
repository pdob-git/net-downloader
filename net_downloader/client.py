"""Web content downloader client for reading URLs and saving to files."""

import os
from urllib.parse import urlparse

import requests
from requests import Response

from .exceptions import FileWriteError, NetworkError, WebPageReaderError


class WebPageReader:
    """A client for reading web pages and saving content to text files."""

    def __init__(self, timeout: int = 30):
        """Initialize the web page reader.

        Args:
            timeout: Request timeout in seconds.
        """
        self.timeout = timeout
        self.session = requests.Session()
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36"
        )
        self.session.headers.update({"User-Agent": user_agent})

    def read_page(self, url: str) -> str:
        """Read content from a web page.

        Args:
            url: The URL to read from.

        Returns:
            The page content as a string.

        Raises:
            NetworkError: If the request fails.
            WebPageReaderError: If the URL is invalid.
        """
        if not self._is_valid_url(url):
            raise WebPageReaderError(f"Invalid URL: {url}")

        try:
            response: Response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise NetworkError(f"Failed to fetch {url}: {e}")

    def save_to_file(self, content: str, filepath: str) -> None:
        """Save content to a text file.

        Args:
            content: The content to save.
            filepath: The path to save the file to.

        Raises:
            FileWriteError: If file write fails.
        """
        try:
            dir_path = os.path.dirname(filepath)
            if dir_path:  # Only create directory if there is one
                os.makedirs(dir_path, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        except (OSError, IOError) as e:
            raise FileWriteError(f"Failed to write to {filepath}: {e}")

    def read_and_save(self, url: str, filepath: str) -> None:
        """Read a web page and save it to a file.

        Args:
            url: The URL to read from.
            filepath: The path to save the file to.

        Raises:
            WebPageReaderError: If any operation fails.
        """
        content = self.read_page(url)
        self.save_to_file(content, filepath)

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Check if a URL is valid.

        Args:
            url: The URL to validate.

        Returns:
            True if valid, False otherwise.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.scheme in (
                "http",
                "https",
            )
        except Exception:
            return False

    def download_pdf(self, url: str, filepath: str) -> None:
        """Download a PDF file from a URL.

        Args:
            url: The PDF URL to download from.
            filepath: The path to save the PDF file to.

        Raises:
            NetworkError: If the download fails.
            WebPageReaderError: If the URL is invalid.
            FileWriteError: If file write fails.
        """
        if not self._is_valid_url(url):
            raise WebPageReaderError(f"Invalid URL: {url}")

        try:
            response: Response = self.session.get(
                url, timeout=self.timeout, stream=True
            )
            response.raise_for_status()

            # Check if content is actually a PDF
            content_type = response.headers.get("content-type", "").lower()
            if "pdf" not in content_type and not url.lower().endswith(".pdf"):
                raise WebPageReaderError(
                    f"URL does not appear to be a PDF: {url}"
                )

            dir_path = os.path.dirname(filepath)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        except requests.RequestException as e:
            raise NetworkError(f"Failed to download PDF from {url}: {e}")
        except (OSError, IOError) as e:
            raise FileWriteError(f"Failed to write PDF to {filepath}: {e}")

    def close(self) -> None:
        """Close the session."""
        self.session.close()

    def __enter__(self) -> "WebPageReader":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Context manager exit."""
        self.close()
