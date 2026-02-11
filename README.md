# net_downloader

A Python package for downloading web content and saving to files.

## Features

- Read content from any web page
- Save content to text files with customizable filenames
- Configurable URLs via command line or environment variables
- Proper error handling for network and file operations
- Context manager support for resource cleanup

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Usage

### Command Line

```bash
# Read default page (https://example.com)
python main.py

# Read specific URL
python main.py https://httpbin.org/html

# Save to custom file
python main.py https://example.com -o my_page.txt

# Save to custom directory
python main.py https://example.com -d custom_output
```

### Python API

```python
from net_downloader import WebPageReader

# Basic usage
with WebPageReader() as reader:
    content = reader.read_page("https://example.com")
    reader.save_to_file(content, "example.txt")

# Read and save in one step
with WebPageReader(timeout=60) as reader:
    reader.read_and_save("https://example.com", "output/example.txt")

# Custom timeout
reader = WebPageReader(timeout=45)
try:
    content = reader.read_page("https://example.com")
    print(f"Read {len(content)} characters")
finally:
    reader.close()
```

### Environment Variables

```bash
export DEFAULT_URL="https://example.com"
export DEFAULT_OUTPUT_DIR="output"
export REQUEST_TIMEOUT="30"
```

## Configuration

The following environment variables can be used to configure default behavior:

- `DEFAULT_URL`: Default URL to read (default: https://example.com)
- `DEFAULT_OUTPUT_DIR`: Default output directory (default: output)
- `REQUEST_TIMEOUT`: Request timeout in seconds (default: 30)

## Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=net_downloader

# Format code
black .
isort .

# Lint
flake8 net_downloader tests

# Type check
mypy net_downloader
```

## License

MIT License
