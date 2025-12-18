#!/usr/bin/env python3
"""
HackLine Font Visual Test Script
Generates an image from a test string using the built HackLine font.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
FONT_PATH = "build/HackLine-Regular.ttf"
OUTPUT_PATH = "build/test_image.png"
TEXT = """
あのイーハトーヴォの
すきとおった風、
夏でも底に冷たさをもつ青いそら、
うつくしい森で飾られたモーリオ市、
郊外のぎらぎらひかる草の波。

祇辻飴葛蛸鯖鰯噌庖箸

ABCDEFGHIJKLM
abcdefghijklm
1234567890
"""
FONT_SIZE = 24
BACKGROUND_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black
PADDING = 20

# --- Main Script ---
def main():
    """Generates the test image."""
    print("--- Starting Visual Test Script ---")

    # Check if font file exists
    if not os.path.exists(FONT_PATH):
        print(f"Error: Font file not found at '{FONT_PATH}'")
        print("Please run ./build.sh first to generate the font.")
        return

    # Load font
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print(f"Error: Could not load font from '{FONT_PATH}'")
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

    # Save the image
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH)

    print(f"✓ Test image saved successfully to '{OUTPUT_PATH}'")
    print("--- Visual Test Script Finished ---")

if __name__ == "__main__":
    main()
