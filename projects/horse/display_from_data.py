# display_from_data.py
from time import sleep
from graphics import Graphics
import horse_data

def display_pixel_data(graphics, pixel_data, width, height):
    """Display preloaded pixel data on the neon display"""
    # Clear display
    graphics.fill(0x000000)
    
    # Draw each pixel from the data array
    for y in range(height):
        for x in range(width):
            color = pixel_data[y][x]
            graphics.place(x, y, color)
    
    # Refresh display
    graphics.refresh()
    print(f"Displayed {width}x{height} image on neon display!")

def main():
    print("Starting horse display...")
    
    # Initialize graphics
    graphics = Graphics()
    
    print("Display functioning!")
    
    sleep(1)
    
    # Display the preloaded image data
    display_pixel_data(graphics, horse_data.PIXEL_DATA, horse_data.WIDTH, horse_data.HEIGHT)
    
    # Keep display on
    while True:
        sleep(1)

if __name__ == "__main__":
    main()
