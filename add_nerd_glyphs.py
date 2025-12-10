#!/usr/bin/env python3
"""
Nerd Font Patcher for HackLine v2
Uses pre-patched HackNerdFont to extract Nerd Font glyphs.
This ensures all Nerd Font glyphs (including CFF-based ones) are included.
"""

import sys
import os
import copy
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

# Nerd Font source (pre-patched)
NERD_FONT_REGULAR = "HackNerdFont/HackNerdFontMono-Regular.ttf"
NERD_FONT_BOLD = "HackNerdFont/HackNerdFontMono-Bold.ttf"

# Nerd Font Unicode ranges to copy
NERD_FONT_RANGES = [
    # Powerline
    (0xE0A0, 0xE0A3),
    (0xE0B0, 0xE0D7),
    # Seti-UI + Custom
    (0xE5FA, 0xE6B7),
    # Devicons
    (0xE700, 0xE8E3),
    # Font Awesome
    (0xE200, 0xE2A9),  # FA Extension
    (0xED00, 0xF2FF),  # FA Main - includes Linux Tux U+F17C
    # Weather
    (0xE300, 0xE3E3),
    # Octicons
    (0xF400, 0xF533),
    (0x2665, 0x2665),  # Heart
    (0x26A1, 0x26A1),  # Lightning
    # IEC Power Symbols
    (0x23FB, 0x23FE),
    (0x2B58, 0x2B58),
    # Font Logos
    (0xF300, 0xF381),
    # Pomicons
    (0xE000, 0xE00A),
    # Codicons
    (0xEA60, 0xEC1E),
    # Note: Material Design (0xF0001+) excluded - causes cmap overflow
]


def is_nerd_glyph(cp):
    """Check if codepoint is in Nerd Font ranges."""
    for start, end in NERD_FONT_RANGES:
        if start <= cp <= end:
            return True
    return False


def patch_with_nerd_glyphs(base_font_path, nerd_font_path, output_path):
    """Add Nerd Font glyphs from HackNerdFont to HackLine."""
    print(f"Loading {base_font_path}...")
    font = TTFont(base_font_path)
    
    print(f"Loading {nerd_font_path}...")
    nerd_font = TTFont(nerd_font_path)
    
    base_upm = font['head'].unitsPerEm
    nerd_upm = nerd_font['head'].unitsPerEm
    scale = base_upm / nerd_upm
    print(f"Base UPM: {base_upm}, Nerd UPM: {nerd_upm}, Scale: {scale:.4f}")
    
    base_cmap = font.getBestCmap()
    nerd_cmap = nerd_font.getBestCmap()
    
    glyf_table = font['glyf']
    nerd_glyf = nerd_font['glyf']
    glyph_order = list(font.getGlyphOrder())
    
    added = 0
    for codepoint, nerd_glyph_name in nerd_cmap.items():
        if not is_nerd_glyph(codepoint):
            continue
        
        # Skip if base font already has this glyph
        if codepoint in base_cmap:
            continue
        
        # Get glyph from Nerd Font
        if nerd_glyph_name not in nerd_glyf:
            continue
        
        try:
            new_glyph_name = f"nf_{codepoint:04X}"
            source_glyph = nerd_glyf[nerd_glyph_name]
            new_glyph = copy.deepcopy(source_glyph)
            
            # Scale glyph
            if new_glyph.numberOfContours > 0 and hasattr(new_glyph, 'coordinates') and new_glyph.coordinates:
                scaled_coords = [(int(x * scale), int(y * scale)) for x, y in new_glyph.coordinates]
                new_glyph.coordinates = GlyphCoordinates(scaled_coords)
                new_glyph.recalcBounds(glyf_table)
            elif new_glyph.numberOfContours == -1 and hasattr(new_glyph, 'components'):
                for comp in new_glyph.components:
                    if hasattr(comp, 'x'):
                        comp.x = int(comp.x * scale)
                    if hasattr(comp, 'y'):
                        comp.y = int(comp.y * scale)
            
            glyf_table[new_glyph_name] = new_glyph
            glyph_order.append(new_glyph_name)
            base_cmap[codepoint] = new_glyph_name
            
            # Add hmtx
            if nerd_glyph_name in nerd_font['hmtx'].metrics:
                width, lsb = nerd_font['hmtx'].metrics[nerd_glyph_name]
                font['hmtx'].metrics[new_glyph_name] = (int(width * scale), int(lsb * scale))
            
            added += 1
            
        except Exception as e:
            print(f"Warning: Failed to copy U+{codepoint:04X}: {e}")
            continue
    
    print(f"Added {added} Nerd Font glyphs")
    
    # Update font
    font.setGlyphOrder(glyph_order)
    font['maxp'].numGlyphs = len(glyph_order)
    
    # Update font name
    if 'name' in font:
        for record in font['name'].names:
            if record.nameID in [1, 4, 6]:
                try:
                    old_name = record.toUnicode()
                    if "NF" not in old_name:
                        new_name = old_name.replace("HackLine", "HackLineNF")
                        record.string = new_name.encode(record.getEncoding())
                except:
                    pass
    
    print(f"Saving to {output_path}...")
    font.save(output_path)
    font.close()
    nerd_font.close()


def main():
    print("=" * 60)
    print("HackLine Nerd Font Patcher v2")
    print("=" * 60)
    
    # Check for HackNerdFont
    if not os.path.exists(NERD_FONT_REGULAR):
        print(f"Error: {NERD_FONT_REGULAR} not found")
        print("Please download HackNerdFont from:")
        print("https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/Hack.zip")
        sys.exit(1)
    
    # Input/Output paths
    inputs = [
        ("build/HackLine-Regular.ttf", NERD_FONT_REGULAR, "build/HackLineNF-Regular.ttf"),
        ("build/HackLine-Bold.ttf", NERD_FONT_BOLD, "build/HackLineNF-Bold.ttf"),
    ]
    
    for base_path, nerd_path, output_path in inputs:
        if not os.path.exists(base_path):
            print(f"Error: {base_path} not found")
            continue
        
        if not os.path.exists(nerd_path):
            print(f"Warning: {nerd_path} not found, skipping")
            continue
        
        print(f"\n--- Patching {base_path} ---")
        patch_with_nerd_glyphs(base_path, nerd_path, output_path)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
