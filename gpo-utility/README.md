# GPO Utility for Raspberry Pi

A simple utility to prove Pi's GPOs are working, and to validate your LED wiring.

## Initial Setup and Assumptions

* Your Pi is assembled and powered up.
* Raspberry Pi OS Full (32-bit) is installed.
* The GPIOs you wish to control have been connected to LEDs with series resistors (Canakit guide recommends 220-ohm).  
  A breadboard is handy here.
* This repo has been cloned to your Pi, or to your workstation and files copied to your Pi.
  

## Usage Instructions

1. Edit one of the `.json` config files.  
   Set `gpo_list` to reflect the GPIO pins you are using as outputs to control the LEDs.
   If you wish to change the blink period and duty cycle, adjust those.
   
   **Note**: Period cannot be negative, and duty cycle must be between 0.0 and 1.0. 
   
   Save the file.
   
2. Ensure the required Python modules are installed on the Pi.  To check:
 
   `python3 -m pip list`
   
   To install any missing module, e.g. `jsons`
   
   `python3 -m pip install jsons`
   
3. Run the program and supply your config file name as an argument:

    `python3 gpo_utility.py config_quick.json`
    
The LEDs will blink first in sequence, then all blink simultaneously.
See video [here](https://rumble.com/vi8wt5-raspberry-pi-gpo-led-controller.html).


