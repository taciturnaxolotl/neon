# main.py
import requests
from time import sleep
from config import COLORS
from display import init_display
from graphics import Graphics
from wakatime import get_wakatime_stats

def main():
    print("Hello, world!")

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

    print("Display functioning!")

    # Get wakatime stats for the last week
    data = get_wakatime_stats(7)

    print("got data")

    sleep(1)

    graphics.fill(COLORS["background"])

    # display bar graph of coding time over the last week
    max_height = 30  # Maximum display height
    max_time = max(day["total_sum"] for day in data)
    scale_factor = max_height / max_time if max_time > 0 else 1

    for i, day in enumerate(data):
        x = 5 + i * 10
        y = 30
        height = int(day["total_sum"] * scale_factor)
        graphics.draw_rectangle(x, y - height, 8, height, COLORS["bar"])
        display.refresh()
        sleep(0.1)

if __name__ == "__main__":
    main()
