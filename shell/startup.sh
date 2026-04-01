#!/bin/bash

# Navigate to your project directory (adjust as needed)
cd /home/juli/git/j-pi-py

# Start Python scripts in the background

/home/juli/env/bin/python3.11 /home/juli/git/wearpi-py/wearpi-osc-lists-adc-norm-smooth-4in.py &   
sleep 2
/home/juli/env/bin/python3.11 /home/juli/git/wearpi-py/wearpi-osc-lists-controls.py &    
sleep 2

# Launch Pd patch in nogui mode
# puredata -nogui -stderr -audiodev "4" /home/wearpi/git/wearpi-py/pd/wearpi-regression-sound-4in.pd &
# puredata -nogui -stderr -audiodev "4" /home/wearpi/git/wearpi-py/pd/wearpi-regression-granular.pd &
puredata -nogui -stderr -audiodev "4" /home/juli/git/j-pi-py/pd/test.pd & 
# puredata -nogui -stderr -audiodev "4" /home/wearpi/git/wearpi-py/pd/wearpi-regression-fx.pd &