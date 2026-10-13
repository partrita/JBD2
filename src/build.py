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
    KOREAN_FONT_PATH,
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
    """Download a file. Raises RuntimeError on failure."""
    print(f"[INFO] Downloading {filename}...")
    if USE_SYSTEM_WGET:
        result = subprocess.run(["wget", "-q", url, "-O", filename]).returncode
        if result != 0:
            raise RuntimeError(f"Failed to download {url} using system wget.")
    else:
        wget.download(url, out=filename)
        print()  # Add newline after wget progress bar
    if not os.path.exists(filename) or not zipfile.is_zipfile(filename):
        raise RuntimeError(f"Download failed or produced invalid archive: {filename}")


def extract_zip(zip_path: str, extract_to: str) -> None:
    """Extract a ZIP archive to a specific directory."""
    print(f"[INFO] Extracting {os.path.basename(zip_path)}...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def _prune_downloads() -> None:
    """Keep only files needed for the merge.

    Keeps: standard D2Coding Regular TTF (KOREAN_FONT_PATH), OFL.txt,
    and standard Regular TTFs (JetBrainsMono-Regular.ttf, JetBrainsMonoNerdFont-Regular.ttf).
    Removes Bold/Ligature/TTC files and non-standard variants (NL, Mono, Propo)
    to save disk space and prevent unwanted output overwrites.
    """
    keep_d2 = os.path.abspath(KOREAN_FONT_PATH)
    for root, _, files in os.walk(DOWNLOAD_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            if file == "OFL.txt":
                continue
            if os.path.abspath(file_path) == keep_d2:
                continue
            if file.endswith(".ttc"):
                os.remove(file_path)
                continue
            if not file.endswith(".ttf"):
                continue
            # Drop unused D2Coding variants (Bold / ligature).
            if "D2Coding" in file:
                os.remove(file_path)
                continue
            # Drop non-Regular styles from other families.
            if "Regular" not in file:
                os.remove(file_path)
                continue
            # Drop NL (No-Ligatures), Propo, and NerdFontMono variants.
            if "NL" in file or "Propo" in file or "NerdFontMono" in file:
                os.remove(file_path)
                continue


def setup() -> None:
    """Download and prepare the source font files."""
    print("[INFO] Starting setup...")

    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    archives_info = [
        (ENGLISH_FONT_URL, os.path.join(DOWNLOAD_PATH, ENGLISH_FONT_ZIP_NAME)),
        (KOREAN_FONT_URL, os.path.join(DOWNLOAD_PATH, KOREAN_FONT_ZIP_NAME)),
        (ENGLISH_FONT_NF_URL, os.path.join(DOWNLOAD_PATH, ENGLISH_FONT_NF_ZIP_NAME)),
    ]

    # Remove stale archives so a failed download never looks valid.
    for _, path in archives_info:
        if os.path.exists(path):
            os.remove(path)

    # Download concurrently; download_file() already validates each archive.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(executor.map(lambda item: download_file(*item), archives_info))

    # Extract concurrently.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(executor.map(lambda path: extract_zip(path, DOWNLOAD_PATH), [p for _, p in archives_info]))

    # Cleanup: remove non-Regular fonts and unnecessary files from downloads.
    print("[INFO] Cleaning up downloaded files...")
    _prune_downloads()


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
