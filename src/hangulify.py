"""Merge D2Coding Hangul glyphs into JetBrains Mono (plain + Nerd Font)."""

import os
from typing import Any, List, Tuple

import fontforge

from .config import (
    BUILT_FONTS_PATH,
    ENGLISH_FONT_NF_PATH,
    ENGLISH_FONT_PATH,
    KOREAN_FONT_PATH,
    KOREAN_FONT_WIDTH,
)

# Value to adjust the side bearings of the glyphs.
BEARING_ADJUSTMENT: int = 200

# Hangul Jamo (U+3131-U+318E) and Hangul Syllables (U+AC00-U+D7A3).
HANGUL_RANGES: Tuple[Tuple[int, int], ...] = ((0x3131, 0x318E), (0xAC00, 0xD7A3))


def select_hangul(font: fontforge.font) -> None:
    """Select all Hangul glyphs merged from D2Coding."""
    start, end = HANGUL_RANGES[0]
    font.selection.select(("unicode", "ranges"), start, end)
    for start, end in HANGUL_RANGES[1:]:
        font.selection.select(("unicode", "ranges", "more"), start, end)


def adjust_glyph_bearing(glyph: Any, adjustment: int) -> None:
    """Adjust the left and right side bearings of a glyph."""
    glyph.left_side_bearing = (adjustment // 2) + int(glyph.left_side_bearing)
    glyph.right_side_bearing = (adjustment // 2) + int(glyph.right_side_bearing)


def _has_d2_width(glyph: Any) -> bool:
    return int(glyph.width) == KOREAN_FONT_WIDTH


def process_hangul_glyphs(font: fontforge.font) -> None:
    """Adjust bearings of Hangul glyphs so they align with JetBrains Mono."""
    select_hangul(font)

    for glyph in font.selection.byGlyphs:
        if not glyph.references:
            if _has_d2_width(glyph):
                adjust_glyph_bearing(glyph, BEARING_ADJUSTMENT)
            continue
        for ref in glyph.references:
            ref_glyph = font[ref[0]]
            if _has_d2_width(ref_glyph):
                adjust_glyph_bearing(ref_glyph, BEARING_ADJUSTMENT)


def get_font_style(filename: str) -> str:
    """Extract font style (e.g., Bold, Regular) from the filename."""
    base_name = os.path.splitext(filename)[0]
    if "Regular" in base_name:
        return "Regular"
    # Assume styles are separated by '-' (e.g., 'JetBrainsMono-Bold.ttf').
    return base_name.split("-")[-1] or "Regular"


def format_style_name(style: str) -> str:
    """Format style name (e.g., 'BoldItalic' -> 'Bold Italic')."""
    chars: List[str] = []
    for i, char in enumerate(style):
        if char.isupper() and i > 0 and not style[i - 1].isupper():
            chars.append(" ")
        chars.append(char)
    return "".join(chars).strip()


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
        if "heart" in font and 0xF08D0 in font:
            src = font[0xF08D0]
            dst = font.createChar(0x2665)
            dst.foreground = src.foreground
            dst.width = src.width
            src.clear()
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


def process_font_file(font_path: str, is_nerd_font: bool, d2_font: fontforge.font) -> None:
    """Merge Hangul glyphs into a single English font file and update its metadata."""
    font = fontforge.open(font_path)
    try:
        # Guarantee clipboard has Hangul glyphs from D2Coding
        d2_font.copy()
        select_hangul(font)
        font.paste()

        if is_nerd_font:
            fix_nerd_font_mappings(font)

        style = get_font_style(os.path.basename(font_path))
        update_font_metadata(font, style, is_nerd_font)
        generate_font_files(font, style)
    finally:
        font.close()


def build_fonts() -> None:
    """Process D2Coding font and merge it with JetBrains Mono files."""
    os.makedirs(BUILT_FONTS_PATH, exist_ok=True)

    d2_font = fontforge.open(KOREAN_FONT_PATH)
    try:
        process_hangul_glyphs(d2_font)

        # Copy once and reuse for every target font (avoids N reselections).
        select_hangul(d2_font)
        d2_font.copy()

        fonts_to_process: List[Tuple[str, bool]] = [
            (ENGLISH_FONT_PATH, False),
            (ENGLISH_FONT_NF_PATH, True),
        ]
        for dir_path, is_nerd_font in fonts_to_process:
            if not os.path.exists(dir_path):
                print(f"[WARNING] Directory not found: {dir_path}. Skipping.")
                continue
            for filename in sorted(os.listdir(dir_path)):
                if filename.lower().endswith(".ttf"):
                    process_font_file(os.path.join(dir_path, filename), is_nerd_font, d2_font)
    finally:
        d2_font.close()
