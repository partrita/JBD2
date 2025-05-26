import os

# =========================
# Build & Path Configuration
# =========================
DOWNLOAD_PATH = "assets"
BUILT_FONTS_PATH = "built_fonts"
BUILT_FONT_FILENAME_BASE = "JBD2"
USE_SYSTEM_WGET = False

# =========================
# D2Coding Font Configuration
# =========================
D2_CODING_VERSION = "1.3.2"
D2_CODING_DATE = "20180524"
D2_CODING_URL = (
    f"https://github.com/naver/d2codingfont/releases/download/VER{D2_CODING_VERSION}/"
    f"D2Coding-Ver{D2_CODING_VERSION}-{D2_CODING_DATE}.zip"
)
D2_CODING_ZIP_NAME = "D2_Coding.zip"
D2_CODING_WIDTH = 1000
# Path to D2 Coding TTF file
SOURCE_D2_CODING_FONT_PATH = os.path.join(
    DOWNLOAD_PATH, "D2Coding", f"D2Coding-Ver{D2_CODING_VERSION}-{D2_CODING_DATE}.ttf"
)

# =========================
# JetBrains Mono Font Configuration
# =========================
JETBRAINS_MONO_VERSION = "2.304"
JETBRAINS_MONO_URL = (
    f"https://github.com/JetBrains/JetBrainsMono/releases/download/v{JETBRAINS_MONO_VERSION}/"
    f"JetBrainsMono-{JETBRAINS_MONO_VERSION}.zip"
)
JETBRAINS_MONO_ZIP_NAME = "JetBrains_Mono.zip"
JETBRAINS_MONO_WIDTH = 1200
# Path to extracted JetBrains Mono TTF files
DOWNLOAD_JETBRAINS_TTF_PATH = os.path.join(DOWNLOAD_PATH, "fonts", "ttf")


# =========================
# JetBrains Mono Nerd Font Configuration
# =========================
JETBRAINS_MONO_NF_VERSION = "2.304"
JETBRAINS_MONO_NF_URL = (
    "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/JetBrainsMono.zip"
)
JETBRAINS_MONO_NF_ZIP_NAME = "JetBrains_Mono_NF.zip"
JETBRAINS_MONO_NF_WIDTH = 1200
# Path to extracted JetBrains Mono TTF files
DOWNLOAD_JETBRAINS_MONO_NF_TTF_PATH = DOWNLOAD_PATH
