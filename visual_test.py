#!/usr/bin/env python3
"""
HackLine Font Visual Test Script
Generates an image from a test string using the built HackLine font.
"""

import os
import argparse
from PIL import Image, ImageDraw, ImageFont

# --- Default Configuration ---
DEFAULT_FONT_PATH = "build/HackLine-Regular.ttf"
DEFAULT_OUTPUT_PATH = "build/test_image.png"

# Basic text test
# U+3000 = Ideographic Space (全角スペース)
FULLWIDTH_SPACE = "\u3000"
TEXT_JAPANESE = "Lorem ipsumであのイーハトーヴォの世界が広がります。"
TEXT_KOREAN = "가나다라마바사 아자차카타파하 LOREM IPSUM."
TEXT_ALPHANUMERIC = f"""\
abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890 `~!@#$%^&*()_-=+[]{{}}|;:'",.<>/
全角スペース：[{FULLWIDTH_SPACE}] ← 括弧内に全角スペース
"""

# Nerd Font icon test (representative glyphs from each set)
# Using Unicode escapes to ensure correct encoding
NERD_ICONS = {
    "Powerline": ["\ue0a0", "\ue0a1", "\ue0a2", "\ue0b0", "\ue0b2", "\ue0b4", "\ue0b6", "\ue0c0", "\ue0c4", "\ue0d0"],
    "Seti-UI": ["\ue5fa", "\ue5fb", "\ue5fc", "\ue5fd", "\ue5fe", "\ue5ff", "\ue600", "\ue601", "\ue602", "\ue603"],
    "Devicons": ["\ue700", "\ue701", "\ue702", "\ue703", "\ue704", "\ue705", "\ue706", "\ue707", "\ue708", "\ue709"],
    "Font Awesome": ["\ued00", "\uf000", "\uf001", "\uf002", "\uf004", "\uf005", "\uf007", "\uf008", "\uf009", "\uf00a"],
    "Weather": ["\ue300", "\ue301", "\ue302", "\ue303", "\ue304", "\ue305", "\ue306", "\ue307", "\ue308", "\ue309"],
    "Octicons": ["\uf400", "\uf401", "\uf402", "\uf403", "\uf404", "\uf405", "\uf406", "\uf407", "\uf408", "\uf409"],
    "Font Logos": ["\uf300", "\uf301", "\uf302", "\uf303", "\uf304", "\uf305", "\uf306", "\uf307", "\uf308", "\uf309"],
    "Pomicons": ["\ue000", "\ue001", "\ue002", "\ue003", "\ue004", "\ue005", "\ue006", "\ue007", "\ue008", "\ue009"],
    "Codicons": ["\uea60", "\uea61", "\uea62", "\uea63", "\uea64", "\uea65", "\uea66", "\uea67", "\uea68", "\uea69"],
    "Material Design": ["\U000f0372", "\U000f0794", "\U000f0238", "\U000f02a4", "\U000f03d8", "\U000f1c3e", "\U000f08c7", "\U000f056e", "\U000f1918", "\U000f0668"],
}

def build_nerd_font_text():
    """Build Nerd Font test text from icon definitions."""
    lines = ["--- Nerd Font Icon Test ---"]
    for name, icons in NERD_ICONS.items():
        icons_str = " ".join(icons)
        lines.append(f"{name}: {icons_str}")
    return "\n".join(lines)

TEXT_NERD_FONT = build_nerd_font_text()


FONT_SIZE = 24
BACKGROUND_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black
PADDING = 20

# --- Main Script ---
def main():
    """Generates the test image."""
    parser = argparse.ArgumentParser(description="Generate a visual test image for a font.")
    parser.add_argument("--font-path", default=DEFAULT_FONT_PATH, help="Path to the TTF font file.")
    parser.add_argument("--output-path", default=DEFAULT_OUTPUT_PATH, help="Path to save the output PNG image.")
    args = parser.parse_args()

    print("--- Starting Visual Test Script ---")

    # Check if font file exists
    if not os.path.exists(args.font_path):
        print(f"Error: Font file not found at '{args.font_path}'")
        print("Please ensure the font has been built and the path is correct.")
        return

    # Load font
    try:
        font = ImageFont.truetype(args.font_path, FONT_SIZE)
    except IOError:
        print(f"Error: Could not load font from '{args.font_path}'")
        return

    # Determine which text to use based on font type
    base_text_parts = [TEXT_JAPANESE]
    font_name = os.path.basename(args.font_path)

    # Add Korean text only for JK variants
    if "JK" in font_name:
        base_text_parts.append(TEXT_KOREAN)
        print("Korean text included for JK variant.")

    base_text_parts.append(TEXT_ALPHANUMERIC)
    text = "\n".join(base_text_parts)

    # If font path contains 'NF', include Nerd Font icon test
    if 'NF' in font_name or 'nerd' in font_name.lower():
        text += "\n" + TEXT_NERD_FONT
        print("Using Nerd Font test (includes icon test)")
    else:
        print("Using basic test (no icons)")

    # Create a dummy image to calculate text size
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)

    # Calculate text bounding box
    text_bbox = draw.multiline_textbbox((0, 0), text.strip(), font=font, spacing=10)

    # Calculate image dimensions
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    img_width = text_width + 2 * PADDING
    img_height = text_height + 2 * PADDING

    # Create the actual image
    img = Image.new("RGB", (int(img_width), int(img_height)), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw the text on the image
    draw.multiline_text(
        (PADDING, PADDING),
        text.strip(),
        fill=TEXT_COLOR,
        font=font,
        spacing=10
    )

    # Ensure output directory exists and save the image
    output_dir = os.path.dirname(args.output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    img.save(args.output_path)

    print(f"✓ Test image saved successfully to '{args.output_path}'")
    print("--- Visual Test Script Finished ---")

if __name__ == "__main__":
    main()
