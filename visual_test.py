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
TEXT = """
Lorem ipsumであのイーハトーヴォの世界が広がります。
abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890 `~!@#$%^&*()_-=+[]{}|;:'",.<>/
"""
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

    # Create a dummy image to calculate text size
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)

    # Calculate text bounding box
    text_bbox = draw.multiline_textbbox((0, 0), TEXT.strip(), font=font, spacing=10)

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
        TEXT.strip(),
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
