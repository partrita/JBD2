import os
import shutil
import subprocess
import sys
import zipfile
import concurrent.futures

from .config import (
    BUILT_FONTS_PATH,
    DOWNLOAD_PATH,
    ENGLISH_FONT_NF_URL,
    ENGLISH_FONT_NF_ZIP_NAME,
    ENGLISH_FONT_URL,
    ENGLISH_FONT_ZIP_NAME,
    KOREAN_FONT_URL,
    KOREAN_FONT_ZIP_NAME,
    USE_SYSTEM_WGET,
)
from .hangulify import build_fonts

# If USE_SYSTEM_WGET is False, try importing the wget library.
if not USE_SYSTEM_WGET:
    try:
        import wget
    except ImportError:
        print("[ERROR] 'wget' library not found. Please install it or set USE_SYSTEM_WGET to True.")
        sys.exit(1)


def print_usage() -> None:
    """Print the usage instructions for this script."""
    print("Usage: python -m src.build <subcommand>\n")
    print("Available subcommands:")
    print("    all    : Automatically setup environment and build fonts.")
    print("    setup  : Download source font files and extract them.")
    print("    build  : Merge fonts and generate output files.")
    print("    clean  : Delete downloaded and generated files.")


def download_file(url: str, filename: str) -> None:
    """Download a file from a URL using wget or the system's wget command."""
    print(f"[INFO] Downloading {filename}...")
    if USE_SYSTEM_WGET:
        result = subprocess.run(["wget", "-q", url, "-O", filename]).returncode
        if result != 0:
            print(f"[ERROR] Failed to download {url} using system wget.")
    else:
        wget.download(url, out=filename)
        print()  # Add newline after wget progress bar


def extract_zip(zip_path: str, extract_to: str) -> None:
    """Extract a ZIP archive to a specific directory."""
    print(f"[INFO] Extracting {os.path.basename(zip_path)}...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def setup() -> None:
    """Download and prepare the source font files."""
    print("[INFO] Starting setup...")

    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    archives_info = [
        (ENGLISH_FONT_URL, os.path.join(DOWNLOAD_PATH, ENGLISH_FONT_ZIP_NAME)),
        (KOREAN_FONT_URL, os.path.join(DOWNLOAD_PATH, KOREAN_FONT_ZIP_NAME)),
        (ENGLISH_FONT_NF_URL, os.path.join(DOWNLOAD_PATH, ENGLISH_FONT_NF_ZIP_NAME)),
    ]

    # Concurrently download font archives directly to DOWNLOAD_PATH.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_file, url, path) for url, path in archives_info]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # Concurrently extract all archives.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_zip, path, DOWNLOAD_PATH) for _, path in archives_info]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # Cleanup: remove non-Regular fonts and unnecessary files from downloads.
    print("[INFO] Cleaning up downloaded files...")
    for root, _, files in os.walk(DOWNLOAD_PATH):
        for file in files:
            file_path = os.path.join(root, file)

            # Keep D2Coding files.
            if file.endswith(".ttf") and "D2Coding" in file:
                continue

            # Remove non-Regular fonts.
            if file.endswith(".ttf") and "Regular" not in file:
                os.remove(file_path)


def clean() -> None:
    """Delete the downloaded assets and built font files."""
    for path, label in [(DOWNLOAD_PATH, "Downloads"), (BUILT_FONTS_PATH, "Built fonts")]:
        if os.path.exists(path):
            print(f"[INFO] Removing {label} directory: {path}")
            shutil.rmtree(path)
        else:
            print(f"[INFO] {label} directory not found, skipping.")


def main() -> None:
    """Entry point for the build script."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    subcommand = sys.argv[1].lower()

    if subcommand == "all":
        clean()
        setup()
        build_fonts()
    elif subcommand == "setup":
        setup()
    elif subcommand == "build":
        build_fonts()
    elif subcommand == "clean":
        clean()
    else:
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
