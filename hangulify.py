import os
import fontforge

from config import (
    BUILT_FONTS_PATH,
    DOWNLOAD_JETBRAINS_TTF_PATH,
    SOURCE_D2_CODING_FONT_PATH,
    # BUILT_FONT_FILENAME_BASE, # 더 이상 사용하지 않음
    JETBRAINS_MONO_WIDTH,
    DOWNLOAD_JETBRAINS_MONO_NF_TTF_PATH,
    JETBRAINS_MONO_NF_WIDTH,
)

BEARING_ADJUSTMENT = 200  # 측면 여백 조정 값


def adjust_glyph_bearing(glyph, adjustment):
    """글리프 좌우 측면 여백 조정"""
    glyph.left_side_bearing = adjustment // 2 + int(glyph.left_side_bearing)
    glyph.right_side_bearing = adjustment // 2 + int(glyph.right_side_bearing)
    return glyph


def process_hangul_glyphs(font):
    """한글 글리프 선택 및 여백 조정"""
    hangul_range = font.selection.select(("unicode", "ranges"), 0x3131, 0x318E)
    hangul_range.select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3)

    for glyph_id in hangul_range:
        glyph = font[glyph_id]
        if not glyph.references:
            # Check for font width, apply adjustment if it's a JetBrains Mono or Nerd Font
            if (
                int(glyph.width) == JETBRAINS_MONO_WIDTH
                or int(glyph.width) == JETBRAINS_MONO_NF_WIDTH
            ):
                adjust_glyph_bearing(glyph, BEARING_ADJUSTMENT)
        else:
            for ref in glyph.references:
                ref_glyph = font[ref[0]]
                # Check for font width, apply adjustment if it's a JetBrains Mono or Nerd Font
                if (
                    int(ref_glyph.width) == JETBRAINS_MONO_WIDTH
                    or int(ref_glyph.width) == JETBRAINS_MONO_NF_WIDTH
                ):
                    adjust_glyph_bearing(ref_glyph, BEARING_ADJUSTMENT)
    return font


def get_font_style(original_filename):
    """원본 파일명에서 스타일 추출"""
    base_name = os.path.splitext(original_filename)[0]
    style_parts = base_name.split("-")
    # 파일명에 'Regular'가 포함된 경우를 명확하게 처리
    if "Regular" in base_name:
        return "Regular"
    return style_parts[-1] if len(style_parts) > 1 else "Regular"


def format_style_name(style):
    """스타일 이름 포매팅 (예: BoldItalic -> Bold Italic)"""
    formatted = []
    for i, char in enumerate(style):
        if char.isupper() and i > 0 and not style[i - 1].isupper():
            formatted.append(" ")
        formatted.append(char)
    return "".join(formatted).strip()


def update_font_metadata(font, style):
    """폰트 메타데이터 업데이트"""
    original_family_name = font.familyname
    new_family_name = original_family_name.replace("JetBrains Mono", "JBD2")
    new_family_name = new_family_name.replace(
        "JetBrainsMono", "JBD2"
    )  # 혹시 띄어쓰기 없는 경우 대비

    font.familyname = new_family_name
    formatted_style = format_style_name(style)

    # fontname, fullname, PSName 업데이트
    font.fontname = f"{new_family_name}-{style}"
    font.fullname = f"{new_family_name} {formatted_style}"
    font.appendSFNTName("English (US)", "Preferred Family", new_family_name)
    font.appendSFNTName("English (US)", "Family", new_family_name)
    font.appendSFNTName("English (US)", "Compatible Full", font.fullname)
    font.appendSFNTName("English (US)", "SubFamily", formatted_style)

    # PostScript 이름도 업데이트 (fontname과 동일하게 설정하는 경우가 많음)
    font.fontname = f"{new_family_name}-{style}"
    font.fullname = f"{new_family_name} {formatted_style}"
    font.appendSFNTName("English (US)", "PostScript Name", font.fontname)


def build_font():
    """메인 폰트 빌드 프로세스"""
    # 출력 디렉토리 생성
    os.makedirs(BUILT_FONTS_PATH, exist_ok=True)

    # D2 Coding 폰트 처리
    d2_font = fontforge.open(SOURCE_D2_CODING_FONT_PATH)
    process_hangul_glyphs(d2_font)
    d2_font.copy()

    # JetBrains 폰트 병합
    for download_path in [
        DOWNLOAD_JETBRAINS_TTF_PATH,
        DOWNLOAD_JETBRAINS_MONO_NF_TTF_PATH,
    ]:
        if not os.path.exists(download_path):
            print(f"[WARNING] Font directory not found: {download_path}. Skipping.")
            continue

        for filename in os.listdir(download_path):
            if not filename.lower().endswith(".ttf"):
                continue
            src_path = os.path.join(download_path, filename)
            jb_font = fontforge.open(src_path)

            # 한글 영역 선택 및 D2 Coding 글리프 붙여넣기
            jb_font.selection.select(("unicode", "ranges"), 0x3131, 0x318E).select(
                ("unicode", "ranges", "more"), 0xAC00, 0xD7A3
            )
            jb_font.paste()

            # 메타데이터 업데이트
            style = get_font_style(filename)
            update_font_metadata(jb_font, style)

            # 새로운 파일명 생성
            # 폰트의 실제 familyname과 style을 사용하여 파일명 구성
            output_filename_base = f"{jb_font.familyname.replace(' ', '')}-{style}"
            output_ttf_path = os.path.join(
                BUILT_FONTS_PATH, output_filename_base + ".ttf"
            )
            output_woff2_path = os.path.join(
                BUILT_FONTS_PATH, output_filename_base + ".woff2"
            )

            # TTF 파일 생성
            try:
                jb_font.generate(output_ttf_path)
                print(f"[INFO] Exported {output_ttf_path}")
            except Exception as e:
                print(f"[ERROR] Failed to generate TTF for {filename}: {e}")

            # WOFF2 파일 생성
            try:
                jb_font.generate(output_woff2_path)
                print(f"[INFO] Exported {output_woff2_path}")
            except Exception as e:
                print(f"[ERROR] Failed to generate WOFF2 for {filename}: {e}")

            jb_font.close()  # 폰트 객체 닫기 (메모리 관리)

    # 모든 처리가 끝난 후 D2 Coding 폰트 객체 닫기
    d2_font.close()
