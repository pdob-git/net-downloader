# AGENTS.md

This file contains guidelines and commands for agentic coding agents working in this repository.

## Project Overview

This is a Python project related to HTTP requests functionality. The project uses Python 3.12 with a virtual environment.

## Environment Setup

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Build and Development Commands

### Core Commands
```bash
# Install the package in development mode
pip install -e .

# Run the main application
python main.py

# Run with specific module
python -m net_downloader
```

### Testing Commands
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov= net_downloader

# Run specific test file
pytest tests/test_specific.py

# Run specific test function
pytest tests/test_specific.py::test_function_name

# Run tests with verbose output
pytest -v

# Run tests with specific marker
pytest -m "not slow"
```

### Code Quality Commands
```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 net_downloader tests

# Type checking with mypy
mypy net_downloader

# Run all quality checks together
black . && isort . && flake8 net_downloader tests && mypy net_downloader
```

### Security and Dependencies
```bash
# Check for security vulnerabilities
bandit -r net_downloader

# Check outdated dependencies
pip list --outdated

# Update requirements
pip-compile requirements.in
```

## Code Style Guidelines

### Import Style
- Use `isort` for import sorting (standard configuration)
- Group imports: standard library, third-party, local application
- Use absolute imports for application modules
- Avoid wildcard imports (`from module import *`)

```python
# Standard library
import os
import sys
from typing import Optional, Dict, Any

# Third-party
import requests
from requests import Response, Session

# Local application
from requests_opencode.client import HttpClient
from requests_opencode.exceptions import ApiError
```

### Formatting
- Use `black` for code formatting (88 character line length)
- Use f-strings for string formatting
- Follow PEP 8 naming conventions

### Type Hints
- Use type hints for all function signatures
- Use `Optional[T]` for nullable types
- Use `Dict`, `List`, `Tuple` from typing module
- Use `Union` for multiple possible types

```python
from typing import Optional, Dict, Any

def make_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
) -> Optional[Response]:
    """Make an HTTP request with proper error handling."""
    pass
```

### Naming Conventions
- Variables and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_leading_underscore`

### Error Handling
- Use specific exception types
- Create custom exception classes for domain-specific errors
- Always include meaningful error messages
- Use context managers for resource management

```python
class RequestsOpencodeError(Exception):
    """Base exception for requests-opencode errors."""
    pass
