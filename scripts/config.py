import os

# =======================================
#  빌드 및 경로 구성
# =======================================
# 소스 폰트 파일이 다운로드되는 디렉터리입니다.
DOWNLOAD_PATH: str = "assets"
# 최종 폰트 파일이 저장될 디렉터리입니다.
BUILT_FONTS_PATH: str = "built_fonts"
# True인 경우 시스템의 `wget` 명령을 사용하여 다운로드합니다.
# False인 경우 `wget` Python 라이브러리를 사용합니다.
USE_SYSTEM_WGET: bool = True


# =======================================
#  한글 모노스페이스 폰트 구성
# =======================================
KOREAN_FONT_VERSION: str = "1.3.2"
KOREAN_FONT_RELEASE_DATE: str = "20180524"
KOREAN_FONT_URL: str = (
    f"https://github.com/naver/d2codingfont/releases/download/VER{KOREAN_FONT_VERSION}/"
    f"D2Coding-Ver{KOREAN_FONT_VERSION}-{KOREAN_FONT_RELEASE_DATE}.zip"
)
KOREAN_FONT_ZIP_NAME: str = "D2_Coding.zip"
KOREAN_FONT_WIDTH: int = 1000
# 압축 해제 후 D2Coding TTF 원본 파일의 경로입니다.
KOREAN_FONT_PATH: str = os.path.join(
    DOWNLOAD_PATH,
    "D2Coding",
    f"D2Coding-Ver{KOREAN_FONT_VERSION}-{KOREAN_FONT_RELEASE_DATE}.ttf",
)


# =======================================
#  영문 모노스페이스 폰트 구성
# =======================================
ENGLISH_FONT_VERSION: str = "2.304"
ENGLISH_FONT_URL: str = (
    f"https://github.com/JetBrains/JetBrainsMono/releases/download/v{ENGLISH_FONT_VERSION}/"
    f"JetBrainsMono-{ENGLISH_FONT_VERSION}.zip"
)
ENGLISH_FONT_ZIP_NAME: str = "JetBrains_Mono.zip"
ENGLISH_FONT_WIDTH: int = 1200
# 압축 해제된 JetBrains Mono TTF 파일이 포함된 디렉터리 경로입니다.
ENGLISH_FONT_PATH: str = os.path.join(DOWNLOAD_PATH, "fonts", "ttf")


# =======================================
#  영문 너드 폰트 구성
# =======================================
# ryanoasis/nerd-fonts 저장소에 있는 JetBrains Mono Nerd Font의 URL입니다.
ENGLISH_FONT_NF_URL: str = (
    "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/JetBrainsMono.zip"
)
ENGLISH_FONT_NF_ZIP_NAME: str = "JetBrains_Mono_NF.zip"
ENGLISH_FONT_NF_WIDTH: int = 1200
# 압축 해제된 JetBrains Mono Nerd Font TTF 파일이 포함된 디렉터리 경로입니다.
# DOWNLOAD_PATH의 루트에 압축 해제됩니다.
ENGLISH_FONT_NF_PATH: str = DOWNLOAD_PATH