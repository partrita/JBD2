import os
from typing import Any, List, Tuple

import fontforge

from .config import (
    BUILT_FONTS_PATH,
    ENGLISH_FONT_NF_PATH,
    ENGLISH_FONT_PATH,
    ENGLISH_FONT_NF_WIDTH,
    ENGLISH_FONT_WIDTH,
    KOREAN_FONT_PATH,
)

# Value to adjust the side bearings of the glyphs.
BEARING_ADJUSTMENT: int = 200


def adjust_glyph_bearing(glyph: Any, adjustment: int) -> None:
    """Adjust the left and right side bearings of a glyph."""
    glyph.left_side_bearing = (adjustment // 2) + int(glyph.left_side_bearing)
    glyph.right_side_bearing = (adjustment // 2) + int(glyph.right_side_bearing)


def process_hangul_glyphs(font: fontforge.font) -> None:
    """Select Korean glyphs and adjust their bearings."""
    # Unicode ranges for Hangul Jamo and Syllables.
    font.selection.select(("unicode", "ranges"), 0x3131, 0x318E)
    font.selection.select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3)

    for glyph_id in font.selection.byGlyphs:
        glyph = font[glyph_id]
        is_jetbrains_font = int(glyph.width) in (
            ENGLISH_FONT_WIDTH,
            ENGLISH_FONT_NF_WIDTH,
        )

        if not glyph.references:
            if is_jetbrains_font:
                adjust_glyph_bearing(glyph, BEARING_ADJUSTMENT)
        else:
            for ref in glyph.references:
                ref_glyph = font[ref[0]]
                is_jetbrains_font_ref = int(ref_glyph.width) in (
                    ENGLISH_FONT_WIDTH,
                    ENGLISH_FONT_NF_WIDTH,
                )
                if is_jetbrains_font_ref:
                    adjust_glyph_bearing(ref_glyph, BEARING_ADJUSTMENT)


def get_font_style(filename: str) -> str:
    """Extract font style (e.g., Bold, Italic) from the filename."""
    base_name = os.path.splitext(filename)[0]
    if "Regular" in base_name:
        return "Regular"

    # Assume styles are separated by '-' (e.g., 'JetBrainsMono-Bold.ttf').
    style_parts = base_name.split("-")
    return style_parts[-1] if len(style_parts) > 1 else "Regular"


def format_style_name(style: str) -> str:
    """Format style name (e.g., 'BoldItalic' -> 'Bold Italic')."""
    formatted: List[str] = []
    for i, char in enumerate(style):
        if char.isupper() and i > 0 and not style[i - 1].isupper():
            formatted.append(" ")
        formatted.append(char)
    return "".join(formatted).strip()


def update_font_metadata(font: fontforge.font, style: str, is_nerd_font: bool) -> None:
    """Update font metadata (family name, font name, style, etc.)."""
    family_name: str = "JBD2NF" if is_nerd_font else "JBD2"
    formatted_style: str = format_style_name(style)

    font.familyname = family_name
    font.fontname = f"{family_name}-{style}"
    font.fullname = f"{family_name} {formatted_style}"

    # Add SFNT names for compatibility across platforms.
    font.appendSFNTName("English (US)", "Preferred Family", family_name)
    font.appendSFNTName("English (US)", "Family", family_name)
    font.appendSFNTName("English (US)", "Compatible Full", font.fullname)
    font.appendSFNTName("English (US)", "SubFamily", formatted_style)


def fix_nerd_font_mappings(font: fontforge.font) -> None:
    """Fix specific glyph mapping issues in Nerd Fonts (e.g., heart icon)."""
    try:
        if "heart" in font:
            font.selection.select(0xF08D0)
            font.copy()
            font.selection.select(0x2665)
            font.paste()
            font.selection.select(0xF08D0)
            font.clear()
            print("[INFO] Fixed 'heart' glyph mapping.")
    except Exception as e:
        print(f"[WARNING] Could not fix 'heart' glyph mapping: {e}")


def generate_font_files(font: fontforge.font, style: str) -> None:
    """Export the font into TTF and WOFF2 formats."""
    # Ensure filename is compact (no spaces).
    filename_base: str = f"{font.familyname.replace(' ', '')}-{style}"
    ttf_path: str = os.path.join(BUILT_FONTS_PATH, f"{filename_base}.ttf")
    woff2_path: str = os.path.join(BUILT_FONTS_PATH, f"{filename_base}.woff2")

    try:
        font.generate(ttf_path)
        print(f"[INFO] Exported TTF: {ttf_path}")
    except Exception as e:
        print(f"[ERROR] Failed to generate TTF for {font.fontname}: {e}")

    try:
        font.generate(woff2_path)
        print(f"[INFO] Exported WOFF2: {woff2_path}")
    except Exception as e:
        print(f"[ERROR] Failed to generate WOFF2 for {font.fontname}: {e}")


def process_font_file(font_path: str, is_nerd_font: bool) -> None:
    """Merge Hangul glyphs into a single English font file and update its metadata."""
    font = fontforge.open(font_path)

    if is_nerd_font:
        fix_nerd_font_mappings(font)

    # Re-select the Hangul ranges and paste the copied glyphs from D2Coding.
    font.selection.select(("unicode", "ranges"), 0x3131, 0x318E)
    font.selection.select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3)
    font.paste()

    style = get_font_style(os.path.basename(font_path))
    update_font_metadata(font, style, is_nerd_font)

    generate_font_files(font, style)
    font.close()


def build_fonts() -> None:
    """Main process: Process D2Coding font and merge it with JetBrains Mono files."""
    os.makedirs(BUILT_FONTS_PATH, exist_ok=True)

    # Open D2Coding and prepare Hangul glyphs to be copied.
    d2_font = fontforge.open(KOREAN_FONT_PATH)
    process_hangul_glyphs(d2_font)
    d2_font.copy()

    # Define directories to scan for fonts to merge.
    fonts_to_process: List[Tuple[str, bool]] = [
        (ENGLISH_FONT_PATH, False),
        (ENGLISH_FONT_NF_PATH, True),
    ]

    for dir_path, is_nerd_font in fonts_to_process:
        if not os.path.exists(dir_path):
            print(f"[WARNING] Directory not found: {dir_path}. Skipping.")
            continue

        for filename in os.listdir(dir_path):
            if filename.lower().endswith(".ttf"):
                full_path = os.path.join(dir_path, filename)
                process_font_file(full_path, is_nerd_font)

    d2_font.close()
