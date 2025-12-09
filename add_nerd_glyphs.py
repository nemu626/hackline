#!/usr/bin/env python3
"""
Nerd Font Patcher for HackLine
Adds Nerd Font glyphs to HackLine using fonttools (no fontforge required).
"""

import sys
import os
import copy
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

# Nerd Font glyph sources
GLYPH_SOURCES = [
    ("font_patcher/src/glyphs/powerline-symbols/PowerlineSymbols.otf", "Powerline"),
    ("font_patcher/src/glyphs/powerline-extra/PowerlineExtraSymbols.otf", "PowerlineExtra"),
    ("font_patcher/src/glyphs/font-awesome/FontAwesome.otf", "FontAwesome"),
    ("font_patcher/src/glyphs/devicons/devicons.ttf", "Devicons"),
    ("font_patcher/src/glyphs/octicons/octicons.ttf", "Octicons"),
    ("font_patcher/src/glyphs/pomicons/Pomicons.otf", "Pomicons"),
    ("font_patcher/src/glyphs/codicons/codicon.ttf", "Codicons"),
    ("font_patcher/src/glyphs/font-logos.ttf", "FontLogos"),
    ("font_patcher/src/glyphs/Unicode_IEC_symbol_font.otf", "IEC"),
]

# Nerd Font Unicode ranges to copy
NERD_FONT_RANGES = [
    # Powerline
    (0xE0A0, 0xE0A2),
    (0xE0B0, 0xE0B3),
    # Powerline Extra
    (0xE0A3, 0xE0A3),
    (0xE0B4, 0xE0C8),
    (0xE0CA, 0xE0CA),
    (0xE0CC, 0xE0D7),
    # Seti-UI + Custom
    (0xE5FA, 0xE6B7),
    # Devicons
    (0xE700, 0xE8E3),
    # Font Awesome
    (0xED00, 0xF2FF),
    # Font Awesome Extension
    (0xE200, 0xE2A9),
    # Material Design (skip - too large and requires special handling)
    # (0xF0001, 0xF1AF0),
    # Weather
    (0xE300, 0xE3E3),
    # Octicons
    (0xF400, 0xF533),
    # IEC Power Symbols
    (0x23FB, 0x23FE),
    (0x2B58, 0x2B58),
    # Font Logos
    (0xF300, 0xF381),
    # Pomicons
    (0xE000, 0xE00A),
    # Codicons
    (0xEA60, 0xEC1E),
]


def is_nerd_glyph(cp):
    """Check if codepoint is in Nerd Font ranges."""
    for start, end in NERD_FONT_RANGES:
        if start <= cp <= end:
            return True
    return False


def patch_with_nerd_glyphs(base_font_path, output_path):
    """Add Nerd Font glyphs to a font."""
    print(f"Loading {base_font_path}...")
    font = TTFont(base_font_path)
    
    base_upm = font['head'].unitsPerEm
    base_cmap = font.getBestCmap()
    
    # Check if font has glyf table (TrueType) or CFF (OpenType)
    is_truetype = 'glyf' in font
    
    if not is_truetype:
        print("Warning: Base font is CFF (OpenType). Nerd glyph merging may be limited.")
        font.close()
        # For CFF fonts, just copy the file as-is for now
        import shutil
        shutil.copy(base_font_path, output_path)
        return
    
    glyf_table = font['glyf']
    glyph_order = list(font.getGlyphOrder())
    
    total_added = 0
    
    for source_path, source_name in GLYPH_SOURCES:
        if not os.path.exists(source_path):
            print(f"  Skipping {source_name}: {source_path} not found")
            continue
        
        try:
            source_font = TTFont(source_path)
        except Exception as e:
            print(f"  Skipping {source_name}: {e}")
            continue
        
        source_upm = source_font['head'].unitsPerEm
        scale = base_upm / source_upm
        source_cmap = source_font.getBestCmap()
        
        # Check source font type
        source_is_truetype = 'glyf' in source_font
        
        added = 0
        for codepoint, glyph_name in source_cmap.items():
            if not is_nerd_glyph(codepoint):
                continue
            
            if codepoint in base_cmap:
                continue  # Already have this glyph
            
            try:
                new_glyph_name = f"nf_{codepoint:04X}"
                
                if source_is_truetype:
                    # TrueType source
                    source_glyf = source_font['glyf']
                    if glyph_name not in source_glyf:
                        continue
                    
                    source_glyph = source_glyf[glyph_name]
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
                else:
                    # CFF source - create empty placeholder glyph
                    # Note: Full CFF to TTF conversion is complex, skip for now
                    continue
                
                glyph_order.append(new_glyph_name)
                base_cmap[codepoint] = new_glyph_name
                
                # Add hmtx
                if glyph_name in source_font['hmtx'].metrics:
                    width, lsb = source_font['hmtx'].metrics[glyph_name]
                    font['hmtx'].metrics[new_glyph_name] = (int(width * scale), int(lsb * scale))
                
                added += 1
                
            except Exception as e:
                continue
        
        source_font.close()
        
        if added > 0:
            print(f"  Added {added} glyphs from {source_name}")
            total_added += added
    
    # Update font
    font.setGlyphOrder(glyph_order)
    font['maxp'].numGlyphs = len(glyph_order)
    
    # Update font name to include NF suffix
    if 'name' in font:
        for record in font['name'].names:
            if record.nameID in [1, 4, 6]:
                try:
                    old_name = record.toUnicode()
                    if "NF" not in old_name:
                        new_name = old_name.replace("-Regular", " NF-Regular").replace("-Bold", " NF-Bold")
                        if new_name == old_name:
                            new_name = old_name + " NF"
                        record.string = new_name.encode(record.getEncoding())
                except:
                    pass
    
    print(f"Total: Added {total_added} Nerd Font glyphs")
    print(f"Saving to {output_path}...")
    font.save(output_path)
    font.close()


def main():
    print("=" * 60)
    print("HackLine Nerd Font Patcher")
    print("=" * 60)
    
    # Input/Output paths
    inputs = [
        ("build/HackLine-Regular.ttf", "build/HackLineNF-Regular.ttf"),
        ("build/HackLine-Bold.ttf", "build/HackLineNF-Bold.ttf"),
    ]
    
    for input_path, output_path in inputs:
        if not os.path.exists(input_path):
            print(f"Error: {input_path} not found")
            continue
        
        print(f"\n--- Patching {input_path} ---")
        patch_with_nerd_glyphs(input_path, output_path)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
