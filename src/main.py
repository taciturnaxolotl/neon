# main.py
from config import COLORS
from display import init_display
from graphics import Graphics

def main():
    # Initialize display and graphics
    display, bitmap, palette = init_display()
    graphics = Graphics(bitmap, palette)

    # Draw example shapes
    graphics.fill(COLORS["background"])
    graphics.draw_rectangle(5, 5, 20, 10, COLORS["bar"])
    graphics.draw_circle(40, 16, 8, COLORS["circle"])
    graphics.draw_triangle(10, 25, 20, 10, 30, 25, COLORS["triangle"])
    graphics.draw_curve([(0, 0), (4,25), (63, 31)], COLORS["curve"])

    # Update display
    display.refresh()

if __name__ == "__main__":
    main()
