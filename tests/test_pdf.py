"""Tests for PDF download functionality."""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest
import requests

from net_downloader import WebPageReader, WebPageReaderError


class TestPDFDownload:
    """Test PDF download functionality."""

    def test_download_pdf_success(self) -> None:
        """Test successful PDF download."""
        # Mock response with PDF content
        mock_response = Mock(spec=requests.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"content-type": "application/pdf"}
        mock_response.iter_content.return_value = [
            b"pdf content chunk 1",
            b"pdf content chunk 2",
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, "test.pdf")

            with patch("requests.Session.get", return_value=mock_response):
                reader = WebPageReader()
                reader.download_pdf("https://example.com/test.pdf", pdf_path)

            # Verify file was created and has content
            assert os.path.exists(pdf_path)
            with open(pdf_path, "rb") as f:
                content = f.read()
                assert content == b"pdf content chunk 1pdf content chunk 2"

    def test_download_pdf_invalid_url(self) -> None:
        """Test PDF download with invalid URL."""
        reader = WebPageReader()

        with pytest.raises(WebPageReaderError, match="Invalid URL"):
            reader.download_pdf("invalid-url", "test.pdf")

    def test_download_pdf_non_pdf_content(self) -> None:
        """Test PDF download when content is not actually a PDF."""
        mock_response = Mock(spec=requests.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"content-type": "text/html"}

        with patch("requests.Session.get", return_value=mock_response):
            reader = WebPageReader()

            with pytest.raises(
                WebPageReaderError, match="does not appear to be a PDF"
            ):
                reader.download_pdf("https://example.com/not-pdf", "test.pdf")

    def test_download_pdf_network_error(self) -> None:
        """Test PDF download with network error."""
        with patch(
            "requests.Session.get",
            side_effect=requests.RequestException("Network error"),
        ):
            reader = WebPageReader()

            with pytest.raises(
                WebPageReaderError, match="Failed to download PDF"
            ):
                reader.download_pdf("https://example.com/test.pdf", "test.pdf")

    def test_download_pdf_with_extension_check(self) -> None:
        """Test PDF download works when URL ends with .pdf but content-type is
        missing."""
        mock_response = Mock(spec=requests.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {}  # No content-type header
        mock_response.iter_content.return_value = [b"pdf content"]

        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, "test.pdf")

            with patch("requests.Session.get", return_value=mock_response):
                reader = WebPageReader()
                reader.download_pdf("https://example.com/test.pdf", pdf_path)

            assert os.path.exists(pdf_path)
