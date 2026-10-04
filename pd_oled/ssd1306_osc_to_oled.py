# SPDX-FileCopyrightText: 2014 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

# This is based on the example "ssd1306_pillow_shapes.py" of the 
# ssd1306 Git Example library. Modified by me (JG) and Chat GPT with the prompt 
# can you walk me through an osc setup for a python script? it should receive a slider value and a text from pure data via osc via local host. just super basic! in the end this will be send to an oled display. rifht now my script looks like this and i just want to adjust the values slider0, slider2, slider3, slider 4 and the values text1 and text2
# /home/juli/git/juli-pi/pd_oled/ssd1306_sliders.py

# SPDX-FileCopyrightText: 2014 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

import busio
import threading
import time
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont

import adafruit_ssd1306

# OSC
from pythonosc import dispatcher
from pythonosc.osc_server import OSCUDPServer


# --------------------------------------------------
# VALUES RECEIVED FROM PURE DATA
# --------------------------------------------------

slider_values = [0.0] * 8
blinking1_enabled = False
blinking2_enabled = False
blinking3_enabled = False

text1 = "text1"
text2 = "text2"
text3 = "text3"
display_dirty = threading.Event()


# --------------------------------------------------
# OSC HANDLERS
# --------------------------------------------------

def slider_handler(address, value):
    slider_index = int(address.rsplit("slider", 1)[1]) - 1
    new_value = max(0.0, min(1.0, float(value)))
    if slider_values[slider_index] != new_value:
        slider_values[slider_index] = new_value
        display_dirty.set()


def blink1_handler(address, value):
    global blinking1_enabled, text1_visible
    new_value = bool(float(value))
    if blinking1_enabled != new_value:
        blinking1_enabled = new_value
        if not blinking1_enabled:
            text1_visible = True
        display_dirty.set()


def blink2_handler(address, value):
    global blinking2_enabled, text2_visible
    new_value = bool(float(value))
    if blinking2_enabled != new_value:
        blinking2_enabled = new_value
        if not blinking2_enabled:
            text2_visible = True
        display_dirty.set()


def blink3_handler(address, value):
    global blinking3_enabled, text3_visible
    new_value = bool(float(value))
    if blinking3_enabled != new_value:
        blinking3_enabled = new_value
        if not blinking3_enabled:
            text3_visible = True
        display_dirty.set()


def text1_handler(address, value):
    global text1
    new_value = str(value)
    if text1 != new_value:
        text1 = new_value
        display_dirty.set()


def text2_handler(address, value):
    global text2
    new_value = str(value)
    if text2 != new_value:
        text2 = new_value
        display_dirty.set()


def text3_handler(address, value):
    global text3
    new_value = str(value)
    if text3 != new_value:
        text3 = new_value
        display_dirty.set()


# --------------------------------------------------
# SET UP OSC
# --------------------------------------------------

dispatcher = dispatcher.Dispatcher()

for slider_number in range(1, 9):
    dispatcher.map(f"/slider{slider_number}", slider_handler)
dispatcher.map("/blink1", blink1_handler)
dispatcher.map("/blink2", blink2_handler)
dispatcher.map("/blink3", blink3_handler)

dispatcher.map("/text1", text1_handler)
dispatcher.map("/text2", text2_handler)
dispatcher.map("/text3", text3_handler)

# Listen on localhost, port 8000
server = OSCUDPServer(
    ("127.0.0.1", 8000),
    dispatcher
)
server.timeout = 0.05

print("OSC server listening on 127.0.0.1:8000")


# --------------------------------------------------
# OLED SETUP
# --------------------------------------------------

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)

# Load default font.
font = ImageFont.load_default()

text1_visible = True
text2_visible = True
text3_visible = True
last_blink = time.monotonic()
blink_interval = 0.15
frame_interval = 1 / 20
last_render = 0.0
display_dirty.set()


# --------------------------------------------------
# OSC + OLED LOOP
# --------------------------------------------------

while True:

    # Handle OSC messages.
    # This waits briefly for an OSC message so the blink timer can run.
    server.handle_request()

    if blinking1_enabled or blinking2_enabled or blinking3_enabled:
        now = time.monotonic()
        if now - last_blink >= blink_interval:
            if blinking1_enabled:
                text1_visible = not text1_visible
            if blinking2_enabled:
                text2_visible = not text2_visible
            if blinking3_enabled:
                text3_visible = not text3_visible
            last_blink = now
            display_dirty.set()

    now = time.monotonic()
    if not display_dirty.is_set() or now - last_render < frame_interval:
        continue

    display_dirty.clear()

    # Clear the image.
    draw.rectangle(
        (0, 0, width, height),
        outline=0,
        fill=0
    )

    # --------------------------------------------------
    # DRAW SENSOR INDICATORS
    # --------------------------------------------------

    bar_width = 28
    column_width = width // 4
    for index, value in enumerate(slider_values):
        row = index // 4
        column = index % 4
        bar_length = int(value * bar_width)
        if bar_length:
            x = column * column_width + 2
            y = 3 + row * 6
            draw.line((x, y, x + bar_length - 1, y), fill=255)

    # --------------------------------------------------
    # DRAW TEXT
    # --------------------------------------------------

    text_y = height - 10
    text_values = (text1, text2, text3)
    text_visibility = (text1_visible, text2_visible, text3_visible)
    for index, (value, visible) in enumerate(zip(text_values, text_visibility)):
        if visible:
            draw.text(
                (2 + index * 42, text_y),
                value[:7],
                font=font,
                fill=255
            )

    # --------------------------------------------------
    # UPDATE OLED
    # --------------------------------------------------

    disp.image(image)
    disp.show()
    last_render = time.monotonic()
