"""Tests for the WebPageReader client."""

from unittest.mock import Mock, mock_open, patch

import pytest
from requests import Response

from net_downloader import WebPageReader, WebPageReaderError
from net_downloader.exceptions import FileWriteError, NetworkError


class TestWebPageReader:
    """Test cases for WebPageReader class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.reader = WebPageReader(timeout=10)

    def test_init_default_timeout(self):
        """Test initialization with default timeout."""
        reader = WebPageReader()
        assert reader.timeout == 30
        assert reader.session is not None

    def test_init_custom_timeout(self):
        """Test initialization with custom timeout."""
        reader = WebPageReader(timeout=60)
        assert reader.timeout == 60

    def test_is_valid_url_valid_urls(self):
        """Test URL validation with valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://www.example.com/path",
            "https://example.com:8080/path?query=value",
        ]
        for url in valid_urls:
            assert WebPageReader._is_valid_url(url) is True

    def test_is_valid_url_invalid_urls(self):
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "",
            "just-text",
            "://missing-protocol.com",
        ]
        for url in invalid_urls:
            assert WebPageReader._is_valid_url(url) is False

    @patch("requests.Session.get")
    def test_read_page_success(self, mock_get):
        """Test successful page reading."""
        mock_response = Mock(spec=Response)
        mock_response.text = "<html><body>Test content</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        content = self.reader.read_page("https://example.com")

        assert content == "<html><body>Test content</body></html>"
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("requests.Session.get")
    def test_read_page_network_error(self, mock_get):
        """Test network error handling."""
        import requests

        mock_get.side_effect = requests.RequestException("Network error")

        with pytest.raises(NetworkError):
            self.reader.read_page("https://example.com")

    def test_read_page_invalid_url(self):
        """Test invalid URL handling."""
        with pytest.raises(WebPageReaderError):
            self.reader.read_page("invalid-url")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_save_to_file_success(self, mock_makedirs, mock_file):
        """Test successful file saving."""
        content = "Test content"
        filepath = "output/test.txt"

        self.reader.save_to_file(content, filepath)

        mock_makedirs.assert_called_once_with("output", exist_ok=True)
        mock_file.assert_called_once_with(filepath, "w", encoding="utf-8")
        mock_file().write.assert_called_once_with(content)

    @patch("os.makedirs")
    def test_save_to_file_directory_error(self, mock_makedirs):
        """Test file saving with directory creation error."""
        mock_makedirs.side_effect = OSError("Permission denied")

        with pytest.raises(FileWriteError):
            self.reader.save_to_file("content", "/invalid/path/file.txt")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_to_file_write_error(self, mock_file):
        """Test file saving with write error."""
        mock_file.side_effect = IOError("Disk full")

        with pytest.raises(FileWriteError):
            self.reader.save_to_file("content", "output/test.txt")

    @patch.object(WebPageReader, "save_to_file")
    @patch.object(WebPageReader, "read_page")
    def test_read_and_save_success(self, mock_read, mock_save):
        """Test successful read and save operation."""
        mock_read.return_value = "Page content"

        self.reader.read_and_save("https://example.com", "output/test.txt")

        mock_read.assert_called_once_with("https://example.com")
        mock_save.assert_called_once_with("Page content", "output/test.txt")

    def test_context_manager(self):
        """Test context manager functionality."""
        with patch.object(self.reader.session, "close") as mock_close:
            with self.reader as reader:
                assert reader is self.reader
            mock_close.assert_called_once()

    def test_close(self):
        """Test session closing."""
        with patch.object(self.reader.session, "close") as mock_close:
            self.reader.close()
            mock_close.assert_called_once()
