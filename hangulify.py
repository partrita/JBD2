import fontforge
import shutil
import os

from config import (
    built_fonts_path,
    download_jetbrains_ttf_path,
    source_d2_coding_font_path,
    built_font_filename_base,
    d2_coding_version,
    d2_coding_date,
    jetbrains_mono_width, # Assuming this is still needed
    # d2_coding_width, # Add if used, current snippet doesn't show usage
)

def add_bearing(glyph, addition):
    glyph.left_side_bearing = addition//2+int(glyph.left_side_bearing)
    glyph.right_side_bearing = addition//2+int(glyph.right_side_bearing)
    return glyph

def replace_name(string):
    return string.replace("JetBrainsMono", built_font_filename_base) \
            .replace("JetBrains Mono", built_font_filename_base)

def build_font():
    if not os.path.exists(built_fonts_path):
        print(f'[INFO] Make \'{built_fonts_path}\' directory')
        os.makedirs(built_fonts_path)

    d2 = fontforge.open(source_d2_coding_font_path)

    hangul = d2.selection.select(("unicode", "ranges"), 0x3131, 0x318E) \
            .select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3) 
    for i in hangul:
        glyph = d2[i]
        if not glyph.references:
            add_bearing(glyph, 200)
        else:
            for j in glyph.references:
                refglyph = d2[j[0]]
                if int(refglyph.width) == jetbrains_mono_width:
                    continue
                else:
                    add_bearing(refglyph, 200)
    d2.copy()

    print("[INFO] Merge fonts and output")
    for font_filename in os.listdir(download_jetbrains_ttf_path):
        if not font_filename.lower().endswith(".ttf"):
            continue

        original_font_path = os.path.join(download_jetbrains_ttf_path, font_filename)
        jb = fontforge.open(original_font_path)
        jb.selection.select(("unicode", "ranges"), 0x3131, 0x318E) \
            .select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3)
        jb.paste()

        # Extract style from original_base_name.
        original_base_name = font_filename.split('.')[0] # e.g., "JetBrainsMono-Bold"
        style_parts = original_base_name.split('-')
        style = ""
        if len(style_parts) > 1:
            # Handles cases like "JetBrainsMono-Bold" -> "Bold"
            # and "JetBrainsMonoNL-Bold" -> "Bold"
            # and "JetBrainsMonoNerdFont-Bold" -> "Bold" (if Nerd Font parts are also split by '-')
            # We take the last part as style.
            style = style_parts[-1]
            # If original name was like "JetBrainsMonoNLNerd-Thin" this would take "Thin"
            # If it was "JetBrainsMono-BoldItalic" this would take "BoldItalic"

        # Construct new filename
        if style and style.lower() != "regular":
            new_filename_base = f"{built_font_filename_base}-{style}"
            # For metadata, if style is e.g. "BoldItalic", fullname might be "JBD2 Bold Italic"
            # fontname "JBD2-BoldItalic"
            # familyname "JBD2"
            current_style_for_metadata = style
        else: # style is "Regular" or empty (e.g. "JetBrainsMono.ttf")
            new_filename_base = f"{built_font_filename_base}-Regular"
            current_style_for_metadata = "Regular"

        new_filename = f"{new_filename_base}.ttf"

        # Update font metadata
        jb.familyname = built_font_filename_base # Should be "JBD2"
        
        # Construct fontname like "JBD2-Bold", "JBD2-Regular"
        jb.fontname = f"{built_font_filename_base}-{current_style_for_metadata}"
        
        # Construct fullname like "JBD2 Bold", "JBD2 Regular"
        # Need to insert space before capital letters in style if it's like "BoldItalic"
        # For "Bold" -> "Bold", for "BoldItalic" -> "Bold Italic"
        formatted_style_for_fullname = ""
        if current_style_for_metadata:
            temp_style = current_style_for_metadata
            # Add a space before uppercase letters not at the start of the string
            # e.g., BoldItalic -> Bold Italic
            # Regular -> Regular
            # ExtraLight -> Extra Light
            for i, char in enumerate(temp_style):
                if char.isupper() and i > 0:
                    # Check if previous char is also uppercase (e.g. NL)
                    # We only want to split if it's a transition like 'BoldItalic' not 'NL'
                    if not (temp_style[i-1].isupper() and len(temp_style) > i+1 and temp_style[i+1].islower()): # Avoid splitting "NL" in "JetBrainsMonoNL"
                         formatted_style_for_fullname += " "
                formatted_style_for_fullname += char
            if not formatted_style_for_fullname.strip(): # If style was e.g. ""
                 formatted_style_for_fullname = "Regular"
        else:
            formatted_style_for_fullname = "Regular"

        jb.fullname = f"{built_font_filename_base} {formatted_style_for_fullname.strip()}"


        # Ensure "Regular" is correctly handled for sfnt_names SubFamily
        subfamily_name_for_sfnt = formatted_style_for_fullname.strip()
        if not subfamily_name_for_sfnt : # Should not happen with current logic but as a safeguard
            subfamily_name_for_sfnt = "Regular"


        # Clear existing problematic names first to avoid conflicts or duplications if possible
        # This is a bit of a heavy hammer, might need more nuanced handling
        # For now, let's trust appendSFNTName to override or fontforge to handle it.
        # Common practice is to set specific name IDs if known, but append usually works for general cases.

        jb.appendSFNTName("English (US)", "Preferred Family", jb.familyname)
        jb.appendSFNTName("English (US)", "Family", jb.familyname)
        jb.appendSFNTName("English (US)", "Compatible Full", jb.fullname) # Used by Windows
        jb.appendSFNTName("English (US)", "SubFamily", subfamily_name_for_sfnt) # e.g., "Bold", "Regular", "Bold Italic"
        # Potentially update other name table entries if needed, e.g., Typographic Family, etc.
        # For now, these cover the main ones.

        # Update sfnt names ('fullname', 'familyname', 'fontname', 'subfamily') using the new values
        # FontForge does this implicitly when properties like jb.fontname are set, but explicit appendSFNTName ensures specific entries.
        # The SubFamily entry is particularly important.
        # We need to find and update the existing SubFamily or ensure our appended one takes precedence.
        # The existing code for subFamily was:
        # subFamilyIdx = [x[1] for x in jb.sfnt_names].index("SubFamily")
        # sfntNamesStringIdIdx = 2
        # subFamily = jb.sfnt_names[subFamilyIdx][sfntNamesStringIdIdx]
        # This was reading the *old* SubFamily. We need to set the *new* one.
        # The appendSFNTName("English (US)", "SubFamily", subfamily_name_for_sfnt) should handle this.

        output_font_path = os.path.join(built_fonts_path, new_filename)
        jb.generate(new_filename) # Generates in current dir
        shutil.move(new_filename, output_font_path)
        print(f"[INFO] Exported {output_font_path}")
