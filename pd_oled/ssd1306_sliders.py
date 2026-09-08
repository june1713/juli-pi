# SPDX-FileCopyrightText: 2014 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

# This is based on the example "ssd1306_pillow_shapes.py" of the 
# ssd1306 Git Example library. Modified by me (JG)

import busio
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont

import adafruit_ssd1306

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Note you can change the I2C address, or add a reset pin:
# disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c, reset=reset_pin)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# OSC input from Pure Data
sensor1 = 1
sensor2 = 0.5
sensor3 = 0
sensor4 = 0.35

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 2
shape_width = 12
top = padding
bottom = height - padding
top1 = bottom - (sensor1 * 28)
top2 = bottom - (sensor2 * 28) 
top3 = bottom - (sensor3 * 28)
top4 = bottom - (sensor4 * 28)

# Move left to right keeping track of the current x position for drawing shapes.
x = padding
# Draw an ellipse.
draw.rectangle((x, top1, x + shape_width - padding, bottom), outline=255, fill=0)
x += shape_width + padding
# Draw a rectangle.
draw.rectangle((x, top2, x + shape_width - padding, bottom), outline=255, fill=0)
x += shape_width + padding
# Draw a triangle.
draw.rectangle((x, top3, x + shape_width - padding, bottom), outline=255, fill=0)
x += shape_width + padding
# Draw an X.
draw.rectangle((x, top4, x + shape_width - padding, bottom), outline=255, fill=0)
x += shape_width + padding

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# Write two lines of text.
draw.text((80, top), "text1", font=font, fill=255)
draw.text((80, top + 12), "text2", font=font, fill=255)

# Display image.
disp.image(image)
disp.show()
