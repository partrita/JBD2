import os
import sys
import shutil
import zipfile

from config import (
    DOWNLOAD_PATH,
    BUILT_FONTS_PATH,
    D2_CODING_URL,
    D2_CODING_ZIP_NAME,
    JETBRAINS_MONO_URL,
    JETBRAINS_MONO_ZIP_NAME,
    JETBRAINS_MONO_NF_URL,  # Added
    JETBRAINS_MONO_NF_ZIP_NAME,  # Added
    USE_SYSTEM_WGET,
)
from hangulify import build_font

if not USE_SYSTEM_WGET:
    import wget


def print_usage():
    """사용법 안내 메시지 출력"""
    print(f"python {sys.argv[0]} <subcommand>\n")
    print("subcommand:")
    print("    all    : 자동으로 setup 및 폰트 빌드")
    print("    setup  : 폰트 파일 다운로드 및 압축 해제")
    print("    build  : 폰트 병합 및 출력")
    print("    clean  : 다운로드 및 출력 파일 삭제")


def download_file(url, filename):
    """파일 다운로드 (wget 또는 시스템 명령어 사용)"""
    print(f"[INFO] Download {filename}")
    if USE_SYSTEM_WGET:
        os.system(f"wget {url} -O {filename}")
    else:
        wget.download(url, out=filename)


def extract_zip(zip_path, extract_to):
    """zip 파일 압축 해제"""
    print(f"[INFO] Extract {os.path.basename(zip_path)}")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def setup():
    """폰트 파일 다운로드 및 압축 해제"""
    print("[INFO] Download font files")
    download_file(JETBRAINS_MONO_URL, JETBRAINS_MONO_ZIP_NAME)
    download_file(D2_CODING_URL, D2_CODING_ZIP_NAME)
    download_file(JETBRAINS_MONO_NF_URL, JETBRAINS_MONO_NF_ZIP_NAME)  # Added

    if not os.path.exists(DOWNLOAD_PATH):
        print(f"[INFO] Create directory: {DOWNLOAD_PATH}")
        os.makedirs(DOWNLOAD_PATH)

    print("[INFO] Move downloaded files to assets directory")
    shutil.move(
        JETBRAINS_MONO_ZIP_NAME, os.path.join(DOWNLOAD_PATH, JETBRAINS_MONO_ZIP_NAME)
    )
    shutil.move(D2_CODING_ZIP_NAME, os.path.join(DOWNLOAD_PATH, D2_CODING_ZIP_NAME))
    shutil.move(
        JETBRAINS_MONO_NF_ZIP_NAME,
        os.path.join(DOWNLOAD_PATH, JETBRAINS_MONO_NF_ZIP_NAME),
    )

    extract_zip(os.path.join(DOWNLOAD_PATH, D2_CODING_ZIP_NAME), DOWNLOAD_PATH)
    extract_zip(os.path.join(DOWNLOAD_PATH, JETBRAINS_MONO_ZIP_NAME), DOWNLOAD_PATH)
    extract_zip(os.path.join(DOWNLOAD_PATH, JETBRAINS_MONO_NF_ZIP_NAME), DOWNLOAD_PATH)

    print("[INFO] Deleting non-Regular ttf files.")
    for root, dirs, files in os.walk(DOWNLOAD_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".ttf") and "Regular" not in file:
                print(f"  - Deleting: {file_path}")
                os.remove(file_path)


def clean():
    """다운로드 및 출력 파일 삭제"""
    print("[INFO] Remove downloaded files")
    if os.path.exists(DOWNLOAD_PATH):
        shutil.rmtree(DOWNLOAD_PATH)
    else:
        print(f'[INFO] Directory "{DOWNLOAD_PATH}" not found, skipping.')

    print("[INFO] Remove output files")
    if os.path.exists(BUILT_FONTS_PATH):
        shutil.rmtree(BUILT_FONTS_PATH)
    else:
        print(f'[INFO] Directory "{BUILT_FONTS_PATH}" not found, skipping.')


def main():
    if len(sys.argv) == 1:
        print_usage()
        exit(1)

    subcommand = sys.argv[1]

    if subcommand == "all":
        print("[INFO] Clean up previous files")
        try:
            clean()
        except Exception:
            print("[INFO] No output files found.")
        print("[INFO] Download and extract font files")
        setup()
        print("[INFO] Build fonts")
        build_font()
    elif subcommand == "setup":
        setup()
    elif subcommand == "build":
        build_font()
    elif subcommand == "clean":
        clean()
    else:
        print_usage()
        exit(1)


if __name__ == "__main__":
    main()
