# Neon Kit Setup Guide

This guide will walk you through setting up your neon LED matrix kit with CircuitPython.

## What's in the Box

- Neon LED matrix panel (64x32)
- 4-piece neon stand
- IDC cable (not needed for this setup)
- Power cable with red/black wires
- ESP32-S3 control board (microcontroller)

## What You'll Need

- 5V 3A (15W) power supply with USB-C cable
- Computer for initial setup
- Flat head screwdriver

## Step 1: Install CircuitPython Firmware

1. Connect the ESP32-S3 microcontroller to your computer via USB-C
2. Go to the [CircuitPython downloads page](https://circuitpython.org/board/espressif_esp32s3_devkitm_1_n8/)
3. Click **Open Installer**
4. Select **Install bootloader only**
5. Click **Next** and wait for installation to complete
6. Unplug and replug the microcontroller
7. Download the `.uf2` file from the CircuitPython page
8. Drag the `.uf2` file into the drive that appears
9. Unplug and replug the microcontroller again

## Step 2: Configure Wi-Fi

1. Open the `settings.toml` file on the CircuitPython drive
2. Add the following configuration:

```toml
CIRCUITPY_WIFI_SSID = "your-wifi-name"
CIRCUITPY_WIFI_PASSWORD = "your-wifi-password"
CIRCUITPY_WEB_API_PASSWORD = "password"
```

3. Replace the SSID and password with your network credentials
4. Navigate to `circuitpython.local` in your web browser
5. Click **Full Code Editor**
6. Username: (leave blank)
7. Password: The password you set in `settings.toml`

## Step 3: Wire the Matrix Power

**⚠️ Important: Wire orientation matters! Double-check before powering on.**

1. Take the power cable with red and black wires
2. Using a flathead screwdriver, connect the wires to the control board:
   - **Black wire**: Side closest to the ESP32 chip (away from board edge)
   - **Red wire**: Opposite side from black wire
3. On the matrix board, find the arrow next to the power connector
4. Connect the control board to the left side of the matrix
5. Align the pins and plug into the connector
6. Plug one of the power connectors into the matrix board

## Step 4: Connect Power Supply

1. **Unplug the microcontroller from your computer** (it can't power the matrix reliably)
2. Connect USB-C cable to the power supply
3. Connect the other end to the microcontroller
4. Plug the power supply into the wall outlet

## Step 5: Test Sample Code

1. Download the [test code](https://neon.hackclub.dev/open?author=recursiveforte&repo=neon-example)
2. Extract the `.zip` file and open the Python file
3. Copy all the code
4. In the web editor, paste it into `code.py`
5. Click **Save**

### Installing Required Libraries

If you see an error like `no module named adafruit_display_text`:

1. Go to [CircuitPython Libraries](https://circuitpython.org/libraries)
2. Download the **CircuitPython 9 Bundle**
3. Find the missing library in the bundle (e.g., `adafruit_display_text`)
4. Unplug the matrix and plug the microcontroller into your computer
5. Copy the library folder to the `lib` directory on the CircuitPython drive
6. Unplug from computer and reconnect to power supply

## Step 6: Assemble the Stand

1. Place the base piece where the USB-C cable exits the matrix
2. Attach the spacer pieces (push firmly - they're tight)
3. Place the matrix into the assembled stand

## Important Notes

### Power Management

- **Always use the wall power supply when running the matrix**
- Only connect to your computer when uploading files (and unplug the matrix first)
- Computer USB ports don't provide enough power and will cause crashes

### Pin Definitions

The default pin definitions **will not work**. Use these correct values:

```python
# Get the pin definitions from:
# https://gist.github.com/recursiveforte/f01953798bbeae0342e73c1067ca13d1
```

See the gist linked above for the full pin configuration.

### Migrating Code from Development Environment

If you wrote code in the neon development environment, you'll need to make these changes:

#### 1. RGB Matrix Pins
Replace the default pin definitions with the correct ones from the [pin definitions gist](https://gist.github.com/recursiveforte/f01953798bbeae0342e73c1067ca13d1).

#### 2. Network Requests
`requests` and `urllib` won't work - use CircuitPython's built-in libraries:

- Follow the [WiFi/Requests tutorial](https://learn.adafruit.com/networking-in-circuitpython/networking-with-the-wifi-module#the-adafruit-requests-library-3177159)
- Use `wifi` module for network connectivity
- Use `adafruit_requests` for HTTP requests
- Wi-Fi credentials from `settings.toml` will be available

#### 3. Python Libraries
Some CPython libraries don't work on microcontrollers:

- **Python Pillow (PIL)**: Not available - you'll need to rewrite image handling code
- Check [CircuitPython libraries](https://circuitpython.org/libraries) for compatible alternatives

## Resources

- [CircuitPython Board Info](https://circuitpython.org/board/espressif_esp32s3_devkitm_1_n8/)
- [Test Code](https://neon.hackclub.dev/open?author=recursiveforte&repo=neon-example)
- [Pin Definitions](https://gist.github.com/recursiveforte/f01953798bbeae0342e73c1067ca13d1)
- [WiFi/Requests Tutorial](https://learn.adafruit.com/networking-in-circuitpython/networking-with-the-wifi-module#the-adafruit-requests-library-3177159)

## Troubleshooting

- **Matrix won't turn on**: Check power connections and wire orientation
- **Random crashes**: Likely insufficient power - use wall adapter, not computer USB
- **Module not found errors**: Install the missing library from CircuitPython bundle
- **Code from dev environment won't work**: See "Migrating Code" section above

---

Enjoy your neon matrix! Share your projects in the Slack channel once you're up and running.
