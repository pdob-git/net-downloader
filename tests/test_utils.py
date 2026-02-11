"""Tests for utility functions."""

import os
from unittest.mock import patch

from net_downloader.utils import generate_filename, load_config


class TestUtils:
    """Test cases for utility functions."""

    @patch.dict(
        os.environ,
        {
            "DEFAULT_URL": "https://custom.com",
            "DEFAULT_OUTPUT_DIR": "custom_output",
            "REQUEST_TIMEOUT": "45",
        },
    )
    def test_load_config_with_env_vars(self) -> None:
        """Test loading configuration from environment variables."""
        config = load_config()

        assert config["default_url"] == "https://custom.com"
        assert config["default_output_dir"] == "custom_output"
        assert config["timeout"] == 45

    @patch.dict(os.environ, {}, clear=True)
    def test_load_config_defaults(self) -> None:
        """Test loading configuration with defaults."""
        config = load_config()

        assert config["default_url"] == "https://example.com"
        assert config["default_output_dir"] == "output"
        assert config["timeout"] == 30

    def test_generate_filename_simple_url(self) -> None:
        """Test filename generation for simple URL."""
        filename = generate_filename("https://example.com")
        assert filename == "example.com_index.txt"

    def test_generate_filename_with_www(self) -> None:
        """Test filename generation removing www."""
        filename = generate_filename("https://www.example.com")
        assert filename == "example.com_index.txt"

    def test_generate_filename_with_path(self) -> None:
        """Test filename generation with path."""
        filename = generate_filename("https://example.com/path/to/page")
        assert filename == "example.com_path_to_page.txt"

    def test_generate_filename_custom_extension(self) -> None:
        """Test filename generation with custom extension."""
        filename = generate_filename("https://example.com", "html")
        assert filename == "example.com_index.html"

    def test_generate_filename_trailing_slash(self) -> None:
        """Test filename generation with trailing slash."""
        filename = generate_filename("https://example.com/")
        assert filename == "example.com_index.txt"

    def test_generate_filename_empty_path(self) -> None:
        """Test filename generation with empty path."""
        filename = generate_filename("https://example.com/test/")
        assert filename == "example.com_test.txt"
