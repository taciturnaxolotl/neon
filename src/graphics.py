# graphics.py
class Graphics:
    def __init__(self, bitmap, palette):
        self.bitmap = bitmap
        self.palette = palette
        self.color_map = {}

    def _get_index_for(self, color):
        if color in self.color_map:
            return self.color_map[color]
        index = len(self.color_map)
        self.palette[index] = color
        self.color_map[color] = index
        return index

    def place(self, x, y, color):
        if 0 <= x < self.bitmap.width and 0 <= y < self.bitmap.height:
            self.bitmap[x, y] = self._get_index_for(color)

    def fill(self, color):
        index = self._get_index_for(color)
        for y in range(self.bitmap.height):
            for x in range(self.bitmap.width):
                self.bitmap[x, y] = index

    def draw_rectangle(self, x, y, width, height, color):
        for i in range(x, x + width):
            for j in range(y, y + height):
                self.place(i, j, color)

    def draw_circle(self, cx, cy, radius, color):
        for x in range(cx - radius, cx + radius + 1):
            for y in range(cy - radius, cy + radius + 1):
                if (x - cx)**2 + (y - cy)**2 <= radius**2:
                    self.place(x, y, color)

    def draw_triangle(self, x1, y1, x2, y2, x3, y3, color):
        def draw_line(x0, y0, x1, y1):
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx - dy
            while True:
                self.place(x0, y0, color)
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

    def draw_curve(self, points, color):
        def interpolate(t, p0, p1):
            return (1 - t) * p0 + t * p1

        steps = 100
        for i in range(steps + 1):
            t = i / steps
            x, y = points[0]
            for j in range(1, len(points)):
                x = interpolate(t, x, points[j][0])
                y = interpolate(t, y, points[j][1])
            self.place(int(x), int(y), color)

    def draw_polygon(self, points, color, filled=False):
        # Draw outline
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            def draw_line(x0, y0, x1, y1):
                dx = abs(x1 - x0)
                dy = abs(y1 - y0)
                sx = 1 if x0 < x1 else -1
                sy = 1 if y0 < y1 else -1
                err = dx - dy
                while True:
                    self.place(x0, y0, color)
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

        # Fill polygon if requested
        if filled:
            # Find bounding box
            min_x = min(p[0] for p in points)
            max_x = max(p[0] for p in points)
            min_y = min(p[1] for p in points)
            max_y = max(p[1] for p in points)

            # Scan each row
            for y in range(min_y, max_y + 1):
                intersections = []
                # Find intersections with all edges
                for i in range(len(points)):
                    x1, y1 = points[i]
                    x2, y2 = points[(i + 1) % len(points)]
                    if (y1 <= y < y2) or (y2 <= y < y1):
                        if y2 - y1 != 0:
                            x = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                            intersections.append(int(x))

                # Sort intersections
                intersections.sort()

                # Fill between pairs of intersections
                for i in range(0, len(intersections), 2):
                    if i + 1 < len(intersections):
                        for x in range(intersections[i], intersections[i + 1] + 1):
                            self.place(x, y, color)
