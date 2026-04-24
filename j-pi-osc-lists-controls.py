import time
import board

import digitalio

from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.rotaryio import IncrementalEncoder
from adafruit_seesaw.digitalio import DigitalIO

from adafruit_neokey.neokey1x4 import NeoKey1x4

# OSC
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

# ----------------------------
# OSC SETUP
# ----------------------------

print_osc = True
ip = "127.0.0.1"
port = 57121

osc_startup()
osc_udp_client(ip, port, "client")

# ----------------------------
# I2C + HARDWARE
# ----------------------------

i2c = board.I2C()

seesaw = Seesaw(i2c, 0x49)
neokey = NeoKey1x4(i2c, addr=0x30)

# Encoders (Seesaw)
encoders = [IncrementalEncoder(seesaw, n) for n in range(4)]
switches = [DigitalIO(seesaw, pin) for pin in (12, 14, 17, 9)]

for switch in switches:
    switch.switch_to_input(pull=digitalio.Pull.UP)

# ----------------------------
# STATE
# ----------------------------

last_positions = [0, 0, 0, 0]
enc_rot = [0, 0, 0, 0]

last_enc_button = [True, True, True, True]

last_button = [False, False, False, False]

# ----------------------------
# MAIN LOOP
# ----------------------------

print("Starting controls loop\n")

finished = False

while not finished:

    # ----------------------------
    # ENCODERS
    # ----------------------------

    changed = False
    positions = [encoder.position for encoder in encoders]

    for n, pos in enumerate(positions):
        if pos != last_positions[n]:
            changed = True

            if pos > last_positions[n]:
                enc_rot[n] = 1
            else:
                enc_rot[n] = -1

            last_positions[n] = pos
        else:
            enc_rot[n] = 0

    if changed:
        msg = oscbuildparse.OSCMessage("/enc-rot", None, enc_rot)
        osc_send(msg, "client")
        if print_osc:
            print(msg)

    # ----------------------------
    # ENCODER BUTTONS (Seesaw switches)
    # ----------------------------

    changed = False
    switch_vals = [switch.value for switch in switches]

    for n, val in enumerate(switch_vals):
        if val != last_enc_button[n]:
            changed = True
            last_enc_button[n] = val

    if changed:
        enc_but = [int(not v) for v in switch_vals]
        msg = oscbuildparse.OSCMessage("/enc-but", None, enc_but)
        osc_send(msg, "client")
        if print_osc:
            print(msg)

    # ----------------------------
    # NEOKEY BUTTONS
    # ----------------------------

    changed = False

    for n in range(4):
        val = neokey[n]
        if val != last_button[n]:
            changed = True
        last_button[n] = val

    if changed:
        keys = [int(neokey[i]) for i in range(4)]
        msg = oscbuildparse.OSCMessage("/key", None, keys)
        osc_send(msg, "client")
        if print_osc:
            print(msg)

    # ----------------------------
    # OSC LOOP PROCESSING
    # ----------------------------

    osc_process()

# ----------------------------
# CLEAN EXIT
# ----------------------------

osc_terminate()