import os

download_path = 'assets'
built_fonts_path = 'built_fonts' # Renamed from out_path

# --- New variables for specific font locations ---
# Path to the directory where JetBrains Mono TTF files are extracted
download_jetbrains_ttf_path = os.path.join(download_path, 'fonts', 'ttf')
# Path to the D2 Coding TTF file
source_d2_coding_font_path = os.path.join(download_path, 'D2Coding', f'D2Coding-Ver{d2_coding_version}-{d2_coding_date}.ttf') # d2_coding_version and d2_coding_date will be substituted
# --- End new variables ---

# Output filename base
built_font_filename_base = "JBD2"

jetbrains_mono_version = '2.304'
d2_coding_version = '1.3.2'
d2_coding_date = '20180524'

jetbrains_mono_url = f'https://github.com/JetBrains/JetBrainsMono/releases/download/v{jetbrains_mono_version}/JetBrainsMono-{jetbrains_mono_version}.zip'
d2_coding_url = f'https://github.com/naver/d2codingfont/releases/download/VER{d2_coding_version}/D2Coding-Ver{d2_coding_version}-{d2_coding_date}.zip'

jetbrains_mono_name = 'JetBrains_Mono.zip'
d2_coding_name = 'D2_Coding.zip'

d2_coding_width = 1000
jetbrains_mono_width = 1200

use_system_wget = False
