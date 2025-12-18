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
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program

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


def create_visible_space_glyph(upm):
    """Create a glyph for a visible full-width space (U+3000) as a dashed square."""
    glyph = Glyph()

    # Dashed square parameters
    box_size = int(upm * 0.45)
    margin = int((upm - box_size) / 2)
    dash_thickness = int(upm * 0.035)

    # Dash/gap calculation for each side
    dash_count = 3
    # Ratio of gap length to dash length
    gap_to_dash_ratio = 0.5
    total_dash_units = dash_count + (dash_count - 1) * gap_to_dash_ratio
    dash_len = int(box_size / total_dash_units)
    gap_len = int(dash_len * gap_to_dash_ratio)

    x_min, y_min = margin, margin
    x_max, y_max = margin + box_size, margin + box_size

    coordinates = []
    endPtsOfContours = []
    contour_idx = -1

    # Bottom side
    x_curr = x_min
    for _ in range(dash_count):
        x_start, x_end = x_curr, x_curr + dash_len
        coordinates.extend([
            (x_start, y_min), (x_end, y_min),
            (x_end, y_min + dash_thickness), (x_start, y_min + dash_thickness)
        ])
        contour_idx += 4
        endPtsOfContours.append(contour_idx)
        x_curr = x_end + gap_len

    # Top side
    x_curr = x_min
    for _ in range(dash_count):
        x_start, x_end = x_curr, x_curr + dash_len
        coordinates.extend([
            (x_start, y_max - dash_thickness), (x_end, y_max - dash_thickness),
            (x_end, y_max), (x_start, y_max)
        ])
        contour_idx += 4
        endPtsOfContours.append(contour_idx)
        x_curr = x_end + gap_len

    # Left side
    y_curr = y_min
    for _ in range(dash_count):
        y_start, y_end = y_curr, y_curr + dash_len
        coordinates.extend([
            (x_min, y_start), (x_min + dash_thickness, y_start),
            (x_min + dash_thickness, y_end), (x_min, y_end)
        ])
        contour_idx += 4
        endPtsOfContours.append(contour_idx)
        y_curr = y_end + gap_len

    # Right side
    y_curr = y_min
    for _ in range(dash_count):
        y_start, y_end = y_curr, y_curr + dash_len
        coordinates.extend([
            (x_max - dash_thickness, y_start), (x_max, y_start),
            (x_max, y_end), (x_max - dash_thickness, y_end)
        ])
        contour_idx += 4
        endPtsOfContours.append(contour_idx)
        y_curr = y_end + gap_len

    glyph.coordinates = GlyphCoordinates(coordinates)
    glyph.endPtsOfContours = endPtsOfContours
    glyph.numberOfContours = len(endPtsOfContours)
    glyph.flags = b"\x01" * len(coordinates) # All points on-curve
    glyph.program = Program()

    return glyph


def is_japanese_codepoint(cp):
    """Check if codepoint is in Japanese ranges."""
    for start, end in JAPANESE_RANGES:
        if start <= cp <= end:
            return True
    return False


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

    # Inject visible glyph for U+3000 (full-width space)
    codepoint_space = 0x3000
    if is_japanese_codepoint(codepoint_space):
        print("Injecting visible glyph for U+3000...")
        visible_space_glyph = create_visible_space_glyph(hack_upm)
        visible_space_glyph.recalcBounds(hack_glyf)

        glyph_name = "uni3000.visible"
        if glyph_name in hack_glyph_order:
            glyph_name = "uni3000.visible.alt"

        hack_glyf[glyph_name] = visible_space_glyph
        if glyph_name not in hack_glyph_order:
            hack_glyph_order.append(glyph_name)

        hack_cmap[codepoint_space] = glyph_name
        hack['hmtx'].metrics[glyph_name] = (hack_upm, 0) # Full-width

    for codepoint, jp_glyph_name in jp_cmap.items():
        if not is_japanese_codepoint(codepoint):
            continue
        
        # Skip U+3000 as it's already handled
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
