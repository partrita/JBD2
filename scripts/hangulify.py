import os
from typing import Any

import fontforge

from config import (
    BUILT_FONTS_PATH,
    ENGLISH_FONT_NF_PATH,
    ENGLISH_FONT_PATH,
    ENGLISH_FONT_NF_WIDTH,
    ENGLISH_FONT_WIDTH,
    KOREAN_FONT_PATH,
)

# 글리프의 사이드 베어링을 조정하는 값입니다.
BEARING_ADJUSTMENT: int = 200


def adjust_glyph_bearing(glyph: Any, adjustment: int) -> Any:
    """글리프의 왼쪽 및 오른쪽 사이드 베어링을 조정합니다."""
    glyph.left_side_bearing = adjustment // 2 + int(glyph.left_side_bearing)
    glyph.right_side_bearing = adjustment // 2 + int(glyph.right_side_bearing)
    return glyph


def process_hangul_glyphs(font: fontforge.font) -> fontforge.font:
    """한글 글리프를 선택하고 베어링을 조정합니다."""
    hangul_range = font.selection.select(("unicode", "ranges"), 0x3131, 0x318E)
    hangul_range.select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3)

    for glyph_id in hangul_range:
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
    return font


def get_font_style(original_filename: str) -> str:
    """원본 파일명에서 폰트 스타일을 추출합니다."""
    base_name = os.path.splitext(original_filename)[0]
    if "Regular" in base_name:
        return "Regular"
    style_parts = base_name.split("-")
    return style_parts[-1] if len(style_parts) > 1 else "Regular"


def format_style_name(style: str) -> str:
    """스타일 이름을 포맷팅합니다(예: 'BoldItalic' -> 'Bold Italic')."""
    formatted = []
    for i, char in enumerate(style):
        if char.isupper() and i > 0 and not style[i - 1].isupper():
            formatted.append(" ")
        formatted.append(char)
    return "".join(formatted).strip()


def update_font_metadata(font: fontforge.font, style: str) -> None:
    """폰트의 메타데이터(패밀리 이름, 폰트 이름, 스타일 등)를 업데이트합니다."""
    original_family_name = font.familyname
    new_family_name = original_family_name.replace("JetBrains Mono", "JBD2").replace(
        "JetBrainsMono", "JBD2"
    )

    font.familyname = new_family_name
    formatted_style = format_style_name(style)

    font.fontname = f"{new_family_name}-{style}"
    font.fullname = f"{new_family_name} {formatted_style}"
    font.appendSFNTName("English (US)", "Preferred Family", new_family_name)
    font.appendSFNTName("English (US)", "Family", new_family_name)
    font.appendSFNTName("English (US)", "Compatible Full", font.fullname)
    font.appendSFNTName("English (US)", "SubFamily", formatted_style)


def re_encode_for_nerd_font(font: fontforge.font) -> None:
    """Nerd Font의 특정 글리프 매핑 문제를 수정합니다(예: 하트 아이콘)."""
    try:
        if "heart" in font:
            font.selection.select(0xF08D0)
            font.copy()
            font.selection.select(0x2665)
            font.paste()
            font.selection.select(0xF08D0)
            font.clear()
            print("[INFO] 'heart' 글리프 매핑을 수정했습니다.")
    except Exception as e:
        print(f"[WARNING] 'heart' 글리프 매핑을 수정할 수 없습니다: {e}")


def generate_font_files(font: fontforge.font, style: str) -> None:
    """최종 TTF 및 WOFF2 폰트 파일을 생성하고 내보냅니다."""
    output_filename_base = f"{font.familyname.replace(' ', '')}-{style}"
    output_ttf_path = os.path.join(
        BUILT_FONTS_PATH, f"{output_filename_base}.ttf"
    )
    output_woff2_path = os.path.join(
        BUILT_FONTS_PATH, f"{output_filename_base}.woff2"
    )

    try:
        font.generate(output_ttf_path)
        print(f"[INFO] {output_ttf_path} 내보내기 완료")
    except Exception as e:
        print(f"[ERROR] {font.fontname}에 대한 TTF 생성 실패: {e}")

    try:
        font.generate(output_woff2_path)
        print(f"[INFO] {output_woff2_path} 내보내기 완료")
    except Exception as e:
        print(f"[ERROR] {font.fontname}에 대한 WOFF2 생성 실패: {e}")


def process_font_file(font_path: str, is_nerd_font: bool) -> None:
    """
    단일 폰트 파일을 처리하여 한글 글리프를 병합하고 메타데이터를 업데이트합니다.
    """
    jb_font = fontforge.open(font_path)

    if is_nerd_font:
        re_encode_for_nerd_font(jb_font)

    # 한글 스크립트 범위를 선택하고 복사된 D2Coding 글리프를 붙여넣습니다.
    jb_font.selection.select(("unicode", "ranges"), 0x3131, 0x318E).select(
        ("unicode", "ranges", "more"), 0xAC00, 0xD7A3
    )
    jb_font.paste()

    style = get_font_style(os.path.basename(font_path))
    update_font_metadata(jb_font, style)

    generate_font_files(jb_font, style)
    jb_font.close()


def build_fonts() -> None:
    """
    메인 폰트 빌드 프로세스입니다. D2 Coding 폰트를 열고 처리한 다음,
    각 JetBrains Mono 및 Nerd Font 파일과 병합합니다.
    """
    os.makedirs(BUILT_FONTS_PATH, exist_ok=True)

    d2_font = fontforge.open(KOREAN_FONT_PATH)
    process_hangul_glyphs(d2_font)
    d2_font.copy()

    font_dirs_to_process = [
        (ENGLISH_FONT_PATH, False),
        (ENGLISH_FONT_NF_PATH, True),
    ]

    for dir_path, is_nerd_font in font_dirs_to_process:
        if not os.path.exists(dir_path):
            print(f"[WARNING] 폰트 디렉터리를 찾을 수 없습니다: {dir_path}. 건너뜁니다.")
            continue

        for filename in os.listdir(dir_path):
            if filename.lower().endswith(".ttf"):
                font_file_path = os.path.join(dir_path, filename)
                process_font_file(font_file_path, is_nerd_font)

    d2_font.close()


if __name__ == "__main__":
    build_fonts()