import os
import sys
import shutil
import zipfile

from config import (
    DOWNLOAD_PATH,
    BUILT_FONTS_PATH,
    KOREAN_FONT_URL,
    KOREAN_FONT_ZIP_NAME,
    ENGLISH_FONT_URL,
    ENGLISH_FONT_ZIP_NAME,
    ENGLISH_FONT_NF_URL,
    ENGLISH_FONT_NF_ZIP_NAME,
    USE_SYSTEM_WGET,
)
from hangulify import build_fonts

if not USE_SYSTEM_WGET:
    import wget


def print_usage():
    """사용법 안내 메시지를 출력합니다."""
    print(f"python {sys.argv[0]} <subcommand>\n")
    print("subcommand:")
    print("    all    : 자동으로 setup 및 폰트 빌드를 수행합니다.")
    print("    setup  : 폰트 파일을 다운로드하고 압축을 해제합니다.")
    print("    build  : 폰트를 병합하고 출력합니다.")
    print("    clean  : 다운로드 및 출력 파일을 삭제합니다.")


def download_file(url, filename):
    """wget 또는 시스템 명령어를 사용하여 파일을 다운로드합니다."""
    print(f"[INFO] {filename} 다운로드 중")
    if USE_SYSTEM_WGET:
        os.system(f"wget {url} -O {filename}")
    else:
        wget.download(url, out=filename)


def extract_zip(zip_path, extract_to):
    """zip 파일의 압축을 해제합니다."""
    print(f"[INFO] {os.path.basename(zip_path)} 압축 해제 중")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def setup():
    """폰트 파일을 다운로드하고 압축을 해제합니다."""
    print("[INFO] 폰트 파일 다운로드 중")
    download_file(ENGLISH_FONT_URL, ENGLISH_FONT_ZIP_NAME)
    download_file(KOREAN_FONT_URL, KOREAN_FONT_ZIP_NAME)
    download_file(ENGLISH_FONT_NF_URL, ENGLISH_FONT_NF_ZIP_NAME)

    if not os.path.exists(DOWNLOAD_PATH):
        print(f"[INFO] 디렉터리 생성: {DOWNLOAD_PATH}")
        os.makedirs(DOWNLOAD_PATH)

    print("[INFO] 다운로드한 파일을 assets 디렉터리로 이동 중")
    shutil.move(
        ENGLISH_FONT_ZIP_NAME, os.path.join(DOWNLOAD_PATH, ENGLISH_FONT_ZIP_NAME)
    )
    shutil.move(KOREAN_FONT_ZIP_NAME, os.path.join(DOWNLOAD_PATH, KOREAN_FONT_ZIP_NAME))
    shutil.move(
        ENGLISH_FONT_NF_ZIP_NAME,
        os.path.join(DOWNLOAD_PATH, ENGLISH_FONT_NF_ZIP_NAME),
    )

    extract_zip(os.path.join(DOWNLOAD_PATH, KOREAN_FONT_ZIP_NAME), DOWNLOAD_PATH)
    extract_zip(os.path.join(DOWNLOAD_PATH, ENGLISH_FONT_ZIP_NAME), DOWNLOAD_PATH)
    extract_zip(os.path.join(DOWNLOAD_PATH, ENGLISH_FONT_NF_ZIP_NAME), DOWNLOAD_PATH)

    print("[INFO] Regular가 아닌 ttf 파일 및 기타 불필요한 파일 삭제 중...")
    for root, dirs, files in os.walk(DOWNLOAD_PATH):
        for file in files:
            file_path = os.path.join(root, file)

            # 파일명에 'D2Coding'이 포함된 ttf 파일은 삭제하지 않습니다.
            if file.endswith(".ttf") and "D2Coding" in file:
                print(f"  - D2Coding 폰트 파일 유지: {file_path}")
                continue

            if file.endswith(".ttf") and "Regular" not in file:
                print(f"  - 삭제: {file_path}")
                os.remove(file_path)


def clean():
    """다운로드 및 출력 파일을 삭제합니다."""
    print("[INFO] 다운로드한 파일 삭제 중")
    if os.path.exists(DOWNLOAD_PATH):
        shutil.rmtree(DOWNLOAD_PATH)
    else:
        print(f'[INFO] "{DOWNLOAD_PATH}" 디렉터리를 찾을 수 없어 건너뜁니다.')

    print("[INFO] 출력 파일 삭제 중")
    if os.path.exists(BUILT_FONTS_PATH):
        shutil.rmtree(BUILT_FONTS_PATH)
    else:
        print(f'[INFO] "{BUILT_FONTS_PATH}" 디렉터리를 찾을 수 없어 건너뜁니다.')

def main():
    if len(sys.argv) == 1:
        print_usage()
        exit(1)

    subcommand = sys.argv[1]

    if subcommand == "all":
        print("[INFO] 이전 파일 정리 중")
        try:
            clean()
        except Exception:
            print("[INFO] 출력 파일을 찾을 수 없습니다.")
        print("[INFO] 폰트 파일 다운로드 및 압축 해제 중")
        setup()
        print("[INFO] 폰트 빌드 중")
        build_fonts()
    elif subcommand == "setup":
        setup()
    elif subcommand == "build":
        build_fonts()
    elif subcommand == "clean":
        clean()
    else:
        print_usage()
        exit(1)


if __name__ == "__main__":
    main()