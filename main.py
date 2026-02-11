"""Main application for reading web pages."""

import argparse
import sys
from pathlib import Path

from net_downloader import WebPageReader, WebPageReaderError
from net_downloader.utils import generate_filename, load_config


def main() -> None:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Read web pages and save to text files"
    )
    parser.add_argument(
        "url", nargs="?", help="URL to read (default: https://example.com)"
    )
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-d", "--dir", help="Output directory (default: output)")
    parser.add_argument("-t", "--timeout", type=int, help="Request timeout in seconds")
    parser.add_argument("--pdf", action="store_true", help="Download as PDF file")
    parser.add_argument(
        "--sample-pdf",
        action="store_true",
        help="Download sample PDF from user2019.r-project.org",
    )

    args = parser.parse_args()

    # Handle sample PDF download
    if args.sample_pdf:
        get_sample_pdf(args.output or "sample.pdf")
        return

    # Load configuration
    config = load_config()

    # Set defaults from config and args
    url = args.url or config["default_url"]
    timeout = args.timeout or config["timeout"]
    output_dir = Path(args.dir or config["default_output_dir"])

    # Generate output filename if not provided
    if args.output:
        output_file = Path(args.output)
    else:
        filename = generate_filename(url)
        if args.pdf:
            filename = filename.replace(".txt", ".pdf")
        output_file = output_dir / filename

    print(f"Reading page: {url}")
    print(f"Output file: {output_file}")

    try:
        with WebPageReader(timeout=timeout) as reader:
            if args.pdf:
                reader.download_pdf(str(url), str(output_file))
            else:
                reader.read_and_save(str(url), str(output_file))
        print("✓ File successfully saved!")
    except WebPageReaderError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def get_sample_pdf(output_path: str = "sample.pdf") -> None:
    """Download the sample PDF from user2019.r-project.org.

    Args:
        output_path: Path where to save the PDF file.
    """
    sample_url = "https://user2019.r-project.org/static/pres/t255812.pdf"

    print(f"Downloading sample PDF from: {sample_url}")
    print(f"Saving to: {output_path}")

    try:
        with WebPageReader() as reader:
            reader.download_pdf(sample_url, output_path)
        print("✓ Sample PDF successfully downloaded!")
    except WebPageReaderError as e:
        print(f"✗ Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
