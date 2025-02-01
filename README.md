<h3 align="center">
    <img src="https://raw.githubusercontent.com/taciturnaxolotl/neon/master/.github/images/neon.svg" width="350" alt="Logo"/><br/>
    <img src="https://raw.githubusercontent.com/taciturnaxolotl/carriage/master/.github/images/transparent.png" height="45" width="0px"/>
    <span>Neon</span>
    <img src="https://raw.githubusercontent.com/taciturnaxolotl/carriage/master/.github/images/transparent.png" height="30" width="0px"/>
</h3>

<p align="center">
    <i>The bulbs glow a distinctive amber. It's like nostalgia but for something you never had.</i>
</p>

<p align="center">
	<img src="https://raw.githubusercontent.com/taciturnaxolotl/carriage/master/.github/images/line-break-thin.svg" />
</p>
<p align="center">
	<img src="https://raw.githubusercontent.com/taciturnaxolotl/neon/master/.github/images/demo.gif" />
</p>
<p align="center">
	<img src="https://raw.githubusercontent.com/taciturnaxolotl/carriage/master/.github/images/line-break-thin.svg" />
</p>

## What's this?

This is my submission for the [Hackclub Neon](https://neon.hackclub.com) YSWS! I cycled through quite a few ideas before settling on a hackatime dashboard! It's a simple, clean, and minimalistic dashboard that displays the time coding for the day!

### Standard Lib

My project comes with a standard library of graphics primitives to help you get started quickly. Here are the key functions with example usage:

```python
from graphics import Graphics

# Initialize the display
graphics = Graphics()

# Drawing lines
graphics.draw_line(0, 0, 63, 31, COLORS["line"])  # x1, y1, x2, y2, color

# Drawing rectangles
graphics.draw_rectangle(5, 5, 20, 10, COLORS["bar"])  # x, y, width, height, color

# Drawing circles
graphics.draw_circle(40, 16, 8, COLORS["circle"])  # center_x, center_y, radius, color

# Drawing Bezier curves
graphics.draw_curve([(0, 0), (4,25), (63, 31)], COLORS["curve"])  # control points, color

# Drawing polygons 
graphics.draw_polygon([(45, 16), (40, 32), (63, 31)], COLORS["polygon"], True)  # points, color, fill

# Drawing text
graphics.draw_text(3, 21, "3.2", COLORS["text"], 1)  # x, y, text, color, size

# Filling the display
graphics.fill(COLORS["background"])  # Fills entire display with color

# Updating the display
graphics.refresh()  # Refreshes display buffer
```

The library handles all the low-level matrix display setup including pin configuration and color palette management. Colors are defined using hex values (0xRRGGBB format) and automatically mapped to the 16-bit color space.

<p align="center">
	<img src="https://raw.githubusercontent.com/taciturnaxolotl/neon/master/.github/images/stlib.webp" />
</p>

<p align="center">
	<img src="https://raw.githubusercontent.com/taciturnaxolotl/carriage/master/.github/images/line-break.svg" />
</p>

<p align="center">
	&copy 2025-present <a href="https://github.com/taciturnaxolotl">Kieran Klukas</a>
</p>

<p align="center">
	<a href="https://github.com/taciturnaxolotl/neon/blob/master/LICENSE.md"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a>
</p>
