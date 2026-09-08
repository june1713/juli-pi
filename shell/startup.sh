#!/bin/bash

# Kill any stale instances before launching
pkill -f "wearpi-osc-lists" 2>/dev/null
pkill -f "ssd1306_sliders_2.py" 2>/dev/null
pkill -f puredata 2>/dev/null
sleep 1

# Navigate to your project directory (adjust as needed)
cd /home/juli/git/juli-pi

# Start Python scripts in the background

/home/juli/venv/bin/python /home/juli/git/wearpi-py/wearpi-osc-lists-adc-norm-smooth-4in.py &
sleep 2
/home/juli/venv/bin/python /home/juli/git/wearpi-py/wearpi-osc-lists-controls.py &
sleep 2
/home/juli/venv/bin/python /home/juli/git/juli-pi/pd_oled/ssd1306_sliders_2.py &
sleep 2

# Launch Pd patch in nogui mode
FLUCOMA=/usr/lib/puredata/extra/FluidCorpusManipulation
# MOSO=/home/wearpi/git/MoSo/abs
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-sound-4in.pd &
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-granular.pd &
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-granular-cosima-sounds.pd &
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-fx.pd &
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-audioin-rave.pd &
/usr/local/bin/pd -nogui -stderr -audiodev "4" -path "$FLUCOMA" -lib fluid_libmanipulation /home/juli/git/juli-pi/pd/test_audio_display.pd &
