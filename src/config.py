import os
from typing import Final

# =======================================
#  Build and Path Configuration
# =======================================
# Directory where source font files are downloaded.
DOWNLOAD_PATH: Final[str] = "assets"

# Directory where final font files are saved.
BUILT_FONTS_PATH: Final[str] = "built_fonts"

# If True, use the system's `wget` command for downloading.
# If False, use the `wget` Python library.
USE_SYSTEM_WGET: Final[bool] = True


# =======================================
#  Korean Monospace Font (D2Coding) Configuration
# =======================================
# D2Coding 1.4.0 (2026-10-03): https://d2.naver.com/news/7193556
# Repo moved from naver/d2codingfont -> naver/d2-coding-font.
# Zip layout: D2Coding/ (standard), D2CodingLigature/, D2CodingAll/, OFL.txt.
# JBD2 merges Hangul glyphs from the standard Regular TTF only.
KOREAN_FONT_URL: Final[str] = (
    "https://github.com/naver/d2-coding-font/releases/download/VER1.4.0/"
    "D2Coding-Ver1.4.0-20261003.zip"
)
KOREAN_FONT_ZIP_NAME: Final[str] = "D2_Coding.zip"
KOREAN_FONT_WIDTH: Final[int] = 1000

# Path to the standard Regular TTF after extraction.
KOREAN_FONT_PATH: Final[str] = os.path.join(
    DOWNLOAD_PATH,
    "D2Coding",
    "D2Coding-Ver1.4.0-20261003.ttf",
)


# =======================================
#  English Monospace Font (JetBrains Mono) Configuration
# =======================================
ENGLISH_FONT_VERSION: Final[str] = "2.304"
ENGLISH_FONT_URL: Final[str] = (
    f"https://github.com/JetBrains/JetBrainsMono/releases/download/v{ENGLISH_FONT_VERSION}/"
    f"JetBrainsMono-{ENGLISH_FONT_VERSION}.zip"
)
ENGLISH_FONT_ZIP_NAME: Final[str] = "JetBrains_Mono.zip"
ENGLISH_FONT_WIDTH: Final[int] = 1200

# Path to the directory containing the extracted JetBrains Mono TTF files.
ENGLISH_FONT_PATH: Final[str] = os.path.join(DOWNLOAD_PATH, "fonts", "ttf")


# =======================================
#  English Nerd Font Configuration
# =======================================
# URL for JetBrains Mono Nerd Font from ryanoasis/nerd-fonts repository.
ENGLISH_FONT_NF_URL: Final[str] = (
    "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/JetBrainsMono.zip"
)
ENGLISH_FONT_NF_ZIP_NAME: Final[str] = "JetBrains_Mono_NF.zip"
ENGLISH_FONT_NF_WIDTH: Final[int] = 1200

# Path to the directory containing the extracted JetBrains Mono Nerd Font TTF files.
ENGLISH_FONT_NF_PATH: Final[str] = DOWNLOAD_PATH
