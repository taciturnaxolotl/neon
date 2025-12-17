#!/usr/bin/env python3
"""
Convert BMP image to an importable Python file for microcontroller use.
This creates a file with pixel data as a constant array that can be imported
without needing PIL or file I/O on the microcontroller.
"""
from PIL import Image
import sys

def convert_bmp_to_py(bmp_path, output_path, width=64, height=32):
    """Convert BMP image to Python file with pixel data"""
    # Load the BMP image
    img = Image.open(bmp_path)
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize to target dimensions
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    # Extract pixel data
    pixels = img.load()
    pixel_data = []
    
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = pixels[x, y]
            # Convert RGB to hex color
            color = (r << 16) | (g << 8) | b
            row.append(f"0x{color:06X}")
        pixel_data.append(row)
    
    # Generate Python file content
    content = f'''"""
Auto-generated pixel data for microcontroller display
Generated from: {bmp_path}
Dimensions: {width}x{height}
"""

WIDTH = {width}
HEIGHT = {height}

# Pixel data as 2D array: pixel_data[y][x]
# Each value is a 24-bit RGB color in format 0xRRGGBB
PIXEL_DATA = [
'''
    
    # Add pixel data rows
    for y, row in enumerate(pixel_data):
        content += "    [" + ", ".join(row) + "]"
        if y < len(pixel_data) - 1:
            content += ","
        content += "\n"
    
    content += "]\n"
    
    # Write to output file
    with open(output_path, 'w') as f:
        f.write(content)
    
    # Calculate file size
    import os
    size_kb = os.path.getsize(output_path) / 1024
    
    print(f"Converted {bmp_path} to {output_path}")
    print(f"Dimensions: {width}x{height}")
    print(f"Total pixels: {width * height}")
    print(f"Output file size: {size_kb:.2f} KB")

def main():
    bmp_path = "horse-scene.bmp"
    output_path = "horse_data.py"
    
    if len(sys.argv) > 1:
        bmp_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    convert_bmp_to_py(bmp_path, output_path)

if __name__ == "__main__":
    main()
