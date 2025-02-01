# main.py
import requests
from time import sleep
from config import COLORS
from graphics import Graphics
from wakatime import get_wakatime_stats
import math

def draw_pie_chart(graphics, sorted_projects, total_time):
    graphics.fill(COLORS["background"])

    center_x = 16
    center_y = 16
    radius = 15
    start_angle = -math.pi/9  # Start at -20 degrees to center the empty space

    # Draw slices for top 5 projects
    pie_colors = COLORS["pie"]
    for i, (project, time) in enumerate(sorted_projects):
        percentage = time / total_time
        end_angle = start_angle + (2 * math.pi * percentage)

        # Calculate arc points
        points = []
        points.append((center_x, center_y))
        for angle in [a/10.0 for a in range(int(start_angle*10), int(end_angle*10+1))]:
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            points.append((x, y))
        points.append((center_x, center_y))

        # Draw slice
        graphics.draw_polygon(points, pie_colors[i % len(pie_colors)], True)
        graphics.refresh()
        sleep(0.1)

        start_angle = end_angle

    sleep(0.1)

    # do the same but use text color and false for filled as well as draw text
    start_angle = -math.pi/9  # Reset start angle for second pass
    for i, (project, time) in enumerate(sorted_projects):
        percentage = time / total_time
        end_angle = start_angle + (2 * math.pi * percentage)

        # Calculate arc points
        points = []
        points.append((center_x, center_y))
        for angle in [a/10.0 for a in range(int(start_angle*10), int(end_angle*10+1))]:
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            points.append((x, y))
        points.append((center_x, center_y))

        # Draw slice
        graphics.draw_polygon(points, COLORS["text"], False)
        # draw hours spent truncated to 1 decimal places
        hours = round(time / 3600, 1)
        # clear a space for the text
        graphics.draw_rectangle(38, 16, 46, 36, COLORS["background"])
        graphics.draw_text(38, center_y, str(hours), COLORS["text"], 1)
        graphics.refresh()

        # clear highlight
        graphics.draw_polygon(points, COLORS["pie"][i], True)

        sleep(1)

        start_angle = end_angle

def draw_daily_bar_chart(graphics, data):
    max_time = max(day["total_sum"] for day in data)
    # display coding time for each day
    def draw_bars(delay = 0.0):
        graphics.fill(COLORS["background"])
        for i, day in enumerate(data):
            # get the percentage of coding time for the day
            percentage = day["total_sum"] / max_time
            # draw the bar
            graphics.draw_rectangle(i*9, 32-int(percentage * 30), 8, 31, COLORS["bar"])
            if delay > 0:
                graphics.refresh()
                sleep(delay)

    draw_bars(0.1)

    # display the time spent coding for each day
    for i, day in enumerate(data):
        draw_bars()

        # get the percentage of coding time for the day
        percentage = day["total_sum"] / max_time

        points = []
        points.append((i*9, 32-int(percentage * 30)))
        points.append((i*9, 31))
        points.append((i*9+7, 31))
        points.append((i*9+7, 32-int(percentage * 30)))

        graphics.draw_polygon(points, COLORS["text"], False)

        graphics.draw_text(22, 16, str(round(day["total_sum"] / 3600, 1)), COLORS["text"], 1)

        graphics.refresh()
        sleep(1)

def main():
    print("Hello, world!")

    # Initialize display and graphics
    graphics = Graphics()

    print("Display functioning!")

    sleep(1)

    while True:
        data = get_wakatime_stats(7)
        print("Fetched new data")

        # Get project percentages
        total_time = sum(day["total_sum"] for day in data)
        projects = {}
        for day in data:
            for project in day["projects"]:
                project_key = project["key"]
                if project_key in projects:
                    projects[project_key] += project["total"]
                else:
                    projects[project_key] = project["total"]

        # Sort projects by time
        sorted_projects = sorted(projects.items(), key=lambda x: x[1], reverse=True)

        # Draw the pie chart
        draw_pie_chart(graphics, sorted_projects, total_time)

        # Draw the daily activity chart
        draw_daily_bar_chart(graphics, data)

if __name__ == "__main__":
    main()
