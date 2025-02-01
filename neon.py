import random
import time
import board
import displayio
import framebufferio
import rgbmatrix

# Release any existing displays
displayio.release_displays()

# Initialize the display
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Setup bitmap and palette
SCALE = 1
bitmap = displayio.Bitmap(display.width // SCALE, display.height // SCALE, 65535)
palette = displayio.Palette(65535)
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group(scale=SCALE)
group.append(tile_grid)
display.root_group = group

# Color definitions
COLORS = {
    "background": 0x161B22,
    "bar": 0x26A641,
    "pie": [0x0E4429, 0x006D32, 0x26A641, 0x39D353, 0x39A9D3],
    "circle": 0xFF6347,
    "triangle": 0xFFD700,
    "curve": 0x1E90FF
}

# Color mapping
color_map = {}

def _get_index_for(color):
    if color in color_map:
        return color_map[color]
    index = len(color_map)
    palette[index] = color
    color_map[color] = index
    return index

# Drawing functions
def place(x, y, color):
    if 0 <= x < bitmap.width and 0 <= y < bitmap.height:
        bitmap[x, y] = _get_index_for(color)

def fill(color):
    index = _get_index_for(color)
    for y in range(bitmap.height):
        for x in range(bitmap.width):
            bitmap[x, y] = index

def draw_rectangle(x, y, width, height, color):
    for i in range(x, x + width):
        for j in range(y, y + height):
            place(i, j, color)

def draw_circle(cx, cy, radius, color):
    for x in range(cx - radius, cx + radius + 1):
        for y in range(cy - radius, cy + radius + 1):
            if (x - cx)**2 + (y - cy)**2 <= radius**2:
                place(x, y, color)

def draw_triangle(x1, y1, x2, y2, x3, y3, color):
    def draw_line(x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            place(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    draw_line(x1, y1, x2, y2)
    draw_line(x2, y2, x3, y3)
    draw_line(x3, y3, x1, y1)


def draw_curve(points, color):
    def interpolate(t, p0, p1):
        return (1 - t) * p0 + t * p1

    steps = 100
    for i in range(steps + 1):
        t = i / steps
        x, y = points[0]
        for j in range(1, len(points)):
            x = interpolate(t, x, points[j][0])
            y = interpolate(t, y, points[j][1])
        place(int(x), int(y), color)

# Display update function
def update_display():
    display.refresh()

# Example usage
fill(COLORS["background"])
draw_rectangle(5, 5, 20, 10, COLORS["bar"])
draw_circle(40, 16, 8, COLORS["circle"])
draw_triangle(10, 25, 20, 10, 30, 25, COLORS["triangle"])
draw_curve([(0, 0), (4,25), (63, 31)], COLORS["curve"])
update_display()
