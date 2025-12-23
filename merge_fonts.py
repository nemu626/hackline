#!/usr/bin/env python3
"""
HackLine Font Generator v3
Merges Hack (Latin) and LINE Seed JP (Japanese) to create HackLine.
Uses proper GlyphCoordinates for scaled glyphs.
"""

import sys
import os
import copy
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import ttProgram
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

# Paths
HACK_REGULAR = "hack_font/ttf/Hack-Regular.ttf"
HACK_BOLD = "hack_font/ttf/Hack-Bold.ttf"
LINE_SEED_JP_REGULAR = "line_seed_font/LINESeedJP_20241105/Desktop/TTF/LINESeedJP_TTF_Rg.ttf"
LINE_SEED_JP_BOLD = "line_seed_font/LINESeedJP_20241105/Desktop/TTF/LINESeedJP_TTF_Bd.ttf"

OUTPUT_REGULAR = "build/HackLine-Regular.ttf"
OUTPUT_BOLD = "build/HackLine-Bold.ttf"

# Japanese Unicode ranges (Hiragana, Katakana, CJK, etc.)
JAPANESE_RANGES = [
    (0x3000, 0x303F),  # CJK Symbols and Punctuation
    (0x3040, 0x309F),  # Hiragana
    (0x30A0, 0x30FF),  # Katakana
    (0x31F0, 0x31FF),  # Katakana Phonetic Extensions
    (0x4E00, 0x9FFF),  # CJK Unified Ideographs
    (0xFF00, 0xFFEF),  # Halfwidth and Fullwidth Forms
    (0x2E80, 0x2EFF),  # CJK Radicals Supplement
    (0x3400, 0x4DBF),  # CJK Unified Ideographs Extension A
]


def is_japanese_codepoint(cp):
    """Check if codepoint is in Japanese ranges."""
    for start, end in JAPANESE_RANGES:
        if start <= cp <= end:
            return True
    return False


def draw_dashed_square(pen):
    """Draw a rounded dashed square using the provided pen.
    Coordinates based on HackGen's Ideographic_Space.sfd, scaled by 2.
    """
    scale = 2.0

    def s(val):
        return round(val * scale)

    def m(x, y):
        pen.moveTo((s(x), s(y)))

    def l(x, y):
        pen.lineTo((s(x), s(y)))

    def c(x1, y1, x2, y2, x3, y3):
        pen.curveTo((s(x1), s(y1)), (s(x2), s(y2)), (s(x3), s(y3)))

    # Segment 1: Top-Left Corner
    m(272, 736)
    l(272, 680)
    l(259, 680)
    c(242.75, 680, 232.44, 668.79, 222, 657.44)
    c(222, 657.44, 222, 657.44, 222, 642)
    l(222, 630)
    l(166, 630)
    l(166, 642)
    c(166, 680.61, 166, 680.61, 192.17, 707.83)
    c(218.26, 733.92, 218.26, 733.92, 258.79, 735.99)
    l(259, 736)
    l(272, 736)
    pen.closePath()

    # Segment 2: Top Dash
    m(574, 736)
    l(574, 680)
    l(450, 680)
    l(450, 736)
    l(574, 736)
    pen.closePath()

    # Segment 3: Top-Right Corner
    m(752, 736)
    l(765, 736)
    c(805.75, 736, 831.94, 707.72, 858, 679.57)
    c(858, 679.57, 858, 679.57, 858, 642)
    l(858, 630)
    l(802, 630)
    l(802, 642)
    c(802, 656.44, 791.06, 668.29, 780.25, 680)
    c(780.25, 680, 780.25, 680, 765, 680)
    l(752, 680)
    l(752, 736)
    pen.closePath()

    # Segment 4: Bottom-Left Corner
    m(272, 42)
    l(259, 42)
    c(218.25, 42, 192.06, 70.28, 166, 98.43)
    c(166, 98.43, 166, 98.43, 166, 136)
    l(166, 148)
    l(222, 148)
    l(222, 136)
    c(222, 121.56, 232.94, 109.71, 243.75, 98)
    c(243.75, 98, 243.75, 98, 259, 98)
    l(272, 98)
    l(272, 42)
    pen.closePath()

    # Segment 5: Bottom Dash
    m(574, 42)
    l(450, 42)
    l(450, 98)
    l(574, 98)
    l(574, 42)
    pen.closePath()

    # Segment 6: Bottom-Right Corner
    m(752, 42)
    l(752, 98)
    l(765, 98)
    c(780.25, 98, 791.06, 109.71, 802, 122.48)
    c(802, 122.48, 802, 122.48, 802, 136)
    l(802, 148)
    l(858, 148)
    l(858, 136)
    c(858, 95.30, 831.83, 70.17, 805.74, 44.08)
    c(805.74, 44.08, 765.21, 42.01, 765, 42)
    l(752, 42)
    pen.closePath()

    # Segment 7: Left Dash
    m(166, 452)
    l(222, 452)
    l(222, 328)
    l(166, 328)
    l(166, 452)
    pen.closePath()

    # Segment 8: Right Dash
    m(858, 452)
    l(858, 328)
    l(802, 328)
    l(802, 452)
    l(858, 452)
    pen.closePath()


def create_dashed_square_glyph(font):
    """Create a rounded dashed square glyph for full-width space."""
    glyph = Glyph()

    # Use Pen to draw contours
    tt_pen = TTGlyphPen(font.getGlyphSet())
    cu2qu_pen = Cu2QuPen(tt_pen, max_err=1.0, reverse_direction=True)
    draw_dashed_square(cu2qu_pen)

    # Get the glyph from the pen
    glyph = tt_pen.glyph()

    # Initialize program (instructions)
    glyph.program = ttProgram.Program()
    glyph.program.fromBytecode(b"")

    return glyph


def scale_glyph(glyph, scale, glyf_table):
    """Scale a glyph's coordinates and bounds."""
    if glyph.numberOfContours == 0:
        # Empty glyph
        return glyph
    
    if glyph.numberOfContours == -1:
        # Composite glyph - scale all components
        if hasattr(glyph, 'components') and glyph.components:
            for comp in glyph.components:
                # Scale the offset
                if hasattr(comp, 'x'):
                    comp.x = int(comp.x * scale)
                if hasattr(comp, 'y'):
                    comp.y = int(comp.y * scale)
        return glyph
    
    # Simple glyph
    if hasattr(glyph, 'coordinates') and glyph.coordinates:
        # Scale coordinates
        scaled_coords = [(int(x * scale), int(y * scale)) for x, y in glyph.coordinates]
        glyph.coordinates = GlyphCoordinates(scaled_coords)
    
    # Recalculate bounds after scaling
    if hasattr(glyph, 'coordinates') and glyph.coordinates:
        glyph.recalcBounds(glyf_table)
    
    return glyph


def merge_fonts(hack_path, jp_path, output_path):
    """Merge Japanese glyphs from LINE Seed JP into Hack font."""
    print(f"Loading {hack_path}...")
    hack = TTFont(hack_path)
    
    print(f"Loading {jp_path}...")
    jp_font = TTFont(jp_path)
    
    # Get unitsPerEm
    hack_upm = hack['head'].unitsPerEm
    jp_upm = jp_font['head'].unitsPerEm
    scale = hack_upm / jp_upm
    print(f"Hack unitsPerEm: {hack_upm}, LINE Seed JP unitsPerEm: {jp_upm}, scale: {scale:.4f}")
    
    # Get cmap tables
    hack_cmap = hack.getBestCmap()
    jp_cmap = jp_font.getBestCmap()
    
    # Get glyph tables
    hack_glyf = hack['glyf']
    jp_glyf = jp_font['glyf']
    
    # Get glyph order
    hack_glyph_order = list(hack.getGlyphOrder())
    
    # Find Japanese glyphs to copy
    glyphs_copied = 0

    # Add special handling for U+3000 (Full-width space)
    # We always overwrite U+3000 to ensure visualization
    print("Creating custom rounded dashed square glyph for U+3000...")
    new_glyph_name = "uni3000"

    # Create the glyph
    new_glyph = create_dashed_square_glyph(hack)
    hack_glyf[new_glyph_name] = new_glyph

    # Add to glyph order if not present
    if new_glyph_name not in hack_glyph_order:
        hack_glyph_order.append(new_glyph_name)

    # Add to ALL cmap tables
    for table in hack['cmap'].tables:
        if table.isUnicode():
            table.cmap[0x3000] = new_glyph_name

    # Add hmtx (width 2048, lsb 0)
    # Note: We use 2048 to match the em size, as is common for full-width
    hack['hmtx'].metrics[new_glyph_name] = (2048, 0)

    glyphs_copied += 1

    for codepoint, jp_glyph_name in jp_cmap.items():
        if not is_japanese_codepoint(codepoint):
            continue
        
        # Skip U+3000 as we handled it manually
        if codepoint == 0x3000:
            continue

        # Skip if Hack already has this character
        if codepoint in hack_cmap:
            continue
        
        # Get glyph from LINE Seed JP
        if jp_glyph_name not in jp_glyf:
            continue
        
        jp_glyph = jp_glyf[jp_glyph_name]
        
        # Create new glyph name for Hack (avoid conflicts)
        new_glyph_name = f"uni{codepoint:04X}"
        if new_glyph_name in hack_glyph_order:
            new_glyph_name = f"jp_{codepoint:04X}"
        
        # Copy and scale the glyph
        try:
            new_glyph = copy.deepcopy(jp_glyph)
            new_glyph = scale_glyph(new_glyph, scale, hack_glyf)
            
            # Add to Hack's glyf table
            hack_glyf[new_glyph_name] = new_glyph
            
            # Add to glyph order
            hack_glyph_order.append(new_glyph_name)
            
            # Add to cmap
            hack_cmap[codepoint] = new_glyph_name
            
            # Scale and add hmtx (horizontal metrics)
            if jp_glyph_name in jp_font['hmtx'].metrics:
                width, lsb = jp_font['hmtx'].metrics[jp_glyph_name]
                hack['hmtx'].metrics[new_glyph_name] = (int(width * scale), int(lsb * scale))
            
            glyphs_copied += 1
            
        except Exception as e:
            print(f"Warning: Failed to copy glyph U+{codepoint:04X} ({jp_glyph_name}): {e}")
            continue
    
    print(f"Copied {glyphs_copied} Japanese glyphs")
    
    # Update glyph order
    hack.setGlyphOrder(hack_glyph_order)
    
    # Update maxp table
    hack['maxp'].numGlyphs = len(hack_glyph_order)
    
    # Update font name
    if 'name' in hack:
        for record in hack['name'].names:
            if record.nameID in [1, 4, 6]:  # Family, Full, PostScript name
                try:
                    old_name = record.toUnicode()
                    new_name = old_name.replace("Hack", "HackLine")
                    record.string = new_name.encode(record.getEncoding())
                except:
                    pass
    
    # Save
    print(f"Saving to {output_path}...")
    hack.save(output_path)
    print(f"Saved {output_path}")
    
    hack.close()
    jp_font.close()


def main():
    """Main entry point."""
    print("=" * 60)
    print("HackLine Font Generator v3")
    print("=" * 60)
    
    # Check input files
    if not os.path.exists(HACK_REGULAR):
        print(f"Error: {HACK_REGULAR} not found")
        sys.exit(1)
    
    if not os.path.exists(LINE_SEED_JP_REGULAR):
        print(f"Error: {LINE_SEED_JP_REGULAR} not found")
        sys.exit(1)
    
    # Create build directory
    os.makedirs("build", exist_ok=True)
    
    # Merge Regular
    print("\n--- Generating Regular weight ---")
    merge_fonts(HACK_REGULAR, LINE_SEED_JP_REGULAR, OUTPUT_REGULAR)
    
    # Merge Bold (if available)
    if os.path.exists(HACK_BOLD) and os.path.exists(LINE_SEED_JP_BOLD):
        print("\n--- Generating Bold weight ---")
        merge_fonts(HACK_BOLD, LINE_SEED_JP_BOLD, OUTPUT_BOLD)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
