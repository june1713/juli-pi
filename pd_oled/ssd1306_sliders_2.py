# SPDX-FileCopyrightText: 2014 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

# This is based on the example "ssd1306_pillow_shapes.py" of the 
# ssd1306 Git Example library. Modified by me (JG) and Chat GPT with the prompt 
# can you walk me through an osc setup for a python script? it should receive a slider value and a text from pure data via osc via local host. just super basic! in the end this will be send to an oled display. rifht now my script looks like this and i just want to adjust the values slider1, slider2, slider3, slider 4 and the values text1 and text2
# /home/juli/git/juli-pi/pd_oled/ssd1306_sliders.py

# SPDX-FileCopyrightText: 2014 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

import busio
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont

import adafruit_ssd1306

# OSC
from pythonosc import dispatcher
from pythonosc import osc_server


# --------------------------------------------------
# VALUES RECEIVED FROM PURE DATA
# --------------------------------------------------

slider1 = 1.0
slider2 = 0.5
slider3 = 0.0
slider4 = 0.35

text1 = "text1"
text2 = "text2"


# --------------------------------------------------
# OSC HANDLERS
# --------------------------------------------------

def slider1_handler(address, value):
    global slider1
    slider1 = float(value)
    print("slider1:", slider1)


def slider2_handler(address, value):
    global slider2
    slider2 = float(value)
    print("slider2:", slider2)


def slider3_handler(address, value):
    global slider3
    slider3 = float(value)
    print("slider3:", slider3)


def slider4_handler(address, value):
    global slider4
    slider4 = float(value)
    print("slider4:", slider4)


def text1_handler(address, value):
    global text1
    text1 = str(value)
    print("text1:", text1)


def text2_handler(address, value):
    global text2
    text2 = str(value)
    print("text2:", text2)


# --------------------------------------------------
# SET UP OSC
# --------------------------------------------------

dispatcher = dispatcher.Dispatcher()

dispatcher.map("/slider1", slider1_handler)
dispatcher.map("/slider2", slider2_handler)
dispatcher.map("/slider3", slider3_handler)
dispatcher.map("/slider4", slider4_handler)

dispatcher.map("/text1", text1_handler)
dispatcher.map("/text2", text2_handler)

# Listen on localhost, port 8000
server = osc_server.ThreadingOSCUDPServer(
    ("127.0.0.1", 8000),
    dispatcher
)

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


# --------------------------------------------------
# OSC + OLED LOOP
# --------------------------------------------------

while True:

    # Handle OSC messages.
    # This waits until an OSC message arrives.
    server.handle_request()

    # Clear the image.
    draw.rectangle(
        (0, 0, width, height),
        outline=0,
        fill=0
    )

    # --------------------------------------------------
    # DRAW slider BARS
    # --------------------------------------------------

    padding = 2
    shape_width = 12

    top = padding
    bottom = height - padding

    top1 = bottom - (slider1 * 28)
    top2 = bottom - (slider2 * 28)
    top3 = bottom - (slider3 * 28)
    top4 = bottom - (slider4 * 28)

    x = padding

    draw.rectangle(
        (x, top1, x + shape_width - padding, bottom),
        outline=255,
        fill=0
    )

    x += shape_width + padding

    draw.rectangle(
        (x, top2, x + shape_width - padding, bottom),
        outline=255,
        fill=0
    )

    x += shape_width + padding

    draw.rectangle(
        (x, top3, x + shape_width - padding, bottom),
        outline=255,
        fill=0
    )

    x += shape_width + padding

    draw.rectangle(
        (x, top4, x + shape_width - padding, bottom),
        outline=255,
        fill=0
    )

    # --------------------------------------------------
    # DRAW TEXT
    # --------------------------------------------------

    draw.text(
        (80, top),
        text1,
        font=font,
        fill=255
    )

    draw.text(
        (80, top + 12),
        text2,
        font=font,
        fill=255
    )

    # --------------------------------------------------
    # UPDATE OLED
    # --------------------------------------------------

    disp.image(image)
    disp.show()
