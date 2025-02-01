# display.py
import board
import displayio
import framebufferio
import rgbmatrix
from config import SCALE

def init_display():
    displayio.release_displays()

    matrix = rgbmatrix.RGBMatrix(
        width=64, height=32, bit_depth=1,
        rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
        addr_pins=[board.A5, board.A4, board.A3, board.A2],
        clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

    display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

    bitmap = displayio.Bitmap(display.width // SCALE, display.height // SCALE, 65535)
    palette = displayio.Palette(65535)
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group = displayio.Group(scale=SCALE)
    group.append(tile_grid)
    display.root_group = group

    return display, bitmap, palette
