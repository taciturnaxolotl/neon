import random
import time
import requests
import json

import board
import displayio
import framebufferio
import rgbmatrix

displayio.release_displays()

# Initialize the display
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
SCALE = 1
bitmap = displayio.Bitmap(display.width//SCALE, display.height//SCALE, 65535)
palette = displayio.Palette(65535)
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group(scale=SCALE)
group.append(tile_grid)
display.root_group = group

color_map = {} #hex code : index
def _get_index_for(color):
    index = color_map.get(color, None)
    if index != None:
        return index

    index = len(color_map)
    print(f"DEBUG: Add {hex(color)} to map at {index}")
    palette[index] = color
    color_map[color] = index
    return index

def place(x, y, color):
    """Place a pixel at (x, y) with the given color."""
    if 0 <= x < bitmap.width and 0 <= y < bitmap.height:
        bitmap[x, y] = _get_index_for(color)
        display.auto_refresh = True

def fill(color):
    """Fill the entire display with the given color."""
    for y in range(bitmap.height):
        for x in range(bitmap.width):
            bitmap[x, y] = _get_index_for(color)
    display.auto_refresh = True

# GitHub contribution colors
COLORS = {
    0: 0x161B22, # No contributions
    1: 0x0E4429, # Light
    2: 0x006D32, # Medium
    3: 0x26A641, # Medium-heavy
    4: 0x39D353  # Heavy
}

def get_github_contributions(username):
    """Get contribution data from GitHub GraphQL API"""
    headers = {
        "Authorization": "Bearer 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"
    }

    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """

    variables = {"username": username}
    url = "https://api.github.com/graphql"

    r = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    data = r.json()

    return data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']

# Define a simple 5x5 pixel font
font = {
    'A': [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1]
    ],
    'B': [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0]
    ],
    # Add other characters as needed
    't': [
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
    ],
    'a': [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1]
    ],
    'c': [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0]
    ],
    'i': [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
    ],
    'u': [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0]
    ],
    'r': [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0]
    ],
    'n': [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1]
    ],
    'x': [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1]
    ],
    'o': [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0]
    ],
    'l': [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0]
    ]
}

def display_contributions(username):
    """Display GitHub contributions on LED matrix"""
    fill(0x000000)  # Clear display

    # Get contribution data
    weeks = get_github_contributions(username)

    # Calculate horizontal offset to center the graph
    horizontal_offset = (bitmap.width - 64) // 2

    # Display each day as a single pixel
    # Go through the last 64 weeks of data (width of display)
    for week_idx, week in enumerate(weeks[-64:]):
        for day_idx, day in enumerate(week['contributionDays']):
            count = day['contributionCount']

            # Map contribution count to color
            if count == 0:
                color = COLORS[0]
            elif count <= 3:
                color = COLORS[1]
            elif count <= 6:
                color = COLORS[2]
            elif count <= 9:
                color = COLORS[3]
            else:
                color = COLORS[4]

            # Plot single pixel for the day
            place(week_idx + horizontal_offset, day_idx, color)

    # Display username underneath the graph
    username_x = (bitmap.width - len(username) * 6) // 2  # Assuming each character is 6 pixels wide
    username_y = 8  # Position the username 8 pixels below the graph

    for i, char in enumerate(username):
        char_x = username_x + i * 6
        for y in range(5):  # Assuming character height is 5 pixels
            for x in range(5):  # Assuming character width is 5 pixels
                if font[char][y][x]:  # Assuming font is a dictionary with character bitmaps
                    place(char_x + x, username_y + y, 0xFFFFFF)  # White color for text

# Display contributions for given username
display_contributions("taciturnaxolotl")
