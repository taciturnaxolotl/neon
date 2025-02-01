# main.py
import requests
from time import sleep
from config import COLORS
from display import init_display
from graphics import Graphics

def get_wakatime_stats(day=0):
    from datetime import datetime, timedelta
    today = datetime.today()
    from_date = (today - timedelta(days=day)).strftime('%Y-%m-%d')
    to_date = (today - timedelta(days=day-1)).strftime('%Y-%m-%d')
    response = requests.get(
        "https://waka.hackclub.com/api/summary",
        params={"user": "U062UG485EE", "from": from_date, "to": to_date},
        headers={"Authorization": "Bearer 2ce9e698-8a16-46f0-b49a-ac121bcfd608"}
    )
    data = response.json()
    data["total_sum"] = sum([project["total"] for project in data["categories"]])
    return data

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

    # Get wakatime stats for the last week adding each day to the array
    data = []
    for i in range(1, 7):
        data.append(get_wakatime_stats(i))

    print("got data")

    sleep(2)

    graphics.fill(COLORS["background"])

    # display bar graph of coding time over the last week
    max_height = 30  # Maximum display height
    max_time = max(day["total_sum"] for day in data)
    scale_factor = max_height / max_time if max_time > 0 else 1

    for i, day in enumerate(data):
        print(day["total_sum"])
        x = 5 + i * 10
        y = 30
        height = int(day["total_sum"] * scale_factor)
        graphics.draw_rectangle(x, y - height, 8, height, COLORS["bar"])
        display.refresh()
        sleep(0.1)

if __name__ == "__main__":
    main()
